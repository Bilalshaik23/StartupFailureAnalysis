import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from utils.data_loader import load_data, summary_stats


def main():
    st.set_page_config(
        page_title="Key Insights | Startup Failure Analysis",
        page_icon="💡",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">💡 Evidence-Based Findings</div>
            <div class="ag-hero-title">Key Insights</div>
            <div class="ag-hero-subtitle">What the Data Actually Says</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()
    stats = summary_stats(df)

    closure_rate = stats["closure_rate"]

    top_sector_by_closure = "N/A"
    bot_sector_by_closure = "N/A"
    top_sector_rate = 0.0
    bot_sector_rate = 0.0

    if "primary_category" in df.columns and "is_closed" in df.columns:
        top_cats = df["primary_category"].value_counts().head(20).index
        sub = df[df["primary_category"].isin(top_cats)]
        rates = sub.groupby("primary_category")["is_closed"].mean().mul(100).round(1)
        top_sector_by_closure = rates.idxmax()
        bot_sector_by_closure = rates.idxmin()
        top_sector_rate = float(rates.max())
        bot_sector_rate = float(rates.min())

    usa_share = 0.0
    if "country_for_chart" in df.columns:
        usa_share = round(df["country_for_chart"].value_counts(normalize=True).get("USA", 0) * 100, 1)

    st.markdown(
        '<div class="ag-section-header"><div class="ag-section-title">Primary Statistical Findings</div>'
        '<div class="ag-section-sub">Derived from the hypothesis tests — all numbers from real data</div></div>',
        unsafe_allow_html=True,
    )

    primary_insights = [
        {
            "icon": "📉",
            "color": "#ef4444",
            "title": "Funding Predicts Closure (Weakly but Significantly)",
            "stat": "t ≈ −12.77, p < 0.001, Cohen's d ≈ −0.191",
            "body": (
                f"Closed startups raised statistically significantly less funding than non-closed ones "
                f"(Welch's t-test, p < 0.001). The effect size (Cohen's d ≈ −0.191) is small, meaning "
                f"funding is a <em>necessary but not sufficient</em> predictor — low-funded startups are "
                f"at elevated risk, but high funding alone does not guarantee survival."
            ),
        },
        {
            "icon": "🏭",
            "color": "#a855f7",
            "title": "Sector Membership Is Non-Randomly Associated with Closure",
            "stat": "χ² test, p < 0.001, Cramer's V = 0.122",
            "body": (
                f"The Chi-Square test confirms that sector and closure are not independent (p < 0.001), though the "
                f"association strength is small (Cramer's V = 0.122). "
                f"<strong>{top_sector_by_closure}</strong> shows the highest closure rate in the top-20 sectors "
                f"({top_sector_rate:.1f}%), while <strong>{bot_sector_by_closure}</strong> shows the lowest "
                f"({bot_sector_rate:.1f}%). This {top_sector_rate - bot_sector_rate:.1f}pp gap is actionable "
                f"intelligence for sector-focused investors."
            ),
        },
        {
            "icon": "📊",
            "color": "#6366f1",
            "title": "Large Cross-Sector Funding Variance",
            "stat": "F(14, 7855.18) ≈ 167.99, p < 0.001",
            "body": (
                "The one-way ANOVA rejects equal means across sectors at p < 0.001. The F-statistic of ≈ 167.99 "
                "signals that where a startup operates matters substantially for how much capital it can attract. "
                "Sectors that attract less funding face a double risk: lower capital runway and higher closure rates."
            ),
        },
        {
            "icon": "🌍",
            "color": "#22d3ee",
            "title": "Geographic Variation & US Concentration",
            "stat": "Russia (16.5%) vs China/India (~4.3%)",
            "body": (
                f"The USA accounts for approximately {usa_share}% of startups in the dataset, but closure rates "
                f"vary significantly by country. For instance, Russia saw a 16.5% closure rate compared to just "
                f"roughly 4.3% in China and India among major countries."
            ),
        },
        {
            "icon": "💸",
            "color": "#f59e0b",
            "title": "Overall Closure Rate & Funding Rounds",
            "stat": f"{closure_rate}% overall",
            "body": (
                f"Of {stats['total']:,} startups in the cleaned dataset, {stats['closed']:,} ({closure_rate}%) "
                f"are classified as closed. Notably, closure rates decreased as funding rounds increased, dropping "
                f"from 11.25% for one-round startups to 3.86% for startups with five or more rounds."
            ),
        },
        {
            "icon": "🎯",
            "color": "#10b981",
            "title": "CB Insights: Market Fit Outweighs Funding as Self-Reported Cause",
            "stat": "42% cite No Market Need",
            "body": (
                "While statistical tests confirm a funding deficit among closed startups, CB Insights' post-mortems "
                "show founders most commonly attribute failure to <strong>No Market Need</strong> (42%) rather than "
                "directly to cash. This suggests funding shortfalls are often a downstream symptom — companies "
                "that never achieve product-market fit stop attracting capital, creating the deficit our t-test detects."
            ),
        },
    ]

    for i, ins in enumerate(primary_insights):
        c1, c2 = st.columns([0.06, 0.94])
        with c1:
            st.markdown(
                f'<div style="font-size:2rem;padding-top:0.5rem;">{ins["icon"]}</div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div class="ag-card" style="border-left:4px solid {ins['color']};">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">
                        <div style="font-size:0.95rem;font-weight:700;color:var(--text-primary);">{ins['title']}</div>
                        <span class="ag-chip" style="flex-shrink:0;margin-left:1rem;">{ins['stat']}</span>
                    </div>
                    <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.7;">{ins['body']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="ag-section-header"><div class="ag-section-title">Quick Reference Metrics</div>'
        '<div class="ag-section-sub">Computed live from the cleaned dataset</div></div>',
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(4)
    metric_items = [
        ("Overall Closure Rate",    f"{closure_rate}%",         "of all startups"),
        ("Highest-Risk Sector",     top_sector_by_closure,      f"{top_sector_rate:.1f}% closure rate"),
        ("Lowest-Risk Sector",      bot_sector_by_closure,      f"{bot_sector_rate:.1f}% closure rate"),
        ("US Market Share",         f"{usa_share}%",            "of dataset"),
    ]
    for col, (label, val, sub) in zip(metric_cols, metric_items):
        with col:
            st.markdown(
                f'<div class="ag-stat-card">'
                f'<div class="ag-stat-value" style="font-size:1.4rem;">{val}</div>'
                f'<div class="ag-stat-label">{label}</div>'
                f'<div class="ag-stat-sub">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    

main()
