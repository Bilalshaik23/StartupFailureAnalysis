import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from utils.data_loader import load_data, summary_stats


def main():
    st.set_page_config(
        page_title="Conclusion | Startup Failure Analysis",
        page_icon="📝",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">📝 Synthesis</div>
            <div class="ag-hero-title">Conclusion</div>
            <div class="ag-hero-subtitle">Findings, Limitations &amp; Future Scope</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()
    stats = summary_stats(df)

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Research Findings</div></div>',
            unsafe_allow_html=True,
        )

        findings = [
            ("📉", "#ef4444", "Funding Gap is Statistically Real",
             f"Welch's t-test (t ≈ −12.77, p < 0.001) confirms that closed startups raised significantly less "
             f"funding than non-closed ones. However, Cohen's d ≈ −0.191 (small effect) signals that funding is "
             f"one factor among many — not a singular cause."),
            ("🏭", "#a855f7", "Sector Predicts Closure Probability",
             "Chi-square test (p < 0.001) rejects the null hypothesis of independence between sector and closure "
             "status. However, the association strength is small (Cramer's V ≈ 0.122), suggesting sector alone "
             "does not guarantee success or failure."),
            ("📊", "#6366f1", "Cross-Sector Funding Variance is Large",
             "Welch's one-way ANOVA (F ≈ 167.99, p < 0.001) reveals that sectors differ substantially in the "
             "funding they attract — creating compounding risk where high-closure sectors are also low-funding sectors."),
            ("🎯", "#22d3ee", "Market Fit Failure Dominates Self-Reports",
             "CB Insights (101 post-mortems): 42% cite No Market Need as the primary failure cause. This suggests "
             "the funding deficit measured quantitatively is partly a downstream effect of failing to achieve PMF."),
            ("🌍", "#f59e0b", "Geographic and Temporal Breadth",
             f"The dataset covers {stats['n_countries']} countries and spans multiple decades, providing global "
             f"perspective — while noting that the USA accounts for a disproportionate share of observations."),
        ]

        for icon, color, title, body in findings:
            st.markdown(
                f"""
                <div class="ag-card" style="border-left:4px solid {color};margin-bottom:0.75rem;">
                    <div style="display:flex;gap:0.75rem;align-items:flex-start;">
                        <span style="font-size:1.3rem;">{icon}</span>
                        <div>
                            <div style="font-size:0.88rem;font-weight:700;color:var(--text-primary);margin-bottom:0.35rem;">{title}</div>
                            <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.6;">{body}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c2:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Limitations</div></div>',
            unsafe_allow_html=True,
        )

        limitations = [
            ("⚠️", "Historical Snapshot", "Startup status is recorded at a historical point in time; an operating startup is not necessarily a long-term success."),
            ("⚠️", "Missing Shutdown Data", "The data has no actual shutdown date or documented reason for closure."),
            ("⚠️", "Missing Values", "Funding, category, geography, and founding-date information contain missing values."),
            ("⚠️", "Category Ambiguity", "Sector analysis uses each startup's primary category, although many startups belong to multiple categories."),
            ("⚠️", "Causality Not Established", "The findings cannot prove that funding, sector, or geography directly causes startup closure."),
        ]

        for icon, title, body in limitations:
            st.markdown(
                f"""
                <div style="display:flex;gap:0.75rem;align-items:flex-start;padding:0.6rem 0;
                     border-bottom:1px solid rgba(99,102,241,0.08);">
                    <span style="font-size:1rem;color:#f59e0b;">{icon}</span>
                    <div>
                        <div style="font-size:0.82rem;font-weight:600;color:var(--text-primary);">{title}</div>
                        <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.5;margin-top:0.2rem;">{body}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Future Scope</div></div>',
            unsafe_allow_html=True,
        )

        future = [
            ("🤖", "Machine Learning Classifiers", "Train logistic regression, random forest, and gradient boosting models to predict is_closed from the feature set, with SHAP explainability."),
            ("🌐", "Real-Time Data Integration", "Connect to live Crunchbase API for rolling analysis rather than static snapshot evaluation."),
            ("🗺️", "Emerging Market Expansion", "Extend the dataset to include more emerging economies (India, Africa, SE Asia) where startup dynamics differ substantially from the US-dominated current dataset."),
            ("📅", "Survival Analysis", "Apply Kaplan-Meier curves and Cox Proportional Hazards models to model time-to-closure as a function of funding and sector."),
            ("🔬", "Post-Hoc Tests", "Apply Tukey's HSD or Games-Howell post-hoc tests after ANOVA to identify which specific sector pairs drive the funding variance."),
        ]

        for icon, title, body in future:
            st.markdown(
                f"""
                <div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.65rem;
                     background:rgba(99,102,241,0.04);border-radius:8px;padding:0.6rem 0.9rem;">
                    <span style="font-size:1.1rem;">{icon}</span>
                    <div>
                        <div style="font-size:0.82rem;font-weight:600;color:var(--text-primary);">{title}</div>
                        <div style="font-size:0.77rem;color:var(--text-secondary);line-height:1.5;margin-top:0.2rem;">{body}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,rgba(99,102,241,0.12),rgba(34,211,238,0.06));
             border:1px solid rgba(99,102,241,0.2);border-radius:16px;padding:2.5rem;text-align:center;">
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#22d3ee;margin-bottom:1rem;">
                Final Note
            </div>
            <div style="font-size:1.4rem;font-weight:800;color:var(--text-primary);line-height:1.4;max-width:700px;margin:0 auto 1rem;">
                Data doesn't prevent failure — but it builds a more honest picture of the risks before the leap.
            </div>
            <div style="font-size:0.85rem;color:var(--text-muted);max-width:600px;margin:0 auto;">
                This project analysed {stats['total']:,} startups across {stats['n_countries']} countries,
                applied three formal hypothesis tests, and synthesised findings with 20 qualitatively-coded
                failure reasons. The goal: replace anecdote with evidence.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    

main()
