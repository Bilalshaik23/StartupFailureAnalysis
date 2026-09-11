import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


def main():
    st.set_page_config(
        page_title="About | Startup Failure Analysis",
        page_icon="ℹ️",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">ℹ️ About This Project</div>
            <div class="ag-hero-title">Project Overview</div>
            <div class="ag-hero-subtitle">Problem, Objectives &amp; Methodology</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.markdown(
            """
            <div class="ag-section-header">
                <div class="ag-section-title">Problem Statement</div>
            </div>
            <div class="ag-card">
                <p style="color:var(--text-secondary);line-height:1.8;font-size:0.92rem;">
                    Startup failure is endemic: industry estimates consistently place failure rates
                    between <strong style="color:var(--text-primary);">70–90%</strong> within the first decade.
                    Despite abundant anecdotal evidence, rigorous statistical analysis of <em>what
                    actually distinguishes</em> closed startups from surviving ones remains rare in
                    accessible, reproducible form.
                </p>
                <p style="color:var(--text-secondary);line-height:1.8;font-size:0.92rem;margin-top:0.75rem;">
                    This project applies EDA and formal hypothesis testing to the Crunchbase dataset
                    to identify statistically significant predictors of startup closure — not opinions,
                    but evidence.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Research Objectives</div></div>',
            unsafe_allow_html=True,
        )

        objectives = [
            ("🔍", "Explore the distribution of startup outcomes across sectors, geographies, and funding levels"),
            ("📐", "Test whether funding levels statistically predict closure using Welch's t-test"),
            ("🏗️", "Determine if sector membership is associated with closure via χ² test"),
            ("📊", "Quantify cross-sector funding differences using Welch's one-way ANOVA"),
            ("💡", "Complement statistical findings with CB Insights' post-mortem failure taxonomy"),
            ("🎯", "Translate findings into actionable recommendations for founders, VCs, and policy"),
        ]

        for icon, obj in objectives:
            st.markdown(
                f"""
                <div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.6rem;
                     background:rgba(99,102,241,0.05);border:1px solid rgba(99,102,241,0.12);
                     border-radius:10px;padding:0.75rem 1rem;">
                    <span style="font-size:1.1rem;">{icon}</span>
                    <span style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;">{obj}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c2:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Dataset Overview</div></div>',
            unsafe_allow_html=True,
        )

        dataset_info = [
            ("📦", "Source",     "Crunchbase (via Kaggle public release)"),
            ("🗂️", "Format",     "CSV — crunchbase_cleaned.csv"),
            ("📏", "Dimensions", "~9,000 rows × 28 features (post-cleaning)"),
            ("🏷️", "Target",     "is_closed (binary) derived from status"),
            ("🕐", "Period",     "Companies founded 1970s – 2014"),
            ("🌍", "Coverage",   "137+ countries, 700+ sectors"),
            ("💰", "Funding",    "funding_total_usd (USD, log-transformed for tests)"),
            ("📈", "Outcomes",   "operating, closed, acquired, ipo"),
        ]

        for icon, key, val in dataset_info:
            st.markdown(
                f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                     padding:0.6rem 1rem;border-bottom:1px solid rgba(99,102,241,0.08);">
                    <span style="font-size:0.82rem;color:var(--text-muted);">{icon} {key}</span>
                    <span style="font-size:0.82rem;color:var(--text-primary);font-weight:500;">{val}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="ag-card">
                <div style="font-size:0.85rem;font-weight:700;color:var(--text-primary);margin-bottom:0.75rem;">
                    📐 Statistical Tests Applied
                </div>
                <div style="display:flex;flex-direction:column;gap:0.5rem;">
                    <div style="display:flex;justify-content:space-between;font-size:0.8rem;">
                        <span style="color:var(--text-secondary);">Sector vs Closure</span>
                        <span class="ag-badge">Chi-Square Test</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:0.8rem;">
                        <span style="color:var(--text-secondary);">Funding vs Closure</span>
                        <span class="ag-badge">Welch's T-Test</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:0.8rem;">
                        <span style="color:var(--text-secondary);">Funding across Sectors</span>
                        <span class="ag-badge">Welch's ANOVA</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:0.8rem;">
                        <span style="color:var(--text-secondary);">Significance Threshold</span>
                        <span class="ag-badge-warning ag-badge">α = 0.05</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="ag-section-header"><div class="ag-section-title">Analysis Workflow</div>'
        '<div class="ag-section-sub">End-to-end pipeline from raw data to business insights</div></div>',
        unsafe_allow_html=True,
    )

    steps = [
        ("📥", "Data Collection",    "Crunchbase CSV acquisition"),
        ("🧹", "Data Cleaning",      "Missing values, deduplication, feature engineering"),
        ("🔬", "EDA",                "Distribution, correlation, sector & geo analysis"),
        ("📐", "Statistical Tests",  "χ², Welch's t-test, Welch's ANOVA"),
        ("📊", "Visualization",      "Interactive Plotly charts"),
        ("💼", "Business Insights",  "Actionable recommendations"),
    ]

    step_html = "".join([
        f'<div class="ag-timeline-step">'
        f'<div class="ag-timeline-icon">{icon}</div>'
        f'<div class="ag-timeline-label">{label}</div>'
        f'<div style="font-size:0.65rem;color:var(--text-muted);margin-top:0.3rem;">{desc}</div>'
        f'</div>'
        for icon, label, desc in steps
    ])

    st.markdown(f'<div class="ag-timeline">{step_html}</div>', unsafe_allow_html=True)

    

main()
