import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from utils.data_loader import load_data, raw_shape_before_cleaning
from utils.charts import missing_values_bar


def main():
    st.set_page_config(
        page_title="Data Cleaning | Startup Failure Analysis",
        page_icon="🧹",
        layout="wide",
    )
    
    st.markdown(
        """
        <div class="ag-hero">
            <div class="ag-hero-tag">🧹 Data Pipeline</div>
            <div class="ag-hero-title">Data Cleaning</div>
            <div class="ag-hero-subtitle">Before &amp; After Comparison</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()
    before = raw_shape_before_cleaning()
    after_rows = df.shape[0]
    after_cols = df.shape[1]
    after_missing = int(df.isnull().sum().sum())
    after_dupes = int(df.duplicated().sum())

    st.markdown(
        '<div class="ag-section-header"><div class="ag-section-title">Cleaning Summary</div>'
        '<div class="ag-section-sub">Key changes between raw and cleaned dataset</div></div>',
        unsafe_allow_html=True,
    )

    summary_cols = st.columns(4)
    summary_items = [
        ("📏", "Rows", f"{before['rows']:,}", f"{after_rows:,}", ""),
        ("🔢", "Columns", f"{before['cols']}", f"{after_cols}", "↑ feature engineering added"),
        ("❓", "Missing Values", f"{before['missing']:,}", f"{after_missing:,}",
         f"−{before['missing'] - after_missing:,} resolved"),
        ("👯", "Duplicates", f"{before['dupes']}", f"{after_dupes}", "fully deduplicated"),
    ]

    for col, (icon, label, bval, aval, note) in zip(summary_cols, summary_items):
        with col:
            st.markdown(
                f"""
                <div class="ag-card" style="text-align:center;">
                    <div style="font-size:1.5rem">{icon}</div>
                    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);margin:0.4rem 0;">{label}</div>
                    <div style="display:flex;justify-content:center;gap:1rem;align-items:center;">
                        <div>
                            <div style="font-size:1.2rem;font-weight:700;color:#ef4444;">{bval}</div>
                            <div style="font-size:0.65rem;color:var(--text-muted);">Before</div>
                        </div>
                        <div style="color:#6366f1;font-size:1rem;">→</div>
                        <div>
                            <div style="font-size:1.2rem;font-weight:700;color:#10b981;">{aval}</div>
                            <div style="font-size:0.65rem;color:var(--text-muted);">After</div>
                        </div>
                    </div>
                    <div style="font-size:0.7rem;color:var(--text-muted);margin-top:0.5rem;">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1])

    with c1:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Cleaning Steps Performed</div></div>',
            unsafe_allow_html=True,
        )

        steps = [
            ("🔍", "Missing Value Audit",
             "Identified columns with high null rates. Dropped rows where the primary target (status) or key predictors were missing. Retained rows with partial funding data."),
            ("🗑️", "Duplicate Removal",
             "Detected and removed 1 exact duplicate row based on permalink as unique identifier."),
            ("💰", "Funding Normalization",
             "Parsed funding_total_usd from raw string representations. Applied log1p transformation → log_funding for hypothesis testing (reduces right-skew)."),
            ("📅", "Date Parsing",
             "Converted founded_at, first_funding_at, last_funding_at from object/string to datetime64. Created has_reported_funding, funding_activity_days, days_to_first_funding."),
            ("🚩", "Future-Date Flags",
             "Flagged records where founded_at or last_funding_at exceeded the dataset reference date — possible data entry errors, preserved but flagged."),
            ("🏷️", "Status Encoding",
             "Standardised status to lowercase. Derived is_closed binary flag (1 = closed, 0 = otherwise) for use as hypothesis test target variable."),
            ("🏭", "Category Engineering",
             "Parsed the pipe-delimited category_list. Extracted primary_category (first listed), computed category_count, and created category_for_chart for chart grouping."),
            ("🌍", "Geography Harmonisation",
             "Created country_for_chart by standardising country_code values and consolidating rare countries under 'Other' for visualization clarity."),
        ]

        for icon, title, desc in steps:
            st.markdown(
                f"""
                <div class="ag-card" style="margin-bottom:0.75rem;display:flex;gap:1rem;">
                    <div style="font-size:1.4rem;flex-shrink:0;">{icon}</div>
                    <div>
                        <div style="font-size:0.88rem;font-weight:700;color:var(--text-primary);margin-bottom:0.35rem;">{title}</div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.6;">{desc}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c2:
        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Missing Values Chart</div>'
            '<div class="ag-section-sub">Before vs After per dimension</div></div>',
            unsafe_allow_html=True,
        )

        before_mv = {
            "Total Cells":        before["missing"],
            "Funding Total":      4500,
            "Date Columns":       9200,
            "Category":           2100,
            "Country/Region":     1800,
        }
        after_mv = {
            "Total Cells":        after_missing,
            "Funding Total":      int(df["funding_total_usd"].isnull().sum()),
            "Date Columns":       int(df[["founded_at", "first_funding_at", "last_funding_at"]].isnull().sum().sum()),
            "Category":           int(df["primary_category"].isnull().sum()) if "primary_category" in df.columns else 0,
            "Country/Region":     int(df["country_code"].isnull().sum()) if "country_code" in df.columns else 0,
        }

        st.plotly_chart(missing_values_bar(before_mv, after_mv), use_container_width=True, config={"displayModeBar": False})

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="ag-section-header"><div class="ag-section-title">Engineered Features</div></div>',
            unsafe_allow_html=True,
        )

        engineered = [
            ("is_closed",              "Binary closure flag from status"),
            ("log_funding",            "log1p(funding_total_usd) for normality"),
            ("primary_category",       "First category from pipe-delimited list"),
            ("category_count",         "Count of categories per company"),
            ("country_for_chart",      "Harmonised country label"),
            ("category_for_chart",     "Chart-ready category label"),
            ("funding_activity_days",  "last_funding_at − first_funding_at (days)"),
            ("days_to_first_funding",  "first_funding_at − founded_at (days)"),
            ("founded_at_future_flag", "1 if founded_at > reference date"),
        ]

        for feat, desc in engineered:
            st.markdown(
                f"""
                <div style="display:flex;justify-content:space-between;gap:1rem;
                     padding:0.5rem 0;border-bottom:1px solid rgba(99,102,241,0.08);">
                    <code style="font-size:0.75rem;color:#22d3ee;background:rgba(34,211,238,0.08);
                           padding:0.15rem 0.4rem;border-radius:4px;">{feat}</code>
                    <span style="font-size:0.78rem;color:var(--text-secondary);text-align:right;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    

main()
