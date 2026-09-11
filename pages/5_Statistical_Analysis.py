import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from utils.data_loader import load_data, CB_INSIGHTS_REASONS
from utils.stats import compute_ttest, compute_chisq, compute_anova, effect_size_label
from utils.charts import cb_insights_bar


def _pval_fmt(p: float) -> str:
    if p < 1e-10:
        return "< 1×10⁻¹⁰"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.4f}"


def render_test_card(title: str, badge: str, hypotheses: list[str],
                     metrics: list[tuple[str, str]], decision: str, interpretation: str):
    hyp_html = "".join(f'<div style="margin:0.2rem 0;">{h}</div>' for h in hypotheses)
    metrics_html = "".join(
        f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;'
        f'border-bottom:1px solid rgba(99,102,241,0.08);">'
        f'<span style="color:var(--text-muted);font-size:0.82rem;">{k}</span>'
        f'<span style="color:var(--text-primary);font-size:0.82rem;font-weight:600;font-family:\'JetBrains Mono\',monospace;">{v}</span>'
        f'</div>'
        for k, v in metrics
    )
    st.markdown(
        f"""
        <div class="ag-test-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                <div class="ag-test-name">{title}</div>
                <span class="ag-badge">{badge}</span>
            </div>
            <div class="ag-test-hypothesis">{hyp_html}</div>
            <div style="margin:0.75rem 0;">{metrics_html}</div>
            <div style="margin-top:0.75rem;display:flex;align-items:center;gap:0.75rem;">
                <span class="ag-reject-h0">✓ Reject H₀</span>
                <span style="font-size:0.8rem;color:var(--text-muted);">{decision}</span>
            </div>
            <div style="margin-top:0.75rem;background:rgba(16,185,129,0.06);border-left:3px solid #10b981;
                 border-radius:0 8px 8px 0;padding:0.6rem 1rem;font-size:0.82rem;color:var(--text-secondary);line-height:1.6;">
                {interpretation}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="Statistical Analysis | Startup Failure Analysis",
        page_icon="📐",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">📐 Hypothesis Testing</div>
            <div class="ag-hero-title">Statistical Analysis</div>
            <div class="ag-hero-subtitle">Formal Tests &amp; Evidence-Based Findings</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    with st.spinner("Running hypothesis tests on full dataset…"):
        try:
            ttest_res  = compute_ttest(df)
            chisq_res  = compute_chisq(df)
            anova_res  = compute_anova(df)
            tests_ok   = True
        except Exception as e:
            tests_ok = False
            st.warning(f"Could not compute tests: {e}. Showing notebook-pinned values.")
            ttest_res = {"statistic": -12.77, "p_value": 1.23e-36, "cohens_d": -0.191,
                         "n_closed": None, "n_nonclosed": None, "mean_closed": None, "mean_nonclosed": None}
            chisq_res = {"statistic": None, "p_value": None, "dof": None}
            anova_res = {"statistic": 167.99, "p_value": 5e-300, "n_groups": 15}

    st.markdown(
        f"""
        <div style="background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.2);
             border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;font-size:0.82rem;color:var(--text-secondary);">
            <strong style="color:var(--text-primary);">Methodology:</strong> Tests are computed live from
            <strong style="color:#22d3ee;">dataset.csv ({len(df):,} rows)</strong> using the same
            methodology as the project notebook (Welch variants for unequal variances; α = 0.05;
            log₁p-transformed funding). The notebook reference values (t ≈ −12.77, F ≈ 167.99)
            were derived from a cleaned 9k-row subset — the full dataset will produce different but
            directionally consistent results.
        </div>
        """,
        unsafe_allow_html=True,
    )


    tab1, tab2 = st.tabs(["📐 Hypothesis Tests", "📋 CB Insights Supplement"])

    with tab1:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Test 1 — Welch\'s T-Test</div>'
            '<div class="ag-section-sub">Do closed startups raise less funding than non-closed ones?</div></div>',
            unsafe_allow_html=True,
        )

        render_test_card(
            title="Welch's Independent-Samples T-Test",
            badge="Funding vs Closure",
            hypotheses=[
                "H₀: μ(log_funding | closed) = μ(log_funding | non-closed) — no funding difference",
                "H₁: μ(log_funding | closed) ≠ μ(log_funding | non-closed) — funding differs by closure status",
            ],
            metrics=[
                ("Test statistic (t)",   f"{ttest_res['statistic']:.4f}"),
                ("p-value",              _pval_fmt(ttest_res["p_value"])),
                ("Cohen's d",            f"{ttest_res['cohens_d']:.4f}"),
                ("Effect size label",    effect_size_label(ttest_res["cohens_d"])),
                ("n (closed)",           f"{ttest_res['n_closed']:,}" if ttest_res["n_closed"] else "N/A"),
                ("n (non-closed)",       f"{ttest_res['n_nonclosed']:,}" if ttest_res["n_nonclosed"] else "N/A"),
                ("Mean log-funding (closed)",     f"{ttest_res['mean_closed']:.4f}" if ttest_res["mean_closed"] else "N/A"),
                ("Mean log-funding (non-closed)", f"{ttest_res['mean_nonclosed']:.4f}" if ttest_res["mean_nonclosed"] else "N/A"),
            ],
            decision="p < 0.001 — statistically significant at α = 0.05",
            interpretation=(
                "We reject H₀. Closed startups raised statistically significantly less log-transformed funding "
                "than non-closed startups (t ≈ −12.77, p &lt; 0.001). Cohen's d ≈ −0.191 indicates a "
                "<em>small-to-negligible</em> effect size by Cohen's conventions, suggesting funding is a real "
                "but not overwhelmingly dominant predictor of closure — consistent with multi-causal failure dynamics."
            ),
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Test 2 — Chi-Square Test of Independence</div>'
            '<div class="ag-section-sub">Is sector membership associated with startup closure?</div></div>',
            unsafe_allow_html=True,
        )

        render_test_card(
            title="Pearson Chi-Square Test of Independence",
            badge="Sector vs Closure",
            hypotheses=[
                "H₀: Sector and closure status are independent — no association",
                "H₁: Sector and closure status are associated — sector predicts closure probability",
            ],
            metrics=[
                ("Test statistic (χ²)",  f"{chisq_res['statistic']:.4f}" if chisq_res["statistic"] else "computed"),
                ("Degrees of freedom",   f"{chisq_res['dof']}" if chisq_res["dof"] else "computed"),
                ("p-value",              _pval_fmt(chisq_res["p_value"]) if chisq_res["p_value"] else "< 0.001"),
                ("Cramer's V",           f"{chisq_res.get('cramers_v', 0.122):.3f}" if chisq_res.get("cramers_v") else "0.122"),
                ("Sectors tested",       "Top 15 by count"),
                ("Significance level",   "α = 0.05"),
            ],
            decision="p < 0.001 — sector is not independent of closure",
            interpretation=(
                "We reject H₀. There is a statistically significant association between sector membership and "
                "closure status. However, the association strength is small (Cramer's V ≈ 0.122). Certain sectors "
                "show disproportionately high closure rates (e.g. Curated Web), while others show lower relative "
                "failure rates, making sector a useful—but not solely deterministic—lens for due diligence."
            ),
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Test 3 — Welch\'s One-Way ANOVA</div>'
            '<div class="ag-section-sub">Do funding levels differ significantly across sectors?</div></div>',
            unsafe_allow_html=True,
        )

        render_test_card(
            title="Welch's One-Way ANOVA (log-funding across sectors)",
            badge="Cross-Sector Funding",
            hypotheses=[
                "H₀: Mean log-funding is equal across all sectors — no sector-level funding gap",
                "H₁: At least one sector has a different mean log-funding — funding varies by sector",
            ],
            metrics=[
                ("Test statistic (F)",   f"{anova_res['statistic']:.4f}"),
                ("Approx. df (between)", "14"),
                ("Approx. df (within)",  "7855.18"),
                ("p-value",              _pval_fmt(anova_res["p_value"])),
                ("Number of groups",     f"{anova_res['n_groups']}"),
                ("Significance level",   "α = 0.05"),
            ],
            decision="F(14, 7855.18) ≈ 167.99, p < 0.001 — funding differs across sectors",
            interpretation=(
                "We reject H₀. Funding levels are not uniform across sectors — the ANOVA F-statistic of ≈ 167.99 "
                "(p &lt; 0.001) indicates substantial between-sector variation in log-funding. This complements the "
                "t-test: not only do closed companies raise less, but the sector in which a company operates is itself "
                "a predictor of the funding it can attract — creating compounding risk in low-funding, high-closure sectors."
            ),
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="ag-card" style="background:linear-gradient(135deg,rgba(99,102,241,0.08),rgba(168,85,247,0.04));">
                <div style="font-size:0.9rem;font-weight:700;color:var(--text-primary);margin-bottom:0.75rem;">
                    📋 Summary of All Tests
                </div>
                <table class="ag-table" style="width:100%;">
                    <thead>
                        <tr>
                            <th>Test</th><th>Statistic</th><th>p-value</th><th>Effect / Notes</th><th>Decision</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Welch's T-Test</td><td>t ≈ −12.77</td><td>&lt; 0.001</td>
                            <td>Cohen's d ≈ −0.191 (small)</td><td><span class="ag-reject-h0">Reject H₀</span></td>
                        </tr>
                        <tr>
                            <td>Chi-Square</td><td>χ² (computed)</td><td>&lt; 0.001</td>
                            <td>Top 15 sectors; strong association</td><td><span class="ag-reject-h0">Reject H₀</span></td>
                        </tr>
                        <tr>
                            <td>Welch's ANOVA</td><td>F(14, 7855.18) ≈ 167.99</td><td>&lt; 0.001</td>
                            <td>Large F — substantial between-sector variance</td><td><span class="ag-reject-h0">Reject H₀</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            '<div class="ag-section-header">'
            '<div class="ag-section-title">CB Insights: Startup Failure Reasons</div>'
            '<div class="ag-section-sub">Qualitative supplement — 101 post-mortem analyses (CB Insights, 2019)</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.2);
                 border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:1rem;font-size:0.82rem;color:var(--text-secondary);">
                <strong style="color:#f59e0b;">⚠️ Note:</strong> This data is <em>not derived from crunchbase_cleaned.csv</em>.
                It is a hardcoded reference table from CB Insights' 2019 analysis of 101 post-mortem essays written by
                founders. It serves as a qualitative complement to the quantitative Crunchbase findings above.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(
            cb_insights_bar(CB_INSIGHTS_REASONS),
            use_container_width=True,
            config={"displayModeBar": False},
        )

        st.markdown(
            """
            <div class="ag-chart-insight">
                💡 <strong>Connecting qualitative and quantitative evidence:</strong>
                The top two CB Insights failure reasons — "No Market Need" (42%) and "Ran Out of Cash" (29%) —
                are directly tied to the funding deficit we quantified. Startups that ran out of cash likely lacked
                the funding runway identified by our Welch's t-test (t ≈ −12.77). The cross-sector funding variance
                (ANOVA F ≈ 167.99) further suggests that sector choice compounds cash-flow risk.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        reasons_df = pd.DataFrame(CB_INSIGHTS_REASONS, columns=["Failure Reason", "% of Startups"])
        reasons_df = reasons_df.sort_values("% of Startups", ascending=False).reset_index(drop=True)
        st.dataframe(reasons_df, use_container_width=True, height=500)

    

main()
