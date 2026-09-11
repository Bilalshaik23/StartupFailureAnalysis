import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path


RAW_PATH     = Path(__file__).parent.parent / "dataset.csv"
CLEANED_PATH = Path(__file__).parent.parent / "crunchbase_cleaned.csv"

STATUS_PALETTE = {
    "operating": "#1e3b3a",
    "closed":    "#ef4444",
    "acquired":  "#8b5cf6",
    "ipo":       "#10b981",
}

REFERENCE_DATE = pd.Timestamp("2015-01-01")


def _resolve_path() -> Path:
    if CLEANED_PATH.exists():
        return CLEANED_PATH
    if RAW_PATH.exists():
        return RAW_PATH
    return CLEANED_PATH


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "status" in df.columns:
        df["status"] = df["status"].str.lower().str.strip()
        df = df[df["status"].isin(["operating", "closed", "acquired", "ipo"])]

    for col in ["founded_at", "first_funding_at", "last_funding_at"]:
        if col in df.columns:
            df[f"{col}_raw"] = df[col]
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "funding_total_usd" in df.columns:
        df["funding_total_usd_raw"] = df["funding_total_usd"]
        df["funding_total_usd"] = pd.to_numeric(
            df["funding_total_usd"].astype(str).str.replace(",", "").str.strip(),
            errors="coerce",
        )
        df["funding_total_usd"] = df["funding_total_usd"].where(df["funding_total_usd"] >= 0)

    if "funding_rounds" in df.columns:
        df["funding_rounds"] = pd.to_numeric(df["funding_rounds"], errors="coerce")

    if "funding_total_usd" in df.columns:
        df["has_reported_funding"] = df["funding_total_usd"].notna() & (df["funding_total_usd"] > 0)
        df["log_funding"] = np.log1p(df["funding_total_usd"].fillna(0))
        df.loc[~df["has_reported_funding"], "log_funding"] = np.nan

    if "status" in df.columns:
        df["is_closed"] = (df["status"] == "closed").astype(int)

    if "founded_at" in df.columns:
        df["founded_at_future_flag"] = (df["founded_at"] > REFERENCE_DATE).astype(int)

    if "last_funding_at" in df.columns:
        df["last_funding_at_future_flag"] = (df["last_funding_at"] > REFERENCE_DATE).astype(int)

    if "first_funding_at" in df.columns and "last_funding_at" in df.columns:
        df["funding_activity_days"] = (
            df["last_funding_at"] - df["first_funding_at"]
        ).dt.days

    if "founded_at" in df.columns and "first_funding_at" in df.columns:
        df["days_to_first_funding"] = (
            df["first_funding_at"] - df["founded_at"]
        ).dt.days

    if "category_list" in df.columns:
        df["primary_category"] = (
            df["category_list"]
            .astype(str)
            .str.split("|")
            .str[0]
            .str.strip()
            .replace("nan", np.nan)
        )
        df["category_count"] = (
            df["category_list"]
            .astype(str)
            .str.split("|")
            .apply(lambda x: len([i for i in x if i.strip() and i.strip() != "nan"]))
        )
        top_cats = (
            df["primary_category"].value_counts().head(19).index.tolist()
        )
        df["category_for_chart"] = df["primary_category"].where(
            df["primary_category"].isin(top_cats), other="Other"
        )

    if "country_code" in df.columns:
        top_countries = df["country_code"].value_counts().head(19).index.tolist()
        df["country_for_chart"] = df["country_code"].where(
            df["country_code"].isin(top_countries), other="Other"
        )

    df = df.drop_duplicates()

    return df.reset_index(drop=True)


@st.cache_data(show_spinner="Loading and cleaning dataset…")
def load_data() -> pd.DataFrame:
    path = _resolve_path()
    if not path.exists():
        st.error(
            "Dataset not found. Place `dataset.csv` or `crunchbase_cleaned.csv` "
            "in the project root (`a:\\ST Failure\\`)."
        )
        st.stop()

    raw = pd.read_csv(path, low_memory=False)

    if "is_closed" in raw.columns and "primary_category" in raw.columns:
        df = raw.copy()
        for col in ["founded_at", "first_funding_at", "last_funding_at"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        if "funding_total_usd" in df.columns:
            df["funding_total_usd"] = pd.to_numeric(df["funding_total_usd"], errors="coerce")
        if "status" in df.columns:
            df["status"] = df["status"].str.lower().str.strip()
        if "log_funding" not in df.columns:
            df["log_funding"] = np.log1p(df["funding_total_usd"].fillna(0))
        return df

    return _clean(raw)


@st.cache_data(show_spinner=False)
def raw_shape_before_cleaning() -> dict:
    path = _resolve_path()
    if not path.exists():
        return {"rows": 0, "cols": 0, "missing": 0, "dupes": 0}
    raw = pd.read_csv(path, low_memory=False)
    return {
        "rows":    raw.shape[0],
        "cols":    raw.shape[1],
        "missing": int(raw.isnull().sum().sum()),
        "dupes":   int(raw.duplicated().sum()),
    }


@st.cache_data(show_spinner=False)
def summary_stats(df: pd.DataFrame) -> dict:
    total = len(df)
    if total == 0:
        return {k: 0 for k in ["total", "closed", "acquired", "ipo", "operating",
                                "avg_funding", "avg_rounds", "n_countries",
                                "n_sectors", "closure_rate"]}

    status_counts = df["status"].value_counts() if "status" in df.columns else {}

    funded_mask = df["has_reported_funding"] if "has_reported_funding" in df.columns else df["funding_total_usd"].notna()
    avg_funding = df.loc[funded_mask, "funding_total_usd"].mean() if "funding_total_usd" in df.columns else float("nan")
    avg_rounds  = df["funding_rounds"].mean() if "funding_rounds" in df.columns else float("nan")

    n_countries = (
        df["country_for_chart"].nunique()
        if "country_for_chart" in df.columns
        else df["country_code"].nunique() if "country_code" in df.columns
        else "N/A"
    )
    n_sectors = df["primary_category"].nunique() if "primary_category" in df.columns else "N/A"

    return {
        "total":        total,
        "closed":       int(status_counts.get("closed", 0)),
        "acquired":     int(status_counts.get("acquired", 0)),
        "ipo":          int(status_counts.get("ipo", 0)),
        "operating":    int(status_counts.get("operating", 0)),
        "avg_funding":  avg_funding,
        "avg_rounds":   avg_rounds,
        "n_countries":  n_countries,
        "n_sectors":    n_sectors,
        "closure_rate": round(status_counts.get("closed", 0) / total * 100, 1) if total else 0,
    }


CB_INSIGHTS_REASONS = [
    ("No Market Need",               42),
    ("Ran Out of Cash",              29),
    ("Not the Right Team",           23),
    ("Got Outcompeted",              19),
    ("Pricing / Cost Issues",        18),
    ("Poor Product",                 17),
    ("Lack of Business Model",       17),
    ("Poor Marketing",               14),
    ("Ignored Customers",            14),
    ("Product Mistimed",             13),
    ("Lost Focus",                   13),
    ("Disharmony on Team/Investors", 13),
    ("Pivot Gone Bad",               10),
    ("Lack of Passion",               9),
    ("Bad Location",                  9),
    ("No Financing/Investor Interest",8),
    ("Legal Challenges",              8),
    ("Didn't Use Network",            8),
    ("Burn Out",                      8),
    ("Failure to Pivot",              7),
]

