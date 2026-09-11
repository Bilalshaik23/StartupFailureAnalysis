import streamlit as st
import pandas as pd
from utils.data_loader import load_data, summary_stats, STATUS_PALETTE
from utils.charts import status_pie, funding_violin
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Startup Failure Analysis | Home",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Top Navigation functionality
t1, t2, t3 = st.columns([2, 1, 1])
with t1:
    search_term = st.text_input("Search", placeholder="🔍 Search startups, sectors, countries...", label_visibility="collapsed")
with t3:
    st.markdown('<div style="display:flex; justify-content:flex-end; padding-top:0.5rem; color:#64748b; font-size:0.85rem; font-weight:600;">CSM353 | LPU</div>', unsafe_allow_html=True)

df = load_data()
if search_term:
    search_lower = search_term.lower()
    df = df[
        df['name'].str.lower().fillna('').str.contains(search_lower) | 
        df['primary_category'].str.lower().fillna('').str.contains(search_lower) |
        df['country_for_chart'].str.lower().fillna('').str.contains(search_lower)
    ]

stats = summary_stats(df)

# Hero Section
st.markdown(
    """
    <div class="ag-hero">
        <div class="ag-hero-content">
            <div class="ag-hero-pretitle">REAL DATA. REAL PATTERNS. REAL IMPACT.</div>
            <div class="ag-hero-title">Startup <span>Failure</span> Analysis</div>
            <div class="ag-hero-subtitle">What Statistically Predicts Shutdown</div>
            <div class="ag-hero-desc">
                An exploratory data analysis and statistical inference project to understand<br>
                why startups fail, using real-world data from Crunchbase.
            </div>
            <div class="ag-hero-buttons">
                <a href="Interactive_Dashboard" target="_self" class="ag-btn-primary">Explore the Analysis →</a>
                <a href="About_Me" target="_self" class="ag-btn-secondary">Learn More</a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

def _fmt(val):
    if val >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    return f"${val:,.0f}"

metrics = [
    {"icon": "🏢", "val": f"{stats['total']:,}", "label": "Total Startups", "sub": "", "color": "#1e3b3a"},
    {"icon": "❌", "val": f"{stats['closed']:,}", "label": "Closed", "sub": f"{stats['closure_rate']}%", "color": "#ef4444"},
    {"icon": "🤝", "val": f"{stats['acquired']:,}", "label": "Acquired", "sub": f"{round(stats['acquired']/stats['total']*100,1)}%", "color": "#8b5cf6"},
    {"icon": "📈", "val": f"{stats['ipo']:,}", "label": "IPO", "sub": f"{round(stats['ipo']/stats['total']*100,1)}%", "color": "#10b981"},
    {"icon": "▶️", "val": f"{stats['operating']:,}", "label": "Operating", "sub": f"{round(stats['operating']/stats['total']*100,1)}%", "color": "#3b82f6"},
    {"icon": "💲", "val": _fmt(stats['avg_funding']), "label": "Avg. Funding", "sub": "(reported)", "color": "#1e3b3a"},
    {"icon": "💿", "val": f"{stats['avg_rounds']:.1f}", "label": "Avg. Funding Rounds", "sub": "", "color": "#a855f7"},
    {"icon": "🌐", "val": f"{stats['n_countries']}", "label": "Countries", "sub": "Covered", "color": "#3b82f6"},
]

metric_html = '<div class="ag-metric-row">'
for m in metrics:
    metric_html += f'<div class="ag-metric-card"><div class="ag-metric-icon" style="background: {m["color"]}20; color: {m["color"]};">{m["icon"]}</div><div class="ag-metric-value">{m["val"]}</div><div class="ag-metric-label">{m["label"]}</div>'
    if m["sub"]:
        metric_html += f'<div class="ag-metric-sub" style="color: {m["color"]};">{m["sub"]}</div>'
    metric_html += '</div>'
metric_html += '</div>'
st.markdown(metric_html, unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.2, 0.8])

with c1:
    st.markdown('<div class="ag-card-header" style="padding-top:1rem;">Startup Status Distribution</div><div class="ag-card-sub">Share of startup outcomes in the dataset</div>', unsafe_allow_html=True)
    st.plotly_chart(status_pie(df), use_container_width=True, config={"displayModeBar": False})

with c2:
    st.markdown('<div class="ag-card-header" style="padding-top:1rem;">Funding Distribution by Status</div><div class="ag-card-sub">Startups that closed had significantly lower funding (p < 0.001)</div>', unsafe_allow_html=True)
    st.plotly_chart(funding_violin(df), use_container_width=True, config={"displayModeBar": False})

with c3:
    st.markdown(
        """
        <div class="ag-card" style="height: 100%;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1.5rem;">
                <div>
                    <div class="ag-card-header" style="display:flex; align-items:center; gap:0.5rem;"><span style="color:#f59e0b;">💡</span> Key Takeaways</div>
                </div>
                <a href="#" style="font-size:0.8rem; font-weight:600; color:#1e3b3a; text-decoration:none;">View All →</a>
            </div>
            <div class="ag-takeaway-item">
                <div class="ag-takeaway-icon" style="color:#ef4444;">📊</div>
                <div class="ag-takeaway-text"><b>Startups that fail have significantly lower funding</b> (t = -12.77, p < 0.001).</div>
            </div>
            <div class="ag-takeaway-item">
                <div class="ag-takeaway-icon" style="color:#3b82f6;">📉</div>
                <div class="ag-takeaway-text"><b>Certain sectors are more prone to failure</b> (χ² test, p < 0.001).</div>
            </div>
            <div class="ag-takeaway-item">
                <div class="ag-takeaway-icon" style="color:#10b981;">📈</div>
                <div class="ag-takeaway-text"><b>Funding levels differ significantly across sectors</b> (ANOVA, p < 0.001).</div>
            </div>
            <div class="ag-takeaway-item">
                <div class="ag-takeaway-icon" style="color:#f59e0b;">📄</div>
                <div class="ag-takeaway-text"><b>Top failure reason: No Market Need (42%)</b> – CB Insights.</div>
            </div>
            <div class="ag-takeaway-item">
                <div class="ag-takeaway-icon" style="color:#10b981;">🌱</div>
                <div class="ag-takeaway-text">Data-driven insights can help build more resilient startups.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="ag-footer-banner">
        <div class="ag-footer-content">
            <div class="ag-footer-pre">A MORE RESILIENT TOMORROW</div>
            <div class="ag-footer-title">Behind every failed startup is a lesson that can build a better one.</div>
        </div>
        <div class="ag-footer-content">
            <a href="#" class="ag-footer-link">Turn data into better decisions.</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
