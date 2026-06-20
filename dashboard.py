import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL CSS + ANIMATIONS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #060910;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 4px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0a0d14 !important;
    border-right: 1px solid #0f1e33;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label {
    color: #64748b !important;
    font-size: 13px;
    padding: 6px 0;
    transition: color 0.2s ease;
}
[data-testid="stSidebar"] .stRadio [data-checked="true"] label {
    color: #38bdf8 !important;
    font-weight: 600;
}

/* ── MAIN BG ── */
.main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: #060910;
}

/* ── PAGE FADE-IN ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.6; }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position:  200% 0; }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.85); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes borderGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(56,189,248,0); }
    50%       { box-shadow: 0 0 12px 2px rgba(56,189,248,0.12); }
}

/* ── KPI CARDS ── */
.kpi-card {
    background: linear-gradient(135deg, #0d1520 0%, #111827 60%, #0f1e33 100%);
    border: 1px solid #1a2a40;
    border-radius: 14px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s ease both;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    cursor: default;
}
.kpi-card:hover {
    transform: translateY(-3px);
    border-color: #2a4a6b;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(56,189,248,0.08);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 14px 14px 0 0;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 120px; height: 120px;
    border-radius: 50%;
    opacity: 0.04;
}
.kpi-card.blue::before  { background: linear-gradient(90deg, #3b82f6, #60a5fa, #93c5fd); }
.kpi-card.cyan::before  { background: linear-gradient(90deg, #06b6d4, #22d3ee, #67e8f9); }
.kpi-card.violet::before{ background: linear-gradient(90deg, #8b5cf6, #a78bfa, #c4b5fd); }
.kpi-card.emerald::before{ background: linear-gradient(90deg, #10b981, #34d399, #6ee7b7); }
.kpi-card.rose::before  { background: linear-gradient(90deg, #f43f5e, #fb7185, #fda4af); }

.kpi-card.blue::after   { background: #3b82f6; }
.kpi-card.cyan::after   { background: #06b6d4; }
.kpi-card.violet::after { background: #8b5cf6; }
.kpi-card.emerald::after{ background: #10b981; }
.kpi-card.rose::after   { background: #f43f5e; }

.kpi-icon {
    font-size: 18px;
    margin-bottom: 10px;
    display: block;
}
.kpi-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #f1f5f9;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
    animation: countUp 0.6s ease both;
}
.kpi-sub {
    font-size: 11px;
    color: #334155;
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 4px;
}
.kpi-sub.up   { color: #34d399; }
.kpi-sub.down { color: #f87171; }

/* ── SECTION HEADERS ── */
.section-header {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #38bdf8;
    margin: 4px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 10px;
    animation: slideInLeft 0.4s ease both;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e3a5f 0%, transparent 100%);
}

/* ── INSIGHT CARDS ── */
.insight-card {
    background: #0d1520;
    border: 1px solid #1a2a40;
    border-left: 3px solid #38bdf8;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.7;
    animation: fadeInUp 0.5s ease both;
    transition: border-left-color 0.2s ease, background 0.2s ease;
}
.insight-card:hover { background: #111827; }
.insight-card.warning { border-left-color: #f59e0b; }
.insight-card.success { border-left-color: #10b981; }
.insight-card.danger  { border-left-color: #ef4444; }

/* ── PAGE TITLE ── */
.page-title {
    font-size: 28px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.02em;
    animation: fadeInUp 0.4s ease both;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 13px;
    color: #334155;
    margin-bottom: 28px;
    animation: fadeInUp 0.5s ease both;
}

/* ── LOGO ── */
.sidebar-logo {
    font-size: 18px;
    font-weight: 700;
    color: #f1f5f9 !important;
    letter-spacing: -0.02em;
    font-family: 'JetBrains Mono', monospace;
}
.sidebar-logo span { color: #38bdf8; }

/* ── NAV ACTIVE DOT ── */
.nav-dot {
    width: 6px; height: 6px;
    background: #38bdf8;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    animation: pulse 2s infinite;
}

/* ── STATUS BADGE ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.badge-green  { background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.2); }
.badge-red    { background: rgba(239, 68,68,0.12);  color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.badge-yellow { background: rgba(245,158,11,0.12);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }
.badge-blue   { background: rgba(56,189,248,0.10);  color: #38bdf8; border: 1px solid rgba(56,189,248,0.2); }

/* ── DIVIDER ── */
hr { border-color: #0f1e33 !important; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1a2a40 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── METRIC OVERRIDE ── */
h1, h2, h3 { color: #f1f5f9 !important; }
p, li { color: #64748b !important; }
[data-testid="metric-container"] { background: transparent; }
.js-plotly-plot { border-radius: 10px; overflow: hidden; }

/* ── LOADING SKELETON SHIMMER ── */
.skeleton {
    background: linear-gradient(90deg, #0d1520 25%, #1a2a40 50%, #0d1520 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 8px;
    height: 80px;
}

/* ── STAGGER ANIMATION DELAYS ── */
.kpi-card:nth-child(1) { animation-delay: 0.0s; }
.kpi-card:nth-child(2) { animation-delay: 0.08s; }
.kpi-card:nth-child(3) { animation-delay: 0.16s; }
.kpi-card:nth-child(4) { animation-delay: 0.24s; }
.kpi-card:nth-child(5) { animation-delay: 0.32s; }

/* ── SELECTBOX / DATEINPUT ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stDateInput"] > div > div {
    background: #0d1520 !important;
    border: 1px solid #1a2a40 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
}
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ──────────────────────────────────────────────────────────────────
import os
_BASE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_BASE, "data")

@st.cache_data
def load_data():
    retail   = pd.read_csv(os.path.join(_DATA, "cleaned_retail.csv"))
    segments = pd.read_csv(os.path.join(_DATA, "customer_segments.csv"))
    forecast = pd.read_csv(os.path.join(_DATA, "future_forecast_prophet.csv"))

    retail["InvoiceDate"] = pd.to_datetime(retail["InvoiceDate"], errors="coerce")
    retail["TotalAmount"] = retail["Quantity"] * retail["UnitPrice"]
    retail["Month"]       = retail["InvoiceDate"].dt.to_period("M").astype(str)
    retail["DayOfWeek"]   = retail["InvoiceDate"].dt.day_name()
    retail["Hour"]        = retail["InvoiceDate"].dt.hour

    forecast["ds"] = pd.to_datetime(forecast["ds"])
    return retail, segments, forecast

retail, segments, forecast = load_data()


# ── PLOTLY THEME ───────────────────────────────────────────────────────────────
CHART_BG = "#0d1520"
CHART_THEME = dict(
    plot_bgcolor  = CHART_BG,
    paper_bgcolor = CHART_BG,
    font          = dict(family="Inter", color="#64748b", size=11),
    xaxis         = dict(
        gridcolor="#0f1e33", linecolor="#0f1e33",
        tickfont=dict(color="#475569", size=10),
        showgrid=True, zeroline=False
    ),
    yaxis         = dict(
        gridcolor="#0f1e33", linecolor="#0f1e33",
        tickfont=dict(color="#475569", size=10),
        showgrid=True, zeroline=False
    ),
    margin        = dict(l=40, r=20, t=36, b=40),
    colorway      = ["#38bdf8","#818cf8","#34d399","#fb923c","#f472b6","#facc15"],
    legend        = dict(
        font=dict(color="#64748b", size=11),
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)"
    ),
)

def apply_theme(fig):
    fig.update_layout(**CHART_THEME)
    return fig

def styled_chart(fig, yprefix="", ysuffix="", xprefix="", xsuffix=""):
    apply_theme(fig)
    if yprefix or ysuffix:
        fig.update_yaxes(tickprefix=yprefix, ticksuffix=ysuffix)
    if xprefix or xsuffix:
        fig.update_xaxes(tickprefix=xprefix, ticksuffix=xsuffix)
    return fig


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 16px 0;'>
        <div class='sidebar-logo'>Retail<span>Pulse</span></div>
        <div style='font-size:11px; color:#1e3a5f; margin-top:4px; font-family: JetBrains Mono, monospace;'>
            v1.0 · Zidio Internship
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Overview", "Customer Intelligence", "Product & Inventory", "Demand Forecast"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    countries = ["All"] + sorted(retail["Country"].dropna().unique().tolist())
    selected_country = st.selectbox("🌍 Country", countries)

    min_date = retail["InvoiceDate"].min().date()
    max_date = retail["InvoiceDate"].max().date()
    date_range = st.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("---")

    # Live status indicator
    st.markdown("""
    <div style='display:flex; align-items:center; gap:8px; padding: 8px 0;'>
        <div style='width:7px;height:7px;background:#34d399;border-radius:50%;
                    box-shadow:0 0 6px #34d399; animation: pulse 2s infinite;'></div>
        <span style='font-size:11px; color:#334155;'>Data loaded</span>
    </div>
    """, unsafe_allow_html=True)


# ── FILTER ─────────────────────────────────────────────────────────────────────
filtered = retail.copy()
if selected_country != "All":
    filtered = filtered[filtered["Country"] == selected_country]
if len(date_range) == 2:
    filtered = filtered[
        (filtered["InvoiceDate"].dt.date >= date_range[0]) &
        (filtered["InvoiceDate"].dt.date <= date_range[1])
    ]


# ── GLOBAL KPIs ────────────────────────────────────────────────────────────────
total_revenue   = filtered["TotalAmount"].sum()
total_orders    = filtered["InvoiceNo"].nunique()
total_customers = filtered["CustomerID"].nunique()
total_products  = filtered["StockCode"].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

monthly = filtered.groupby("Month")["TotalAmount"].sum().sort_index()
mom_growth = ((monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2]) * 100 if len(monthly) >= 2 else 0
mom_arrow  = "▲" if mom_growth >= 0 else "▼"
mom_class  = "up" if mom_growth >= 0 else "down"


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: KPI CARD
# ══════════════════════════════════════════════════════════════════════════════
def kpi(icon, label, value, sub, color, sub_class=""):
    return f"""
    <div class="kpi-card {color}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub {sub_class}">{sub}</div>
    </div>"""


def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown('<div class="page-title">Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Business performance at a glance</div>', unsafe_allow_html=True)

    # KPI Row
    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        (c1, kpi("💰", "Total Revenue",   f"£{total_revenue/1e6:.2f}M",  f"{mom_arrow} {abs(mom_growth):.1f}% MoM", "blue",    mom_class)),
        (c2, kpi("🧾", "Total Orders",    f"{total_orders:,}",           "Unique invoices",                          "cyan")),
        (c3, kpi("👥", "Customers",       f"{int(total_customers):,}",   "With purchase history",                    "violet")),
        (c4, kpi("💳", "Avg Order Value", f"£{avg_order_value:.0f}",     "Per invoice",                              "emerald")),
        (c5, kpi("📦", "Active SKUs",     f"{total_products:,}",         "Unique products",                          "rose")),
    ]
    for col, card_html in cards:
        with col:
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Revenue Trend + Day of Week
    col1, col2 = st.columns([2, 1])

    with col1:
        section("Revenue Trend")
        monthly_df = filtered.groupby("Month")["TotalAmount"].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_df["Month"], y=monthly_df["TotalAmount"],
            mode="lines+markers",
            line=dict(color="#38bdf8", width=2.5),
            marker=dict(size=5, color="#38bdf8", line=dict(color="#060910", width=1.5)),
            fill="tozeroy",
            fillcolor="rgba(56,189,248,0.06)",
            name="Revenue"
        ))
        styled_chart(fig, yprefix="£")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Sales by Day")
        dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dow = filtered.groupby("DayOfWeek")["TotalAmount"].sum().reindex(dow_order).reset_index()
        fig2 = go.Figure(go.Bar(
            x=dow["TotalAmount"], y=dow["DayOfWeek"],
            orientation="h",
            marker=dict(
                color=dow["TotalAmount"],
                colorscale=[[0,"#0f1e33"],[0.5,"#1e3a5f"],[1,"#38bdf8"]],
                showscale=False
            )
        ))
        styled_chart(fig2, xprefix="£")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Country Revenue — always uses full dataset, filter makes no sense here
    section("Revenue by Country — Top 15")
    # Apply only date filter, not country filter (country chart = comparison view)
    date_filtered = retail.copy()
    if len(date_range) == 2:
        date_filtered = date_filtered[
            (date_filtered["InvoiceDate"].dt.date >= date_range[0]) &
            (date_filtered["InvoiceDate"].dt.date <= date_range[1])
        ]
    date_filtered["TotalAmount"] = date_filtered["Quantity"] * date_filtered["UnitPrice"]
    country_rev = (
        date_filtered.groupby("Country")["TotalAmount"].sum()
        .reset_index().sort_values("TotalAmount", ascending=False).head(15)
        .rename(columns={"TotalAmount": "Revenue"})
    )
    if selected_country != "All":
        st.markdown(
            '<div class="insight-card" style="margin-bottom:12px">ℹ️ Country filter ignored here — this chart always shows all countries for comparison.</div>',
            unsafe_allow_html=True
        )
    fig3 = px.bar(
        country_rev, x="Country", y="Revenue",
        color="Revenue",
        color_continuous_scale=[[0,"#0f1e33"],[0.5,"#1e3a5f"],[1,"#38bdf8"]],
        labels={"Revenue": "Revenue (£)", "Country": "Country"}
    )
    fig3.update_traces(marker_line_width=0)
    styled_chart(fig3, yprefix="£")
    fig3.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Revenue (£)",
        xaxis_title="Country"
    )
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Customer Intelligence":
    st.markdown('<div class="page-title">Customer Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">RFM segmentation and behavioural analysis</div>', unsafe_allow_html=True)

    SEG_COLORS = {
        "Champions"          : "#38bdf8",
        "Loyal Customers"    : "#818cf8",
        "Potential Customers": "#34d399",
        "New Customers"      : "#facc15",
        "At Risk"            : "#fb923c",
        "Lost Customers"     : "#ef4444",
    }

    seg_counts  = segments["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment","Count"]
    seg_revenue = segments.groupby("Segment")["Monetary"].sum().reset_index()
    seg_revenue.columns = ["Segment","Revenue"]
    seg_rfm     = segments.groupby("Segment")[["Recency","Frequency","Monetary"]].mean().reset_index()

    # Summary KPIs
    total_cust    = seg_counts["Count"].sum()
    champ_row     = seg_counts[seg_counts["Segment"]=="Champions"]
    champ_pct     = (champ_row["Count"].values[0] / total_cust * 100) if len(champ_row) else 0
    at_risk_row   = seg_counts[seg_counts["Segment"]=="At Risk"]
    at_risk_n     = at_risk_row["Count"].values[0] if len(at_risk_row) else 0
    lost_row      = seg_counts[seg_counts["Segment"]=="Lost Customers"]
    lost_n        = lost_row["Count"].values[0] if len(lost_row) else 0

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi("🏆", "Champions",    f"{champ_pct:.1f}%",   "Of customer base",  "blue"),    unsafe_allow_html=True)
    with c2: st.markdown(kpi("⚠️", "At Risk",      f"{at_risk_n:,}",     "Need re-engagement","rose"),    unsafe_allow_html=True)
    with c3: st.markdown(kpi("💤", "Lost Customers",f"{lost_n:,}",        "Win-back target",   "violet"),  unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section("Segment Distribution")
        colors = [SEG_COLORS.get(s, "#64748b") for s in seg_counts["Segment"]]
        fig = go.Figure(go.Pie(
            labels=seg_counts["Segment"],
            values=seg_counts["Count"],
            hole=0.58,
            marker=dict(colors=colors, line=dict(color="#060910", width=2.5)),
            textfont=dict(size=11),
        ))
        fig.update_layout(
            **CHART_THEME,
            annotations=[dict(
                text=f"<b>{total_cust:,}</b><br><span style='font-size:10px'>customers</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#f1f5f9", family="JetBrains Mono")
            )]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Revenue by Segment")
        seg_rev_sorted = seg_revenue.sort_values("Revenue", ascending=True)
        fig2 = go.Figure(go.Bar(
            x=seg_rev_sorted["Revenue"],
            y=seg_rev_sorted["Segment"],
            orientation="h",
            marker=dict(
                color=[SEG_COLORS.get(s,"#64748b") for s in seg_rev_sorted["Segment"]],
                opacity=0.85,
                line=dict(width=0)
            )
        ))
        styled_chart(fig2, xprefix="£")
        st.plotly_chart(fig2, use_container_width=True)

    # RFM Scatter
    section("RFM Scatter — Recency vs Monetary")
    sample = segments.sample(min(2000, len(segments)), random_state=42)
    fig3 = px.scatter(
        sample, x="Recency", y="Monetary",
        color="Segment", size="Frequency",
        color_discrete_map=SEG_COLORS,
        opacity=0.75,
        hover_data=["CustomerID","RFM_Score"]
    )
    styled_chart(fig3, yprefix="£")
    st.plotly_chart(fig3, use_container_width=True)

    # RFM Table
    section("Average RFM per Segment")
    seg_rfm_display = seg_rfm.copy()
    seg_rfm_display["Monetary"]  = seg_rfm_display["Monetary"].apply(lambda x: f"£{x:,.0f}")
    seg_rfm_display["Recency"]   = seg_rfm_display["Recency"].apply(lambda x: f"{x:.0f} days")
    seg_rfm_display["Frequency"] = seg_rfm_display["Frequency"].apply(lambda x: f"{x:.1f} orders")
    st.dataframe(seg_rfm_display.set_index("Segment"), use_container_width=True)

    # Insights
    section("Segment Insights")
    st.markdown(f'<div class="insight-card success">Champions represent <strong>{champ_pct:.1f}%</strong> of customers but drive a disproportionate share of revenue — prioritise retention campaigns for this cohort.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-card danger"><strong>{lost_n:,}</strong> customers classified as Lost. Win-back campaigns with discount triggers recommended before permanent churn.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-card warning"><strong>{at_risk_n:,}</strong> At Risk customers show declining recency — immediate re-engagement via personalised offers can recover this segment.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PRODUCT & INVENTORY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Product & Inventory":
    st.markdown('<div class="page-title">Product & Inventory</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">SKU performance and stock health</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section("Top 10 by Quantity Sold")
        top_qty = (
            filtered.groupby("Description")["Quantity"]
            .sum().sort_values(ascending=False).head(10).reset_index()
        )
        fig = px.bar(
            top_qty, x="Quantity", y="Description", orientation="h",
            color="Quantity",
            color_continuous_scale=[[0,"#0f1e33"],[1,"#38bdf8"]]
        )
        fig.update_layout(coloraxis_showscale=False)
        fig.update_yaxes(autorange="reversed")
        fig.update_traces(marker_line_width=0)
        styled_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Top 10 by Revenue")
        top_rev = (
            filtered.groupby("Description")["TotalAmount"]
            .sum().sort_values(ascending=False).head(10).reset_index()
        )
        fig2 = px.bar(
            top_rev, x="TotalAmount", y="Description", orientation="h",
            color="TotalAmount",
            color_continuous_scale=[[0,"#1a1040"],[1,"#818cf8"]]
        )
        fig2.update_layout(coloraxis_showscale=False)
        fig2.update_yaxes(autorange="reversed")
        fig2.update_traces(marker_line_width=0)
        styled_chart(fig2, xprefix="£")
        st.plotly_chart(fig2, use_container_width=True)

    # Inventory Health
    section("Inventory Health Status")
    inventory = (
        filtered.groupby(["StockCode","Description"])["Quantity"]
        .sum().reset_index()
    )
    q25 = inventory["Quantity"].quantile(0.25)
    q75 = inventory["Quantity"].quantile(0.75)
    def classify(q):
        if q < q25:   return "Reorder Needed"
        elif q > q75: return "Overstocked"
        else:         return "Healthy Stock"
    inventory["Status"] = inventory["Quantity"].apply(classify)

    status_counts = inventory["Status"].value_counts().reset_index()
    status_counts.columns = ["Status","Count"]

    STATUS_COLORS = {
        "Reorder Needed": "#ef4444",
        "Healthy Stock" : "#10b981",
        "Overstocked"   : "#f59e0b"
    }

    col3, col4 = st.columns([1,2])
    with col3:
        fig3 = go.Figure(go.Pie(
            labels=status_counts["Status"],
            values=status_counts["Count"],
            hole=0.55,
            marker=dict(
                colors=[STATUS_COLORS.get(s,"#64748b") for s in status_counts["Status"]],
                line=dict(color="#060910", width=2.5)
            ),
            textfont=dict(size=11)
        ))
        fig3.update_layout(**CHART_THEME)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        reorder_items = inventory[inventory["Status"]=="Reorder Needed"].sort_values("Quantity").head(15)
        reorder_count = len(inventory[inventory["Status"]=="Reorder Needed"])
        st.markdown(f'<div class="insight-card danger"><strong>{reorder_count:,}</strong> SKUs below reorder threshold (bottom 25% of stock levels). Top 15 critical shown below.</div>', unsafe_allow_html=True)
        st.dataframe(
            reorder_items[["StockCode","Description","Quantity"]].reset_index(drop=True),
            use_container_width=True,
            height=270
        )

    # Pareto
    section("Revenue Concentration — Pareto View")
    prod_rev = (
        filtered.groupby("Description")["TotalAmount"]
        .sum().sort_values(ascending=False).reset_index()
    )
    prod_rev["cumulative_pct"] = prod_rev["TotalAmount"].cumsum() / prod_rev["TotalAmount"].sum() * 100
    prod_rev["rank"] = range(1, len(prod_rev)+1)
    top80 = prod_rev[prod_rev["cumulative_pct"] <= 80]

    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Bar(
        x=prod_rev["rank"].head(50), y=prod_rev["TotalAmount"].head(50),
        marker=dict(
            color=prod_rev["TotalAmount"].head(50),
            colorscale=[[0,"#0f1e33"],[1,"#38bdf8"]],
            showscale=False,
            line=dict(width=0)
        ),
        name="Revenue", opacity=0.85
    ), secondary_y=False)
    fig4.add_trace(go.Scatter(
        x=prod_rev["rank"].head(50), y=prod_rev["cumulative_pct"].head(50),
        line=dict(color="#f59e0b", width=2),
        mode="lines",
        name="Cumulative %"
    ), secondary_y=True)
    fig4.update_layout(
        **CHART_THEME,
        title=dict(
            text=f"Top 50 SKUs — <b>{len(top80)}</b> products drive 80% of revenue",
            font=dict(color="#64748b", size=12)
        )
    )
    fig4.update_yaxes(tickprefix="£", secondary_y=False, **CHART_THEME["yaxis"])
    fig4.update_yaxes(
        ticksuffix="%", secondary_y=True,
        gridcolor="rgba(0,0,0,0)",
        tickfont=dict(color="#64748b", size=10)
    )
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DEMAND FORECAST
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Demand Forecast":
    st.markdown('<div class="page-title">Demand Forecast</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Prophet model · 30-day forward outlook</div>', unsafe_allow_html=True)

    daily_hist = (
        filtered.groupby(filtered["InvoiceDate"].dt.date)["TotalAmount"]
        .sum().reset_index()
    )
    daily_hist.columns = ["ds","y"]
    daily_hist["ds"] = pd.to_datetime(daily_hist["ds"])

    future_only = forecast[forecast["ds"] > retail["InvoiceDate"].max()]
    if future_only.empty:
        future_only = forecast.tail(30)

    forecast_total    = future_only["yhat"].clip(lower=0).sum()
    forecast_avg_day  = future_only["yhat"].clip(lower=0).mean()
    peak_idx          = future_only["yhat"].idxmax() if not future_only.empty else None
    forecast_peak     = future_only.loc[peak_idx, "yhat"] if peak_idx is not None else 0
    forecast_peak_date = future_only.loc[peak_idx, "ds"].strftime("%d %b %Y") if peak_idx is not None else "N/A"

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi("📈", "Forecasted 30-Day Revenue", f"£{forecast_total:,.0f}", "Prophet model estimate", "blue"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("📅", "Avg Daily Forecast",        f"£{forecast_avg_day:,.0f}", "Next 30 days",         "cyan"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("🎯", "Peak Forecast Day",         f"£{forecast_peak:,.0f}",  forecast_peak_date,      "violet"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Forecast Chart
    section("Historical Sales + 30-Day Forecast")
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_hist["ds"], y=daily_hist["y"],
        name="Historical",
        line=dict(color="#475569", width=1.5),
        fill="tozeroy",
        fillcolor="rgba(71,85,105,0.05)"
    ))

    if "yhat_lower" in forecast.columns and "yhat_upper" in forecast.columns:
        fig.add_trace(go.Scatter(
            x=pd.concat([future_only["ds"], future_only["ds"][::-1]]),
            y=pd.concat([future_only["yhat_upper"], future_only["yhat_lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(56,189,248,0.08)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Confidence Band",
        ))

    fig.add_trace(go.Scatter(
        x=future_only["ds"], y=future_only["yhat"],
        name="Forecast",
        line=dict(color="#38bdf8", width=2.5, dash="dot"),
        mode="lines+markers",
        marker=dict(size=4, color="#38bdf8", line=dict(color="#060910", width=1))
    ))

    split_date = daily_hist["ds"].max()
    fig.add_vline(
        x=split_date,
        line_dash="dash", line_color="#1e3a5f",
        annotation_text="Forecast Start",
        annotation_font_color="#475569",
        annotation_font_size=11
    )
    styled_chart(fig, yprefix="£")
    st.plotly_chart(fig, use_container_width=True)

    # Day of week + table
    col1, col2 = st.columns(2)

    with col1:
        section("Forecast by Day of Week")
        foc = future_only.copy()
        foc["DayOfWeek"] = foc["ds"].dt.day_name()
        dow_fc = (
            foc.groupby("DayOfWeek")["yhat"].mean()
            .reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
            .reset_index()
        )
        fig2 = px.bar(
            dow_fc, x="DayOfWeek", y="yhat",
            color="yhat",
            color_continuous_scale=[[0,"#0f1e33"],[1,"#38bdf8"]]
        )
        fig2.update_layout(coloraxis_showscale=False)
        fig2.update_traces(marker_line_width=0)
        styled_chart(fig2, yprefix="£")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        section("30-Day Forecast Table")
        ft = future_only[["ds","yhat","yhat_lower","yhat_upper"]].copy()
        ft.columns = ["Date","Forecast","Lower","Upper"]
        ft["Date"] = ft["Date"].dt.strftime("%d %b %Y")
        for c in ["Forecast","Lower","Upper"]:
            ft[c] = ft[c].apply(lambda x: f"£{max(x,0):,.0f}")
        st.dataframe(ft.reset_index(drop=True), use_container_width=True, height=340)

    # Model Notes
    section("Model Notes")
    st.markdown('<div class="insight-card warning">Prophet trained on historical daily aggregates. SMAPE ~45% — high variance due to bulk B2B orders in UCI dataset. Directional trend is reliable; point estimates carry ±40% uncertainty. Recommended: log-transform or outlier capping before next training cycle.</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-card">Ensemble (Prophet + LSTM) was tested but underperformed standalone models — both correlate on the same error patterns. Ensemble benefit requires models with uncorrelated residuals.</div>', unsafe_allow_html=True)
