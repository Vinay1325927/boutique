import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv("credentials/.env")

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Boutique Manager",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PREMIUM CSS — Luxury Dark Gold Theme (Enhanced)
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold:        #C9A84C;
    --gold-light:  #E8C97A;
    --gold-dark:   #9A7A30;
    --gold-glow:   rgba(201,168,76,0.15);
    --dark:        #0D0C0A;
    --dark-2:      #161512;
    --dark-3:      #1E1D19;
    --dark-4:      #272622;
    --dark-5:      #2E2D28;
    --text-main:   #F0EDE6;
    --text-muted:  #9B9688;
    --text-dim:    #6B6860;
    --success:     #5DBB8A;
    --warning:     #E8A030;
    --danger:      #E05252;
    --info:        #5B9BD5;
    --radius:      10px;
    --radius-lg:   18px;
    --radius-xl:   24px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--dark) !important;
    color: var(--text-main) !important;
}

.stApp {
    background: var(--dark) !important;
    background-image:
        radial-gradient(ellipse at 15% 10%, rgba(201,168,76,0.06) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 85%, rgba(201,168,76,0.04) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 50%, rgba(201,168,76,0.01) 0%, transparent 80%);
}

/* ── TYPOGRAPHY ── */
.main-header {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.6rem;
    font-weight: 600;
    color: var(--gold);
    text-align: center;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
    text-shadow: 0 0 60px rgba(201,168,76,0.2);
    line-height: 1.2;
}
.main-subheader {
    text-align: center;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--text-dim);
    margin-bottom: 2rem;
}
h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--gold-light) !important;
    letter-spacing: 0.04em;
}
h4, h5 {
    color: var(--text-muted) !important;
    letter-spacing: 0.05em;
    font-size: 0.85rem !important;
    text-transform: uppercase;
}
p, span, div { font-family: 'DM Sans', sans-serif; }

/* ── DIVIDERS ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,168,76,0.5), transparent);
    margin: 1.8rem 0;
}
.gold-divider-sm {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,168,76,0.25), transparent);
    margin: 1rem 0;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--dark-3), var(--dark-4)) !important;
    border: 1px solid rgba(201,168,76,0.18) !important;
    border-radius: var(--radius) !important;
    padding: 1.1rem 1.4rem !important;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--gold), transparent);
    opacity: 0.6;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(201,168,76,0.45) !important;
    box-shadow: 0 6px 28px rgba(201,168,76,0.1) !important;
    transform: translateY(-1px);
}
[data-testid="stMetricLabel"] > div {
    color: var(--text-muted) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: var(--gold-light) !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--dark-2) !important;
    border-right: 1px solid rgba(201,168,76,0.12) !important;
}
[data-testid="stSidebar"] * { color: var(--text-main) !important; }
[data-testid="stSidebar"] .stRadio label {
    color: var(--text-main) !important;
    font-size: 0.88rem !important;
    font-weight: 400 !important;
    padding: 0.55rem 1rem;
    border-radius: 8px;
    transition: background 0.2s;
    display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(201,168,76,0.08);
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--gold-dark), var(--gold)) !important;
    color: #0D0C0A !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.06em;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 18px rgba(201,168,76,0.22) !important;
    width: 100% !important;
    text-transform: uppercase;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--gold), var(--gold-light)) !important;
    box-shadow: 0 8px 28px rgba(201,168,76,0.38) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
    background: transparent !important;
    color: var(--gold) !important;
    border: 1px solid rgba(201,168,76,0.35) !important;
    border-radius: var(--radius) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em;
    transition: all 0.25s ease !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: rgba(201,168,76,0.1) !important;
    border-color: var(--gold) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(201,168,76,0.15) !important;
}

/* ── FORMS ── */
.stForm button[type="submit"] {
    background: linear-gradient(135deg, var(--gold-dark), var(--gold)) !important;
    color: #0D0C0A !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.08em;
    padding: 0.8rem 2rem !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
    text-transform: uppercase;
}
.stForm button[type="submit"]:hover {
    box-shadow: 0 8px 30px rgba(201,168,76,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    background: var(--dark-3) !important;
    border: 1px solid rgba(201,168,76,0.18) !important;
    border-radius: var(--radius) !important;
    color: var(--text-main) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.25s ease !important;
    padding: 0.55rem 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stDateInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-dim) !important;
}

.stSelectbox > div > div {
    background: var(--dark-3) !important;
    border: 1px solid rgba(201,168,76,0.18) !important;
    border-radius: var(--radius) !important;
    color: var(--text-main) !important;
    transition: border-color 0.25s ease;
}
.stSelectbox > div > div:hover {
    border-color: rgba(201,168,76,0.4) !important;
}

/* ── LABELS ── */
.stTextInput label, .stNumberInput label, .stSelectbox label,
.stTextArea label, .stDateInput label, .stRadio label {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 0.3rem !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border-radius: var(--radius) !important;
    border: 1px solid rgba(201,168,76,0.12) !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background: var(--dark-3) !important;
    color: var(--gold) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
[data-testid="stDataFrame"] td {
    background: var(--dark-2) !important;
    color: var(--text-main) !important;
    font-size: 0.88rem;
    border-bottom: 1px solid rgba(201,168,76,0.06) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--dark-3) !important;
    border-radius: var(--radius) !important;
    padding: 4px !important;
    gap: 3px;
    border: 1px solid rgba(201,168,76,0.1);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
    padding: 0.5rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(201,168,76,0.15) !important;
    color: var(--gold-light) !important;
    box-shadow: 0 2px 8px rgba(201,168,76,0.1) !important;
}

/* ── EXPANDERS ── */
.streamlit-expanderHeader {
    background: var(--dark-3) !important;
    border: 1px solid rgba(201,168,76,0.15) !important;
    border-radius: var(--radius) !important;
    color: var(--gold-light) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s;
}
.streamlit-expanderHeader:hover {
    border-color: rgba(201,168,76,0.35) !important;
    background: var(--dark-4) !important;
}
.streamlit-expanderContent {
    background: var(--dark-2) !important;
    border: 1px solid rgba(201,168,76,0.1) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
}

/* ── ALERTS ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: var(--radius) !important;
    border-width: 1px !important;
}

/* ── LOGIN ── */
.login-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
}
.login-card {
    background: var(--dark-2);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: var(--radius-xl);
    padding: 3rem 2.8rem;
    box-shadow: 0 30px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(201,168,76,0.05);
    max-width: 420px;
    width: 100%;
}
.login-brand {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 600;
    color: var(--gold);
    letter-spacing: 0.12em;
    text-align: center;
    line-height: 1;
    text-shadow: 0 0 40px rgba(201,168,76,0.2);
}
.login-tagline {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.25em;
    color: var(--text-dim);
    text-align: center;
    margin-top: 0.4rem;
    margin-bottom: 2.5rem;
}

/* ── SIDEBAR BRAND ── */
.sidebar-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.65rem;
    font-weight: 600;
    color: var(--gold);
    letter-spacing: 0.08em;
    text-align: center;
    padding: 1rem 0 0.2rem;
}
.sidebar-sub {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: var(--text-dim);
    text-align: center;
    margin-bottom: 0.5rem;
}
.sidebar-user {
    font-size: 0.78rem;
    color: var(--text-muted);
    text-align: center;
    padding: 0.4rem 0;
}

/* ── CARDS ── */
.stat-card {
    background: var(--dark-3);
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}
.kpi-badge {
    display: inline-block;
    background: rgba(201,168,76,0.12);
    color: var(--gold);
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-success {
    background: rgba(93,187,138,0.12);
    color: var(--success);
}
.badge-warning {
    background: rgba(232,160,48,0.12);
    color: var(--warning);
}
.badge-danger {
    background: rgba(224,82,82,0.12);
    color: var(--danger);
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--dark-2); }
::-webkit-scrollbar-thumb { background: rgba(201,168,76,0.25); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(201,168,76,0.5); }

/* ── CHECKBOX ── */
.stCheckbox > label {
    color: var(--text-muted) !important;
    font-size: 0.88rem !important;
}

/* ── RADIO ── */
.stRadio > div { gap: 0.5rem; }
.stRadio > div > label {
    background: var(--dark-3) !important;
    border: 1px solid rgba(201,168,76,0.15) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
    cursor: pointer;
}
.stRadio > div > label[data-baseweb="radio"] input:checked + div {
    background: var(--gold) !important;
}

/* ── MISC ── */
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-weight: 500;
    color: var(--gold-light);
    letter-spacing: 0.04em;
    margin: 1.5rem 0 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(201,168,76,0.15);
}
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: var(--text-dim);
    font-size: 0.95rem;
}
.empty-state .icon { font-size: 2.5rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# PLOTLY DARK TEMPLATE
# =====================================================

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#9B9688", size=12),
    title=dict(font=dict(family="Cormorant Garamond", size=18, color="#E8C97A"), pad=dict(b=10)),
    xaxis=dict(
        gridcolor="rgba(201,168,76,0.07)",
        linecolor="rgba(201,168,76,0.15)",
        tickfont=dict(size=11),
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor="rgba(201,168,76,0.07)",
        linecolor="rgba(201,168,76,0.15)",
        tickfont=dict(size=11),
        showgrid=True,
    ),
    legend=dict(
        bgcolor="rgba(20,19,17,0.8)",
        bordercolor="rgba(201,168,76,0.2)",
        borderwidth=1,
        font=dict(color="#9B9688", size=11),
    ),
    margin=dict(l=16, r=16, t=48, b=16),
    colorway=["#C9A84C","#E8C97A","#9A7A30","#F0EDE6","#6B5A2E","#D4B46A","#5DBB8A","#5B9BD5"],
    hoverlabel=dict(
        bgcolor="rgba(20,19,17,0.95)",
        bordercolor="rgba(201,168,76,0.3)",
        font=dict(color="#F0EDE6", size=12),
    ),
)

def styled_fig(fig, height=360):
    fig.update_layout(**PLOT_LAYOUT, height=height)
    return fig

# =====================================================
# CONSTANTS
# =====================================================

CATEGORIES      = ["Sarees","Salwar Suits","Lehengas","Kurtis","Western Wear",
                    "Accessories","Kids Wear","Blouse","Fabric","Other"]
PAYMENT_METHODS = ["Cash","UPI","Card","Bank Transfer","Part Payment","Credit"]
STATE_OPTIONS   = ["Tamil Nadu","Maharashtra","Karnataka","Delhi","Gujarat","Rajasthan",
                    "West Bengal","Uttar Pradesh","Andhra Pradesh","Telangana","Other"]

# =====================================================
# MONGODB
# =====================================================

@st.cache_resource
def get_mongo_client():
    try:
        try:
            uri = st.secrets.get("MONGO_URI", os.getenv("MONGO_URI"))
        except Exception:
            uri = os.getenv("MONGO_URI")
        if not uri:
            st.error("⚠️ MONGO_URI not configured. Add it to Streamlit secrets or .env file.")
            st.stop()
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client
    except Exception as e:
        st.error(f"MongoDB connection failed: {e}")
        st.stop()

def get_db():
    return get_mongo_client()["boutique_db"]

def get_col():
    return get_db()["sales"]

def get_next_id():
    counter = get_db()["counters"].find_one_and_update(
        {"_id": "sales_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True,
    )
    return counter["seq"]

# =====================================================
# DATA HELPERS
# =====================================================

@st.cache_data(ttl=30)
def fetch_all() -> pd.DataFrame:
    docs = list(get_col().find({}, {"_id": 0}))
    if not docs:
        return pd.DataFrame()
    df = pd.DataFrame(docs)

    # Numeric coercion
    for c in ["buying_price", "selling_price", "amount_paid", "pending_amount"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    # Integer flags
    for c in ["payment_received", "delay_status"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    # Dates
    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    # Computed columns
    df["profit"] = df["selling_price"] - df["buying_price"]
    df["margin"] = (
        df["profit"] / df["selling_price"].replace(0, 1) * 100
    ).round(2)

    # Ensure optional columns exist
    for col in ["vendor", "product_description", "notes", "customer_phone"]:
        if col not in df.columns:
            df[col] = ""

    return df


def invalidate_cache():
    fetch_all.clear()


def metrics(df: pd.DataFrame) -> dict:
    if df.empty:
        return dict(sales=0, revenue=0, profit=0, pending=0, delayed=0, margin=0, customers=0)
    return dict(
        sales     = len(df),
        revenue   = df["selling_price"].sum(),
        profit    = df["profit"].sum(),
        pending   = df["pending_amount"].sum(),
        delayed   = int((df["delay_status"] == 1).sum()),
        margin    = df["margin"].mean(),
        customers = df["customer_name"].nunique(),
    )


def to_excel(df: pd.DataFrame) -> BytesIO:
    out = BytesIO()
    ex = df.copy()
    if "sale_date" in ex.columns:
        ex["sale_date"] = ex["sale_date"].astype(str)
    ex["profit"]        = (ex["selling_price"] - ex["buying_price"]).round(2)
    ex["profit_margin"] = (
        ex["profit"] / ex["selling_price"].replace(0, 1) * 100
    ).round(2)
    ex["status"]  = ex["payment_received"].map({0: "Pending", 1: "Received"})
    ex["delayed"] = ex["delay_status"].map({0: "No", 1: "Yes"})

    ordered = [
        "id","customer_name","customer_phone","sale_date","vendor",
        "product_category","product_description","buying_price","selling_price",
        "profit","profit_margin","amount_paid","pending_amount","status",
        "delayed","payment_method","notes","created_at",
    ]
    cols = [c for c in ordered if c in ex.columns]
    ex = ex[cols]
    ex.columns = [c.replace("_", " ").title() for c in ex.columns]

    with pd.ExcelWriter(out, engine="openpyxl") as w:
        ex.to_excel(w, index=False)
        ws = w.sheets["Sheet1"]
        for i, col in enumerate(ex.columns, 1):
            ml = max(
                ex.iloc[:, i - 1].astype(str).map(len).max(),
                len(col),
            ) + 4
            ws.column_dimensions[ws.cell(1, i).column_letter].width = min(ml, 45)

        # Style header row
        from openpyxl.styles import Font, PatternFill, Alignment
        gold_fill = PatternFill("solid", fgColor="C9A84C")
        for cell in ws[1]:
            cell.font = Font(bold=True, color="0D0C0A")
            cell.fill = gold_fill
            cell.alignment = Alignment(horizontal="center")

    out.seek(0)
    return out

# =====================================================
# SEARCH HELPERS
# =====================================================

def get_existing_customers():
    pipeline = [
        {"$match": {"customer_name": {"$ne": None, "$ne": ""}}},
        {"$group": {
            "_id": "$customer_name",
            "phone": {"$first": "$customer_phone"},
            "visits": {"$sum": 1},
            "last_sale": {"$max": "$sale_date"},
        }},
        {"$sort": {"_id": 1}},
    ]
    return list(get_col().aggregate(pipeline))

# =====================================================
# LOGIN
# =====================================================

def login():
    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown("""
        <div class='login-card'>
            <div class='login-brand'>✦ BOUTIQUE</div>
            <div class='login-tagline'>Management System</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            u = st.text_input("Username", placeholder="Enter your username")
            p = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In →", use_container_width=True)

        if submitted:
            try:
                cu = st.secrets.get("USERNAME", os.getenv("USERNAME", "admin"))
                cp = st.secrets.get("PASSWORD", os.getenv("PASSWORD", "1234"))
            except Exception:
                cu = os.getenv("USERNAME", "admin")
                cp = os.getenv("PASSWORD", "1234")

            if u == cu and p == cp:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

# =====================================================
# SIDEBAR
# =====================================================

def sidebar():
    with st.sidebar:
        st.markdown("<div class='sidebar-logo'>✦ BOUTIQUE</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-sub'>Management System</div>", unsafe_allow_html=True)
        st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)

        # Quick sidebar metrics
        df = fetch_all()
        m  = metrics(df)

        c1, c2 = st.columns(2)
        c1.metric("Pending", f"₹{m['pending']:,.0f}")
        c2.metric("Profit",  f"₹{m['profit']:,.0f}")
        c1.metric("Sales",   m["sales"])
        c2.metric("Clients", m["customers"])

        st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)

        nav = st.radio("Navigation", [
            "🏠  Dashboard",
            "➕  Add Sale",
            "📋  Review Accounts",
            "✏️  Update Transaction",
            "👥  Customer List",
            "📊  Analytics",
            "🔔  Reminders & Alerts",
            "📦  Inventory Tracker",
            "🚪  Logout",
        ], label_visibility="collapsed")

        st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='sidebar-user'>👤 {st.session_state.get('username','Admin').title()}</div>",
            unsafe_allow_html=True,
        )
    return nav

# =====================================================
# DASHBOARD
# =====================================================

def page_dashboard():
    st.markdown("<div class='main-header'>Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Business Overview</div>", unsafe_allow_html=True)

    df = fetch_all()
    m  = metrics(df)

    # KPI row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Sales",  m["sales"])
    c2.metric("Revenue",      f"₹{m['revenue']:,.0f}")
    c3.metric("Net Profit",   f"₹{m['profit']:,.0f}")
    c4.metric("Pending",      f"₹{m['pending']:,.0f}")
    c5.metric("Avg Margin",   f"{m['margin']:.1f}%")
    c6.metric("Customers",    m["customers"])

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
        <div class='empty-state'>
            <div class='icon'>✦</div>
            <div>No sales yet — start adding sales to see your dashboard come alive!</div>
        </div>
        """, unsafe_allow_html=True)
        return

    df["month"]  = df["sale_date"].dt.to_period("M").astype(str)

    # Charts row 1
    cl, cr = st.columns([3, 2])

    with cl:
        monthly = df.groupby("month").agg(
            revenue=("selling_price", "sum"),
            profit=("profit", "sum"),
            sales=("id", "count"),
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly["month"], y=monthly["revenue"],
            name="Revenue",
            marker_color="rgba(201,168,76,0.45)",
            marker_line_color="#C9A84C",
            marker_line_width=1.2,
        ))
        fig.add_trace(go.Scatter(
            x=monthly["month"], y=monthly["profit"],
            name="Profit",
            mode="lines+markers",
            line=dict(color="#5DBB8A", width=2.5),
            marker=dict(size=7, color="#5DBB8A"),
        ))
        styled_fig(fig, 300).update_layout(
            title="Monthly Revenue & Profit",
            barmode="overlay",
            legend=dict(orientation="h", y=1.15),
        )
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        paid    = (df["payment_received"] == 1).sum()
        pending = (df["payment_received"] == 0).sum()

        fig2 = go.Figure(go.Pie(
            labels=["Collected", "Pending"],
            values=[paid, pending],
            hole=0.68,
            marker=dict(colors=["#C9A84C", "#272622"]),
            textfont=dict(size=12),
            hovertemplate="%{label}: %{value} sales<extra></extra>",
        ))
        fig2.add_annotation(
            text=f"<b>{paid + pending}</b><br><span style='font-size:10px'>Sales</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="#E8C97A", family="Cormorant Garamond", size=22),
        )
        styled_fig(fig2, 300).update_layout(
            title="Payment Status",
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, x=0.3),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Charts row 2 — Category breakdown
    cl2, cr2 = st.columns(2)
    with cl2:
        cat_rev = df.groupby("product_category")["selling_price"].sum().reset_index()
        fig3 = px.pie(
            cat_rev, values="selling_price", names="product_category",
            title="Revenue by Category", hole=0.5,
            color_discrete_sequence=["#C9A84C","#E8C97A","#9A7A30","#D4B46A",
                                      "#6B5A2E","#F0EDE6","#B89640","#7A6728","#5DBB8A","#5B9BD5"],
        )
        styled_fig(fig3, 280)
        st.plotly_chart(fig3, use_container_width=True)

    with cr2:
        # 7-day rolling revenue
        daily = df.set_index("sale_date")["selling_price"].resample("D").sum().reset_index()
        daily.columns = ["date", "revenue"]
        daily["rolling"] = daily["revenue"].rolling(7, min_periods=1).mean()

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=daily["date"], y=daily["revenue"],
            name="Daily", marker_color="rgba(201,168,76,0.3)",
        ))
        fig4.add_trace(go.Scatter(
            x=daily["date"], y=daily["rolling"],
            name="7-day avg", line=dict(color="#E8C97A", width=2),
        ))
        styled_fig(fig4, 280).update_layout(title="Daily Revenue (7-day avg)", legend=dict(orientation="h", y=1.15))
        st.plotly_chart(fig4, use_container_width=True)

    # Recent sales table
    st.markdown("<div class='section-title'>Recent Sales</div>", unsafe_allow_html=True)
    recent = df.sort_values("sale_date", ascending=False).head(10).copy()
    recent["sale_date"] = recent["sale_date"].dt.strftime("%d %b %Y")
    recent["Status"]    = recent["payment_received"].map({1: "✅ Paid", 0: "⏳ Pending"})
    recent["Delayed"]   = recent["delay_status"].map({0: "—", 1: "⚠️ Yes"})

    show = recent[[
        "id","customer_name","sale_date","product_category",
        "selling_price","profit","pending_amount","Status","Delayed",
    ]].copy()
    show.columns = ["ID","Customer","Date","Category","Amount ₹","Profit ₹","Pending ₹","Status","Delayed"]
    st.dataframe(show, use_container_width=True, hide_index=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    da, db, _ = st.columns([1, 1, 2])
    with da:
        st.download_button(
            "📥 Export CSV",
            data=df.assign(sale_date=df["sale_date"].astype(str)).to_csv(index=False),
            file_name=f"boutique_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with db:
        st.download_button(
            "📊 Export Excel",
            data=to_excel(df),
            file_name=f"boutique_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

# =====================================================
# ADD SALE
# =====================================================

def page_add_sale():
    st.markdown("<div class='main-header'>Add New Sale</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Record a Transaction</div>", unsafe_allow_html=True)

    ctype = st.radio("", ["🆕 New Customer", "👥 Existing Customer"], horizontal=True)
    st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)

    cname, cphone = "", ""

    if ctype == "👥 Existing Customer":
        existing = get_existing_customers()
        if existing:
            opts  = [f"{r['_id']}  —  {r.get('phone','') or 'No phone'}" for r in existing]
            sel   = st.selectbox("Select Customer", opts)
            cname = sel.split("  —  ")[0].strip()
            rec   = next((r for r in existing if r["_id"] == cname), {})
            cphone = rec.get("phone", "")
            ca, cb, cc = st.columns(3)
            ca.info(f"**Name:** {cname}")
            cb.info(f"**Phone:** {cphone or 'N/A'}")
            cc.info(f"**Visits:** {rec.get('visits', '—')}")
        else:
            st.warning("No existing customers found. Switching to New Customer.")
            ctype = "🆕 New Customer"

    with st.form("sale_form", clear_on_submit=True):
        # Section: Customer
        st.markdown("<div class='section-title'>Customer Information</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            cname  = st.text_input("Customer Name *", value=cname,
                                   disabled=(ctype == "👥 Existing Customer"))
        with c2:
            cphone = st.text_input("Phone Number", value=cphone, placeholder="+91 XXXXXXXXXX",
                                   disabled=(ctype == "👥 Existing Customer"))
        with c3:
            sdate  = st.date_input("Sale Date", date.today())

        # Section: Product
        st.markdown("<div class='section-title'>Product Details</div>", unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        with p1:
            cat  = st.selectbox("Category *", CATEGORIES)
        with p2:
            vend = st.text_input("Vendor / Supplier")
        with p3:
            qty  = st.number_input("Quantity", min_value=1, step=1, value=1)

        desc = st.text_area("Product Description", placeholder="Describe the item — fabric, colour, design...", height=75)

        # Section: Pricing
        st.markdown("<div class='section-title'>Pricing & Payment</div>", unsafe_allow_html=True)
        pr1, pr2, pr3, pr4 = st.columns(4)
        with pr1:
            buy  = st.number_input("Buying Price (₹) *",  min_value=0.0, step=100.0, format="%.2f")
        with pr2:
            sell = st.number_input("Selling Price (₹) *", min_value=0.0, step=100.0, format="%.2f")
        with pr3:
            paid_amt = st.number_input("Amount Paid (₹)",     min_value=0.0, step=100.0, format="%.2f")
        with pr4:
            pm   = st.selectbox("Payment Method", PAYMENT_METHODS)

        # Live computed preview
        pending_amt = max(round(sell - paid_amt, 2), 0.0)
        profit_amt  = round((sell - buy) * qty, 2)
        margin_pct  = round(profit_amt / (sell * qty) * 100, 2) if sell > 0 else 0.0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Pending",       f"₹{pending_amt:,.2f}")
        m2.metric("Profit (Total)",f"₹{profit_amt:,.2f}")
        m3.metric("Margin",        f"{margin_pct:.1f}%")
        m4.metric("Total Value",   f"₹{sell * qty:,.2f}")

        notes = st.text_area("Notes / Remarks", placeholder="Any special instructions or notes...", height=65)

        submitted = st.form_submit_button("💾  Save Sale", use_container_width=True)

        if submitted:
            errs = []
            if not cname.strip():   errs.append("Customer name is required.")
            if buy  <= 0:           errs.append("Buying price must be greater than 0.")
            if sell <= 0:           errs.append("Selling price must be greater than 0.")
            if paid_amt > sell:     errs.append("Amount paid cannot exceed the selling price.")
            if sell < buy:
                st.warning("⚠️ Selling price is below buying price — this will result in a loss.")

            if errs:
                for e in errs:
                    st.error(e)
            else:
                get_col().insert_one({
                    "id":                 get_next_id(),
                    "customer_name":      cname.strip(),
                    "customer_phone":     cphone.strip(),
                    "sale_date":          str(sdate),
                    "vendor":             vend.strip(),
                    "product_category":   cat,
                    "product_description":desc.strip(),
                    "quantity":           qty,
                    "buying_price":       round(buy, 2),
                    "selling_price":      round(sell, 2),
                    "amount_paid":        round(paid_amt, 2),
                    "pending_amount":     pending_amt,
                    "payment_received":   1 if pending_amt == 0 else 0,
                    "delay_status":       0,
                    "payment_method":     pm,
                    "notes":              notes.strip(),
                    "created_at":         str(datetime.now()),
                })
                invalidate_cache()
                st.success(f"✅ Sale recorded for **{cname.strip()}**!")
                st.balloons()
                st.rerun()

# =====================================================
# REVIEW ACCOUNTS
# =====================================================

def page_review():
    st.markdown("<div class='main-header'>Review Accounts</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>All Transactions</div>", unsafe_allow_html=True)

    df = fetch_all()
    if df.empty:
        st.markdown("<div class='empty-state'><div class='icon'>📋</div><div>No transactions yet.</div></div>",
                    unsafe_allow_html=True)
        return

    # Filters
    with st.expander("🔍 Filter & Sort", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1: srch   = st.text_input("Customer Name / Phone")
        with c2: catf   = st.selectbox("Category",  ["All"] + CATEGORIES)
        with c3: payf   = st.selectbox("Payment",   ["All", "Paid", "Pending"])
        with c4: dlayf  = st.selectbox("Delay Flag",["All", "On Time", "Delayed"])

        c5, c6, c7 = st.columns(3)
        with c5:
            sortby = st.selectbox("Sort By", ["Date ↓","Date ↑","Amount ↓","Pending ↓","Profit ↓"])
        with c6:
            d_from = st.date_input("From Date", value=date.today() - timedelta(days=90))
        with c7:
            d_to   = st.date_input("To Date",   value=date.today())

    fdf = df.copy()

    # Apply filters
    if srch:
        mask = (
            fdf["customer_name"].str.contains(srch, case=False, na=False) |
            fdf["customer_phone"].astype(str).str.contains(srch, na=False)
        )
        fdf = fdf[mask]

    if catf != "All":
        fdf = fdf[fdf["product_category"] == catf]
    if payf == "Paid":
        fdf = fdf[fdf["payment_received"] == 1]
    elif payf == "Pending":
        fdf = fdf[fdf["payment_received"] == 0]
    if dlayf == "On Time":
        fdf = fdf[fdf["delay_status"] == 0]
    elif dlayf == "Delayed":
        fdf = fdf[fdf["delay_status"] == 1]

    # Date range
    fdf = fdf[
        (fdf["sale_date"] >= pd.Timestamp(d_from)) &
        (fdf["sale_date"] <= pd.Timestamp(d_to))
    ]

    # Sort
    sm = {
        "Date ↓":    ("sale_date",      False),
        "Date ↑":    ("sale_date",      True),
        "Amount ↓":  ("selling_price",  False),
        "Pending ↓": ("pending_amount", False),
        "Profit ↓":  ("profit",         False),
    }
    sc, sa = sm[sortby]
    fdf = fdf.sort_values(sc, ascending=sa)

    # Summary metrics
    st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Transactions",  len(fdf))
    m2.metric("Revenue",       f"₹{fdf['selling_price'].sum():,.0f}")
    m3.metric("Profit",        f"₹{fdf['profit'].sum():,.0f}")
    m4.metric("Pending",       f"₹{fdf['pending_amount'].sum():,.0f}")
    m5.metric("Avg Margin",    f"{fdf['margin'].mean():.1f}%" if not fdf.empty else "—")
    st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)

    # Table
    show = fdf[[
        "id","customer_name","customer_phone","sale_date","product_category",
        "buying_price","selling_price","profit","amount_paid","pending_amount",
        "payment_method","delay_status","payment_received",
    ]].copy()
    show["sale_date"]        = show["sale_date"].dt.strftime("%d %b %Y")
    show["delay_status"]     = show["delay_status"].map({0: "—", 1: "⚠️ Yes"})
    show["payment_received"] = show["payment_received"].map({0: "⏳ Pending", 1: "✅ Paid"})
    show.columns = ["ID","Customer","Phone","Date","Category","Buy ₹","Sell ₹",
                    "Profit ₹","Paid ₹","Pending ₹","Method","Delayed","Status"]
    st.dataframe(show, use_container_width=True, hide_index=True)

    # Export
    dc, de, _ = st.columns([1, 1, 2])
    with dc:
        st.download_button(
            "📥 CSV",
            data=fdf.assign(sale_date=fdf["sale_date"].astype(str)).to_csv(index=False),
            file_name=f"accounts_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with de:
        st.download_button(
            "📊 Excel",
            data=to_excel(fdf),
            file_name=f"accounts_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    # Mark payments section
    st.markdown("<div class='section-title'>Mark Payments</div>", unsafe_allow_html=True)
    pend = fdf[fdf["pending_amount"] > 0].sort_values("pending_amount", ascending=False)

    if pend.empty:
        st.success("🎉 All payments received for current filter!")
    else:
        st.markdown(
            f"<span class='kpi-badge badge-warning'>⚠️ {len(pend)} pending — ₹{pend['pending_amount'].sum():,.0f}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        for _, row in pend.iterrows():
            ca, cb, cc, cd, ce = st.columns([3, 2, 1.5, 1, 1])
            ca.write(f"**{row['customer_name']}** · {row['product_category']}")
            cb.write(f"₹{row['pending_amount']:,.2f} pending")
            cc.write(row["sale_date"].strftime("%d %b %Y") if pd.notna(row["sale_date"]) else "—")
            with cd:
                if st.button("✅ Paid", key=f"p_{row['id']}_{row['customer_name']}"):
                    get_col().update_one(
                        {"id": row["id"]},
                        {"$set": {
                            "payment_received": 1,
                            "amount_paid":       float(row["selling_price"]),
                            "pending_amount":    0.0,
                        }},
                    )
                    invalidate_cache()
                    st.success(f"Payment marked for {row['customer_name']}!")
                    st.rerun()
            with ce:
                if st.button("⚠️ Flag", key=f"f_{row['id']}_{row['customer_name']}"):
                    get_col().update_one({"id": row["id"]}, {"$set": {"delay_status": 1}})
                    invalidate_cache()
                    st.rerun()

# =====================================================
# UPDATE TRANSACTION
# =====================================================

def page_update():
    st.markdown("<div class='main-header'>Update Transaction</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Edit or Delete a Record</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        sname = st.text_input("🔍 Search by Customer Name")
    with c2:
        sid   = st.number_input("Or by Sale ID", min_value=0, step=1)

    if not sname and sid == 0:
        st.info("Enter a customer name or sale ID to search.")
        return

    q = (
        {"customer_name": {"$regex": sname, "$options": "i"}}
        if sname
        else {"id": int(sid)}
    )
    docs = list(get_col().find(q, {"_id": 0}))

    if not docs:
        st.warning("No matching transaction found.")
        return

    df = pd.DataFrame(docs)
    for c in ["buying_price", "selling_price", "amount_paid", "pending_amount"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    preview_cols = [c for c in ["id","customer_name","sale_date","product_category","selling_price","pending_amount","payment_received"] if c in df.columns]
    preview = df[preview_cols].copy()
    if "payment_received" in preview.columns:
        preview["payment_received"] = preview["payment_received"].map({0: "⏳ Pending", 1: "✅ Paid"})
    st.dataframe(preview, use_container_width=True, hide_index=True)

    sel = st.selectbox(
        "Select ID to Edit",
        df["id"].tolist(),
        format_func=lambda x: f"#{x} — {df[df['id']==x]['customer_name'].values[0]}",
    )
    row = df[df["id"] == sel].iloc[0]

    st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)

    with st.form("update_form"):
        st.markdown("<div class='section-title'>Customer & Product</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            nn  = st.text_input("Customer Name",  value=str(row.get("customer_name", "")))
            np  = st.text_input("Phone",           value=str(row.get("customer_phone", "")))
        with c2:
            ci  = CATEGORIES.index(row["product_category"]) if row.get("product_category") in CATEGORIES else 0
            nc  = st.selectbox("Category", CATEGORIES, index=ci)
            nv  = st.text_input("Vendor",  value=str(row.get("vendor", "")))
        with c3:
            # Parse existing date
            try:
                existing_date = pd.to_datetime(row.get("sale_date")).date()
            except Exception:
                existing_date = date.today()
            new_date = st.date_input("Sale Date", value=existing_date)
            nqty = st.number_input("Quantity", min_value=1, step=1,
                                   value=int(row.get("quantity", 1)))

        ndesc = st.text_area("Description", value=str(row.get("product_description", "")), height=65)

        st.markdown("<div class='section-title'>Pricing & Payment</div>", unsafe_allow_html=True)
        pr1, pr2, pr3, pr4 = st.columns(4)
        with pr1:
            nb  = st.number_input("Buying Price (₹)",  value=float(row["buying_price"]),  min_value=0.0, step=100.0, format="%.2f")
        with pr2:
            ns  = st.number_input("Selling Price (₹)", value=float(row["selling_price"]), min_value=0.0, step=100.0, format="%.2f")
        with pr3:
            npa = st.number_input("Amount Paid (₹)",   value=float(row["amount_paid"]),   min_value=0.0, step=100.0, format="%.2f")
        with pr4:
            pi  = PAYMENT_METHODS.index(row["payment_method"]) if row.get("payment_method") in PAYMENT_METHODS else 0
            npm = st.selectbox("Payment Method", PAYMENT_METHODS, index=pi)

        nd     = st.checkbox("Mark as Delayed", value=bool(row.get("delay_status", 0)))
        nnotes = st.text_area("Notes", value=str(row.get("notes", "")), height=65)

        npend  = max(round(ns - npa, 2), 0.0)
        nprofit = round(ns - nb, 2)

        m1, m2, m3 = st.columns(3)
        m1.metric("Updated Pending",  f"₹{npend:,.2f}")
        m2.metric("Updated Profit",   f"₹{nprofit:,.2f}")
        m3.metric("Updated Margin",   f"{(nprofit / ns * 100 if ns > 0 else 0):.1f}%")

        bu, bd = st.columns(2)
        with bu:
            upd = st.form_submit_button("💾  Save Changes", use_container_width=True)
        with bd:
            dlt = st.form_submit_button("🗑️  Delete Transaction", use_container_width=True)

        if upd:
            if npa > ns:
                st.error("Amount paid cannot exceed selling price.")
            else:
                get_col().update_one(
                    {"id": sel},
                    {"$set": {
                        "customer_name":       nn.strip(),
                        "customer_phone":      np.strip(),
                        "sale_date":           str(new_date),
                        "product_category":    nc,
                        "vendor":              nv.strip(),
                        "product_description": ndesc.strip(),
                        "quantity":            nqty,
                        "buying_price":        round(nb, 2),
                        "selling_price":       round(ns, 2),
                        "amount_paid":         round(npa, 2),
                        "pending_amount":      npend,
                        "delay_status":        int(nd),
                        "payment_method":      npm,
                        "notes":               nnotes.strip(),
                        "payment_received":    1 if npend == 0 else 0,
                        "updated_at":          str(datetime.now()),
                    }},
                )
                invalidate_cache()
                st.success("✅ Transaction updated successfully!")
                st.rerun()

        if dlt:
            get_col().delete_one({"id": sel})
            invalidate_cache()
            st.success("🗑️ Transaction deleted.")
            st.rerun()

# =====================================================
# CUSTOMER LIST
# =====================================================

def page_customers():
    st.markdown("<div class='main-header'>Customer List</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>All Clients</div>", unsafe_allow_html=True)

    df = fetch_all()
    if df.empty:
        st.markdown("<div class='empty-state'><div class='icon'>👥</div><div>No customers yet.</div></div>",
                    unsafe_allow_html=True)
        return

    summ = (
        df.groupby("customer_name")
        .agg(
            phone        =("customer_phone", "first"),
            transactions =("id",             "count"),
            spent        =("selling_price",  "sum"),
            pending      =("pending_amount", "sum"),
            last_visit   =("sale_date",      "max"),
            profit       =("profit",         "sum"),
        )
        .reset_index()
    )
    summ["last_visit"] = pd.to_datetime(summ["last_visit"]).dt.strftime("%d %b %Y")
    summ = summ.sort_values("spent", ascending=False).reset_index(drop=True)

    # Tier labels
    summ["tier"] = pd.cut(
        summ["spent"],
        bins=[0, 5000, 20000, 50000, float("inf")],
        labels=["🥉 Bronze", "🥈 Silver", "🥇 Gold", "💎 Platinum"],
    )

    # KPIs
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Customers",      len(summ))
    m2.metric("Avg Spend",            f"₹{summ['spent'].mean():,.0f}")
    m3.metric("With Pending",         len(summ[summ["pending"] > 0]))
    m4.metric("Total Revenue",        f"₹{summ['spent'].sum():,.0f}")

    st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        srch = st.text_input("🔍 Search Customer")
    with c2:
        tier_f = st.selectbox("Filter by Tier", ["All","🥉 Bronze","🥈 Silver","🥇 Gold","💎 Platinum"])

    view = summ.copy()
    if srch:
        view = view[view["customer_name"].str.contains(srch, case=False, na=False)]
    if tier_f != "All":
        view = view[view["tier"] == tier_f]

    disp = view.rename(columns={
        "customer_name": "Customer",
        "phone":         "Phone",
        "transactions":  "Visits",
        "spent":         "Total Spent ₹",
        "pending":       "Pending ₹",
        "last_visit":    "Last Visit",
        "profit":        "Profit ₹",
        "tier":          "Tier",
    })
    st.dataframe(
        disp.style.format({"Total Spent ₹": "₹{:,.0f}", "Pending ₹": "₹{:,.0f}", "Profit ₹": "₹{:,.0f}"}),
        use_container_width=True,
        hide_index=True,
    )

    # Download
    dc, de = st.columns(2)
    with dc:
        st.download_button("📥 CSV", data=disp.to_csv(index=False),
                           file_name=f"customers_{date.today()}.csv", mime="text/csv",
                           use_container_width=True)
    with de:
        out = BytesIO()
        with pd.ExcelWriter(out, engine="openpyxl") as w:
            disp.to_excel(w, index=False)
        out.seek(0)
        st.download_button("📊 Excel", data=out,
                           file_name=f"customers_{date.today()}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    # Purchase history
    st.markdown("<div class='section-title'>Purchase History</div>", unsafe_allow_html=True)
    chosen = st.selectbox("Select Customer", summ["customer_name"].tolist())

    if chosen:
        hist = df[df["customer_name"] == chosen].sort_values("sale_date", ascending=False).copy()
        hist["status"] = hist["payment_received"].map({0: "⏳ Pending", 1: "✅ Paid"})
        hist["sale_date"] = hist["sale_date"].dt.strftime("%d %b %Y")

        h1, h2, h3, h4 = st.columns(4)
        h1.metric("Visits",      len(hist))
        h2.metric("Total Spent", f"₹{hist['selling_price'].sum():,.0f}")
        h3.metric("Pending",     f"₹{hist['pending_amount'].sum():,.0f}")
        h4.metric("Profit",      f"₹{hist['profit'].sum():,.0f}")

        cols = [c for c in [
            "sale_date","product_category","product_description","selling_price",
            "amount_paid","pending_amount","payment_method","status",
        ] if c in hist.columns]
        show = hist[cols].copy()
        show.columns = ["Date","Category","Description","Price ₹","Paid ₹","Pending ₹","Method","Status"][:len(cols)]
        st.dataframe(show, use_container_width=True, hide_index=True)

        # Spending trend chart
        if len(hist) > 1:
            hist_sorted = df[df["customer_name"] == chosen].sort_values("sale_date").copy()
            hist_sorted["cumulative"] = hist_sorted["selling_price"].cumsum()
            fig = px.line(
                hist_sorted, x="sale_date", y="cumulative",
                title=f"Cumulative Spending — {chosen}",
                markers=True,
            )
            fig.update_traces(line_color="#C9A84C", marker_color="#E8C97A")
            styled_fig(fig, 240)
            st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ANALYTICS
# =====================================================

def page_analytics():
    st.markdown("<div class='main-header'>Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Business Intelligence</div>", unsafe_allow_html=True)

    df = fetch_all()
    if df.empty:
        st.info("No data available for analytics.")
        return

    df["month"] = df["sale_date"].dt.to_period("M").astype(str)
    df["dow"]   = df["sale_date"].dt.day_name()
    df["week"]  = df["sale_date"].dt.isocalendar().week.astype(str)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Revenue",       f"₹{df['selling_price'].sum():,.0f}")
    k2.metric("Profit",        f"₹{df['profit'].sum():,.0f}")
    k3.metric("Avg Order",     f"₹{df['selling_price'].mean():,.0f}")
    k4.metric("Avg Margin",    f"{df['margin'].mean():.1f}%")
    k5.metric("Delayed Count", int((df["delay_status"] == 1).sum()))

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs(["📈 Trends","👥 Customers","📦 Categories","💸 Payments","🏆 Top Items"])

    # ── TRENDS ──
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            monthly = df.groupby("month").agg(
                revenue=("selling_price","sum"), profit=("profit","sum"),
            ).reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=monthly["month"], y=monthly["revenue"], name="Revenue",
                                 marker_color="rgba(201,168,76,0.45)", marker_line_color="#C9A84C", marker_line_width=1.2))
            fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["profit"], name="Profit",
                                     mode="lines+markers", line=dict(color="#5DBB8A", width=2.5), marker=dict(size=7)))
            styled_fig(fig).update_layout(title="Revenue & Profit by Month", barmode="overlay",
                                          legend=dict(orientation="h", y=1.15))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            daily = df.set_index("sale_date")["selling_price"].resample("D").sum().reset_index()
            daily.columns = ["date", "revenue"]
            fig2 = px.area(daily, x="date", y="revenue", title="Daily Revenue Trend")
            fig2.update_traces(fillcolor="rgba(201,168,76,0.12)", line_color="#C9A84C")
            styled_fig(fig2)
            st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            dow = df.groupby("dow").agg(sales=("id","count"), revenue=("selling_price","sum")).reset_index()
            dow["dow"] = pd.Categorical(dow["dow"], categories=dow_order, ordered=True)
            dow = dow.sort_values("dow")
            fig3 = px.bar(dow, x="dow", y="sales", title="Sales by Day of Week",
                          color="revenue",
                          color_continuous_scale=[[0,"#1E1D19"],[1,"#C9A84C"]])
            styled_fig(fig3)
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            monthly["MoM Growth %"] = monthly["revenue"].pct_change() * 100
            fig4 = px.bar(
                monthly.dropna(), x="month", y="MoM Growth %",
                title="Month-over-Month Revenue Growth",
                color="MoM Growth %",
                color_continuous_scale=[[0,"#E05252"],[0.5,"#272622"],[1,"#5DBB8A"]],
            )
            styled_fig(fig4)
            st.plotly_chart(fig4, use_container_width=True)

    # ── CUSTOMERS ──
    with t2:
        c1, c2 = st.columns(2)
        with c1:
            top_c = df.groupby("customer_name")["selling_price"].sum().nlargest(10).reset_index()
            fig5  = px.bar(top_c, x="selling_price", y="customer_name", orientation="h",
                           title="Top 10 Customers by Revenue",
                           color="selling_price",
                           color_continuous_scale=[[0,"#1E1D19"],[1,"#C9A84C"]])
            styled_fig(fig5)
            fig5.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig5, use_container_width=True)

        with c2:
            cp = df.groupby("customer_name")["pending_amount"].sum()
            cp = cp[cp > 0].nlargest(10).reset_index()
            if not cp.empty:
                fig6 = px.bar(cp, x="pending_amount", y="customer_name", orientation="h",
                              title="Top Customers by Pending",
                              color="pending_amount",
                              color_continuous_scale=[[0,"#1E1D19"],[1,"#E8A030"]])
                styled_fig(fig6)
                fig6.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.success("🎉 No pending amounts!")

        # Customer frequency vs value scatter
        cust_stats = df.groupby("customer_name").agg(
            visits=("id","count"),
            revenue=("selling_price","sum"),
            avg_order=("selling_price","mean"),
        ).reset_index()
        fig_scatter = px.scatter(
            cust_stats, x="visits", y="revenue", size="avg_order",
            hover_name="customer_name", title="Customer Value Matrix (size = avg order)",
            color="revenue", color_continuous_scale=[[0,"#1E1D19"],[1,"#C9A84C"]],
        )
        styled_fig(fig_scatter, 350)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Tier table
        seg = df.groupby("customer_name").agg(spend=("selling_price","sum")).reset_index()
        seg["tier"] = pd.cut(seg["spend"], bins=[0,5000,20000,50000,float("inf")],
                             labels=["🥉 Bronze","🥈 Silver","🥇 Gold","💎 Platinum"])
        st.markdown("<div class='section-title'>Customer Tier Distribution</div>", unsafe_allow_html=True)
        sg = (
            seg.groupby("tier", observed=True)
            .agg(customers=("customer_name","count"), total=("spend","sum"))
            .reset_index()
        )
        sg.columns = ["Tier","Customers","Total Spend ₹"]
        st.dataframe(sg, use_container_width=True, hide_index=True)

    # ── CATEGORIES ──
    with t3:
        c1, c2 = st.columns(2)
        with c1:
            cd = df.groupby("product_category").size().reset_index(name="count")
            fig7 = px.pie(cd, values="count", names="product_category",
                          title="Sales Volume by Category", hole=0.52,
                          color_discrete_sequence=["#C9A84C","#E8C97A","#9A7A30","#D4B46A",
                                                    "#6B5A2E","#F0EDE6","#B89640","#7A6728","#5DBB8A","#5B9BD5"])
            styled_fig(fig7)
            st.plotly_chart(fig7, use_container_width=True)

        with c2:
            cp2 = df.groupby("product_category").agg(
                profit=("profit","sum"), revenue=("selling_price","sum"),
            ).reset_index()
            cp2["margin"] = (cp2["profit"] / cp2["revenue"] * 100).round(1)
            fig8 = px.bar(cp2, x="product_category", y="profit", title="Profit by Category",
                          color="margin", color_continuous_scale=[[0,"#1E1D19"],[1,"#5DBB8A"]],
                          labels={"margin":"Margin %"})
            styled_fig(fig8)
            st.plotly_chart(fig8, use_container_width=True)

        cm = df.groupby(["month","product_category"])["selling_price"].sum().unstack(fill_value=0)
        if not cm.empty:
            fig9 = px.imshow(
                cm.T, title="Category × Month Revenue Heatmap",
                color_continuous_scale=[[0,"#0D0C0A"],[0.4,"#6B5A2E"],[1,"#C9A84C"]],
                aspect="auto",
            )
            styled_fig(fig9, 320)
            st.plotly_chart(fig9, use_container_width=True)

    # ── PAYMENTS ──
    with t4:
        c1, c2 = st.columns(2)
        with c1:
            pm = df.groupby("payment_method").size().reset_index(name="count")
            fig10 = px.pie(pm, values="count", names="payment_method",
                           title="Payment Method Distribution", hole=0.55,
                           color_discrete_sequence=["#C9A84C","#E8C97A","#9A7A30","#D4B46A","#6B5A2E","#5DBB8A"])
            styled_fig(fig10)
            st.plotly_chart(fig10, use_container_width=True)

        with c2:
            ps = df.groupby("payment_received").agg(count=("id","count"), total=("pending_amount","sum")).reset_index()
            ps["label"] = ps["payment_received"].map({0: "Pending", 1: "Received"})
            fig11 = px.bar(ps, x="label", y="count", title="Payment Status Count",
                           color="label", color_discrete_map={"Pending":"#E8A030","Received":"#5DBB8A"})
            styled_fig(fig11)
            st.plotly_chart(fig11, use_container_width=True)

        # Aging buckets
        aged = df[df["pending_amount"] > 0].copy()
        if not aged.empty:
            today_ts = pd.Timestamp(date.today())
            aged["days"] = (today_ts - aged["sale_date"]).dt.days
            aged["bucket"] = pd.cut(
                aged["days"],
                bins=[0, 7, 15, 30, 60, 9999],
                labels=["0–7 days","8–15 days","16–30 days","31–60 days","60+ days"],
            )
            ag = aged.groupby("bucket", observed=True)["pending_amount"].sum().reset_index()
            fig12 = px.bar(ag, x="bucket", y="pending_amount", title="Pending Payments — Aging Buckets",
                           color="pending_amount",
                           color_continuous_scale=[[0,"#E8A030"],[1,"#E05252"]])
            styled_fig(fig12)
            st.plotly_chart(fig12, use_container_width=True)
        else:
            st.success("🎉 No pending payments!")

    # ── TOP ITEMS ──
    with t5:
        c1, c2 = st.columns(2)
        with c1:
            if "vendor" in df.columns:
                vd = (
                    df[df["vendor"].astype(str).str.strip() != ""]
                    .groupby("vendor")
                    .agg(revenue=("selling_price","sum"), items=("id","count"))
                    .nlargest(10, "revenue")
                    .reset_index()
                )
                if not vd.empty:
                    fig13 = px.bar(vd, x="revenue", y="vendor", orientation="h", title="Top Vendors by Revenue",
                                   color="revenue", color_continuous_scale=[[0,"#1E1D19"],[1,"#C9A84C"]])
                    styled_fig(fig13)
                    fig13.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig13, use_container_width=True)
                else:
                    st.info("Add vendor names to see this chart.")

        with c2:
            if "product_description" in df.columns:
                pd2 = df[df["product_description"].astype(str).str.strip() != ""].copy()
                if not pd2.empty:
                    tm = (
                        pd2.groupby("product_description")
                        .agg(margin=("margin","mean"), revenue=("selling_price","sum"))
                        .nlargest(10, "margin")
                        .reset_index()
                    )
                    tm["product_description"] = tm["product_description"].str[:32]
                    fig14 = px.bar(tm, x="margin", y="product_description", orientation="h",
                                   title="Top Products by Margin %",
                                   color="margin",
                                   color_continuous_scale=[[0,"#1E1D19"],[1,"#5DBB8A"]])
                    styled_fig(fig14)
                    fig14.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig14, use_container_width=True)
                else:
                    st.info("Add product descriptions to see this chart.")

# =====================================================
# REMINDERS & ALERTS
# =====================================================

def page_reminders():
    st.markdown("<div class='main-header'>Reminders & Alerts</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Payment Follow-ups</div>", unsafe_allow_html=True)

    df = fetch_all()
    if df.empty:
        st.info("No data available.")
        return

    today_ts  = pd.Timestamp(date.today())
    df["days_old"] = (today_ts - df["sale_date"]).dt.days

    # Alert banner
    overdue_count = len(df[(df["pending_amount"] > 0) & (df["days_old"] > 30)])
    flagged_count = int((df["delay_status"] == 1).sum())

    if overdue_count or flagged_count:
        bc = st.columns(2)
        if overdue_count:
            bc[0].error(f"🔴 **{overdue_count}** payments overdue (30+ days)")
        if flagged_count:
            bc[1].warning(f"⚠️ **{flagged_count}** transactions flagged as delayed")
    else:
        st.success("✅ All clear! No overdue or flagged payments.")

    st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs([
        "⚠️ Overdue (30d+)",
        "🔴 Flagged Delayed",
        "💎 High Value Sales",
        "📆 Upcoming Follow-ups",
    ])

    with t1:
        ov = df[(df["pending_amount"] > 0) & (df["days_old"] > 30)].sort_values("days_old", ascending=False)
        if ov.empty:
            st.success("✅ No overdue payments!")
        else:
            st.warning(f"**{len(ov)} overdue** — ₹{ov['pending_amount'].sum():,.0f} total")
            for _, r in ov.iterrows():
                with st.expander(
                    f"**{r['customer_name']}**  ·  ₹{r['pending_amount']:,.0f}  ·  {int(r['days_old'])} days overdue"
                ):
                    ca, cb, cc, cd = st.columns([2, 2, 1, 1])
                    ca.write(f"📅 {r['sale_date'].strftime('%d %b %Y')}")
                    cb.write(f"📦 {r.get('product_category','—')}")
                    with cc:
                        if st.button("✅ Mark Paid", key=f"op_{r['id']}"):
                            get_col().update_one(
                                {"id": r["id"]},
                                {"$set": {
                                    "payment_received": 1,
                                    "amount_paid":       float(r["selling_price"]),
                                    "pending_amount":    0.0,
                                }},
                            )
                            invalidate_cache()
                            st.rerun()
                    with cd:
                        if st.button("📱 Remind", key=f"or_{r['id']}"):
                            st.toast(f"Reminder note created for {r['customer_name']} ✓")

    with t2:
        dl = df[df["delay_status"] == 1].sort_values("pending_amount", ascending=False)
        if dl.empty:
            st.success("✅ No flagged payments!")
        else:
            st.error(f"**{len(dl)} flagged** — ₹{dl['pending_amount'].sum():,.0f}")
            show = dl[[
                "customer_name","sale_date","product_category","selling_price","pending_amount","days_old",
            ]].copy()
            show["sale_date"] = show["sale_date"].dt.strftime("%d %b %Y")
            show.columns = ["Customer","Date","Category","Amount ₹","Pending ₹","Days Old"]
            st.dataframe(show, use_container_width=True, hide_index=True)

            sc = st.selectbox("Clear delay flag for:", dl["id"].tolist(),
                              format_func=lambda x: f"#{x} — {dl[dl['id']==x]['customer_name'].values[0]}")
            if st.button("✅ Clear Flag"):
                get_col().update_one({"id": sc}, {"$set": {"delay_status": 0}})
                invalidate_cache()
                st.success("Flag cleared.")
                st.rerun()

    with t3:
        hv = df[df["selling_price"] >= 10000].sort_values("selling_price", ascending=False).head(20).copy()
        if hv.empty:
            st.info("No high-value sales (₹10,000+) yet.")
        else:
            hv["sale_date"]        = hv["sale_date"].dt.strftime("%d %b %Y")
            hv["payment_received"] = hv["payment_received"].map({0: "⏳ Pending", 1: "✅ Paid"})
            show = hv[[
                "customer_name","sale_date","product_category",
                "selling_price","profit","payment_received",
            ]].copy()
            show.columns = ["Customer","Date","Category","Amount ₹","Profit ₹","Status"]
            st.dataframe(show, use_container_width=True, hide_index=True)

    with t4:
        # Upcoming: pending payments < 30 days old (follow up soon)
        soon = df[
            (df["pending_amount"] > 0) &
            (df["days_old"] >= 7) &
            (df["days_old"] <= 30) &
            (df["delay_status"] == 0)
        ].sort_values("days_old", ascending=False)

        if soon.empty:
            st.info("No follow-ups needed in the 7–30 day window.")
        else:
            st.info(f"**{len(soon)} sales** have pending payments between 7–30 days old.")
            show = soon[[
                "customer_name","customer_phone","sale_date","product_category",
                "pending_amount","days_old",
            ]].copy()
            show["sale_date"] = show["sale_date"].dt.strftime("%d %b %Y")
            show.columns = ["Customer","Phone","Date","Category","Pending ₹","Days Old"]
            st.dataframe(show, use_container_width=True, hide_index=True)

# =====================================================
# INVENTORY TRACKER (NEW)
# =====================================================

def page_inventory():
    st.markdown("<div class='main-header'>Inventory Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subheader'>Stock Management</div>", unsafe_allow_html=True)

    inv_col = get_db()["inventory"]

    t1, t2 = st.tabs(["📦 Current Stock", "➕ Add / Update Stock"])

    with t1:
        items = list(inv_col.find({}, {"_id": 0}))
        if not items:
            st.markdown("""
            <div class='empty-state'>
                <div class='icon'>📦</div>
                <div>No inventory items yet. Add stock in the second tab.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            inv_df = pd.DataFrame(items)

            # KPIs
            m1, m2, m3, m4 = st.columns(4)
            total_items  = len(inv_df)
            total_value  = (inv_df.get("quantity", pd.Series([0])) * inv_df.get("cost_price", pd.Series([0]))).sum()
            low_stock    = inv_df[inv_df.get("quantity", pd.Series([0])) <= inv_df.get("min_stock", pd.Series([5]))]
            out_of_stock = inv_df[inv_df.get("quantity", pd.Series([0])) == 0]

            m1.metric("Total SKUs",    total_items)
            m2.metric("Inventory Value", f"₹{total_value:,.0f}")
            m3.metric("Low Stock",     len(low_stock))
            m4.metric("Out of Stock",  len(out_of_stock))

            if not low_stock.empty:
                st.warning(f"⚠️ {len(low_stock)} item(s) running low on stock!")

            st.markdown("<div class='gold-divider-sm'></div>", unsafe_allow_html=True)

            cat_f = st.selectbox("Filter by Category", ["All"] + CATEGORIES)
            view  = inv_df.copy()
            if cat_f != "All" and "category" in view.columns:
                view = view[view["category"] == cat_f]

            if "quantity" in view.columns and "min_stock" in view.columns:
                view["Stock Status"] = view.apply(
                    lambda r: "🔴 Out of Stock" if r["quantity"] == 0
                    else ("⚠️ Low Stock" if r["quantity"] <= r["min_stock"] else "✅ OK"),
                    axis=1,
                )

            st.dataframe(view, use_container_width=True, hide_index=True)

            if "category" in inv_df.columns and "quantity" in inv_df.columns:
                cat_stock = inv_df.groupby("category")["quantity"].sum().reset_index()
                fig = px.bar(cat_stock, x="category", y="quantity",
                             title="Stock by Category",
                             color="quantity",
                             color_continuous_scale=[[0,"#E05252"],[0.4,"#E8A030"],[1,"#5DBB8A"]])
                styled_fig(fig, 280)
                st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.markdown("<div class='section-title'>Add or Update Stock Item</div>", unsafe_allow_html=True)
        with st.form("inv_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                item_name  = st.text_input("Item Name *", placeholder="e.g. Banarasi Silk Saree")
                item_sku   = st.text_input("SKU / Code",  placeholder="e.g. SAR-001")
                item_cat   = st.selectbox("Category", CATEGORIES)
                item_vend  = st.text_input("Vendor / Supplier")
            with c2:
                item_qty   = st.number_input("Current Quantity *", min_value=0, step=1)
                item_min   = st.number_input("Minimum Stock Alert", min_value=0, step=1, value=5)
                item_cost  = st.number_input("Cost Price (₹) *",  min_value=0.0, step=50.0, format="%.2f")
                item_mrp   = st.number_input("Selling Price (₹)", min_value=0.0, step=50.0, format="%.2f")

            item_notes = st.text_area("Notes", height=60)

            if st.form_submit_button("💾  Save Item", use_container_width=True):
                if not item_name.strip():
                    st.error("Item name is required.")
                else:
                    inv_col.update_one(
                        {"sku": item_sku.strip() or item_name.strip()},
                        {"$set": {
                            "name":       item_name.strip(),
                            "sku":        item_sku.strip(),
                            "category":   item_cat,
                            "vendor":     item_vend.strip(),
                            "quantity":   item_qty,
                            "min_stock":  item_min,
                            "cost_price": round(item_cost, 2),
                            "sell_price": round(item_mrp, 2),
                            "notes":      item_notes.strip(),
                            "updated_at": str(datetime.now()),
                        }},
                        upsert=True,
                    )
                    st.success(f"✅ '{item_name.strip()}' saved to inventory!")
                    st.rerun()

# =====================================================
# MAIN
# =====================================================

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
        return

    page = sidebar()

    if   "Dashboard"   in page: page_dashboard()
    elif "Add Sale"    in page: page_add_sale()
    elif "Review"      in page: page_review()
    elif "Update"      in page: page_update()
    elif "Customer"    in page: page_customers()
    elif "Analytics"   in page: page_analytics()
    elif "Reminders"   in page: page_reminders()
    elif "Inventory"   in page: page_inventory()
    elif "Logout"      in page:
        st.session_state.logged_in = False
        st.session_state.username  = None
        st.rerun()

if __name__ == "__main__":
    main()
