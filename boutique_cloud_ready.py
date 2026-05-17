import os
import streamlit as st
import pandas as pd
import io
from itertools import groupby
from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from pymongo import MongoClient
from bson import ObjectId

# ── Load .env ─────────────────────────────────────────────────────────────────
load_dotenv("credentials/.env")

try:
    MONGO_URI    = st.secrets.get("MONGO_URI",    os.getenv("MONGO_URI"))
    ADMIN_USER   = st.secrets.get("ADMIN_USER",   os.getenv("ADMIN_USER"))
    ADMIN_PASS   = st.secrets.get("ADMIN_PASS",   os.getenv("ADMIN_PASS"))
    STUDENT_USER = st.secrets.get("STUDENT_USER", os.getenv("STUDENT_USER"))
    STUDENT_PASS = st.secrets.get("STUDENT_PASS", os.getenv("STUDENT_PASS"))
except Exception:
    MONGO_URI    = os.getenv("MONGO_URI")
    ADMIN_USER   = os.getenv("ADMIN_USER")
    ADMIN_PASS   = os.getenv("ADMIN_PASS")
    STUDENT_USER = os.getenv("STUDENT_USER")
    STUDENT_PASS = os.getenv("STUDENT_PASS")

USERS = {ADMIN_USER: ADMIN_PASS, STUDENT_USER: STUDENT_PASS}

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Study Abroad Packing List", page_icon="🧳", layout="wide")

# ── MongoDB ───────────────────────────────────────────────────────────────────
@st.cache_resource
def get_col():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client["packing_list_db"]["items"]

def load_items():
    items = list(get_col().find().sort([("category", 1), ("name", 1)]))
    for item in items:
        item["id"]      = str(item["_id"])
        item["checked"] = int(item.get("checked", 0))
        item["note"]    = item.get("note", "")
    return items

def toggle_item(item_id, checked):
    get_col().update_one({"_id": ObjectId(item_id)}, {"$set": {"checked": 1 if checked else 0}})

def add_item(name, category, note=""):
    get_col().insert_one({"category": category, "name": name, "note": note, "checked": 0})

def delete_item(item_id):
    get_col().delete_one({"_id": ObjectId(item_id)})

def get_categories():
    return sorted(get_col().distinct("category"))

# ── Excel export ──────────────────────────────────────────────────────────────
def build_excel(items):
    wb = Workbook()
    ws = wb.active
    ws.title = "Packing List"

    green_fill  = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    header_fill = PatternFill(start_color="2E6FD8", end_color="2E6FD8", fill_type="solid")
    cat_fill    = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
    thin   = Side(border_style="thin", color="BBBBBB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    headers    = ["#", "Category", "Item Name", "Note", "Packed"]
    col_widths = [5, 28, 35, 45, 10]

    for ci, (h, w) in enumerate(zip(headers, col_widths), 1):
        cell           = ws.cell(row=1, column=ci, value=h)
        cell.font      = Font(bold=True, color="FFFFFF", size=11)
        cell.fill      = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border    = border
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.row_dimensions[1].height = 22

    items_sorted = sorted(items, key=lambda x: (x["category"], x["name"]))
    row = 2
    idx = 1
    for cat, group in groupby(items_sorted, key=lambda x: x["category"]):
        group_list = list(group)
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
        cat_cell           = ws.cell(row=row, column=1, value=f"  {cat}")
        cat_cell.fill      = cat_fill
        cat_cell.font      = Font(bold=True, size=11, color="1A3A72")
        cat_cell.alignment = Alignment(vertical="center")
        cat_cell.border    = border
        ws.row_dimensions[row].height = 18
        row += 1

        for item in group_list:
            is_checked = bool(item["checked"])
            values     = [idx, item["category"], item["name"], item["note"] or "", "✓" if is_checked else ""]
            for ci, val in enumerate(values, 1):
                cell           = ws.cell(row=row, column=ci, value=val)
                cell.border    = border
                cell.alignment = Alignment(vertical="center", wrap_text=(ci == 4))
                if is_checked:
                    cell.fill = green_fill
                    cell.font = Font(color="276221")
                if ci == 5:
                    cell.alignment = Alignment(horizontal="center", vertical="center")
            ws.row_dimensions[row].height = 16
            row += 1
            idx += 1

    ws.freeze_panes = "A2"
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf

# ── Excel import ──────────────────────────────────────────────────────────────
def restore_from_excel(file):
    try:
        df = pd.read_excel(file, sheet_name="Packing List")
    except Exception as e:
        return 0, f"Could not read sheet 'Packing List': {e}"

    df.columns = [c.strip().lower() for c in df.columns]
    required   = {"category", "item name", "note", "packed"}
    if not required.issubset(set(df.columns)):
        return 0, f"Missing columns. Expected: {required}. Got: {set(df.columns)}"

    df = df.dropna(subset=["item name"])
    df = df[df["item name"].astype(str).str.strip() != ""]

    col      = get_col()
    existing = set(
        (d["category"].strip().lower(), d["name"].strip().lower())
        for d in col.find({}, {"category": 1, "name": 1})
    )

    unique_rows, duplicates = [], []
    for _, r in df.iterrows():
        cat        = str(r["category"]).strip()
        name       = str(r["item name"]).strip()
        note       = "" if pd.isna(r["note"]) else str(r["note"]).strip()
        packed_val = str(r["packed"]).strip()
        checked    = 1 if packed_val in ("✓", "1", "True", "true", "yes", "Yes") else 0
        if not cat or not name:
            continue
        key = (cat.lower(), name.lower())
        if key in existing:
            duplicates.append(name)
        else:
            existing.add(key)
            unique_rows.append({"category": cat, "name": name, "note": note, "checked": checked})

    if not unique_rows and not duplicates:
        return 0, "No valid data rows found."

    if unique_rows:
        col.insert_many(unique_rows)

    msg = ""
    if duplicates:
        dup_list = ", ".join(f'"{d}"' for d in duplicates[:5])
        more     = f" (+{len(duplicates)-5} more)" if len(duplicates) > 5 else ""
        msg      = f"Skipped {len(duplicates)} duplicate(s): {dup_list}{more}"

    return len(unique_rows), msg

# ── CSS — Light mode, Playfair + Jost, blue accents ──────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap');

/* ── Base ── */
#MainMenu, footer { visibility: hidden; }
html, body, [class*="css"] {
    font-family: 'Jost', sans-serif !important;
    background: #EEF2FA !important;
    color: #1A2A42 !important;
}
.stApp { background: #EEF2FA !important; }
.block-container { padding-top: 1.5rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #E2E8F4 !important; border-right: 1px solid rgba(46,111,216,0.15) !important; }
[data-testid="stSidebar"] * { color: #1A2A42 !important; -webkit-text-fill-color: #1A2A42 !important; }

/* ── Sidebar brand ── */
.sb-brand { padding: 1.5rem 1rem 0.5rem; text-align: center; }
.sb-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem; font-weight: 500;
    color: #2E6FD8 !important; -webkit-text-fill-color: #2E6FD8 !important;
    letter-spacing: 0.06em;
}
.sb-mark {
    font-size: 0.6rem; text-transform: uppercase;
    letter-spacing: 0.22em; color: #5070A0 !important;
    -webkit-text-fill-color: #5070A0 !important; margin-top: 0.2rem;
}
.sb-sep { height: 1px; background: rgba(46,111,216,0.18); margin: 0.8rem 0.5rem; }

/* ── Page title ── */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem; font-weight: 500;
    color: #0F1E36; letter-spacing: 0.01em;
    line-height: 1.15; margin-bottom: 0.1rem;
}
.page-sub {
    font-size: 0.68rem; text-transform: uppercase;
    letter-spacing: 0.22em; color: #5070A0;
    margin-bottom: 1.8rem; font-weight: 400;
}

/* ── Stat boxes ── */
.stat-box {
    background: #FFFFFF;
    border: 1px solid rgba(46,111,216,0.18);
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
    box-shadow: 0 1px 6px rgba(46,111,216,0.08);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.stat-box:hover { box-shadow: 0 4px 16px rgba(46,111,216,0.14); transform: translateY(-1px); }
.stat-num { font-family: 'Playfair Display', serif; font-size: 1.7rem; font-weight: 500; color: #1A2A42; line-height: 1.2; }
.stat-lbl { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.14em; color: #5070A0; font-weight: 600; margin-top: 2px; }

/* ── Category header ── */
.cat-header {
    background: #EDF2FC;
    border-left: 4px solid #2E6FD8;
    padding: 9px 16px;
    border-radius: 0 8px 8px 0;
    font-family: 'Jost', sans-serif;
    font-weight: 600; font-size: 0.88rem;
    color: #1A3A72;
    margin: 18px 0 6px 0;
    letter-spacing: 0.02em;
}

/* ── Item rows ── */
.item-row {
    background: #FFFFFF;
    border: 1px solid rgba(46,111,216,0.1);
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 5px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.item-row:hover { border-color: rgba(46,111,216,0.3); box-shadow: 0 2px 8px rgba(46,111,216,0.08); }

/* ── Buttons ── */
.stButton > button {
    background: #FFFFFF !important;
    color: #2E6FD8 !important;
    border: 1px solid rgba(46,111,216,0.35) !important;
    border-radius: 8px !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #EDF2FC !important;
    color: #1A56C4 !important;
    border-color: #2E6FD8 !important;
    box-shadow: 0 2px 8px rgba(46,111,216,0.15) !important;
}
[data-testid="stBaseButton-primary"] {
    background: #2E6FD8 !important;
    color: #FFFFFF !important;
    border: none !important;
}
[data-testid="stBaseButton-primary"]:hover {
    background: #1A56C4 !important;
    box-shadow: 0 4px 16px rgba(46,111,216,0.3) !important;
}
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #5070A0 !important;
    border: 1px solid rgba(46,111,216,0.25) !important;
    border-radius: 8px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    border-color: #2E6FD8 !important;
    color: #2E6FD8 !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
input[type="text"], input[type="password"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(46,111,216,0.22) !important;
    border-radius: 8px !important;
    color: #1A2A42 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #2E6FD8 !important;
    box-shadow: 0 0 0 3px rgba(46,111,216,0.12) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid rgba(46,111,216,0.22) !important;
    border-radius: 8px !important;
    color: #1A2A42 !important;
}
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul { background: #FFFFFF !important; border: 1px solid rgba(46,111,216,0.18) !important; }
[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"] { background: #FFFFFF !important; color: #1A2A42 !important; }
[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] [role="option"]:hover { background: #EDF2FC !important; }

/* ── Labels ── */
.stTextInput label, .stSelectbox label, .stTextArea label,
.stCheckbox label, [data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {
    color: #5070A0 !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-family: 'Jost', sans-serif !important;
}

/* ── Alerts ── */
.stSuccess { background: rgba(61,154,108,0.08) !important; border: 1px solid rgba(61,154,108,0.28) !important; border-radius: 8px !important; }
.stInfo    { background: rgba(46,111,216,0.07) !important; border: 1px solid rgba(46,111,216,0.22) !important; border-radius: 8px !important; }
.stWarning { background: rgba(200,160,50,0.08) !important; border: 1px solid rgba(200,160,50,0.26) !important; border-radius: 8px !important; }
.stError   { background: rgba(192,80,96,0.08)  !important; border: 1px solid rgba(192,80,96,0.26)  !important; border-radius: 8px !important; }

/* ── Progress bar ── */
.stProgress > div > div { background: #2E6FD8 !important; }
.stProgress > div { background: rgba(46,111,216,0.12) !important; border-radius: 99px !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] > div {
    background: #FFFFFF !important;
    border: 2px dashed rgba(46,111,216,0.28) !important;
    border-radius: 10px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(46,111,216,0.3); border-radius: 99px; }

/* ── Backup section header ── */
.backup-head {
    font-family: 'Jost', sans-serif;
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.18em;
    color: #5070A0; margin: 1rem 0 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Login ─────────────────────────────────────────────────────────────────────
def login_screen():
    st.markdown("""
    <div style='text-align:center; padding-top:70px; padding-bottom:2rem;'>
        <div style='font-family:"Playfair Display",serif; font-size:2.2rem; font-weight:500; color:#0F1E36; letter-spacing:0.01em;'>
            🧳 Study Abroad
        </div>
        <div style='font-size:0.68rem; text-transform:uppercase; letter-spacing:0.28em; color:#5070A0; margin-top:0.4rem;'>
            Packing List Manager
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 1.1, 1])[1]
    with col:
        with st.container(border=True):
            st.markdown("<div style='font-family:\"Playfair Display\",serif; font-size:1.1rem; color:#0F1E36; margin-bottom:1rem;'>Sign in</div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            if st.button("Sign in", use_container_width=True, type="primary"):
                if username in USERS and USERS[username] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"]  = username
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

# ── Main App ──────────────────────────────────────────────────────────────────
def main_app():
    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div class='sb-brand'>
            <div class='sb-logo'>🧳 Packing</div>
            <div class='sb-mark'>Study Abroad Manager</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='sb-sep'></div>", unsafe_allow_html=True)

        st.markdown("<div class='backup-head'>🔍 Filter</div>", unsafe_allow_html=True)
        cats         = ["All"] + get_categories()
        selected_cat = st.selectbox("Category", cats, label_visibility="collapsed")
        search       = st.text_input("Search", placeholder="Search items...", label_visibility="collapsed")

        st.markdown("<div class='sb-sep'></div>", unsafe_allow_html=True)
        show_only_packed   = st.checkbox("Show only packed")
        show_only_unpacked = st.checkbox("Show only unpacked")

        st.markdown("<div class='sb-sep'></div>", unsafe_allow_html=True)
        st.markdown("<div class='backup-head'>💾 Backup & Restore</div>", unsafe_allow_html=True)

        _items = load_items()
        _excel = build_excel(_items)
        st.download_button(
            label="⬇️ Download checkpoint",
            data=_excel,
            file_name="packing_list_backup.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        uploaded = st.file_uploader("Restore from checkpoint", type=["xlsx"], label_visibility="collapsed")
        if uploaded:
            if st.button("✅ Confirm restore", use_container_width=True, type="primary"):
                n, msg = restore_from_excel(uploaded)
                if n == 0 and msg.startswith(("Could not", "Missing", "No valid")):
                    st.error(f"Restore failed: {msg}")
                else:
                    if n > 0:
                        st.success(f"Restored {n} new item(s)!")
                    if msg:
                        st.warning(msg)
                    st.rerun()

        st.markdown("<div class='sb-sep'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.72rem;color:#5070A0;text-align:center;padding-bottom:0.5rem;'>◆ {st.session_state.get('username','').title()}</div>", unsafe_allow_html=True)
        if st.button("🚪 Sign out", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # ── Header ────────────────────────────────────────────────────────────────
    col_title, col_add, col_dl = st.columns([4, 1, 1])
    with col_title:
        st.markdown("<div class='page-title'>🧳 Packing List</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Study Abroad · Item Tracker</div>", unsafe_allow_html=True)
    with col_add:
        st.markdown("<div style='margin-top:20px'>", unsafe_allow_html=True)
        if st.button("➕ Add item", use_container_width=True):
            st.session_state["show_add"] = not st.session_state.get("show_add", False)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_dl:
        st.markdown("<div style='margin-top:20px'>", unsafe_allow_html=True)
        items_all = load_items()
        excel_buf = build_excel(items_all)
        st.download_button(
            label="📥 Save Excel",
            data=excel_buf,
            file_name="packing_list.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Add item form ─────────────────────────────────────────────────────────
    if st.session_state.get("show_add", False):
        with st.container(border=True):
            st.markdown("<div style='font-family:\"Playfair Display\",serif;font-size:1rem;color:#0F1E36;margin-bottom:0.8rem;font-style:italic;'>Add a new item</div>", unsafe_allow_html=True)
            fc1, fc2 = st.columns(2)
            with fc1:
                new_name = st.text_input("Item name *", key="new_name", placeholder="e.g. Laptop charger")
            with fc2:
                existing_cats = get_categories()
                cat_options   = existing_cats + ["+ New category..."]
                cat_choice    = st.selectbox("Category *", cat_options, key="cat_choice")
            if cat_choice == "+ New category...":
                new_cat = st.text_input("New category name *", key="new_cat")
            else:
                new_cat = cat_choice
            new_note = st.text_input("Note (optional)", key="new_note", placeholder="e.g. 2 pcs, buy in India")
            c1, c2 = st.columns([1, 5])
            with c1:
                if st.button("Save", type="primary"):
                    if new_name.strip() and new_cat.strip():
                        add_item(new_name.strip(), new_cat.strip(), new_note.strip())
                        st.session_state["show_add"] = False
                        for k in ["new_name", "new_note", "new_cat", "cat_choice"]:
                            st.session_state.pop(k, None)
                        st.success(f"'{new_name}' added!")
                        st.rerun()
                    else:
                        st.error("Item name and category are required.")
            with c2:
                if st.button("Cancel"):
                    st.session_state["show_add"] = False
                    st.rerun()

    # ── Stats ─────────────────────────────────────────────────────────────────
    items_all = load_items()
    total  = len(items_all)
    packed = sum(1 for i in items_all if i["checked"])
    pct    = int(packed / total * 100) if total else 0

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{total}</div><div class='stat-lbl'>Total Items</div></div>", unsafe_allow_html=True)
    with s2:
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{packed}</div><div class='stat-lbl'>Packed ✓</div></div>", unsafe_allow_html=True)
    with s3:
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{total - packed}</div><div class='stat-lbl'>Remaining</div></div>", unsafe_allow_html=True)
    with s4:
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{pct}%</div><div class='stat-lbl'>Complete</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 12px 0 4px;'>", unsafe_allow_html=True)
    st.progress(pct / 100)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Filter ────────────────────────────────────────────────────────────────
    items = items_all
    if selected_cat != "All":
        items = [i for i in items if i["category"] == selected_cat]
    if search:
        q     = search.lower()
        items = [i for i in items if q in i["name"].lower() or q in (i["note"] or "").lower()]
    if show_only_packed:
        items = [i for i in items if i["checked"]]
    if show_only_unpacked:
        items = [i for i in items if not i["checked"]]

    items_sorted = sorted(items, key=lambda x: (x["category"], x["name"]))
    if not items_sorted:
        st.info("No items found. Try adjusting your filters.")
        return

    # ── Item list ─────────────────────────────────────────────────────────────
    for cat, group in groupby(items_sorted, key=lambda x: x["category"]):
        group_list     = list(group)
        checked_in_cat = sum(1 for i in group_list if i["checked"])
        st.markdown(
            f"<div class='cat-header'>{cat}"
            f"<span style='font-weight:400;font-size:0.78rem;color:#8AA0C0;margin-left:10px;'>{checked_in_cat}/{len(group_list)} packed</span></div>",
            unsafe_allow_html=True
        )
        for item in group_list:
            col_chk, col_info, col_del = st.columns([0.4, 9.2, 0.4])
            with col_chk:
                checked = st.checkbox(
                    label="packed", value=bool(item["checked"]),
                    key=f"chk_{item['id']}", label_visibility="collapsed"
                )
                if checked != bool(item["checked"]):
                    toggle_item(item["id"], checked)
                    st.rerun()
            with col_info:
                name_style = "color:#8AA0C0;text-decoration:line-through;" if item["checked"] else "color:#1A2A42;"
                note_html  = f"<span style='font-size:0.78rem;color:#8AA0C0;'> — {item['note']}</span>" if item["note"] else ""
                bg         = "background:#F0FDF4;border:1px solid rgba(61,154,108,0.18);" if item["checked"] else "background:#FFFFFF;border:1px solid rgba(46,111,216,0.1);"
                st.markdown(
                    f"<div style='padding:7px 12px;border-radius:8px;{bg}margin-bottom:4px;'>"
                    f"<span style='font-family:Jost,sans-serif;font-size:0.9rem;{name_style}'>{item['name']}</span>{note_html}"
                    f"</div>", unsafe_allow_html=True
                )
            with col_del:
                if st.button("🗑", key=f"del_{item['id']}", help="Delete"):
                    delete_item(item["id"])
                    st.rerun()

# ── Entry point ───────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_screen()
else:
    main_app()
