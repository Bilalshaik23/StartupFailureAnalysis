import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chi2_contingency, ttest_ind, f_oneway


NOTEBOOK_RESULTS = {
    "ttest": {
        "statistic": -12.77,
        "p_value":   1.23e-36,
        "cohens_d":  -0.191,
        "df":        None,
    },
    "chisq": {
        "statistic": None,
        "p_value":   None,
        "dof":       None,
    },
    "anova": {
        "statistic": 167.99,
        "p_value":   5e-300,
        "df_between": 14,
        "df_within":  7855.18,
    },
}

TTEST_TOLERANCE = 15.0
ANOVA_TOLERANCE = 500.0

USE_NOTEBOOK_FALLBACK = False


def compute_ttest(df: pd.DataFrame) -> dict:
    sub = df[df["log_funding"].notna() & df["is_closed"].notna()].copy()
    closed     = sub[sub["is_closed"] == 1]["log_funding"].values
    non_closed = sub[sub["is_closed"] == 0]["log_funding"].values

    t_stat, p_val = ttest_ind(closed, non_closed, equal_var=False)

    n1, n2 = len(closed), len(non_closed)
    pooled_std = np.sqrt(
        ((n1 - 1) * closed.std(ddof=1) ** 2 + (n2 - 1) * non_closed.std(ddof=1) ** 2)
        / (n1 + n2 - 2)
    )
    cohens_d = (closed.mean() - non_closed.mean()) / pooled_std

    expected_t = NOTEBOOK_RESULTS["ttest"]["statistic"]
    if abs(t_stat - expected_t) > TTEST_TOLERANCE:
        import warnings
        warnings.warn(
            f"T-test result ({t_stat:.3f}) differs from notebook value ({expected_t}). "
            "Dataset may differ from the notebook's subset."
        )

    return {
        "statistic": round(t_stat, 4),
        "p_value":   p_val,
        "cohens_d":  round(cohens_d, 4),
        "n_closed":  n1,
        "n_nonclosed": n2,
        "mean_closed":    round(closed.mean(), 4),
        "mean_nonclosed": round(non_closed.mean(), 4),
    }


def compute_chisq(df: pd.DataFrame) -> dict:
    sub = df[df["primary_category"].notna() & df["is_closed"].notna()].copy()
    top_cats = sub["primary_category"].value_counts().head(15).index
    sub = sub[sub["primary_category"].isin(top_cats)]

    ct = pd.crosstab(sub["primary_category"], sub["is_closed"])
    chi2, p, dof, expected = chi2_contingency(ct)

    n = ct.sum().sum()
    min_dim = min(ct.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0

    return {
        "statistic": round(chi2, 4),
        "p_value":   p,
        "dof":       dof,
        "cramers_v": round(cramers_v, 3),
        "contingency_table": ct,
    }


def compute_anova(df: pd.DataFrame) -> dict:
    sub = df[df["primary_category"].notna() & df["log_funding"].notna()].copy()
    top_cats = sub["primary_category"].value_counts().head(15).index
    sub = sub[sub["primary_category"].isin(top_cats)]

    groups = [
        grp["log_funding"].values
        for _, grp in sub.groupby("primary_category")
        if len(grp) > 5
    ]
    f_stat, p_val = f_oneway(*groups)

    expected_f = NOTEBOOK_RESULTS["anova"]["statistic"]
    if abs(f_stat - expected_f) > ANOVA_TOLERANCE:
        import warnings
        warnings.warn(
            f"ANOVA result ({f_stat:.3f}) differs from notebook value ({expected_f}). "
            "Dataset may differ from the notebook's subset."
        )

    return {
        "statistic": round(f_stat, 4),
        "p_value":   p_val,
        "n_groups":  len(groups),
    }


def effect_size_label(d: float) -> str:
    ad = abs(d)
    if ad < 0.2:
        return "negligible"
    if ad < 0.5:
        return "small"
    if ad < 0.8:
        return "medium"
    return "large"
