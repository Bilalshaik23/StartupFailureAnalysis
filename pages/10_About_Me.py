import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


PROFILE = {
    "name":     "BilalShaik",
    "role":     "Data Science Student, Lovely Professional University",
    "bio": (
        "Passionate about turning raw data into evidence-based narratives. "
        "This project combines academic statistical inference with product-quality "
        "data visualisation to understand one of the most consequential questions "
        "in entrepreneurship: why do startups fail?"
    ),
    "skills": [
        "Python", "Pandas", "NumPy", "SciPy", "Statsmodels",
        "Plotly", "Streamlit", "Machine Learning", "EDA",
        "Hypothesis Testing", "Data Cleaning", "SQL",
    ],
    "links": {
        "GitHub":   None,
        "LinkedIn": None,
        "Email":    None,
        "Resume":   None,
    },
}

LINK_ICONS = {
    "GitHub":   "🐙",
    "LinkedIn": "🔗",
    "Email":    "✉️",
    "Resume":   "📄",
}


def main():
    st.set_page_config(
        page_title="About Me | Startup Failure Analysis",
        page_icon="👤",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">👤 The Builder</div>
            <div class="ag-hero-title">About Me</div>
            <div class="ag-hero-subtitle">The Person Behind the Analysis</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1.5])

    with c1:
        st.markdown(
            f"""
            <div class="ag-profile-card">
                <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#22d3ee);
                     display:flex;align-items:center;justify-content:center;font-size:2.2rem;margin:0 auto 1rem;">
                    👤
                </div>
                <div style="font-size:1.4rem;font-weight:800;color:var(--text-primary);margin-bottom:0.35rem;">{PROFILE['name']}</div>
                <div style="font-size:0.8rem;color:#22d3ee;font-weight:500;margin-bottom:1rem;">{PROFILE['role']}</div>
                <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.7;margin-bottom:1.5rem;">{PROFILE['bio']}</div>
                <div style="display:flex;flex-wrap:wrap;gap:0.4rem;justify-content:center;margin-bottom:1.5rem;">
                    {''.join(f'<span class="ag-badge">{skill}</span>' for skill in PROFILE["skills"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin-top:1rem;text-align:center;'>", unsafe_allow_html=True)
        for platform, url in PROFILE["links"].items():
            icon = LINK_ICONS.get(platform, "🔗")
            if url:
                st.markdown(
                    f'<a href="{url}" target="_blank" class="ag-social-btn">{icon} {platform}</a>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<span class="ag-social-btn" style="opacity:0.4;cursor:not-allowed;" '
                    f'title="Link not configured">{icon} {platform}</span>',
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align:center;font-size:0.7rem;color:#475569;margin-top:0.75rem;">'
            'To add your links, edit PROFILE[\'links\'] in pages/10_About_Me.py</div>',
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Project Details</div></div>',
            unsafe_allow_html=True,
        )

        project_info = [
            ("📚", "Course",           "Data Science & Machine Learning"),
            ("🏛️", "Institution",      "Lovely Professional University (LPU)"),
            ("📊", "Dataset",          "Crunchbase (via Kaggle public release)"),
            ("🧪", "Tests Applied",    "Welch's T-Test, Chi-Square, Welch's ANOVA"),
            ("🛠️", "Tech Stack",       "Python, Pandas, SciPy, Plotly, Streamlit"),
            ("🎯", "Primary Goal",     "Statistical predictors of startup closure"),
        ]

        for icon, key, val in project_info:
            st.markdown(
                f"""
                <div style="display:flex;gap:1rem;align-items:center;padding:0.65rem 0;
                     border-bottom:1px solid rgba(99,102,241,0.08);">
                    <span style="font-size:1.1rem;width:1.5rem;text-align:center;">{icon}</span>
                    <span style="font-size:0.82rem;color:var(--text-muted);min-width:110px;">{key}</span>
                    <span style="font-size:0.85rem;color:var(--text-primary);font-weight:500;">{val}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Key Contributions</div></div>',
            unsafe_allow_html=True,
        )

        contributions = [
            ("🧹", "Full data cleaning pipeline with before/after auditing"),
            ("📐", "Three formal hypothesis tests with notebook-matched results"),
            ("📊", "11+ interactive Plotly visualisations with real insights"),
            ("🎛️", "Reactive multi-filter dashboard with live KPI updates"),
            ("💼", "Audience-specific recommendations for 5 stakeholder groups"),
            ("🔬", "CB Insights 20-reason failure taxonomy integration"),
            ("🎨", "Dark-mode design system with a single centralised CSS block"),
        ]

        for icon, contribution in contributions:
            st.markdown(
                f"""
                <div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.55rem;
                     background:rgba(99,102,241,0.04);border-radius:8px;padding:0.6rem 0.9rem;">
                    <span style="font-size:1rem;">{icon}</span>
                    <span style="font-size:0.83rem;color:var(--text-secondary);line-height:1.6;">{contribution}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="ag-card" style="background:linear-gradient(135deg,rgba(99,102,241,0.08),rgba(168,85,247,0.04));">
                <div style="font-size:1.1rem;font-weight:700;background:linear-gradient(135deg,#6366f1,#22d3ee);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.5rem;">
                    "Not every failure is a loss — it's data for a better tomorrow."
                </div>
                <div style="font-size:0.78rem;color:var(--text-muted);">— Project motto, CSM353 Startup Failure Analysis</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    

main()
