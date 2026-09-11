import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_data, summary_stats


def main():
    st.set_page_config(
        page_title="Dataset | Startup Failure Analysis",
        page_icon="🗂️",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">🗂️ Dataset Explorer</div>
            <div class="ag-hero-title">Dataset Overview</div>
            <div class="ag-hero-subtitle">Shape, Quality &amp; Distribution</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()
    stats = summary_stats(df)

    overview_cols = st.columns(5)
    overview_items = [
        ("📏", f"{df.shape[0]:,}", "Total Rows"),
        ("🔢", f"{df.shape[1]}", "Features"),
        ("❓", f"{df.isnull().sum().sum():,}", "Missing Values"),
        ("👯", f"{df.duplicated().sum()}", "Duplicate Rows"),
        ("🏷️", f"{df['status'].nunique()}" if "status" in df.columns else "N/A", "Unique Statuses"),
    ]
    for col, (icon, val, label) in zip(overview_cols, overview_items):
        with col:
            st.markdown(
                f'<div class="ag-stat-card"><div style="font-size:1.3rem">{icon}</div>'
                f'<div class="ag-stat-value">{val}</div>'
                f'<div class="ag-stat-label">{label}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Quick Stats", "🔍 Data Preview", "📋 Column Info", "📥 Download"])

    with tab1:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                '<div class="ag-section-header"><div class="ag-section-title">Status Distribution</div></div>',
                unsafe_allow_html=True,
            )
            if "status" in df.columns:
                sc = df["status"].value_counts()
                for s, cnt in sc.items():
                    pct = round(cnt / len(df) * 100, 1)
                    color_map = {"operating": "#10b981", "closed": "#ef4444", "acquired": "#a855f7", "ipo": "#f59e0b"}
                    color = color_map.get(s, "#6366f1")
                    st.markdown(
                        f"""
                        <div style="display:flex;justify-content:space-between;align-items:center;
                             padding:0.6rem 0;border-bottom:1px solid rgba(99,102,241,0.08);">
                            <span style="display:flex;align-items:center;gap:0.5rem;">
                                <span style="width:10px;height:10px;border-radius:50%;background:{color};display:inline-block;"></span>
                                <span style="color:var(--text-secondary);font-size:0.85rem;">{s.capitalize()}</span>
                            </span>
                            <span style="color:var(--text-primary);font-weight:600;font-size:0.85rem;">{cnt:,}
                                <span style="color:var(--text-muted);font-weight:400;">({pct}%)</span>
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        with c2:
            st.markdown(
                '<div class="ag-section-header"><div class="ag-section-title">Funding Stats (Reported)</div></div>',
                unsafe_allow_html=True,
            )
            if "funding_total_usd" in df.columns:
                funded = df[df["funding_total_usd"] > 0]["funding_total_usd"]
                funding_stats = [
                    ("Count with Funding",  f"{len(funded):,}"),
                    ("Median",              f"${funded.median()/1e6:.2f}M"),
                    ("Mean",                f"${funded.mean()/1e6:.2f}M"),
                    ("Std Dev",             f"${funded.std()/1e6:.2f}M"),
                    ("Min",                 f"${funded.min():,.0f}"),
                    ("Max",                 f"${funded.max()/1e9:.2f}B"),
                    ("75th Percentile",     f"${funded.quantile(0.75)/1e6:.2f}M"),
                ]
                for key, val in funding_stats:
                    st.markdown(
                        f"""
                        <div style="display:flex;justify-content:space-between;
                             padding:0.5rem 0;border-bottom:1px solid rgba(99,102,241,0.08);">
                            <span style="color:var(--text-muted);font-size:0.82rem;">{key}</span>
                            <span style="color:var(--text-primary);font-size:0.82rem;font-weight:500;">{val}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        with c3:
            st.markdown(
                '<div class="ag-section-header"><div class="ag-section-title">Coverage</div></div>',
                unsafe_allow_html=True,
            )
            coverage_items = [
                ("🌍 Countries",  f"{stats['n_countries']}"),
                ("🏭 Sectors",    f"{stats['n_sectors']}"),
                ("🏙️ Cities",     f"{df['city'].nunique():,}" if "city" in df.columns else "N/A"),
                ("📅 Date Range",
                 f"{df['founded_at'].dt.year.min():.0f}–{df['founded_at'].dt.year.max():.0f}"
                 if "founded_at" in df.columns and df["founded_at"].notna().any() else "N/A"),
                ("💰 Has Funding",
                 f"{int(df['has_reported_funding'].sum()):,}" if "has_reported_funding" in df.columns else "N/A"),
                ("🔄 Avg Rounds",  f"{df['funding_rounds'].mean():.1f}" if "funding_rounds" in df.columns else "N/A"),
                ("📊 Closure Rate", f"{stats['closure_rate']}%"),
            ]
            for key, val in coverage_items:
                st.markdown(
                    f"""
                    <div style="display:flex;justify-content:space-between;
                         padding:0.5rem 0;border-bottom:1px solid rgba(99,102,241,0.08);">
                        <span style="color:var(--text-muted);font-size:0.82rem;">{key}</span>
                        <span style="color:var(--text-primary);font-size:0.82rem;font-weight:500;">{val}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with tab2:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Dataset Preview</div>'
            '<div class="ag-section-sub">Use filters to explore specific rows</div></div>',
            unsafe_allow_html=True,
        )

        fcol1, fcol2, fcol3 = st.columns(3)
        with fcol1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=sorted(df["status"].dropna().unique()) if "status" in df.columns else [],
                default=[],
            )
        with fcol2:
            country_filter = st.multiselect(
                "Filter by Country",
                options=sorted(df["country_for_chart"].dropna().unique()[:50]) if "country_for_chart" in df.columns else [],
                default=[],
            )
        with fcol3:
            search_term = st.text_input("Search company name", placeholder="e.g. twitter")

        preview_df = df.copy()
        if status_filter:
            preview_df = preview_df[preview_df["status"].isin(status_filter)]
        if country_filter:
            preview_df = preview_df[preview_df["country_for_chart"].isin(country_filter)]
        if search_term and "name" in preview_df.columns:
            preview_df = preview_df[preview_df["name"].str.contains(search_term, case=False, na=False)]

        display_cols = ["name", "status", "primary_category", "funding_total_usd",
                        "funding_rounds", "country_for_chart", "founded_at"]
        available_display = [c for c in display_cols if c in preview_df.columns]

        st.markdown(
            f'<div style="color:var(--text-muted);font-size:0.8rem;margin-bottom:0.5rem;">'
            f'Showing {min(500, len(preview_df)):,} of {len(preview_df):,} matching rows</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            preview_df[available_display].head(500).reset_index(drop=True),
            use_container_width=True,
            height=400,
        )

    with tab3:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Column Reference</div>'
            '<div class="ag-section-sub">Data types, null counts, and sample values</div></div>',
            unsafe_allow_html=True,
        )

        col_info = []
        for col in df.columns:
            nulls = df[col].isnull().sum()
            col_info.append({
                "Column":      col,
                "Type":        str(df[col].dtype),
                "Non-Null":    f"{(len(df) - nulls):,}",
                "Null Count":  f"{nulls:,}",
                "Null %":      f"{nulls/len(df)*100:.1f}%",
                "Unique":      f"{df[col].nunique():,}",
                "Sample":      str(df[col].dropna().iloc[0]) if df[col].notna().any() else "—",
            })

        st.dataframe(pd.DataFrame(col_info), use_container_width=True, height=500)

    with tab4:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Download Dataset</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="ag-card" style="text-align:center;padding:2rem;">
                <div style="font-size:2rem;margin-bottom:1rem;">📥</div>
                <div style="font-size:1rem;font-weight:600;color:var(--text-primary);margin-bottom:0.5rem;">
                    Download Cleaned Dataset
                </div>
                <div style="font-size:0.82rem;color:var(--text-muted);margin-bottom:1.5rem;">
                    CSV format — all cleaning and feature engineering applied
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            label="⬇️ Download crunchbase_cleaned.csv",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="crunchbase_cleaned.csv",
            mime="text/csv",
        )

    

main()
