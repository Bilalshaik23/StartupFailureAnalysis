import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data, summary_stats, STATUS_PALETTE


def main():
    st.set_page_config(
        page_title="Interactive Dashboard | Startup Failure Analysis",
        page_icon="🎛️",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">🎛️ Explore the Data</div>
            <div class="ag-hero-title">Interactive Dashboard</div>
            <div class="ag-hero-subtitle">Filter, Drill Down &amp; Discover</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    with st.sidebar:
        st.markdown(
            '<div style="font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;'
            'color:#6366f1;padding:0.75rem 0 0.5rem;">🎛️ Dashboard Filters</div>',
            unsafe_allow_html=True,
        )

        statuses = sorted(df["status"].dropna().unique()) if "status" in df.columns else []
        selected_status = st.multiselect("Status", options=statuses, default=statuses)

        countries = sorted(df["country_for_chart"].dropna().unique()) if "country_for_chart" in df.columns else []
        top_countries = df["country_for_chart"].value_counts().head(30).index.tolist() if "country_for_chart" in df.columns else []
        selected_countries = st.multiselect("Country (top 30)", options=top_countries, default=[])

        sectors = sorted(df["primary_category"].dropna().unique()) if "primary_category" in df.columns else []
        top_sectors = df["primary_category"].value_counts().head(30).index.tolist() if "primary_category" in df.columns else []
        selected_sectors = st.multiselect("Sector (top 30)", options=top_sectors, default=[])

        if "funding_total_usd" in df.columns:
            max_fund = float(df["funding_total_usd"].quantile(0.99))
            fund_range = st.slider(
                "Funding Range (USD M)",
                min_value=0.0,
                max_value=round(max_fund / 1e6, 1),
                value=(0.0, round(max_fund / 1e6, 1)),
            )
        else:
            fund_range = (0.0, 1e9)

        if "funding_rounds" in df.columns:
            max_rounds = int(df["funding_rounds"].max())
            rounds_range = st.slider("Funding Rounds", min_value=0, max_value=max_rounds, value=(0, max_rounds))
        else:
            rounds_range = (0, 100)

        if "founded_at" in df.columns and df["founded_at"].notna().any():
            min_year = int(df["founded_at"].dt.year.min())
            max_year = int(df["founded_at"].dt.year.max())
            year_range = st.slider("Founded Year", min_value=min_year, max_value=max_year, value=(min_year, max_year))
        else:
            year_range = (1970, 2015)

    filtered = df.copy()
    if selected_status:
        filtered = filtered[filtered["status"].isin(selected_status)]
    if selected_countries:
        filtered = filtered[filtered["country_for_chart"].isin(selected_countries)]
    if selected_sectors:
        filtered = filtered[filtered["primary_category"].isin(selected_sectors)]
    if "funding_total_usd" in filtered.columns:
        filtered = filtered[
            (filtered["funding_total_usd"].fillna(0) >= fund_range[0] * 1e6) &
            (filtered["funding_total_usd"].fillna(0) <= fund_range[1] * 1e6)
        ]
    if "funding_rounds" in filtered.columns:
        filtered = filtered[
            (filtered["funding_rounds"].fillna(0) >= rounds_range[0]) &
            (filtered["funding_rounds"].fillna(0) <= rounds_range[1])
        ]
    if "founded_at" in filtered.columns:
        filtered = filtered[
            (filtered["founded_at"].dt.year.fillna(0) >= year_range[0]) &
            (filtered["founded_at"].dt.year.fillna(0) <= year_range[1])
        ]

    n_filtered = len(filtered)
    n_total    = len(df)

    st.markdown(
        f'<div style="font-size:0.82rem;color:var(--text-muted);margin-bottom:1rem;">'
        f'Showing <strong style="color:var(--text-primary);">{n_filtered:,}</strong> of '
        f'<strong style="color:var(--text-primary);">{n_total:,}</strong> companies matching current filters'
        f'</div>',
        unsafe_allow_html=True,
    )

    kpi_cols = st.columns(5)
    kpi_data = summary_stats(filtered)
    kpis = [
        ("📋", f"{kpi_data['total']:,}",     "Startups"),
        ("❌", f"{kpi_data['closed']:,}",    f"Closed ({kpi_data['closure_rate']}%)"),
        ("🤝", f"{kpi_data['acquired']:,}", "Acquired"),
        ("🚀", f"{kpi_data['ipo']:,}",      "IPO"),
        ("⚡", f"{kpi_data['operating']:,}", "Operating"),
    ]
    for col, (icon, val, label) in zip(kpi_cols, kpis):
        with col:
            st.markdown(
                f'<div class="ag-stat-card"><div style="font-size:1.1rem">{icon}</div>'
                f'<div class="ag-stat-value" style="font-size:1.5rem;">{val}</div>'
                f'<div class="ag-stat-label">{label}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#94a3b8", size=12),
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis=dict(gridcolor="rgba(99,102,241,0.08)"),
        yaxis=dict(gridcolor="rgba(99,102,241,0.08)"),
    )

    with c1:
        st.markdown('<div class="ag-section-header"><div class="ag-section-title">Status Distribution</div></div>', unsafe_allow_html=True)
        if n_filtered > 0 and "status" in filtered.columns:
            sc = filtered["status"].value_counts().reset_index()
            sc.columns = ["status", "count"]
            colors = [STATUS_PALETTE.get(s, "#6366f1") for s in sc["status"]]
            fig = go.Figure(go.Pie(
                labels=sc["status"].str.capitalize(), values=sc["count"], hole=0.55,
                marker=dict(colors=colors, line=dict(color="#0a0e1a", width=2)),
            ))
            fig.update_layout(**LAYOUT, title=dict(text="", font=dict(color="#f1f5f9")))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data matching current filters.")

    with c2:
        st.markdown('<div class="ag-section-header"><div class="ag-section-title">Funding by Status</div></div>', unsafe_allow_html=True)
        if n_filtered > 0 and "log_funding" in filtered.columns:
            fig2 = go.Figure()
            for status, color in STATUS_PALETTE.items():
                grp = filtered[filtered["status"] == status]["log_funding"].dropna()
                if len(grp) < 3:
                    continue
                fig2.add_trace(go.Box(y=grp, name=status.capitalize(), marker_color=color, line_color=color, boxmean=True))
            fig2.update_layout(**LAYOUT)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data matching current filters.")

    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="ag-section-header"><div class="ag-section-title">Top Sectors in Selection</div></div>', unsafe_allow_html=True)
        if n_filtered > 0 and "primary_category" in filtered.columns:
            top15 = filtered["primary_category"].value_counts().head(15).reset_index()
            top15.columns = ["sector", "count"]
            fig3 = px.bar(top15, x="count", y="sector", orientation="h",
                          color="count", color_continuous_scale=["#6366f1", "#a855f7", "#22d3ee"])
            fig3.update_layout(**LAYOUT, coloraxis_showscale=False)
            fig3.update_yaxes(autorange="reversed")
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with c4:
        st.markdown('<div class="ag-section-header"><div class="ag-section-title">Closure Rate by Sector</div></div>', unsafe_allow_html=True)
        if n_filtered > 0 and "primary_category" in filtered.columns and "is_closed" in filtered.columns:
            top_s = filtered["primary_category"].value_counts().head(15).index
            sub = filtered[filtered["primary_category"].isin(top_s)]
            rate = (
                sub.groupby("primary_category")["is_closed"]
                .mean().mul(100).round(1).sort_values().reset_index()
            )
            rate.columns = ["sector", "rate"]
            fig4 = px.bar(rate, x="rate", y="sector", orientation="h",
                          color="rate", color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
                          text="rate")
            fig4.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig4.update_layout(**LAYOUT, coloraxis_showscale=False)
            fig4.update_yaxes(autorange="reversed")
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="ag-section-header"><div class="ag-section-title">Founded Year Trend</div></div>', unsafe_allow_html=True)
    if n_filtered > 0 and "founded_at" in filtered.columns:
        yr = filtered.copy()
        yr["year"] = yr["founded_at"].dt.year
        yr = yr[yr["year"].between(1990, 2015)]
        trend = yr.groupby(["year", "status"]).size().reset_index(name="count")
        fig5 = px.line(trend, x="year", y="count", color="status",
                       color_discrete_map=STATUS_PALETTE,
                       markers=True)
        fig5.update_layout(**LAYOUT)
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

    

main()
