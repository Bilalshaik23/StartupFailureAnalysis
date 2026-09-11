import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from utils.data_loader import load_data
from utils.charts import (
    status_pie,
    funding_box_by_status,
    funding_rounds_box,
    funding_histogram,
    sector_bar,
    country_bar,
    closure_by_sector,
    correlation_heatmap,
    company_age_histogram,
    funding_violin,
    scatter_funding_rounds,
)


CHART_INSIGHTS = {
    "status_pie":           "Operating companies dominate (68.4%), but closure at 17.3% is non-trivial — roughly 1 in 6 startups shuts down.",
    "funding_box":          "Closed startups' median log-funding is visibly lower than operating/acquired/IPO companies — confirmed by Welch's t-test (t ≈ −12.77, p < 0.001).",
    "funding_rounds":       "Closed startups complete fewer funding rounds on average, suggesting early capital exhaustion before reaching Series B+.",
    "funding_hist":         "The log-funding distributions of closed vs non-closed companies show a clear leftward shift for closed firms, validating the t-test finding.",
    "sector_bar":           "Software and Biotech dominate by count; long-tail sectors with few companies show higher variance in closure rates.",
    "country_bar":          "The USA accounts for the majority of startups — geographic concentration could bias sector and funding comparisons.",
    "closure_sector":       "Certain sectors show closure rates 2–3× the dataset average — a key signal for investors performing sector due diligence.",
    "corr_heatmap":         "funding_total_usd and funding_rounds are positively correlated; is_closed shows a small negative correlation with funding — directionally consistent with t-test results.",
    "company_age":          "Founding activity peaked 2007–2012; the skew toward recent companies means some may still be pre-outcome, slightly underrepresenting closure rates.",
    "funding_violin":       "Violin plots reveal the full shape of funding distributions — the IPO group shows a distinct upper-tail extending well beyond operating companies.",
    "scatter_rounds":       "Higher funding rounds generally correlate with higher total funding; closed companies cluster in the low-rounds, low-funding quadrant.",
}


def chart_with_insight(fig, key: str):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        f'<div class="ag-chart-insight">💡 {CHART_INSIGHTS.get(key, "")}</div>',
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="EDA | Startup Failure Analysis",
        page_icon="🔬",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">🔬 Exploratory Data Analysis</div>
            <div class="ag-hero-title">EDA Dashboard</div>
            <div class="ag-hero-subtitle">Patterns, Distributions &amp; Relationships</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distributions", "💰 Funding Analysis", "🏭 Sector & Geo", "🔗 Relationships"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="ag-section-header"><div class="ag-section-title">Status Distribution</div></div>', unsafe_allow_html=True)
            chart_with_insight(status_pie(df), "status_pie")

        with c2:
            st.markdown('<div class="ag-section-header"><div class="ag-section-title">Company Founding Year</div></div>', unsafe_allow_html=True)
            chart_with_insight(company_age_histogram(df), "company_age")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="ag-section-header"><div class="ag-section-title">Log Funding by Status</div></div>', unsafe_allow_html=True)
            chart_with_insight(funding_box_by_status(df), "funding_box")

        with c2:
            st.markdown('<div class="ag-section-header"><div class="ag-section-title">Funding Rounds by Status</div></div>', unsafe_allow_html=True)
            chart_with_insight(funding_rounds_box(df), "funding_rounds")

        st.markdown("<br>", unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="ag-section-header"><div class="ag-section-title">Funding Histogram: Closed vs Non-Closed</div></div>', unsafe_allow_html=True)
            chart_with_insight(funding_histogram(df), "funding_hist")

        with c4:
            st.markdown('<div class="ag-section-header"><div class="ag-section-title">Funding Violin Plot</div></div>', unsafe_allow_html=True)
            chart_with_insight(funding_violin(df), "funding_violin")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="ag-section-header"><div class="ag-section-title">Funding Rounds vs Total Funding</div></div>', unsafe_allow_html=True)
        chart_with_insight(scatter_funding_rounds(df), "scatter_rounds")

    with tab3:
        top_n = st.slider("Number of top sectors/countries to display", min_value=10, max_value=30, value=20, step=5)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="ag-section-header"><div class="ag-section-title">Top Sectors</div></div>', unsafe_allow_html=True)
            chart_with_insight(sector_bar(df, top_n=top_n), "sector_bar")

        with c2:
            st.markdown('<div class="ag-section-header"><div class="ag-section-title">Top Countries</div></div>', unsafe_allow_html=True)
            chart_with_insight(country_bar(df, top_n=top_n), "country_bar")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="ag-section-header"><div class="ag-section-title">Closure Rate by Sector</div>'
                    '<div class="ag-section-sub">% of companies in each sector that are classified as "closed"</div></div>', unsafe_allow_html=True)
        chart_with_insight(closure_by_sector(df, top_n=top_n), "closure_sector")

    with tab4:
        st.markdown('<div class="ag-section-header"><div class="ag-section-title">Feature Correlation Heatmap</div></div>', unsafe_allow_html=True)
        chart_with_insight(correlation_heatmap(df), "corr_heatmap")

    

main()
