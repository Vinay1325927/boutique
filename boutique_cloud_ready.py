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
    page_title="Vinay",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PREMIUM CSS — Editorial Luxury Redesign
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap');

:root {
    --ink:          #1A1714;
    --ink-2:        #242018;
    --ink-3:        #2E2A24;
    --ink-4:        #3A342C;
    --ink-5:        #47403A;
    --gold:         #2A5FA5;
    --gold-soft:    #4A80C8;
    --gold-pale:    #A8C4E8;
    --gold-glow:    rgba(42,95,165,0.12);
    --cream:        #F5F0E8;
    --cream-dim:    #E8E0D0;
    --muted:        #8C8070;
    --dim:          #5C5248;
    --emerald:      #3D7A5C;
    --rose:         #B05050;
    --sky:          #4A7FA0;
    --r:            8px;
    --r-lg:         14px;
    --r-xl:         20px;
    --border:       rgba(42,95,165,0.14);
    --border-hover: rgba(42,95,165,0.32);
    --shadow:       0 2px 24px rgba(0,0,0,0.4);
    --shadow-lg:    0 8px 48px rgba(0,0,0,0.55);
}

/* ━━━ BASE ━━━ */
html, body, [class*="css"] {
    font-family: 'Jost', sans-serif !important;
    background: var(--ink) !important;
    color: var(--cream) !important;
}

.stApp {
    background: var(--ink) !important;
    background-image:
        radial-gradient(ellipse 900px 600px at 0% 0%, rgba(42,95,165,0.06) 0%, transparent 70%),
        radial-gradient(ellipse 700px 500px at 100% 100%, rgba(42,95,165,0.04) 0%, transparent 70%);
    background-attachment: fixed;
}

/* ━━━ SCROLLBAR ━━━ */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(42,95,165,0.35); border-radius: 99px; }

/* ━━━ TYPOGRAPHY ━━━ */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--cream) !important;
    letter-spacing: 0.01em;
    font-weight: 500 !important;
}
h4, h5, h6 {
    font-family: 'Jost', sans-serif !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
}

/* PAGE TITLE */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 500;
    color: var(--cream);
    letter-spacing: 0.01em;
    line-height: 1.15;
    margin-bottom: 0.2rem;
}
.page-sub {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    color: var(--dim);
    margin-bottom: 2.4rem;
    font-weight: 400;
}
.rule {
    height: 1px;
    background: linear-gradient(90deg, var(--gold) 0%, rgba(42,95,165,0.2) 60%, transparent 100%);
    margin: 2rem 0;
    border: none;
}
.rule-sm {
    height: 1px;
    background: linear-gradient(90deg, rgba(42,95,165,0.35), transparent);
    margin: 1.2rem 0;
    border: none;
}

/* ━━━ SIDEBAR ━━━ */
[data-testid="stSidebar"] {
    background: var(--ink-2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }

.sb-brand {
    padding: 2rem 1.5rem 0.5rem;
    text-align: center;
}
.sb-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.75rem;
    font-weight: 500;
    color: var(--gold-soft);
    letter-spacing: 0.12em;
    line-height: 1;
}
.sb-mark {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.28em;
    color: var(--dim);
    margin-top: 0.3rem;
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
}
[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent !important;
    border: none !important;
    border-radius: var(--r) !important;
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.03em !important;
    padding: 0.55rem 1rem 0.55rem 0.75rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer;
    display: flex;
    align-items: center;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(42,95,165,0.1) !important;
    color: var(--cream) !important;
}
/* hide radio dot */
[data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none !important; }

.sb-user {
    font-size: 0.75rem;
    color: var(--dim);
    text-align: center;
    padding: 0.6rem 0 1.5rem;
    letter-spacing: 0.06em;
}
.sb-sep {
    height: 1px;
    background: var(--border);
    margin: 0.8rem 1rem;
}

/* ━━━ METRICS ━━━ */
[data-testid="stMetric"] {
    background: var(--ink-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important;
    padding: 1.25rem 1.4rem !important;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s ease, transform 0.2s ease !important;
}
[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--gold), transparent);
    opacity: 0.5;
}
[data-testid="stMetric"]:hover {
    border-color: var(--border-hover) !important;
    transform: translateY(-2px);
}
[data-testid="stMetricLabel"] > div {
    color: var(--dim) !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.16em !important;
    font-weight: 600 !important;
    font-family: 'Jost', sans-serif !important;
}
[data-testid="stMetricValue"] {
    color: var(--cream) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

/* ━━━ BUTTONS ━━━ */
.stButton > button {
    background: transparent !important;
    color: var(--gold-soft) !important;
    border: 1px solid var(--border-hover) !important;
    border-radius: var(--r) !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: rgba(42,95,165,0.1) !important;
    border-color: var(--gold) !important;
    color: var(--gold-pale) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: scale(0.98) !important; }

.stDownloadButton > button {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    border-color: var(--border-hover) !important;
    color: var(--cream) !important;
}

/* ━━━ FORM SUBMIT ━━━ */
.stForm button[type="submit"] {
    background: var(--gold) !important;
    color: var(--ink) !important;
    border: none !important;
    border-radius: var(--r) !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2.5rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
}
.stForm button[type="submit"]:hover {
    background: var(--gold-soft) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(42,95,165,0.35) !important;
}

/* ━━━ INPUTS ━━━ */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    background: var(--ink-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--cream) !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 300 !important;
    padding: 0.6rem 0.9rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stDateInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(42,95,165,0.1) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder { color: var(--ink-5) !important; }

.stSelectbox > div > div {
    background: var(--ink-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--cream) !important;
    transition: border-color 0.2s ease !important;
}
.stSelectbox > div > div:hover { border-color: var(--border-hover) !important; }

/* ━━━ LABELS ━━━ */
.stTextInput label, .stNumberInput label, .stSelectbox label,
.stTextArea label, .stDateInput label, .stRadio label,
.stCheckbox label {
    color: var(--dim) !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    font-family: 'Jost', sans-serif !important;
}

/* ━━━ DATAFRAME ━━━ */
.stDataFrame {
    border-radius: var(--r-lg) !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background: var(--ink-3) !important;
    color: var(--dim) !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-weight: 600 !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stDataFrame"] td {
    background: var(--ink-2) !important;
    color: var(--cream) !important;
    font-size: 0.85rem !important;
    font-weight: 300 !important;
    border-bottom: 1px solid rgba(42,95,165,0.06) !important;
    padding: 0.7rem 1rem !important;
}
[data-testid="stDataFrame"] tr:hover td {
    background: var(--ink-3) !important;
}

/* ━━━ TABS ━━━ */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    border-radius: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 0 !important;
    color: var(--dim) !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.25rem !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
    margin-bottom: -1px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--cream) !important;
    border-bottom-color: var(--gold) !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--cream) !important; }

/* ━━━ EXPANDERS ━━━ */
.streamlit-expanderHeader {
    background: var(--ink-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--muted) !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.8rem 1rem !important;
    transition: all 0.2s;
}
.streamlit-expanderHeader:hover {
    border-color: var(--border-hover) !important;
    color: var(--cream) !important;
}
.streamlit-expanderContent {
    background: var(--ink-2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r) var(--r) !important;
    padding: 1rem !important;
}

/* ━━━ ALERTS ━━━ */
.stSuccess {
    background: rgba(61,122,92,0.12) !important;
    border: 1px solid rgba(61,122,92,0.3) !important;
    border-radius: var(--r) !important;
    color: #7ABFA0 !important;
}
.stInfo {
    background: rgba(74,127,160,0.1) !important;
    border: 1px solid rgba(74,127,160,0.25) !important;
    border-radius: var(--r) !important;
}
.stWarning {
    background: rgba(42,95,165,0.1) !important;
    border: 1px solid rgba(42,95,165,0.28) !important;
    border-radius: var(--r) !important;
}
.stError {
    background: rgba(176,80,80,0.1) !important;
    border: 1px solid rgba(176,80,80,0.28) !important;
    border-radius: var(--r) !important;
}

/* ━━━ RADIO (inline) ━━━ */
.stRadio > div {
    gap: 0.5rem !important;
    flex-direction: row !important;
}
.stRadio > div > label {
    background: var(--ink-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    padding: 0.5rem 1.1rem !important;
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s !important;
    cursor: pointer;
}
.stRadio > div > label:hover {
    border-color: var(--border-hover) !important;
    color: var(--cream) !important;
}

/* ━━━ CHECKBOX ━━━ */
.stCheckbox > label { color: var(--muted) !important; font-size: 0.85rem !important; }

/* ━━━ LOGIN ━━━ */
.login-outer {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4rem 1rem;
}
.login-card {
    background: var(--ink-2);
    border: 1px solid var(--border);
    border-radius: var(--r-xl);
    padding: 3.5rem 3rem;
    max-width: 400px;
    width: 100%;
    position: relative;
    overflow: hidden;
}
.login-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.login-name {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 400;
    font-style: italic;
    color: var(--cream);
    text-align: center;
    line-height: 1;
    margin-bottom: 0.3rem;
    letter-spacing: 0.02em;
}
.login-sub {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.32em;
    color: var(--dim);
    text-align: center;
    margin-bottom: 2.8rem;
}
.login-dot {
    color: var(--gold);
    font-size: 0.5rem;
    vertical-align: middle;
    margin: 0 0.5rem;
}

/* ━━━ SECTION HEADERS ━━━ */
.sec-head {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 500;
    font-style: italic;
    color: var(--cream);
    margin: 1.8rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
    letter-spacing: 0.01em;
}

/* ━━━ CUSTOM BADGES ━━━ */
.badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.22rem 0.65rem;
    border-radius: 4px;
}
.badge-gold    { background: rgba(42,95,165,0.15); color: var(--gold-soft); }
.badge-green   { background: rgba(61,122,92,0.15);  color: #7ABFA0; }
.badge-red     { background: rgba(176,80,80,0.15);  color: #D88080; }
.badge-muted   { background: var(--ink-4); color: var(--muted); }

/* ━━━ EMPTY STATE ━━━ */
.empty {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--dim);
}
.empty-glyph {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: var(--ink-5);
}

/* ━━━ NUMBER INPUT SPINNER ━━━ */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: var(--ink-4) !important;
    border-color: var(--border) !important;
    color: var(--muted) !important;
}

/* ━━━ PLOTLY TOOLTIPS OVERRIDE ━━━ */
.js-plotly-plot .plotly .hoverlayer { pointer-events: none; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# PLOTLY TEMPLATE
# =====================================================

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Jost", color="#5C5248", size=11),
    title=dict(font=dict(family="Playfair Display", size=17, color="#E8E0D0"), pad=dict(b=12), x=0),
    xaxis=dict(
        gridcolor="rgba(42,95,165,0.06)",
        linecolor="rgba(42,95,165,0.12)",
        tickfont=dict(size=10, color="#5C5248"),
        showgrid=True,
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor="rgba(42,95,165,0.06)",
        linecolor="rgba(42,95,165,0.12)",
        tickfont=dict(size=10, color="#5C5248"),
        showgrid=True,
        zeroline=False,
    ),
    legend=dict(
        bgcolor="rgba(26,23,20,0.85)",
        bordercolor="rgba(42,95,165,0.18)",
        borderwidth=1,
        font=dict(color="#8C8070", size=10),
    ),
    margin=dict(l=12, r=12, t=44, b=12),
    colorway=["#2A5FA5","#4A80C8","#7ABFA0","#8BACC8","#C87878","#1A3D70","#3D7A5C","#4A7FA0"],
    hoverlabel=dict(
        bgcolor="rgba(26,23,20,0.96)",
        bordercolor="rgba(42,95,165,0.25)",
        font=dict(color="#F5F0E8", size=11, family="Jost"),
        align="left",
    ),
    bargap=0.35,
)

def styled_fig(fig, height=340):
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
            st.error("⚠️ MONGO_URI not configured.")
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

    for c in ["buying_price", "selling_price", "amount_paid", "pending_amount"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    for c in ["payment_received", "delay_status"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    df["profit"] = df["selling_price"] - df["buying_price"]
    df["margin"] = (
        df["profit"] / df["selling_price"].replace(0, 1) * 100
    ).round(2)

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
            ml = max(ex.iloc[:, i-1].astype(str).map(len).max(), len(col)) + 4
            ws.column_dimensions[ws.cell(1, i).column_letter].width = min(ml, 45)

        from openpyxl.styles import Font, PatternFill, Alignment
        gold_fill = PatternFill("solid", fgColor="2A5FA5")
        for cell in ws[1]:
            cell.font = Font(bold=True, color="F0F4FA")
            cell.fill = gold_fill
            cell.alignment = Alignment(horizontal="center")

    out.seek(0)
    return out


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
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown("""
        <div class='login-outer'>
          <div class='login-card'>
            <div class='login-name'>Vinay</div>
            <div class='login-sub'>◆ Boutique Management ◆</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            u = st.text_input("Username", placeholder="username")
            p = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign in", use_container_width=True)

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
                st.error("Invalid credentials.")

# =====================================================
# SIDEBAR
# =====================================================

def sidebar():
    with st.sidebar:
        st.markdown("""
        <div class='sb-brand'>
            <div class='sb-logo'>Vinay</div>
            <div class='sb-mark'>Boutique Manager</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='sb-sep'></div>", unsafe_allow_html=True)

        df = fetch_all()
        m  = metrics(df)

        c1, c2 = st.columns(2)
        c1.metric("Pending", f"₹{m['pending']:,.0f}")
        c2.metric("Profit",  f"₹{m['profit']:,.0f}")
        c1.metric("Sales",   m["sales"])
        c2.metric("Clients", m["customers"])

        st.markdown("<div class='sb-sep'></div>", unsafe_allow_html=True)

        nav = st.radio("Navigation", [
            "Dashboard",
            "Add Sale",
            "Review Accounts",
            "Update Transaction",
            "Customer List",
            "Analytics",
            "Reminders & Alerts",
            "Inventory Tracker",
            "Logout",
        ], label_visibility="collapsed")

        st.markdown("<div class='sb-sep'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='sb-user'>◆ {st.session_state.get('username','Admin').title()}</div>",
            unsafe_allow_html=True,
        )
    return nav

# =====================================================
# HELPERS
# =====================================================

def page_header(title, sub):
    st.markdown(f"<div class='page-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-sub'>{sub}</div>", unsafe_allow_html=True)

def sec(label):
    st.markdown(f"<div class='sec-head'>{label}</div>", unsafe_allow_html=True)

def rule():
    st.markdown("<hr class='rule'>", unsafe_allow_html=True)

def rule_sm():
    st.markdown("<hr class='rule-sm'>", unsafe_allow_html=True)

# =====================================================
# DASHBOARD
# =====================================================

def page_dashboard():
    page_header("Dashboard", "Business Overview")

    df = fetch_all()
    m  = metrics(df)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Sales",      m["sales"])
    c2.metric("Revenue",    f"₹{m['revenue']:,.0f}")
    c3.metric("Net Profit", f"₹{m['profit']:,.0f}")
    c4.metric("Pending",    f"₹{m['pending']:,.0f}")
    c5.metric("Avg Margin", f"{m['margin']:.1f}%")
    c6.metric("Customers",  m["customers"])

    rule()

    if df.empty:
        st.markdown("""
        <div class='empty'>
            <div class='empty-glyph'>◆</div>
            <div>No sales yet. Start adding transactions to see your dashboard.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    df["month"] = df["sale_date"].dt.to_period("M").astype(str)

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
            marker_color="rgba(42,95,165,0.4)",
            marker_line_color="#2A5FA5",
            marker_line_width=1,
        ))
        fig.add_trace(go.Scatter(
            x=monthly["month"], y=monthly["profit"],
            name="Profit",
            mode="lines+markers",
            line=dict(color="#7ABFA0", width=2),
            marker=dict(size=5, color="#7ABFA0"),
        ))
        styled_fig(fig, 300).update_layout(
            title="Monthly Revenue & Profit",
            barmode="overlay",
            legend=dict(orientation="h", y=1.18, x=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        paid    = (df["payment_received"] == 1).sum()
        pending = (df["payment_received"] == 0).sum()

        fig2 = go.Figure(go.Pie(
            labels=["Collected", "Pending"],
            values=[paid, pending],
            hole=0.72,
            marker=dict(colors=["#2A5FA5", "#1A2540"]),
            textfont=dict(size=11),
            hovertemplate="%{label}: %{value}<extra></extra>",
        ))
        fig2.add_annotation(
            text=f"<b>{paid + pending}</b>",
            x=0.5, y=0.52, showarrow=False,
            font=dict(color="#F5F0E8", family="Playfair Display", size=28),
        )
        fig2.add_annotation(
            text="sales",
            x=0.5, y=0.38, showarrow=False,
            font=dict(color="#5C5248", family="Jost", size=11),
        )
        styled_fig(fig2, 300).update_layout(
            title="Payment Status",
            showlegend=True,
            legend=dict(orientation="h", y=-0.05, x=0.25),
        )
        st.plotly_chart(fig2, use_container_width=True)

    cl2, cr2 = st.columns(2)
    with cl2:
        cat_rev = df.groupby("product_category")["selling_price"].sum().reset_index()
        fig3 = px.pie(
            cat_rev, values="selling_price", names="product_category",
            title="Revenue by Category", hole=0.55,
            color_discrete_sequence=["#2A5FA5","#4A80C8","#7ABFA0","#8BACC8",
                                      "#C87878","#1A3D70","#3D7A5C","#4A7FA0","#9B8070","#A8C4E8"],
        )
        styled_fig(fig3, 270)
        st.plotly_chart(fig3, use_container_width=True)

    with cr2:
        daily = df.set_index("sale_date")["selling_price"].resample("D").sum().reset_index()
        daily.columns = ["date", "revenue"]
        daily["rolling"] = daily["revenue"].rolling(7, min_periods=1).mean()

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=daily["date"], y=daily["revenue"],
            name="Daily", marker_color="rgba(42,95,165,0.25)",
            marker_line_width=0,
        ))
        fig4.add_trace(go.Scatter(
            x=daily["date"], y=daily["rolling"],
            name="7-day avg", line=dict(color="#2A5FA5", width=1.8),
        ))
        styled_fig(fig4, 270).update_layout(
            title="Daily Revenue",
            legend=dict(orientation="h", y=1.18, x=0),
        )
        st.plotly_chart(fig4, use_container_width=True)

    sec("Recent Transactions")
    recent = df.sort_values("sale_date", ascending=False).head(10).copy()
    recent["sale_date"] = recent["sale_date"].dt.strftime("%d %b %Y")
    recent["Status"]    = recent["payment_received"].map({1: "Paid", 0: "Pending"})
    recent["Delayed"]   = recent["delay_status"].map({0: "—", 1: "Yes"})

    show = recent[[
        "id","customer_name","sale_date","product_category",
        "selling_price","profit","pending_amount","Status","Delayed",
    ]].copy()
    show.columns = ["ID","Customer","Date","Category","Amount ₹","Profit ₹","Pending ₹","Status","Delayed"]
    st.dataframe(show, use_container_width=True, hide_index=True)

    rule()
    da, db, _ = st.columns([1, 1, 2])
    with da:
        st.download_button(
            "Export CSV",
            data=df.assign(sale_date=df["sale_date"].astype(str)).to_csv(index=False),
            file_name=f"boutique_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with db:
        st.download_button(
            "Export Excel",
            data=to_excel(df),
            file_name=f"boutique_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

# =====================================================
# ADD SALE
# =====================================================

def page_add_sale():
    page_header("New Sale", "Record a Transaction")

    ctype = st.radio("", ["New Customer", "Existing Customer"], horizontal=True)
    rule_sm()

    cname, cphone = "", ""

    if ctype == "Existing Customer":
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
            st.warning("No existing customers found.")
            ctype = "New Customer"

    with st.form("sale_form", clear_on_submit=True):
        sec("Customer")
        c1, c2, c3 = st.columns(3)
        with c1:
            cname  = st.text_input("Customer Name *", value=cname,
                                   disabled=(ctype == "Existing Customer"))
        with c2:
            cphone = st.text_input("Phone", value=cphone, placeholder="+91 XXXXXXXXXX",
                                   disabled=(ctype == "Existing Customer"))
        with c3:
            sdate  = st.date_input("Sale Date", date.today())

        sec("Product")
        p1, p2, p3 = st.columns(3)
        with p1: cat  = st.selectbox("Category *", CATEGORIES)
        with p2: vend = st.text_input("Vendor / Supplier")
        with p3: qty  = st.number_input("Quantity", min_value=1, step=1, value=1)
        desc = st.text_area("Description", placeholder="Fabric, colour, design details…", height=70)

        sec("Pricing & Payment")
        pr1, pr2, pr3, pr4 = st.columns(4)
        with pr1: buy      = st.number_input("Buying Price (₹) *",  min_value=0.0, step=100.0, format="%.2f")
        with pr2: sell     = st.number_input("Selling Price (₹) *", min_value=0.0, step=100.0, format="%.2f")
        with pr3: paid_amt = st.number_input("Amount Paid (₹)",     min_value=0.0, step=100.0, format="%.2f")
        with pr4: pm       = st.selectbox("Payment Method", PAYMENT_METHODS)

        pending_amt = max(round(sell - paid_amt, 2), 0.0)
        profit_amt  = round((sell - buy) * qty, 2)
        margin_pct  = round(profit_amt / (sell * qty) * 100, 2) if sell > 0 else 0.0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Pending",        f"₹{pending_amt:,.2f}")
        m2.metric("Profit (Total)", f"₹{profit_amt:,.2f}")
        m3.metric("Margin",         f"{margin_pct:.1f}%")
        m4.metric("Total Value",    f"₹{sell * qty:,.2f}")

        notes = st.text_area("Notes", placeholder="Special instructions…", height=60)

        submitted = st.form_submit_button("Save Sale", use_container_width=True)

        if submitted:
            errs = []
            if not cname.strip():   errs.append("Customer name is required.")
            if buy  <= 0:           errs.append("Buying price must be > 0.")
            if sell <= 0:           errs.append("Selling price must be > 0.")
            if paid_amt > sell:     errs.append("Amount paid cannot exceed selling price.")
            if sell < buy:
                st.warning("Selling price is below buying price — this sale will be a loss.")

            if errs:
                for e in errs: st.error(e)
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
                st.success(f"Sale recorded for {cname.strip()}.")
                st.balloons()
                st.rerun()

# =====================================================
# REVIEW ACCOUNTS
# =====================================================

def page_review():
    page_header("Accounts", "All Transactions")

    df = fetch_all()
    if df.empty:
        st.markdown("<div class='empty'><div class='empty-glyph'>◆</div><div>No transactions yet.</div></div>",
                    unsafe_allow_html=True)
        return

    with st.expander("Filter & Sort", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1: srch  = st.text_input("Customer / Phone")
        with c2: catf  = st.selectbox("Category",   ["All"] + CATEGORIES)
        with c3: payf  = st.selectbox("Payment",    ["All", "Paid", "Pending"])
        with c4: dlayf = st.selectbox("Delay Flag", ["All", "On Time", "Delayed"])

        c5, c6, c7 = st.columns(3)
        with c5: sortby = st.selectbox("Sort By", ["Date ↓","Date ↑","Amount ↓","Pending ↓","Profit ↓"])
        with c6: d_from = st.date_input("From", value=date.today() - timedelta(days=90))
        with c7: d_to   = st.date_input("To",   value=date.today())

    fdf = df.copy()

    if srch:
        mask = (
            fdf["customer_name"].str.contains(srch, case=False, na=False) |
            fdf["customer_phone"].astype(str).str.contains(srch, na=False)
        )
        fdf = fdf[mask]

    if catf  != "All": fdf = fdf[fdf["product_category"] == catf]
    if payf  == "Paid":    fdf = fdf[fdf["payment_received"] == 1]
    elif payf == "Pending": fdf = fdf[fdf["payment_received"] == 0]
    if dlayf == "On Time":  fdf = fdf[fdf["delay_status"] == 0]
    elif dlayf == "Delayed": fdf = fdf[fdf["delay_status"] == 1]

    fdf = fdf[
        (fdf["sale_date"] >= pd.Timestamp(d_from)) &
        (fdf["sale_date"] <= pd.Timestamp(d_to))
    ]

    sm = {
        "Date ↓":    ("sale_date",      False),
        "Date ↑":    ("sale_date",      True),
        "Amount ↓":  ("selling_price",  False),
        "Pending ↓": ("pending_amount", False),
        "Profit ↓":  ("profit",         False),
    }
    sc, sa = sm[sortby]
    fdf = fdf.sort_values(sc, ascending=sa)

    rule_sm()
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Transactions", len(fdf))
    m2.metric("Revenue",      f"₹{fdf['selling_price'].sum():,.0f}")
    m3.metric("Profit",       f"₹{fdf['profit'].sum():,.0f}")
    m4.metric("Pending",      f"₹{fdf['pending_amount'].sum():,.0f}")
    m5.metric("Avg Margin",   f"{fdf['margin'].mean():.1f}%" if not fdf.empty else "—")
    rule_sm()

    show = fdf[[
        "id","customer_name","customer_phone","sale_date","product_category",
        "buying_price","selling_price","profit","amount_paid","pending_amount",
        "payment_method","delay_status","payment_received",
    ]].copy()
    show["sale_date"]        = show["sale_date"].dt.strftime("%d %b %Y")
    show["delay_status"]     = show["delay_status"].map({0: "—", 1: "Yes"})
    show["payment_received"] = show["payment_received"].map({0: "Pending", 1: "Paid"})
    show.columns = ["ID","Customer","Phone","Date","Category","Buy ₹","Sell ₹",
                    "Profit ₹","Paid ₹","Pending ₹","Method","Delayed","Status"]
    st.dataframe(show, use_container_width=True, hide_index=True)

    dc, de, _ = st.columns([1, 1, 2])
    with dc:
        st.download_button("Export CSV",
            data=fdf.assign(sale_date=fdf["sale_date"].astype(str)).to_csv(index=False),
            file_name=f"accounts_{date.today()}.csv", mime="text/csv",
            use_container_width=True)
    with de:
        st.download_button("Export Excel", data=to_excel(fdf),
            file_name=f"accounts_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True)

    sec("Mark Payments")
    pend = fdf[fdf["pending_amount"] > 0].sort_values("pending_amount", ascending=False)

    if pend.empty:
        st.success("All payments received for current filter.")
    else:
        st.markdown(
            f"<span class='badge badge-gold'>{len(pend)} pending — ₹{pend['pending_amount'].sum():,.0f}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        for _, row in pend.iterrows():
            ca, cb, cc, cd, ce = st.columns([3, 2, 1.5, 1, 1])
            ca.write(f"**{row['customer_name']}** · {row['product_category']}")
            cb.write(f"₹{row['pending_amount']:,.2f} pending")
            cc.write(row["sale_date"].strftime("%d %b %Y") if pd.notna(row["sale_date"]) else "—")
            with cd:
                if st.button("Mark Paid", key=f"p_{row['id']}_{row['customer_name']}"):
                    get_col().update_one(
                        {"id": row["id"]},
                        {"$set": {"payment_received": 1, "amount_paid": float(row["selling_price"]), "pending_amount": 0.0}},
                    )
                    invalidate_cache(); st.rerun()
            with ce:
                if st.button("Flag", key=f"f_{row['id']}_{row['customer_name']}"):
                    get_col().update_one({"id": row["id"]}, {"$set": {"delay_status": 1}})
                    invalidate_cache(); st.rerun()

# =====================================================
# UPDATE TRANSACTION
# =====================================================

def page_update():
    page_header("Update", "Edit or Delete a Record")

    c1, c2 = st.columns([2, 1])
    with c1: sname = st.text_input("Search by Customer Name")
    with c2: sid   = st.number_input("Or by Sale ID", min_value=0, step=1)

    if not sname and sid == 0:
        st.info("Enter a customer name or sale ID to search.")
        return

    q = ({"customer_name": {"$regex": sname, "$options": "i"}} if sname else {"id": int(sid)})
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
        preview["payment_received"] = preview["payment_received"].map({0: "Pending", 1: "Paid"})
    st.dataframe(preview, use_container_width=True, hide_index=True)

    sel = st.selectbox("Select ID to Edit", df["id"].tolist(),
        format_func=lambda x: f"#{x} — {df[df['id']==x]['customer_name'].values[0]}")
    row = df[df["id"] == sel].iloc[0]
    rule_sm()

    with st.form("update_form"):
        sec("Customer & Product")
        c1, c2, c3 = st.columns(3)
        with c1:
            nn  = st.text_input("Customer Name", value=str(row.get("customer_name", "")))
            np  = st.text_input("Phone",          value=str(row.get("customer_phone", "")))
        with c2:
            ci  = CATEGORIES.index(row["product_category"]) if row.get("product_category") in CATEGORIES else 0
            nc  = st.selectbox("Category", CATEGORIES, index=ci)
            nv  = st.text_input("Vendor", value=str(row.get("vendor", "")))
        with c3:
            try:    existing_date = pd.to_datetime(row.get("sale_date")).date()
            except: existing_date = date.today()
            new_date = st.date_input("Sale Date", value=existing_date)
            nqty = st.number_input("Quantity", min_value=1, step=1, value=int(row.get("quantity", 1)))

        ndesc = st.text_area("Description", value=str(row.get("product_description", "")), height=60)

        sec("Pricing & Payment")
        pr1, pr2, pr3, pr4 = st.columns(4)
        with pr1: nb  = st.number_input("Buying Price (₹)",  value=float(row["buying_price"]),  min_value=0.0, step=100.0, format="%.2f")
        with pr2: ns  = st.number_input("Selling Price (₹)", value=float(row["selling_price"]), min_value=0.0, step=100.0, format="%.2f")
        with pr3: npa = st.number_input("Amount Paid (₹)",   value=float(row["amount_paid"]),   min_value=0.0, step=100.0, format="%.2f")
        with pr4:
            pi  = PAYMENT_METHODS.index(row["payment_method"]) if row.get("payment_method") in PAYMENT_METHODS else 0
            npm = st.selectbox("Payment Method", PAYMENT_METHODS, index=pi)

        nd     = st.checkbox("Mark as Delayed", value=bool(row.get("delay_status", 0)))
        nnotes = st.text_area("Notes", value=str(row.get("notes", "")), height=60)

        npend   = max(round(ns - npa, 2), 0.0)
        nprofit = round(ns - nb, 2)

        m1, m2, m3 = st.columns(3)
        m1.metric("Updated Pending", f"₹{npend:,.2f}")
        m2.metric("Updated Profit",  f"₹{nprofit:,.2f}")
        m3.metric("Updated Margin",  f"{(nprofit / ns * 100 if ns > 0 else 0):.1f}%")

        bu, bd = st.columns(2)
        with bu: upd = st.form_submit_button("Save Changes",       use_container_width=True)
        with bd: dlt = st.form_submit_button("Delete Transaction",  use_container_width=True)

        if upd:
            if npa > ns:
                st.error("Amount paid cannot exceed selling price.")
            else:
                get_col().update_one({"id": sel}, {"$set": {
                    "customer_name": nn.strip(), "customer_phone": np.strip(),
                    "sale_date": str(new_date), "product_category": nc,
                    "vendor": nv.strip(), "product_description": ndesc.strip(),
                    "quantity": nqty, "buying_price": round(nb, 2),
                    "selling_price": round(ns, 2), "amount_paid": round(npa, 2),
                    "pending_amount": npend, "delay_status": int(nd),
                    "payment_method": npm, "notes": nnotes.strip(),
                    "payment_received": 1 if npend == 0 else 0,
                    "updated_at": str(datetime.now()),
                }})
                invalidate_cache()
                st.success("Transaction updated.")
                st.rerun()

        if dlt:
            get_col().delete_one({"id": sel})
            invalidate_cache()
            st.success("Transaction deleted.")
            st.rerun()

# =====================================================
# CUSTOMER LIST
# =====================================================

def page_customers():
    page_header("Customers", "All Clients")

    df = fetch_all()
    if df.empty:
        st.markdown("<div class='empty'><div class='empty-glyph'>◆</div><div>No customers yet.</div></div>",
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
    summ["tier"] = pd.cut(
        summ["spent"],
        bins=[0, 5000, 20000, 50000, float("inf")],
        labels=["Bronze", "Silver", "Gold", "Platinum"],
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Customers",  len(summ))
    m2.metric("Avg Spend",        f"₹{summ['spent'].mean():,.0f}")
    m3.metric("With Pending",     len(summ[summ["pending"] > 0]))
    m4.metric("Total Revenue",    f"₹{summ['spent'].sum():,.0f}")

    rule_sm()
    c1, c2 = st.columns([2, 1])
    with c1: srch   = st.text_input("Search Customer")
    with c2: tier_f = st.selectbox("Tier", ["All","Bronze","Silver","Gold","Platinum"])

    view = summ.copy()
    if srch:   view = view[view["customer_name"].str.contains(srch, case=False, na=False)]
    if tier_f != "All": view = view[view["tier"] == tier_f]

    disp = view.rename(columns={
        "customer_name":"Customer","phone":"Phone","transactions":"Visits",
        "spent":"Total Spent ₹","pending":"Pending ₹","last_visit":"Last Visit",
        "profit":"Profit ₹","tier":"Tier",
    })
    st.dataframe(
        disp.style.format({"Total Spent ₹": "₹{:,.0f}", "Pending ₹": "₹{:,.0f}", "Profit ₹": "₹{:,.0f}"}),
        use_container_width=True, hide_index=True,
    )

    dc, de = st.columns(2)
    with dc:
        st.download_button("Export CSV", data=disp.to_csv(index=False),
                           file_name=f"customers_{date.today()}.csv", mime="text/csv",
                           use_container_width=True)
    with de:
        out = BytesIO()
        with pd.ExcelWriter(out, engine="openpyxl") as w: disp.to_excel(w, index=False)
        out.seek(0)
        st.download_button("Export Excel", data=out,
                           file_name=f"customers_{date.today()}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    sec("Purchase History")
    chosen = st.selectbox("Select Customer", summ["customer_name"].tolist())

    if chosen:
        hist = df[df["customer_name"] == chosen].sort_values("sale_date", ascending=False).copy()
        hist["status"] = hist["payment_received"].map({0: "Pending", 1: "Paid"})
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

        if len(hist) > 1:
            hist_sorted = df[df["customer_name"] == chosen].sort_values("sale_date").copy()
            hist_sorted["cumulative"] = hist_sorted["selling_price"].cumsum()
            fig = px.line(hist_sorted, x="sale_date", y="cumulative",
                          title=f"Cumulative Spend — {chosen}", markers=True)
            fig.update_traces(line_color="#2A5FA5", marker_color="#4A80C8", marker_size=5)
            styled_fig(fig, 230)
            st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ANALYTICS
# =====================================================

def page_analytics():
    page_header("Analytics", "Business Intelligence")

    df = fetch_all()
    if df.empty:
        st.info("No data available.")
        return

    df["month"] = df["sale_date"].dt.to_period("M").astype(str)
    df["dow"]   = df["sale_date"].dt.day_name()

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Revenue",       f"₹{df['selling_price'].sum():,.0f}")
    k2.metric("Profit",        f"₹{df['profit'].sum():,.0f}")
    k3.metric("Avg Order",     f"₹{df['selling_price'].mean():,.0f}")
    k4.metric("Avg Margin",    f"{df['margin'].mean():.1f}%")
    k5.metric("Delayed Count", int((df["delay_status"] == 1).sum()))

    rule()

    t1, t2, t3, t4, t5 = st.tabs(["Trends","Customers","Categories","Payments","Top Items"])

    with t1:
        c1, c2 = st.columns(2)
        with c1:
            monthly = df.groupby("month").agg(revenue=("selling_price","sum"), profit=("profit","sum")).reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=monthly["month"], y=monthly["revenue"], name="Revenue",
                                 marker_color="rgba(42,95,165,0.4)", marker_line_color="#2A5FA5", marker_line_width=1))
            fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["profit"], name="Profit",
                                     mode="lines+markers", line=dict(color="#7ABFA0", width=2), marker=dict(size=5)))
            styled_fig(fig).update_layout(title="Revenue & Profit by Month", barmode="overlay",
                                          legend=dict(orientation="h", y=1.18, x=0))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            daily = df.set_index("sale_date")["selling_price"].resample("D").sum().reset_index()
            daily.columns = ["date", "revenue"]
            fig2 = px.area(daily, x="date", y="revenue", title="Daily Revenue")
            fig2.update_traces(fillcolor="rgba(42,95,165,0.1)", line_color="#2A5FA5", line_width=1.5)
            styled_fig(fig2)
            st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            dow = df.groupby("dow").agg(sales=("id","count"), revenue=("selling_price","sum")).reset_index()
            dow["dow"] = pd.Categorical(dow["dow"], categories=dow_order, ordered=True)
            dow = dow.sort_values("dow")
            fig3 = px.bar(dow, x="dow", y="sales", title="Sales by Day of Week",
                          color="revenue", color_continuous_scale=[[0,"#1A1714"],[1,"#2A5FA5"]])
            styled_fig(fig3); st.plotly_chart(fig3, use_container_width=True)

        with c4:
            monthly["MoM Growth %"] = monthly["revenue"].pct_change() * 100
            fig4 = px.bar(monthly.dropna(), x="month", y="MoM Growth %",
                          title="Month-over-Month Growth",
                          color="MoM Growth %",
                          color_continuous_scale=[[0,"#B05050"],[0.5,"#2E2A24"],[1,"#7ABFA0"]])
            styled_fig(fig4); st.plotly_chart(fig4, use_container_width=True)

    with t2:
        c1, c2 = st.columns(2)
        with c1:
            top_c = df.groupby("customer_name")["selling_price"].sum().nlargest(10).reset_index()
            fig5  = px.bar(top_c, x="selling_price", y="customer_name", orientation="h",
                           title="Top 10 Customers by Revenue",
                           color="selling_price", color_continuous_scale=[[0,"#1A1714"],[1,"#2A5FA5"]])
            styled_fig(fig5); fig5.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig5, use_container_width=True)

        with c2:
            cp = df.groupby("customer_name")["pending_amount"].sum()
            cp = cp[cp > 0].nlargest(10).reset_index()
            if not cp.empty:
                fig6 = px.bar(cp, x="pending_amount", y="customer_name", orientation="h",
                              title="Top Customers by Pending",
                              color="pending_amount", color_continuous_scale=[[0,"#1A1714"],[1,"#C87878"]])
                styled_fig(fig6); fig6.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.success("No pending amounts.")

        cust_stats = df.groupby("customer_name").agg(
            visits=("id","count"), revenue=("selling_price","sum"), avg_order=("selling_price","mean"),
        ).reset_index()
        fig_scatter = px.scatter(cust_stats, x="visits", y="revenue", size="avg_order",
            hover_name="customer_name", title="Customer Value Matrix (size = avg order)",
            color="revenue", color_continuous_scale=[[0,"#1A1714"],[1,"#2A5FA5"]])
        styled_fig(fig_scatter, 330); st.plotly_chart(fig_scatter, use_container_width=True)

        seg = df.groupby("customer_name").agg(spend=("selling_price","sum")).reset_index()
        seg["tier"] = pd.cut(seg["spend"], bins=[0,5000,20000,50000,float("inf")],
                             labels=["Bronze","Silver","Gold","Platinum"])
        sec("Customer Tier Distribution")
        sg = (seg.groupby("tier", observed=True).agg(customers=("customer_name","count"), total=("spend","sum")).reset_index())
        sg.columns = ["Tier","Customers","Total Spend ₹"]
        st.dataframe(sg, use_container_width=True, hide_index=True)

    with t3:
        c1, c2 = st.columns(2)
        with c1:
            cd = df.groupby("product_category").size().reset_index(name="count")
            fig7 = px.pie(cd, values="count", names="product_category",
                          title="Sales Volume by Category", hole=0.55,
                          color_discrete_sequence=["#2A5FA5","#4A80C8","#7ABFA0","#8BACC8",
                                                    "#C87878","#1A3D70","#3D7A5C","#4A7FA0","#9B8070","#A8C4E8"])
            styled_fig(fig7); st.plotly_chart(fig7, use_container_width=True)

        with c2:
            cp2 = df.groupby("product_category").agg(profit=("profit","sum"), revenue=("selling_price","sum")).reset_index()
            cp2["margin"] = (cp2["profit"] / cp2["revenue"] * 100).round(1)
            fig8 = px.bar(cp2, x="product_category", y="profit", title="Profit by Category",
                          color="margin", color_continuous_scale=[[0,"#1A1714"],[1,"#7ABFA0"]])
            styled_fig(fig8); st.plotly_chart(fig8, use_container_width=True)

        cm = df.groupby(["month","product_category"])["selling_price"].sum().unstack(fill_value=0)
        if not cm.empty:
            fig9 = px.imshow(cm.T, title="Category × Month Heatmap",
                             color_continuous_scale=[[0,"#1A1714"],[0.4,"#6B5A2E"],[1,"#2A5FA5"]], aspect="auto")
            styled_fig(fig9, 300); st.plotly_chart(fig9, use_container_width=True)

    with t4:
        c1, c2 = st.columns(2)
        with c1:
            pm = df.groupby("payment_method").size().reset_index(name="count")
            fig10 = px.pie(pm, values="count", names="payment_method",
                           title="Payment Method Distribution", hole=0.58,
                           color_discrete_sequence=["#2A5FA5","#4A80C8","#7ABFA0","#8BACC8","#1A3D70","#C87878"])
            styled_fig(fig10); st.plotly_chart(fig10, use_container_width=True)

        with c2:
            ps = df.groupby("payment_received").agg(count=("id","count"), total=("pending_amount","sum")).reset_index()
            ps["label"] = ps["payment_received"].map({0: "Pending", 1: "Received"})
            fig11 = px.bar(ps, x="label", y="count", title="Payment Status",
                           color="label", color_discrete_map={"Pending":"#2A5FA5","Received":"#7ABFA0"})
            styled_fig(fig11); st.plotly_chart(fig11, use_container_width=True)

        aged = df[df["pending_amount"] > 0].copy()
        if not aged.empty:
            today_ts = pd.Timestamp(date.today())
            aged["days"] = (today_ts - aged["sale_date"]).dt.days
            aged["bucket"] = pd.cut(aged["days"], bins=[0,7,15,30,60,9999],
                                    labels=["0–7d","8–15d","16–30d","31–60d","60d+"])
            ag = aged.groupby("bucket", observed=True)["pending_amount"].sum().reset_index()
            fig12 = px.bar(ag, x="bucket", y="pending_amount", title="Pending — Aging Buckets",
                           color="pending_amount", color_continuous_scale=[[0,"#2A5FA5"],[1,"#B05050"]])
            styled_fig(fig12); st.plotly_chart(fig12, use_container_width=True)
        else:
            st.success("No pending payments.")

    with t5:
        c1, c2 = st.columns(2)
        with c1:
            if "vendor" in df.columns:
                vd = (df[df["vendor"].astype(str).str.strip() != ""]
                      .groupby("vendor").agg(revenue=("selling_price","sum"), items=("id","count"))
                      .nlargest(10, "revenue").reset_index())
                if not vd.empty:
                    fig13 = px.bar(vd, x="revenue", y="vendor", orientation="h", title="Top Vendors by Revenue",
                                   color="revenue", color_continuous_scale=[[0,"#1A1714"],[1,"#2A5FA5"]])
                    styled_fig(fig13); fig13.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig13, use_container_width=True)
                else:
                    st.info("Add vendor names to see this chart.")

        with c2:
            if "product_description" in df.columns:
                pd2 = df[df["product_description"].astype(str).str.strip() != ""].copy()
                if not pd2.empty:
                    tm = (pd2.groupby("product_description")
                          .agg(margin=("margin","mean"), revenue=("selling_price","sum"))
                          .nlargest(10, "margin").reset_index())
                    tm["product_description"] = tm["product_description"].str[:30]
                    fig14 = px.bar(tm, x="margin", y="product_description", orientation="h",
                                   title="Top Products by Margin %",
                                   color="margin", color_continuous_scale=[[0,"#1A1714"],[1,"#7ABFA0"]])
                    styled_fig(fig14); fig14.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig14, use_container_width=True)
                else:
                    st.info("Add product descriptions to see this chart.")

# =====================================================
# REMINDERS & ALERTS
# =====================================================

def page_reminders():
    page_header("Reminders", "Payment Follow-ups")

    df = fetch_all()
    if df.empty:
        st.info("No data available.")
        return

    today_ts  = pd.Timestamp(date.today())
    df["days_old"] = (today_ts - df["sale_date"]).dt.days

    overdue_count = len(df[(df["pending_amount"] > 0) & (df["days_old"] > 30)])
    flagged_count = int((df["delay_status"] == 1).sum())

    if overdue_count or flagged_count:
        bc = st.columns(2)
        if overdue_count: bc[0].error(f"{overdue_count} payments overdue (30+ days)")
        if flagged_count: bc[1].warning(f"{flagged_count} transactions flagged")
    else:
        st.success("All clear — no overdue or flagged payments.")

    rule_sm()

    t1, t2, t3, t4 = st.tabs(["Overdue (30d+)","Flagged","High Value","Upcoming"])

    with t1:
        ov = df[(df["pending_amount"] > 0) & (df["days_old"] > 30)].sort_values("days_old", ascending=False)
        if ov.empty:
            st.success("No overdue payments.")
        else:
            st.warning(f"{len(ov)} overdue — ₹{ov['pending_amount'].sum():,.0f} total")
            for _, r in ov.iterrows():
                with st.expander(f"{r['customer_name']}  ·  ₹{r['pending_amount']:,.0f}  ·  {int(r['days_old'])} days"):
                    ca, cb, cc, cd = st.columns([2, 2, 1, 1])
                    ca.write(r["sale_date"].strftime("%d %b %Y"))
                    cb.write(r.get("product_category","—"))
                    with cc:
                        if st.button("Mark Paid", key=f"op_{r['id']}"):
                            get_col().update_one({"id": r["id"]},
                                {"$set": {"payment_received": 1, "amount_paid": float(r["selling_price"]), "pending_amount": 0.0}})
                            invalidate_cache(); st.rerun()
                    with cd:
                        if st.button("Remind", key=f"or_{r['id']}"):
                            st.toast(f"Reminder noted for {r['customer_name']}.")

    with t2:
        dl = df[df["delay_status"] == 1].sort_values("pending_amount", ascending=False)
        if dl.empty:
            st.success("No flagged payments.")
        else:
            st.error(f"{len(dl)} flagged — ₹{dl['pending_amount'].sum():,.0f}")
            show = dl[["customer_name","sale_date","product_category","selling_price","pending_amount","days_old"]].copy()
            show["sale_date"] = show["sale_date"].dt.strftime("%d %b %Y")
            show.columns = ["Customer","Date","Category","Amount ₹","Pending ₹","Days Old"]
            st.dataframe(show, use_container_width=True, hide_index=True)
            sc = st.selectbox("Clear flag for:", dl["id"].tolist(),
                              format_func=lambda x: f"#{x} — {dl[dl['id']==x]['customer_name'].values[0]}")
            if st.button("Clear Flag"):
                get_col().update_one({"id": sc}, {"$set": {"delay_status": 0}})
                invalidate_cache(); st.success("Flag cleared."); st.rerun()

    with t3:
        hv = df[df["selling_price"] >= 10000].sort_values("selling_price", ascending=False).head(20).copy()
        if hv.empty:
            st.info("No high-value sales (₹10,000+) yet.")
        else:
            hv["sale_date"]        = hv["sale_date"].dt.strftime("%d %b %Y")
            hv["payment_received"] = hv["payment_received"].map({0: "Pending", 1: "Paid"})
            show = hv[["customer_name","sale_date","product_category","selling_price","profit","payment_received"]].copy()
            show.columns = ["Customer","Date","Category","Amount ₹","Profit ₹","Status"]
            st.dataframe(show, use_container_width=True, hide_index=True)

    with t4:
        soon = df[(df["pending_amount"] > 0) & (df["days_old"] >= 7) &
                  (df["days_old"] <= 30) & (df["delay_status"] == 0)].sort_values("days_old", ascending=False)
        if soon.empty:
            st.info("No follow-ups needed in the 7–30 day window.")
        else:
            st.info(f"{len(soon)} sales with pending payments between 7–30 days old.")
            show = soon[["customer_name","customer_phone","sale_date","product_category","pending_amount","days_old"]].copy()
            show["sale_date"] = show["sale_date"].dt.strftime("%d %b %Y")
            show.columns = ["Customer","Phone","Date","Category","Pending ₹","Days Old"]
            st.dataframe(show, use_container_width=True, hide_index=True)

# =====================================================
# INVENTORY
# =====================================================

def page_inventory():
    page_header("Inventory", "Stock Management")

    inv_col = get_db()["inventory"]
    t1, t2 = st.tabs(["Current Stock", "Add / Update Stock"])

    with t1:
        items = list(inv_col.find({}, {"_id": 0}))
        if not items:
            st.markdown("<div class='empty'><div class='empty-glyph'>◆</div><div>No inventory items yet.</div></div>",
                        unsafe_allow_html=True)
        else:
            inv_df = pd.DataFrame(items)
            m1, m2, m3, m4 = st.columns(4)
            total_value  = (inv_df.get("quantity", pd.Series([0])) * inv_df.get("cost_price", pd.Series([0]))).sum()
            low_stock    = inv_df[inv_df.get("quantity", pd.Series([0])) <= inv_df.get("min_stock", pd.Series([5]))]
            out_of_stock = inv_df[inv_df.get("quantity", pd.Series([0])) == 0]

            m1.metric("Total SKUs",       len(inv_df))
            m2.metric("Inventory Value",  f"₹{total_value:,.0f}")
            m3.metric("Low Stock",        len(low_stock))
            m4.metric("Out of Stock",     len(out_of_stock))

            if not low_stock.empty:
                st.warning(f"{len(low_stock)} item(s) running low.")

            rule_sm()
            cat_f = st.selectbox("Filter by Category", ["All"] + CATEGORIES)
            view  = inv_df.copy()
            if cat_f != "All" and "category" in view.columns:
                view = view[view["category"] == cat_f]

            if "quantity" in view.columns and "min_stock" in view.columns:
                view["Status"] = view.apply(
                    lambda r: "Out of Stock" if r["quantity"] == 0
                    else ("Low Stock" if r["quantity"] <= r["min_stock"] else "OK"), axis=1)

            st.dataframe(view, use_container_width=True, hide_index=True)

            if "category" in inv_df.columns and "quantity" in inv_df.columns:
                cat_stock = inv_df.groupby("category")["quantity"].sum().reset_index()
                fig = px.bar(cat_stock, x="category", y="quantity", title="Stock by Category",
                             color="quantity", color_continuous_scale=[[0,"#B05050"],[0.4,"#2A5FA5"],[1,"#7ABFA0"]])
                styled_fig(fig, 260); st.plotly_chart(fig, use_container_width=True)

    with t2:
        sec("Add or Update Stock Item")
        with st.form("inv_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                item_name  = st.text_input("Item Name *", placeholder="e.g. Banarasi Silk Saree")
                item_sku   = st.text_input("SKU / Code",  placeholder="e.g. SAR-001")
                item_cat   = st.selectbox("Category", CATEGORIES)
                item_vend  = st.text_input("Vendor")
            with c2:
                item_qty   = st.number_input("Quantity *",        min_value=0, step=1)
                item_min   = st.number_input("Min Stock Alert",   min_value=0, step=1, value=5)
                item_cost  = st.number_input("Cost Price (₹) *",  min_value=0.0, step=50.0, format="%.2f")
                item_mrp   = st.number_input("Selling Price (₹)", min_value=0.0, step=50.0, format="%.2f")

            item_notes = st.text_area("Notes", height=55)

            if st.form_submit_button("Save Item", use_container_width=True):
                if not item_name.strip():
                    st.error("Item name is required.")
                else:
                    inv_col.update_one(
                        {"sku": item_sku.strip() or item_name.strip()},
                        {"$set": {
                            "name": item_name.strip(), "sku": item_sku.strip(),
                            "category": item_cat, "vendor": item_vend.strip(),
                            "quantity": item_qty, "min_stock": item_min,
                            "cost_price": round(item_cost, 2), "sell_price": round(item_mrp, 2),
                            "notes": item_notes.strip(), "updated_at": str(datetime.now()),
                        }}, upsert=True,
                    )
                    st.success(f"'{item_name.strip()}' saved to inventory.")
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
