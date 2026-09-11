import streamlit as st
from utils.data_loader import load_data, summary_stats

def _load_css() -> str:
    from pathlib import Path
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return ""

st.set_page_config(
    page_title="Startup Failure Analysis | CSM353",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Global CSS
st.markdown(f"<style>{_load_css()}</style>", unsafe_allow_html=True)

# Define pages
pg = st.navigation([
    st.Page("pages/0_Home.py", title="Home", icon="🏠"),
    st.Page("pages/3_Data_Cleaning.py", title="Data Cleaning", icon="🧹"),
    st.Page("pages/4_EDA.py", title="Exploratory Analysis", icon="📈"),
    st.Page("pages/5_Statistical_Analysis.py", title="Statistical Analysis", icon="🔬"),
    st.Page("pages/6_Interactive_Dashboard.py", title="Interactive Dashboard", icon="🕹️"),
    st.Page("pages/7_Key_Insights.py", title="Key Insights", icon="💡"),
    st.Page("pages/9_Conclusion.py", title="Conclusion", icon="📝"),
    st.Page("pages/10_About_Me.py", title="About Me", icon="👤")
])

# Sidebar styling injection
st.sidebar.markdown(
    """
    <div class="ag-sidebar-brand">
        <span class="ag-sidebar-brand-icon">📊</span>
        <span>Startup Failure Analysis</span>
    </div>
    """,
    unsafe_allow_html=True
)

is_dark = st.sidebar.toggle("🌙 Dark Theme", key="global_theme_toggle")
if is_dark:
    st.markdown('''
    <style>
    :root {
        --bg-primary: #0a0e1a;
        --bg-secondary: #111827;
        --bg-card: #1a2236;
        --bg-card-hover: #1e293b;
        --border: rgba(99,102,241,0.2);
        --border-hover: rgba(99,102,241,0.5);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-teal: #3b82f6;
        --accent-light: #22d3ee;
    }

    /* ── Global app background & base text ── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    section[data-testid="stMainBlockContainer"] {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    /* ── All text elements in main content ── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] ol,
    [data-testid="stMarkdownContainer"] ul,
    [data-testid="stMarkdownContainer"] blockquote,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] h6 {
        color: var(--text-primary) !important;
    }

    /* ── Plotly legend & chart text ── */
    .js-plotly-plot .plotly text,
    .js-plotly-plot .plotly .legendtext,
    .js-plotly-plot .plotly .gtitle,
    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle,
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {
        fill: #cbd5e1 !important;
    }
    .js-plotly-plot .plotly .legend .bg {
        fill: #1a2236 !important;
    }

    /* ── Labels, inputs, selects ── */
    label,
    .stSelectbox label,
    .stMultiSelect label,
    .stSlider label,
    .stTextInput label,
    .stNumberInput label,
    .stTextArea label,
    .stRadio label,
    .stCheckbox label,
    .stToggle label,
    [data-testid="stWidgetLabel"] {
        color: #94a3b8 !important;
    }

    /* ── Metric widgets ── */
    [data-testid="stMetric"] label,
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: var(--text-primary) !important;
    }

    /* ── Dataframes / tables ── */
    [data-testid="stDataFrame"] *,
    .stDataFrame *,
    table, th, td {
        color: #cbd5e1 !important;
        background: var(--bg-card) !important;
    }

    /* ── Expanders ── */
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] .streamlit-expanderHeader {
        color: var(--text-primary) !important;
    }

    /* ── Section headers, cards (custom classes) ── */
    .ag-section-title, .ag-section-sub,
    .ag-card-header, .ag-card-sub,
    .ag-metric-value, .ag-metric-label, .ag-metric-sub,
    .ag-takeaway-text, .ag-footer-pre, .ag-footer-title {
        color: var(--text-primary) !important;
    }

    /* ── Hero banner ── */
    .ag-hero::before {
        background: linear-gradient(90deg, rgba(10,14,26,0.95) 0%, rgba(10,14,26,0.85) 40%, rgba(10,14,26,0) 100%) !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] { background: var(--bg-secondary) !important; }
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] p,
    [data-testid="stSidebar"] nav a span,
    [data-testid="stSidebar"] nav span,
    [data-testid="stSidebar"] section[data-testid="stSidebarContent"] span,
    [data-testid="stSidebar"] section[data-testid="stSidebarContent"] p,
    [data-testid="stSidebar"] section[data-testid="stSidebarContent"] a {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] nav li[aria-selected="true"] span,
    [data-testid="stSidebar"] nav a[aria-selected="true"] span {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stToggle label {
        color: #94a3b8 !important;
    }
    </style>
    ''', unsafe_allow_html=True)

pg.run()

# Sidebar quote block appended at the end of the sidebar
st.sidebar.markdown(
    """
    <div class="ag-sidebar-quote">
        Not every failure is a loss — it's data for a better tomorrow.
        <br><br>
        <span style="font-size:0.7rem;text-transform:uppercase;font-weight:600;letter-spacing:0.05em;color:#94a3b8;">Data drives progress.</span>
    </div>
    """,
    unsafe_allow_html=True
)
