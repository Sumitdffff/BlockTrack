"""
BlockTrack — Blockchain-Based Transaction Tracker
==================================================
Author  : BlockTrack Project
Language: Python 3.8+
Storage : CSV (transactions.csv)
"""

import hashlib
import csv
import os
from datetime import datetime, date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

CSV_FILE = "transactions.csv"

CSV_COLUMNS = [
    "transaction_id", "date", "type", "amount", "category",
    "payment_method", "description", "current_hash", "previous_hash",
]

GENESIS_HASH = "0" * 64
DATE_FORMAT  = "%Y-%m-%d"

INCOME_CATEGORIES  = ["Salary", "Freelance", "Business", "Investment",
                      "Rental", "Gift", "Other Income"]
EXPENSE_CATEGORIES = ["Food", "Travel", "Shopping", "Utilities", "Healthcare",
                      "Education", "Entertainment", "Rent", "Insurance", "Other Expense"]
PAYMENT_METHODS    = ["Cash", "UPI", "Bank Transfer", "Credit Card",
                      "Debit Card", "Cheque", "Other"]

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  (premium dark glassmorphism theme)
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(ellipse at top left, #0d1b2a 0%, #0a0f1e 60%, #080c18 100%);
    color: #e2e8f0;
}

/* ── Widget Labels (Transaction ID, Date, Category, Amount, etc.) ── */
label,
.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSelectbox label,
.stDateInput label,
.stRadio label,
.stCheckbox label,
.stMultiSelect label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stFormLabel"],
[data-testid="stFormLabel"] p,
.stForm label,
div[class*="stTextInput"] label,
div[class*="stSelectbox"] label,
div[class*="stDateInput"] label,
div[class*="stNumberInput"] label,
div[class*="stTextArea"] label {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    letter-spacing: 0.2px !important;
}

/* Help/hint text under inputs */
.stTextInput small, .stSelectbox small,
.stDateInput small, .stNumberInput small,
[data-testid="InputInstructions"],
[data-testid="stWidgetLabel"] + div small {
    color: #64748b !important;
}

/* Selectbox dropdown text */
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] div {
    color: #f1f5f9 !important;
}

/* Tab labels */
[data-testid="stTabs"] button[role="tab"] {
    color: #94a3b8 !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #a78bfa !important;
    border-bottom: 2px solid #7c3aed !important;
    font-weight: 700 !important;
}

/* General paragraph / markdown text inside main area */
.stMarkdown p, .element-container p {
    color: #cbd5e1;
}

/* Number input spin buttons */
.stNumberInput button { color: #94a3b8 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #0a0f1e 100%);
    border-right: 1px solid rgba(99,102,241,0.2);
    box-shadow: 4px 0 24px rgba(0,0,0,0.4);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label { color: #cbd5e1 !important; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: rgba(15,23,42,0.8) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    transition: border-color .2s;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.8) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
}

/* ── Select boxes ── */
.stSelectbox > div > div {
    background: rgba(15,23,42,0.8) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 10px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6d28d9 0%, #4f46e5 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: .4px !important;
    padding: 10px 22px !important;
    transition: all .25s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.5) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Form container ── */
[data-testid="stForm"] {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 28px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ── Headings ── */
h1, h2, h3, h4 { color: #f8fafc !important; letter-spacing: -.3px; }

/* ── Dividers ── */
hr { border-color: rgba(99,102,241,0.2) !important; }

/* ── DataFrames ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden; }
.stDataFrame thead th {
    background: rgba(99,102,241,0.2) !important;
    color: #a5b4fc !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 12px !important; backdrop-filter: blur(6px); }

/* ── Date input ── */
.stDateInput > div > div > input {
    background: rgba(15,23,42,0.8) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 10px !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 14px;
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #7c3aed !important; }

/* ── Radio ── */
[data-testid="stSidebar"] .stRadio > label { color: #94a3b8 !important; }

footer { visibility: hidden; }
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# UI HELPER — CARDS
# ─────────────────────────────────────────────────────────────────────────────

def glow_card(icon, label, value, accent="#7c3aed", sub=None):
    sub_html = f'<p style="color:#64748b;font-size:11px;margin:4px 0 0 0;">{sub}</p>' if sub else ""
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(10,15,30,0.95) 100%);
        border: 1px solid rgba(99,102,241,0.25);
        border-top: 3px solid {accent};
        border-radius: 14px;
        padding: 22px 20px 18px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35), 0 0 20px {accent}18;
        transition: transform .2s;
        backdrop-filter: blur(10px);
    ">
        <div style="font-size:26px; margin-bottom:6px;">{icon}</div>
        <p style="color:#94a3b8; font-size:11px; font-weight:600; text-transform:uppercase;
                  letter-spacing:1.2px; margin:0 0 8px 0;">{label}</p>
        <p style="color:{accent}; font-size:26px; font-weight:800; margin:0; line-height:1.1;">
            {value}</p>
        {sub_html}
    </div>
    """

def section_header(title, subtitle=""):
    sub = f'<p style="color:#64748b;font-size:13px;margin:2px 0 0 0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom:20px;">
        <h3 style="margin:0; background:linear-gradient(90deg,#a78bfa,#60a5fa);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                   font-size:20px; font-weight:700;">{title}</h3>
        {sub}
    </div>
    """

def badge(text, color="#7c3aed"):
    return (f'<span style="background:{color}22; color:{color}; border:1px solid {color}44; '
            f'border-radius:20px; padding:2px 10px; font-size:11px; font-weight:600;">{text}</span>')

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#cbd5e1",
    font_family="Inter",
    legend_font_color="#94a3b8",
    margin=dict(t=10, b=10, l=10, r=10),
    xaxis=dict(color="#64748b", gridcolor="rgba(99,102,241,0.1)", zeroline=False),
    yaxis=dict(color="#64748b", gridcolor="rgba(99,102,241,0.1)", zeroline=False),
)

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKCHAIN / HASHING
# ─────────────────────────────────────────────────────────────────────────────

def compute_hash(tx_id, date_str, tx_type, amount, category,
                 payment_method, description, previous_hash):
    """SHA-256 over all transaction fields joined by '|'."""
    raw = "|".join([
        str(tx_id).strip(), str(date_str).strip(), str(tx_type).strip(),
        str(amount).strip(), str(category).strip(), str(payment_method).strip(),
        str(description).strip(), str(previous_hash).strip(),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

# ─────────────────────────────────────────────────────────────────────────────
# CSV OPERATIONS
# ─────────────────────────────────────────────────────────────────────────────

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=CSV_COLUMNS).writeheader()

def _empty_df():
    df = pd.DataFrame(columns=CSV_COLUMNS)
    df["amount"]    = pd.to_numeric(df["amount"],  errors="coerce")
    df["date"]      = pd.to_datetime(df["date"],   errors="coerce")
    df["date_only"] = pd.Series(dtype="object")
    return df

def load_transactions():
    initialize_csv()
    try:
        df = pd.read_csv(CSV_FILE, dtype=str)
        if df.empty or not all(c in df.columns for c in CSV_COLUMNS):
            return _empty_df()
        df["amount"]   = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        df["date"]     = pd.to_datetime(df["date"], format=DATE_FORMAT, errors="coerce")
        df             = df.dropna(subset=["date"])
        df["date_only"] = df["date"].dt.date
        return df.reset_index(drop=True)
    except Exception:
        return _empty_df()

def save_transaction(record):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CSV_COLUMNS).writerow(
            {k: record[k] for k in CSV_COLUMNS}
        )

def get_last_hash():
    df = load_transactions()
    return GENESIS_HASH if df.empty else str(df.iloc[-1]["current_hash"])

def transaction_id_exists(tx_id):
    df = load_transactions()
    return False if df.empty else (
        tx_id.strip() in df["transaction_id"].astype(str).str.strip().values
    )

# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_transaction(tx_id, date_str, tx_type, amount_str,
                         category, payment_method, description):
    errors = []
    if not tx_id or not tx_id.strip():
        errors.append("Transaction ID is required.")
    elif transaction_id_exists(tx_id):
        errors.append(f"Transaction ID '{tx_id}' already exists.")
    try:
        datetime.strptime(str(date_str), DATE_FORMAT)
    except ValueError:
        errors.append("Invalid date. Use YYYY-MM-DD format.")
    if tx_type not in ("Income", "Expense"):
        errors.append("Transaction type must be 'Income' or 'Expense'.")
    try:
        if float(amount_str) <= 0:
            errors.append("Amount must be a positive number.")
    except (ValueError, TypeError):
        errors.append("Amount must be a valid positive number.")
    if not category or not category.strip():
        errors.append("Category is required.")
    if not payment_method or not payment_method.strip():
        errors.append("Payment method is required.")
    if not description or not description.strip():
        errors.append("Description is required.")
    return errors

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKCHAIN VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────

def verify_all():
    """Full chain verification — returns list of per-row result dicts."""
    df = load_transactions()
    results = []
    if df.empty:
        return results
    expected_prev = GENESIS_HASH
    for idx, row in df.iterrows():
        tx_id  = str(row["transaction_id"]).strip()
        ds     = row["date"].strftime(DATE_FORMAT) if pd.notna(row["date"]) else ""
        amt    = str(row["amount"]).strip()
        stored = str(row["current_hash"]).strip()
        s_prev = str(row["previous_hash"]).strip()
        recalc = compute_hash(tx_id, ds, str(row["type"]).strip(), amt,
                              str(row["category"]).strip(),
                              str(row["payment_method"]).strip(),
                              str(row["description"]).strip(), s_prev)
        hash_ok = recalc == stored
        link_ok = s_prev == expected_prev
        results.append({
            "index": idx + 1, "tx_id": tx_id, "date": ds,
            "hash_ok": hash_ok, "link_ok": link_ok,
            "stored": stored[:20] + "…", "recalc": recalc[:20] + "…",
            "exp_prev": expected_prev[:20] + "…", "s_prev": s_prev[:20] + "…",
        })
        expected_prev = stored
    return results


def verify_single(tx_id_input: str, amount_input: float):
    """
    Smart single-record check:
      Step 1 — Look up the transaction by ID.
      Step 2 — Compare the user-supplied amount with the stored amount.
               If they match → PASS (amount is intact).
               If they differ → FAIL immediately (amount was tampered).
      Step 3 — Also run hash verification so the full picture is shown.
    Returns a dict with all details.
    """
    df = load_transactions()
    tx_id_input = tx_id_input.strip().upper()

    if df.empty:
        return {"found": False, "error": "No transactions exist yet."}

    match = df[df["transaction_id"].astype(str).str.strip().str.upper() == tx_id_input]
    if match.empty:
        return {"found": False, "error": f"Transaction ID '{tx_id_input}' not found."}

    row = match.iloc[0]
    stored_amount = float(row["amount"])
    amount_ok     = abs(stored_amount - amount_input) < 1e-6   # float-safe compare

    # Full chain hash verification for this record
    ds     = row["date"].strftime(DATE_FORMAT) if pd.notna(row["date"]) else ""
    s_prev = str(row["previous_hash"]).strip()
    stored_hash = str(row["current_hash"]).strip()
    recalc = compute_hash(
        str(row["transaction_id"]).strip(), ds,
        str(row["type"]).strip(), str(row["amount"]).strip(),
        str(row["category"]).strip(), str(row["payment_method"]).strip(),
        str(row["description"]).strip(), s_prev,
    )
    hash_ok = (recalc == stored_hash)

    # Previous-hash link check
    row_index = match.index[0]
    if row_index == 0:
        expected_prev = GENESIS_HASH
    else:
        prev_row      = df.iloc[row_index - 1]
        expected_prev = str(prev_row["current_hash"]).strip()
    link_ok = (s_prev == expected_prev)

    overall_pass = amount_ok and hash_ok and link_ok

    return {
        "found":          True,
        "tx_id":          str(row["transaction_id"]).strip(),
        "date":           ds,
        "tx_type":        str(row["type"]),
        "stored_amount":  stored_amount,
        "input_amount":   amount_input,
        "amount_ok":      amount_ok,
        "hash_ok":        hash_ok,
        "link_ok":        link_ok,
        "overall_pass":   overall_pass,
        "stored_hash":    stored_hash,
        "recalc_hash":    recalc,
        "category":       str(row["category"]),
        "description":    str(row["description"]),
    }

# ─────────────────────────────────────────────────────────────────────────────
# WEEKLY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_week_bounds(ref):
    mon = ref - timedelta(days=ref.weekday())
    return mon, mon + timedelta(days=6)

def weekly_summary(df, ws, we):
    mask   = (df["date_only"] >= ws) & (df["date_only"] <= we)
    wdf    = df[mask].copy()
    inc    = wdf[wdf["type"] == "Income"]
    exp    = wdf[wdf["type"] == "Expense"]
    ti, te = float(inc["amount"].sum()), float(exp["amount"].sum())
    cat_exp = (exp.groupby("category")["amount"].sum()
               .reset_index().rename(columns={"amount": "total"}))
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    if not exp.empty:
        ec = exp.copy()
        ec["day_name"] = ec["date"].dt.day_name()
        daily = (ec.groupby("day_name")["amount"].sum()
                 .reindex(day_order, fill_value=0)
                 .reset_index())
        daily.columns = ["day", "total"]
    else:
        daily = pd.DataFrame({"day": day_order, "total": [0]*7})
    return {"ti": ti, "te": te, "bal": ti - te, "n": len(wdf),
            "cat_exp": cat_exp, "daily": daily, "wdf": wdf}

# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────────────────────────────────────

SAMPLE = [
    ("TXN0001","2026-10-12","Income","5000.0","Salary","Bank Transfer","Monthly income"),
    ("TXN0002","2026-10-13","Expense","250.0","Food","UPI","Lunch payment"),
    ("TXN0003","2026-10-14","Expense","500.0","Travel","UPI","Bus and travel"),
    ("TXN0004","2026-10-15","Income","1000.0","Freelance","Bank Transfer","Freelance work"),
    ("TXN0005","2026-10-16","Expense","300.0","Shopping","Cash","Personal shopping"),
]

def seed_sample_data():
    if not load_transactions().empty:
        return
    prev = GENESIS_HASH
    for tid, dt, typ, amt, cat, pay, desc in SAMPLE:
        h = compute_hash(tid, dt, typ, amt, cat, pay, desc, prev)
        save_transaction({"transaction_id":tid,"date":dt,"type":typ,"amount":amt,
                          "category":cat,"payment_method":pay,"description":desc,
                          "current_hash":h,"previous_hash":prev})
        prev = h

# ─────────────────────────────────────────────────────────────────────────────
# PAGE — DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

def page_dashboard(df):
    st.markdown(section_header("📊 Dashboard", "Your complete financial overview at a glance"),
                unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px;">
            <div style="font-size:64px; margin-bottom:16px;">🚀</div>
            <h3 style="color:#7c3aed;">No transactions yet</h3>
            <p style="color:#64748b;">Head over to <strong>Add Transaction</strong> to get started!</p>
        </div>""", unsafe_allow_html=True)
        return

    ti   = float(df[df["type"]=="Income"]["amount"].sum())
    te   = float(df[df["type"]=="Expense"]["amount"].sum())
    nb   = ti - te
    ntx  = len(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(glow_card("💰","Total Income",   f"₹{ti:,.0f}",  "#10b981"), unsafe_allow_html=True)
    c2.markdown(glow_card("💸","Total Expenses", f"₹{te:,.0f}",  "#f43f5e"), unsafe_allow_html=True)
    c3.markdown(glow_card("🏦","Net Balance",    f"₹{nb:,.0f}",
                           "#10b981" if nb >= 0 else "#f43f5e"), unsafe_allow_html=True)
    c4.markdown(glow_card("🔗","Transactions",   str(ntx),        "#6366f1"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    exp_df = df[df["type"]=="Expense"].copy()
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        st.markdown('<p style="color:#a78bfa;font-weight:600;margin-bottom:4px;">🥧 Expenses by Category</p>',
                    unsafe_allow_html=True)
        if exp_df.empty:
            st.info("No expense data yet.")
        else:
            cat = exp_df.groupby("category")["amount"].sum().reset_index()
            fig = px.pie(cat, values="amount", names="category",
                         color_discrete_sequence=px.colors.qualitative.Vivid, hole=0.42)
            fig.update_traces(textfont_size=12, textfont_color="#fff")
            fig.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

    with r1c2:
        st.markdown('<p style="color:#a78bfa;font-weight:600;margin-bottom:4px;">📅 Daily Expenses</p>',
                    unsafe_allow_html=True)
        if exp_df.empty:
            st.info("No expense data yet.")
        else:
            cutoff = date.today() - timedelta(days=21)
            src = exp_df[exp_df["date_only"] >= cutoff] if not exp_df[exp_df["date_only"] >= cutoff].empty else exp_df
            daily = src.groupby("date_only")["amount"].sum().reset_index()
            daily.columns = ["date","amount"]
            fig = px.bar(daily, x="date", y="amount",
                         color_discrete_sequence=["#7c3aed"])
            fig.update_traces(marker_line_width=0)
            fig.update_layout(**CHART_LAYOUT, xaxis_title="Date", yaxis_title="Amount (₹)")
            st.plotly_chart(fig, use_container_width=True)

    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.markdown('<p style="color:#a78bfa;font-weight:600;margin-bottom:4px;">📈 Cumulative Spending Trend</p>',
                    unsafe_allow_html=True)
        if exp_df.empty:
            st.info("No expense data yet.")
        else:
            trend = exp_df.groupby("date_only")["amount"].sum().cumsum().reset_index()
            trend.columns = ["date","cumulative"]
            fig = px.area(trend, x="date", y="cumulative",
                          color_discrete_sequence=["#f59e0b"])
            fig.update_traces(fill="tozeroy", fillcolor="rgba(245,158,11,0.12)")
            fig.update_layout(**CHART_LAYOUT, xaxis_title="Date", yaxis_title="Cumulative (₹)")
            st.plotly_chart(fig, use_container_width=True)

    with r2c2:
        st.markdown('<p style="color:#a78bfa;font-weight:600;margin-bottom:4px;">⚖️ Income vs Expenses</p>',
                    unsafe_allow_html=True)
        grp = df.groupby(["date_only","type"])["amount"].sum().reset_index()
        if grp.empty:
            st.info("No data yet.")
        else:
            fig = px.bar(grp, x="date_only", y="amount", color="type", barmode="group",
                         color_discrete_map={"Income":"#10b981","Expense":"#f43f5e"})
            fig.update_traces(marker_line_width=0)
            fig.update_layout(**CHART_LAYOUT, xaxis_title="Date", yaxis_title="Amount (₹)")
            st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE — ADD TRANSACTION
# ─────────────────────────────────────────────────────────────────────────────

def page_add_transaction():
    st.markdown(section_header("➕ Add New Transaction", "Fill in the details below to record a new entry"),
                unsafe_allow_html=True)

    df = load_transactions()
    default_id = f"TXN{len(df)+1:04d}"

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tx_id   = st.text_input("🆔 Transaction ID", value=default_id,
                                    help="Must be unique across all transactions")
            tx_date = st.date_input("📅 Date", value=date.today())
            tx_type = st.selectbox("📂 Type", ["Income", "Expense"])
            amt_str = st.text_input("💵 Amount (₹)", placeholder="e.g. 1500.00")
        with col2:
            cats    = INCOME_CATEGORIES if tx_type == "Income" else EXPENSE_CATEGORIES
            cat     = st.selectbox("🏷️ Category", cats)
            pay     = st.selectbox("💳 Payment Method", PAYMENT_METHODS)
            desc    = st.text_area("📝 Description",
                                   placeholder="Brief note about this transaction",
                                   height=116)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💾 Save Transaction", use_container_width=True)

    if submitted:
        date_str = tx_date.strftime(DATE_FORMAT)
        errs = validate_transaction(tx_id, date_str, tx_type, amt_str, cat, pay, desc)
        if errs:
            for e in errs:
                st.error(f"❌  {e}")
        else:
            prev = get_last_hash()
            h    = compute_hash(tx_id.strip(), date_str, tx_type,
                                str(float(amt_str)), cat, pay, desc.strip(), prev)
            save_transaction({
                "transaction_id": tx_id.strip(), "date": date_str,
                "type": tx_type, "amount": str(float(amt_str)),
                "category": cat, "payment_method": pay,
                "description": desc.strip(), "current_hash": h, "previous_hash": prev,
            })
            st.success(f"✅  Transaction **{tx_id.strip()}** saved successfully!")
            st.markdown(f"""
            <div style="margin-top:16px; background:rgba(10,15,30,0.8);
                border:1px solid rgba(99,102,241,0.25); border-radius:12px; padding:18px;">
                <p style="color:#7c3aed; font-weight:700; font-size:13px;
                           text-transform:uppercase; letter-spacing:1px; margin:0 0 10px 0;">
                    🔐 Blockchain Record Created</p>
                <div style="margin-bottom:10px;">
                    <span style="color:#64748b; font-size:11px;">CURRENT HASH</span><br>
                    <code style="color:#10b981; font-size:11px; word-break:break-all;">{h}</code>
                </div>
                <div>
                    <span style="color:#64748b; font-size:11px;">PREVIOUS HASH (linked from)</span><br>
                    <code style="color:#6366f1; font-size:11px; word-break:break-all;">{prev}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE — TRANSACTION HISTORY
# ─────────────────────────────────────────────────────────────────────────────

def page_transaction_history(df):
    st.markdown(section_header("📋 Transaction History", "Browse, search, and filter all your records"),
                unsafe_allow_html=True)

    if df.empty:
        st.info("📭 No transactions yet. Use **Add Transaction** to create your first record.")
        return

    # Filters
    with st.container():
        st.markdown('<div style="background:rgba(15,23,42,0.5); border:1px solid rgba(99,102,241,0.15); border-radius:12px; padding:16px; margin-bottom:16px;">',
                    unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1:
            ftype = st.selectbox("Filter by Type", ["All","Income","Expense"])
        with f2:
            cats  = sorted(df["category"].dropna().unique().tolist())
            fcat  = st.selectbox("Filter by Category", ["All"]+cats)
        with f3:
            srch  = st.text_input("🔍 Search Description", placeholder="keyword...")
        d1, d2 = st.columns(2)
        with d1:
            min_d = df["date_only"].min() if not df.empty else date.today()
            sd    = st.date_input("From", value=min_d, key="hs")
        with d2:
            ed    = st.date_input("To",   value=date.today(), key="he")
        st.markdown('</div>', unsafe_allow_html=True)

    fil = df.copy()
    if ftype != "All":   fil = fil[fil["type"]==ftype]
    if fcat  != "All":   fil = fil[fil["category"]==fcat]
    if srch:             fil = fil[fil["description"].str.contains(srch, case=False, na=False)]
    fil = fil[(fil["date_only"] >= sd) & (fil["date_only"] <= ed)]

    # Stats row
    ic  = float(fil[fil["type"]=="Income"]["amount"].sum())
    ex  = float(fil[fil["type"]=="Expense"]["amount"].sum())
    net = ic - ex
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.markdown(glow_card("📄","Records",  str(len(fil)),      "#6366f1"), unsafe_allow_html=True)
    sc2.markdown(glow_card("💰","Income",   f"₹{ic:,.0f}",      "#10b981"), unsafe_allow_html=True)
    sc3.markdown(glow_card("💸","Expenses", f"₹{ex:,.0f}",      "#f43f5e"), unsafe_allow_html=True)
    sc4.markdown(glow_card("🏦","Net",      f"₹{net:,.0f}",
                            "#10b981" if net >= 0 else "#f43f5e"),           unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if fil.empty:
        st.warning("⚠️ No transactions match your filters.")
        return

    disp = fil[["transaction_id","date_only","type","amount","category","payment_method","description"]].copy()
    disp.columns = ["ID","Date","Type","Amount (₹)","Category","Payment","Description"]
    disp["Amount (₹)"] = disp["Amount (₹)"].apply(lambda x: f"₹ {float(x):,.2f}")
    st.dataframe(disp, use_container_width=True, height=420)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE — WEEKLY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def page_weekly_analysis(df):
    st.markdown(section_header("📆 Weekly Analysis", "Detailed income & expense breakdown for any week"),
                unsafe_allow_html=True)

    if df.empty:
        st.info("📭 No transactions available for analysis.")
        return

    ref = st.date_input("📅 Pick any date within the week you want to analyse",
                        value=date.today())
    ws, we = get_week_bounds(ref)
    st.markdown(f"""
    <div style="display:inline-block; background:rgba(99,102,241,0.12);
        border:1px solid rgba(99,102,241,0.3); border-radius:20px; padding:6px 16px;
        margin-bottom:16px;">
        <span style="color:#a78bfa; font-size:13px; font-weight:600;">
            📅 {ws.strftime('%d %b %Y')} — {we.strftime('%d %b %Y')}
        </span>
    </div>""", unsafe_allow_html=True)

    s = weekly_summary(df, ws, we)
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(glow_card("💰","Weekly Income",   f"₹{s['ti']:,.0f}", "#10b981"), unsafe_allow_html=True)
    c2.markdown(glow_card("💸","Weekly Expenses", f"₹{s['te']:,.0f}", "#f43f5e"), unsafe_allow_html=True)
    c3.markdown(glow_card("🏦","Weekly Balance",  f"₹{s['bal']:,.0f}",
                           "#10b981" if s["bal"]>=0 else "#f43f5e"), unsafe_allow_html=True)
    c4.markdown(glow_card("🔢","Transactions",    str(s["n"]), "#6366f1"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if s["n"] == 0:
        st.warning("⚠️ No transactions recorded for this week.")
        return

    pc1, pc2 = st.columns(2)
    with pc1:
        st.markdown('<p style="color:#a78bfa;font-weight:600;">🥧 Category-Wise Expenses</p>',
                    unsafe_allow_html=True)
        if s["cat_exp"].empty:
            st.info("No expenses this week.")
        else:
            fig = px.pie(s["cat_exp"], values="total", names="category",
                         color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.38)
            fig.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

    with pc2:
        st.markdown('<p style="color:#a78bfa;font-weight:600;">📊 Daily Expenses</p>',
                    unsafe_allow_html=True)
        fig = px.bar(s["daily"], x="day", y="total",
                     color_discrete_sequence=["#7c3aed"])
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**CHART_LAYOUT, xaxis_title="", yaxis_title="Amount (₹)")
        st.plotly_chart(fig, use_container_width=True)

    if not s["wdf"].empty:
        st.markdown('<p style="color:#a78bfa;font-weight:600;margin-top:8px;">📋 Transactions This Week</p>',
                    unsafe_allow_html=True)
        wd = s["wdf"][["transaction_id","date_only","type","amount","category","description"]].copy()
        wd.columns = ["ID","Date","Type","Amount (₹)","Category","Description"]
        wd["Amount (₹)"] = wd["Amount (₹)"].apply(lambda x: f"₹ {float(x):,.2f}")
        st.dataframe(wd, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE — VERIFY BLOCKCHAIN  (smart single + full chain)
# ─────────────────────────────────────────────────────────────────────────────

def page_verify_blockchain(df):
    st.markdown(
        section_header("🔐 Verify Blockchain Integrity",
                       "Check individual records or scan the entire chain"),
        unsafe_allow_html=True,
    )

    # Info banner
    st.markdown("""
    <div style="background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.25);
                border-radius:12px; padding:14px 18px; margin-bottom:24px;">
        <p style="color:#94a3b8; margin:0; font-size:13px; line-height:1.7;">
            ℹ️  BlockTrack re-computes the <strong style="color:#a78bfa;">SHA-256 hash</strong>
            of every field in a transaction and checks that each record's
            <code style="color:#60a5fa;">previous_hash</code> matches the preceding record.
            Any edit to the CSV will break the hash and be detected here.
            This is an educational demonstration — not a real decentralised blockchain.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("📭 No transactions to verify.")
        return

    # ─── TAB 1: Smart Single-Record Check ────────────────────────────────
    tab1, tab2 = st.tabs(["🎯  Single Record Check", "🔗  Full Chain Verification"])

    with tab1:
        st.markdown("""
        <p style="color:#94a3b8; font-size:13px; margin-bottom:20px;">
            Enter a <strong>Transaction ID</strong> and the <strong>Amount</strong> you expect
            to be stored. If the amount matches → <span style="color:#10b981;font-weight:700;">PASS</span>.
            If it differs → the record has been tampered, and the hash mismatch will confirm it.
        </p>
        """, unsafe_allow_html=True)

        # Show available IDs for reference
        id_list = df["transaction_id"].astype(str).str.strip().tolist()
        st.markdown(
            '<p style="color:#64748b;font-size:12px;">Available IDs: '
            + " · ".join(f'<code style="color:#a78bfa;">{i}</code>' for i in id_list)
            + "</p>",
            unsafe_allow_html=True,
        )

        with st.form("verify_single_form"):
            vc1, vc2 = st.columns(2)
            with vc1:
                in_id  = st.text_input("🆔 Transaction ID",
                                       placeholder="e.g. TXN0001",
                                       help="Case-insensitive")
            with vc2:
                in_amt = st.number_input("💵 Expected Amount (₹)",
                                         min_value=0.0, step=0.01, format="%.2f",
                                         help="The amount you believe should be stored")
            verify_btn = st.form_submit_button("🔍 Verify This Record",
                                               use_container_width=True)

        if verify_btn:
            if not in_id.strip():
                st.error("❌  Please enter a Transaction ID.")
            else:
                with st.spinner("Checking record..."):
                    res = verify_single(in_id, in_amt)

                if not res["found"]:
                    st.error(f"❌  {res['error']}")
                else:
                    # ── Result header ──────────────────────────────────────
                    overall_color = "#10b981" if res["overall_pass"] else "#f43f5e"
                    overall_text  = "✅  PASS — Record is intact" if res["overall_pass"] \
                                    else "❌  FAIL — Record has been tampered"

                    st.markdown(f"""
                    <div style="background:rgba(10,15,30,0.85); border:2px solid {overall_color};
                        border-radius:14px; padding:22px 24px; margin:16px 0;
                        box-shadow: 0 0 30px {overall_color}25;">
                        <h3 style="color:{overall_color}; margin:0 0 16px 0; font-size:20px;">
                            {overall_text}
                        </h3>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                            <div>
                                <span style="color:#64748b;font-size:11px;text-transform:uppercase;
                                             letter-spacing:1px;">Transaction ID</span>
                                <p style="color:#f1f5f9; font-weight:700; margin:2px 0 0 0;">
                                    {res['tx_id']}</p>
                            </div>
                            <div>
                                <span style="color:#64748b;font-size:11px;text-transform:uppercase;
                                             letter-spacing:1px;">Date</span>
                                <p style="color:#f1f5f9; font-weight:700; margin:2px 0 0 0;">
                                    {res['date']}</p>
                            </div>
                            <div>
                                <span style="color:#64748b;font-size:11px;text-transform:uppercase;
                                             letter-spacing:1px;">Type / Category</span>
                                <p style="color:#f1f5f9; font-weight:700; margin:2px 0 0 0;">
                                    {res['tx_type']} · {res['category']}</p>
                            </div>
                            <div>
                                <span style="color:#64748b;font-size:11px;text-transform:uppercase;
                                             letter-spacing:1px;">Description</span>
                                <p style="color:#f1f5f9; font-weight:700; margin:2px 0 0 0;">
                                    {res['description']}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Check rows ─────────────────────────────────────────
                    checks = [
                        {
                            "icon": "💵",
                            "label": "Amount Check",
                            "ok": res["amount_ok"],
                            "detail": (
                                f"Your input <strong>₹ {res['input_amount']:,.2f}</strong> "
                                f"matches stored <strong>₹ {res['stored_amount']:,.2f}</strong> → Amount is correct."
                            ) if res["amount_ok"] else (
                                f"Your input <strong style='color:#f43f5e;'>₹ {res['input_amount']:,.2f}</strong> "
                                f"≠ stored <strong style='color:#f43f5e;'>₹ {res['stored_amount']:,.2f}</strong> → "
                                f"Amount has been <strong>modified!</strong>"
                            ),
                        },
                        {
                            "icon": "🔐",
                            "label": "Hash Integrity",
                            "ok": res["hash_ok"],
                            "detail": (
                                f"Recomputed hash matches stored hash → Data fields are unchanged."
                            ) if res["hash_ok"] else (
                                f"Recomputed hash <strong style='color:#f43f5e;'>does not match</strong> "
                                f"stored hash → One or more fields were altered."
                            ),
                        },
                        {
                            "icon": "🔗",
                            "label": "Chain Link",
                            "ok": res["link_ok"],
                            "detail": (
                                "Previous-hash link is intact → Chain is unbroken."
                            ) if res["link_ok"] else (
                                "Previous-hash link is <strong style='color:#f43f5e;'>broken</strong> "
                                "→ Either this or the preceding record was modified."
                            ),
                        },
                    ]

                    for ck in checks:
                        bg    = "rgba(16,185,129,0.07)" if ck["ok"] else "rgba(244,63,94,0.07)"
                        bdr   = "#10b981"               if ck["ok"] else "#f43f5e"
                        icon2 = "✅" if ck["ok"] else "❌"
                        st.markdown(f"""
                        <div style="background:{bg}; border:1px solid {bdr}44;
                            border-left:4px solid {bdr}; border-radius:10px;
                            padding:14px 18px; margin-bottom:10px;">
                            <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                                <span style="font-size:18px;">{ck['icon']}</span>
                                <span style="color:#f1f5f9; font-weight:700;">{ck['label']}</span>
                                <span style="font-size:16px;">{icon2}</span>
                            </div>
                            <p style="color:#94a3b8; font-size:13px; margin:0;">{ck['detail']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # ── Hash detail expander ───────────────────────────────
                    with st.expander("🔎 Show full hash details"):
                        st.markdown(f"""
                        | Field | Value |
                        |---|---|
                        | **Stored Hash** | `{res['stored_hash']}` |
                        | **Recomputed Hash** | `{res['recalc_hash']}` |
                        | **Match** | {"✅ Yes" if res['hash_ok'] else "❌ No — tampered!"} |
                        """)

    # ─── TAB 2: Full Chain Verification ──────────────────────────────────
    with tab2:
        st.markdown("""
        <p style="color:#94a3b8; font-size:13px; margin-bottom:20px;">
            Scan every transaction in the chain in sequence.
            Each record's hash is recomputed and its previous-hash link is validated.
        </p>
        """, unsafe_allow_html=True)

        if st.button("🔗 Verify Entire Blockchain", use_container_width=True, type="primary"):
            with st.spinner("Scanning all records..."):
                results = verify_all()

            all_ok = all(r["hash_ok"] and r["link_ok"] for r in results)
            fail_c = sum(1 for r in results if not (r["hash_ok"] and r["link_ok"]))

            if all_ok:
                st.success(f"✅  All **{len(results)}** records passed — chain is intact and untampered.")
            else:
                st.error(f"🚨  **{fail_c}** record(s) failed integrity check — tampering detected!")

            st.markdown("<br>", unsafe_allow_html=True)

            # Progress-style summary bar
            pass_c = len(results) - fail_c
            st.markdown(f"""
            <div style="display:flex; gap:8px; margin-bottom:20px;">
                <div style="flex:{pass_c}; background:#10b981; border-radius:4px; height:8px;
                             min-width:{pass_c*2}px;"></div>
                <div style="flex:{fail_c}; background:#f43f5e; border-radius:4px; height:8px;
                             min-width:{fail_c*2}px;"></div>
            </div>
            <p style="color:#64748b; font-size:12px; margin-bottom:16px;">
                <span style="color:#10b981; font-weight:700;">■</span> {pass_c} Passed &nbsp;
                <span style="color:#f43f5e; font-weight:700;">■</span> {fail_c} Failed
            </p>
            """, unsafe_allow_html=True)

            for r in results:
                ok    = r["hash_ok"] and r["link_ok"]
                color = "#10b981" if ok else "#f43f5e"
                icon  = "✅" if ok else "❌"
                label = "PASS" if ok else "FAIL"
                h_ico = "✅" if r["hash_ok"] else "❌"
                l_ico = "✅" if r["link_ok"] else "❌"
                st.markdown(f"""
                <div style="background:rgba(10,15,30,0.7); border-left:4px solid {color};
                    border:1px solid {color}30; border-left:4px solid {color};
                    border-radius:10px; padding:14px 18px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span style="color:#f1f5f9; font-weight:700; font-size:14px;">
                            {icon} &nbsp; #{r['index']} — {r['tx_id']}
                            &nbsp;<span style="color:{color}; font-size:12px;
                                         background:{color}18; padding:2px 8px;
                                         border-radius:10px;">{label}</span>
                        </span>
                        <span style="color:#64748b; font-size:12px;">{r['date']}</span>
                    </div>
                    <div style="font-size:12px; color:#64748b; line-height:1.8;">
                        {h_ico} Hash: <code style="color:#a78bfa;">{r['stored']}</code>
                        → recalc <code style="color:#f59e0b;">{r['recalc']}</code><br>
                        {l_ico} Prev-hash link: <code style="color:#60a5fa;">{r['s_prev']}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="BlockTrack — Transaction Tracker",
        page_icon="🔗",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    initialize_csv()
    seed_sample_data()

    # ── Sidebar ───────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:16px 0 24px;">
            <div style="font-size:40px; margin-bottom:4px;">🔗</div>
            <h1 style="font-size:24px; font-weight:800; margin:0;
                background:linear-gradient(135deg,#a78bfa,#60a5fa);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                BlockTrack
            </h1>
            <p style="color:#475569; font-size:11px; margin:4px 0 0;">
                Blockchain Transaction Tracker
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid rgba(99,102,241,0.2); margin-bottom:16px;"></div>',
                    unsafe_allow_html=True)

        page = st.radio("nav", [
            "📊  Dashboard",
            "➕  Add Transaction",
            "📋  Transaction History",
            "📆  Weekly Analysis",
            "🔐  Verify Blockchain",
        ], label_visibility="collapsed")

        st.markdown('<div style="border-top:1px solid rgba(99,102,241,0.2); margin:16px 0;"></div>',
                    unsafe_allow_html=True)

        df_s = load_transactions()
        if not df_s.empty:
            ti_s  = float(df_s[df_s["type"]=="Income"]["amount"].sum())
            te_s  = float(df_s[df_s["type"]=="Expense"]["amount"].sum())
            nb_s  = ti_s - te_s
            bc    = "#10b981" if nb_s >= 0 else "#f43f5e"
            st.markdown(f"""
            <div style="background:rgba(10,15,30,0.6); border:1px solid rgba(99,102,241,0.2);
                        border-radius:12px; padding:14px 16px;">
                <p style="color:#6366f1; font-size:10px; font-weight:700;
                           text-transform:uppercase; letter-spacing:1px; margin:0 0 10px;">
                    Quick Stats</p>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#94a3b8; font-size:12px;">📄 Records</span>
                    <span style="color:#f1f5f9; font-weight:600; font-size:12px;">{len(df_s)}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#94a3b8; font-size:12px;">💰 Income</span>
                    <span style="color:#10b981; font-weight:600; font-size:12px;">₹{ti_s:,.0f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#94a3b8; font-size:12px;">💸 Expenses</span>
                    <span style="color:#f43f5e; font-weight:600; font-size:12px;">₹{te_s:,.0f}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#94a3b8; font-size:12px;">🏦 Balance</span>
                    <span style="color:{bc}; font-weight:700; font-size:12px;">₹{nb_s:,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <p style="color:#334155; font-size:10px; text-align:center; margin-top:20px;">
            BlockTrack v2.0 · SHA-256 Demo<br>Academic Project
        </p>""", unsafe_allow_html=True)

    # ── Route ─────────────────────────────────────────────────────────────
    df = load_transactions()
    if   "Dashboard"    in page: page_dashboard(df)
    elif "Add"          in page: page_add_transaction()
    elif "History"      in page: page_transaction_history(df)
    elif "Weekly"       in page: page_weekly_analysis(df)
    elif "Verify"       in page: page_verify_blockchain(df)


if __name__ == "__main__":
    main()
