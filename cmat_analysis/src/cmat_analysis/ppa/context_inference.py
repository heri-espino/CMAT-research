"""Cluster-robust inference for observational academic-context models."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
import statsmodels.formula.api as smf

from .encouragement import _collapse_rare_categories


def clustered_academic_context_uptake_models(
    df: pd.DataFrame,
    *,
    outcome_col: str,
    context_cols: Sequence[str],
    period_col: str,
    cluster_col: str,
    major_col: str | None = None,
    professor_col: str | None = None,
    min_major_n: int = 30,
) -> pd.DataFrame:
    """Estimate academic-context associations with cluster-robust inference.

    Each continuous context variable is standardized and entered in a separate linear
    probability model. Standard errors are clustered at the level supplied by
    ``cluster_col``, which should match the level at which the focal context varies
    (for example professor-period classroom for classroom outcomes, or professor for
    historical instructor context).

    Parameters
    ----------
    df : pandas.DataFrame
        Student-level analytical data.
    outcome_col : str
        Binary CMAT-use outcome.
    context_cols : sequence of str
        Continuous context measures to test separately.
    period_col : str
        Academic-period control.
    cluster_col : str
        Column defining independent clusters for covariance estimation.
    major_col : str or None, optional
        Optional degree-programme control.
    professor_col : str or None, optional
        Optional instructor fixed effect for a second specification.
    min_major_n : int, default=30
        Minimum degree-programme size before smaller programmes are pooled.

    Returns
    -------
    pandas.DataFrame
        Standardized context coefficients with cluster-robust standard errors,
        confidence intervals, p-values, R-squared, and cluster counts.
    """
    required = {outcome_col, period_col, cluster_col, *context_cols}
    if major_col is not None:
        required.add(major_col)
    if professor_col is not None:
        required.add(professor_col)
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {sorted(missing)}")

    rows: list[dict[str, object]] = []
    for context_col in context_cols:
        subset = [outcome_col, period_col, cluster_col, context_col]
        if major_col is not None:
            subset.append(major_col)
        if professor_col is not None:
            subset.append(professor_col)
        d = df[subset].dropna().copy()
        d[outcome_col] = pd.to_numeric(d[outcome_col], errors="coerce")
        d[context_col] = pd.to_numeric(d[context_col], errors="coerce")
        d = d.dropna(subset=[outcome_col, context_col, cluster_col])
        if d.empty or float(d[context_col].std(ddof=0)) <= 0:
            continue
        if not set(d[outcome_col].unique()).issubset({0, 1}):
            raise ValueError(f"{outcome_col} must be binary 0/1.")
        if int(d[cluster_col].nunique()) < 2:
            raise ValueError(f"{cluster_col} must contain at least two clusters.")

        d["_CONTEXT_Z"] = (
            d[context_col] - d[context_col].mean()
        ) / d[context_col].std(ddof=0)
        rhs = ["_CONTEXT_Z", f"C({period_col})"]
        if major_col is not None:
            d["_MODEL_MAJOR"] = _collapse_rare_categories(d[major_col], min_major_n)
            rhs.append("C(_MODEL_MAJOR)")

        specifications = [("period_major", rhs.copy())]
        if professor_col is not None:
            specifications.append(
                ("period_major_professor_fe", rhs + [f"C({professor_col})"])
            )

        for specification, terms in specifications:
            fit = smf.ols(
                f"{outcome_col} ~ " + " + ".join(terms), data=d
            ).fit(
                cov_type="cluster",
                cov_kwds={"groups": d[cluster_col]},
            )
            estimate = float(fit.params["_CONTEXT_Z"])
            se = float(fit.bse["_CONTEXT_Z"])
            rows.append({
                "context_measure": context_col,
                "specification": specification,
                "n": int(fit.nobs),
                "clusters": int(d[cluster_col].nunique()),
                "cluster_col": cluster_col,
                "estimate_per_sd": estimate,
                "se_cluster": se,
                "ci_low": estimate - 1.96 * se,
                "ci_high": estimate + 1.96 * se,
                "p_value": float(fit.pvalues["_CONTEXT_Z"]),
                "r2": float(fit.rsquared),
                "note": (
                    "descriptive linear probability model with cluster-robust inference; "
                    "context is not a causal difficulty measure"
                ),
            })
    return pd.DataFrame(rows)
