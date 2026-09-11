import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st


RECOMMENDATIONS = [
    {
        "icon": "🚀",
        "audience": "Founders & Entrepreneurs",
        "title": "Secure Runway Before Scaling",
        "color": "#6366f1",
        "points": [
            "Our t-test shows closed startups raised significantly less funding. Prioritise early-stage fundraising even at dilutive terms — cash depletion is the second most cited failure cause.",
            "Choose sector deliberately: closure rates vary dramatically. Entering a high-closure-rate sector requires a stronger capital cushion.",
            "Validate market demand before scaling. CB Insights data shows 42% of failures cite No Market Need — a problem no amount of funding can retroactively solve.",
            "Track funding_activity_days: sustained investor engagement over multiple rounds signals runway longevity.",
        ],
    },
    {
        "icon": "💼",
        "audience": "Venture Capital & Investors",
        "title": "Use Sector + Funding Signals Together",
        "color": "#a855f7",
        "points": [
            "ANOVA results (F ≈ 167.99) confirm that sector predicts funding levels — sector choice is a first-order risk variable, not a background variable.",
            "Weigh both closure rate and funding availability for a sector: a high-closure sector with low average funding is a compounding risk environment.",
            "Cohen's d ≈ −0.191 means the funding–closure relationship is real but small — do not use funding alone as a survival proxy. Team composition, market fit, and timing matter.",
            "Stage-gate investments tied to funding_rounds milestones can reduce exposure to early-stage closure without eliminating portfolio diversity.",
        ],
    },
    {
        "icon": "🏛️",
        "audience": "Incubators & Accelerators",
        "title": "Target High-Closure Sectors for Mentorship",
        "color": "#22d3ee",
        "points": [
            "Sectors with above-average closure rates are where structured incubation has the greatest potential impact — financial and operational mentorship can partially offset the funding deficit.",
            "Programme design should explicitly address market validation frameworks. CB Insights data shows market-fit failure (42%) is more prevalent than funding failure (29%).",
            "Provide connections to early funding sources for cohort companies — the t-test confirms that early funding access is statistically associated with survival.",
            "Track portfolio closure rates by sector to validate programme effectiveness against the Crunchbase baseline.",
        ],
    },
    {
        "icon": "🏦",
        "audience": "Policymakers",
        "title": "Targeted Ecosystem Interventions",
        "color": "#10b981",
        "points": [
            "Geographic concentration (USA ~" + "majority" + " of dataset) suggests global disparities in capital access. Policy interventions in underrepresented regions could unlock significant entrepreneurial activity.",
            "Public co-investment schemes for high-closure sectors can de-risk private capital, encouraging entry into strategically important but currently under-funded domains.",
            "Data transparency requirements for startup outcomes could improve the accuracy of datasets like Crunchbase, enabling better-calibrated interventions.",
            "Regulatory sandboxes for high-closure, high-innovation sectors can reduce structural failure causes unrelated to market demand.",
        ],
    },
    {
        "icon": "🌐",
        "audience": "VC Firms (Portfolio Strategy)",
        "title": "Diversify Across Sector Closure-Rate Buckets",
        "color": "#f59e0b",
        "points": [
            "Portfolio construction should balance low-closure (stable) and high-closure (high-upside) sectors to optimise risk-adjusted returns.",
            "The chi-square result confirms sector is not just a descriptive label — it is a statistically significant determinant of closure probability.",
            "Monitor days_to_first_funding: companies that take very long to secure initial funding may face structural barriers that compound over time.",
            "Use ANOVA evidence to benchmark portfolio companies' funding against sector norms — an underfunded company in an already low-funding sector carries layered risk.",
        ],
    },
]


def main():
    st.set_page_config(
        page_title="Recommendations | Startup Failure Analysis",
        page_icon="🎯",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">🎯 From Evidence to Action</div>
            <div class="ag-hero-title">Business Recommendations</div>
            <div class="ag-hero-subtitle">Inferences from Statistical Findings — Not Guaranteed Prescriptions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.2);
             border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:1.5rem;font-size:0.82rem;color:var(--text-secondary);">
            <strong style="color:#f59e0b;">⚠️ Interpretive Note:</strong>
            The recommendations below are inferences drawn from the statistical patterns identified in this project.
            They should be treated as informed hypotheses for further investigation, not causal prescriptions.
            The dataset reflects a historical snapshot; survivorship bias and geographic concentration
            (heavy US representation) limit generalisability.
        </div>
        """,
        unsafe_allow_html=True,
    )

    for rec in RECOMMENDATIONS:
        with st.expander(f"{rec['icon']} {rec['audience']} — {rec['title']}", expanded=False):
            st.markdown(
                f'<div style="display:inline-block;background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.2);'
                f'color:{rec["color"]};font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;'
                f'padding:0.25rem 0.8rem;border-radius:100px;margin-bottom:1rem;">{rec["audience"]}</div>',
                unsafe_allow_html=True,
            )
            for point in rec["points"]:
                st.markdown(
                    f"""
                    <div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.65rem;
                         background:rgba(99,102,241,0.04);border-radius:8px;padding:0.7rem 1rem;
                         border-left:3px solid {rec['color']};">
                        <span style="color:{rec['color']};flex-shrink:0;">▸</span>
                        <span style="font-size:0.85rem;color:var(--text-secondary);line-height:1.7;">{point}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="ag-section-header"><div class="ag-section-title">All Recommendations at a Glance</div></div>',
        unsafe_allow_html=True,
    )

    rec_cols = st.columns(len(RECOMMENDATIONS))
    for col, rec in zip(rec_cols, RECOMMENDATIONS):
        with col:
            st.markdown(
                f"""
                <div class="ag-rec-card" style="border-top:4px solid {rec['color']};">
                    <div class="ag-rec-icon">{rec['icon']}</div>
                    <div class="ag-rec-audience">{rec['audience']}</div>
                    <div class="ag-rec-title">{rec['title']}</div>
                    <div class="ag-rec-body">{rec['points'][0]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    

main()
