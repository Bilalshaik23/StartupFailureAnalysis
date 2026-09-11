import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.data_loader import STATUS_PALETTE


LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#64748b", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="rgba(30,59,58,0.1)",
        borderwidth=1,
        font=dict(size=11),
    ),
    xaxis=dict(
        gridcolor="rgba(0,0,0,0.04)",
        zerolinecolor="rgba(0,0,0,0.08)",
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(0,0,0,0.04)",
        zerolinecolor="rgba(0,0,0,0.08)",
        tickfont=dict(size=11),
    ),
)

ACCENT_SEQ = ["#1e3b3a", "#3f6866", "#8b5cf6", "#10b981", "#ef4444", "#f59e0b", "#3b82f6"]


def _apply_layout(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(**LAYOUT_DEFAULTS, title=dict(text=title, font=dict(size=15, color="#0f172a", weight=700)))
    return fig


def status_pie(df: pd.DataFrame) -> go.Figure:
    counts = df["status"].value_counts().reset_index()
    counts.columns = ["status", "count"]
    colors = [STATUS_PALETTE.get(s, "#6366f1") for s in counts["status"]]
    fig = go.Figure(go.Pie(
        labels=counts["status"].str.capitalize(),
        values=counts["count"],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#0a0e1a", width=2)),
        textfont=dict(size=12),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    fig.update_layout(**LAYOUT_DEFAULTS, title=dict(text="Status Distribution", font=dict(size=15, color="#0f172a")))
    return fig


def funding_box_by_status(df: pd.DataFrame) -> go.Figure:
    sub = df[df["log_funding"].notna() & df["status"].notna()].copy()
    fig = go.Figure()
    for status, color in STATUS_PALETTE.items():
        grp = sub[sub["status"] == status]["log_funding"]
        if len(grp) < 5:
            continue
        fig.add_trace(go.Box(
            y=grp,
            name=status.capitalize(),
            marker_color=color,
            line_color=color,
            boxmean=True,
            hovertemplate=f"<b>{status.capitalize()}</b><br>Log Funding: %{{y:.2f}}<extra></extra>",
        ))
    return _apply_layout(fig, "Log Funding Distribution by Status (USD)")


def funding_rounds_box(df: pd.DataFrame) -> go.Figure:
    sub = df[df["funding_rounds"].notna() & df["status"].notna()].copy()
    fig = go.Figure()
    for status, color in STATUS_PALETTE.items():
        grp = sub[sub["status"] == status]["funding_rounds"]
        if len(grp) < 5:
            continue
        fig.add_trace(go.Box(
            y=grp,
            name=status.capitalize(),
            marker_color=color,
            line_color=color,
            boxmean=True,
            hovertemplate=f"<b>{status.capitalize()}</b><br>Rounds: %{{y}}<extra></extra>",
        ))
    return _apply_layout(fig, "Funding Rounds by Status")


def funding_histogram(df: pd.DataFrame) -> go.Figure:
    sub = df[df["log_funding"].notna() & df["is_closed"].notna()].copy()
    closed     = sub[sub["is_closed"] == 1]["log_funding"]
    non_closed = sub[sub["is_closed"] == 0]["log_funding"]
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=closed, name="Closed", marker_color="#ef4444", opacity=0.7,
                               nbinsx=50, hovertemplate="Log Funding: %{x:.2f}<br>Count: %{y}<extra></extra>"))
    fig.add_trace(go.Histogram(x=non_closed, name="Non-Closed", marker_color="#6366f1", opacity=0.7,
                               nbinsx=50, hovertemplate="Log Funding: %{x:.2f}<br>Count: %{y}<extra></extra>"))
    fig.update_layout(**LAYOUT_DEFAULTS,
                      title=dict(text="Log Funding Distribution: Closed vs Non-Closed", font=dict(size=15, color="#0f172a")),
                      barmode="overlay")
    return fig


def sector_bar(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    counts = (
        df["primary_category"].value_counts()
        .head(top_n)
        .reset_index()
    )
    counts.columns = ["sector", "count"]
    fig = px.bar(
        counts, x="count", y="sector", orientation="h",
        color="count",
        color_continuous_scale=["#6366f1", "#a855f7", "#22d3ee"],
        labels={"count": "Company Count", "sector": ""},
    )
    fig.update_layout(**LAYOUT_DEFAULTS,
                      title=dict(text=f"Top {top_n} Sectors by Company Count", font=dict(size=15, color="#0f172a")),
                      coloraxis_showscale=False)
    fig.update_yaxes(autorange="reversed")
    return fig


def country_bar(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    col = "country_for_chart" if "country_for_chart" in df.columns else "country_code"
    counts = df[col].value_counts().head(top_n).reset_index()
    counts.columns = ["country", "count"]
    fig = px.bar(
        counts, x="country", y="count",
        color="count",
        color_continuous_scale=["#6366f1", "#a855f7", "#22d3ee"],
        labels={"count": "Company Count", "country": ""},
    )
    fig.update_layout(**LAYOUT_DEFAULTS,
                      title=dict(text=f"Top {top_n} Countries by Startup Count", font=dict(size=15, color="#0f172a")),
                      coloraxis_showscale=False)
    return fig


def closure_by_sector(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    sub = df[df["primary_category"].notna() & df["is_closed"].notna()].copy()
    top_cats = sub["primary_category"].value_counts().head(top_n).index
    sub = sub[sub["primary_category"].isin(top_cats)]
    rate = (
        sub.groupby("primary_category")["is_closed"]
        .mean()
        .mul(100)
        .round(1)
        .sort_values(ascending=True)
        .reset_index()
    )
    rate.columns = ["sector", "closure_rate"]
    fig = px.bar(
        rate, x="closure_rate", y="sector", orientation="h",
        color="closure_rate",
        color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
        labels={"closure_rate": "Closure Rate (%)", "sector": ""},
        text="closure_rate",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(**LAYOUT_DEFAULTS,
                      title=dict(text="Closure Rate by Sector (%)", font=dict(size=15, color="#0f172a")),
                      coloraxis_showscale=False)
    return fig


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    num_cols = ["funding_total_usd", "funding_rounds", "is_closed",
                "category_count", "funding_activity_days", "days_to_first_funding"]
    available = [c for c in num_cols if c in df.columns]
    corr = df[available].corr(numeric_only=True).round(3)
    labels = [c.replace("_", " ").title() for c in corr.columns]
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=labels, y=labels,
        colorscale=[[0, "#6366f1"], [0.5, "#0a0e1a"], [1, "#22d3ee"]],
        zmid=0,
        text=corr.values.round(2),
        texttemplate="%{text}",
        hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>r = %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(**LAYOUT_DEFAULTS,
                      title=dict(text="Feature Correlation Heatmap", font=dict(size=15, color="#0f172a")))
    return fig


def company_age_histogram(df: pd.DataFrame) -> go.Figure:
    sub = df[df["founded_at"].notna() & df["status"].notna()].copy()
    sub["founded_year"] = sub["founded_at"].dt.year
    sub = sub[sub["founded_year"].between(1990, 2015)]
    fig = px.histogram(
        sub, x="founded_year", color="status",
        color_discrete_map=STATUS_PALETTE,
        nbins=26,
        barmode="stack",
        labels={"founded_year": "Founded Year", "count": "Count"},
    )
    fig.update_layout(**LAYOUT_DEFAULTS,
                      title=dict(text="Company Founding Year Distribution", font=dict(size=15, color="#0f172a")))
    return fig


def cb_insights_bar(reasons: list) -> go.Figure:
    reasons_sorted = sorted(reasons, key=lambda x: x[1])
    labels = [r[0] for r in reasons_sorted]
    values = [r[1] for r in reasons_sorted]

    colors = [
        "#ef4444" if v >= 30
        else "#f59e0b" if v >= 15
        else "#6366f1"
        for v in values
    ]

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors),
        text=[f"{v}%" for v in values],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x}% of startups cited this<extra></extra>",
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(text="CB Insights: Top 20 Startup Failure Reasons (101 Post-Mortems)", font=dict(size=15, color="#0f172a")),
    )
    fig.update_xaxes(title="% of startups citing this reason")
    return fig


def funding_violin(df: pd.DataFrame) -> go.Figure:
    sub = df[df["log_funding"].notna() & df["status"].notna()].copy()
    fig = go.Figure()
    for status, color in STATUS_PALETTE.items():
        grp = sub[sub["status"] == status]["log_funding"]
        if len(grp) < 5:
            continue
        fig.add_trace(go.Violin(
            y=grp, name=status.capitalize(),
            line_color=color, fillcolor=color + "33",
            box_visible=True, meanline_visible=True,
            hovertemplate=f"<b>{status.capitalize()}</b><br>Log Funding: %{{y:.2f}}<extra></extra>",
        ))
    return _apply_layout(fig, "Funding Distribution Violin Plot by Status")


def scatter_funding_rounds(df: pd.DataFrame) -> go.Figure:
    sub = df[df["funding_total_usd"].notna() & df["funding_rounds"].notna() & df["status"].notna()].copy()
    sub = sub[sub["funding_total_usd"] > 0].copy()
    sub["log_f"] = np.log10(sub["funding_total_usd"])
    sample = sub.sample(min(len(sub), 3000), random_state=42)
    fig = px.scatter(
        sample, x="funding_rounds", y="log_f",
        color="status",
        color_discrete_map=STATUS_PALETTE,
        opacity=0.6,
        labels={"funding_rounds": "Funding Rounds", "log_f": "Log₁₀ Funding (USD)"},
        hover_data=["name"] if "name" in sample.columns else None,
    )
    fig.update_layout(**LAYOUT_DEFAULTS,
                      title=dict(text="Funding Rounds vs Total Funding", font=dict(size=15, color="#0f172a")))
    return fig


def missing_values_bar(before: dict, after: dict) -> go.Figure:
    categories = list(before.keys())
    fig = go.Figure(data=[
        go.Bar(name="Before Cleaning", x=categories, y=list(before.values()),
               marker_color="#ef4444", text=list(before.values()), textposition="outside"),
        go.Bar(name="After Cleaning",  x=categories, y=list(after.values()),
               marker_color="#10b981", text=list(after.values()), textposition="outside"),
    ])
    fig.update_layout(**LAYOUT_DEFAULTS,
                      title=dict(text="Data Quality: Before vs After Cleaning", font=dict(size=15, color="#0f172a")),
                      barmode="group")
    return fig
