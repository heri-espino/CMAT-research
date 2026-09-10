from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm


GROUP_ORDER = ["0", "1-2", "3", "4+"]


def group_summary(df: pd.DataFrame, group_col: str, outcome_col: str) -> pd.DataFrame:
    rows = []
    for group, g in df.groupby(group_col, observed=True):
        x = g[outcome_col].dropna().to_numpy(float)
        if not len(x):
            continue
        se = np.std(x, ddof=1) / np.sqrt(len(x)) if len(x) > 1 else np.nan
        rows.append({
            "group": str(group),
            "n": int(len(x)),
            "mean": float(np.mean(x)),
            "sd": float(np.std(x, ddof=1)) if len(x) > 1 else np.nan,
            "median": float(np.median(x)),
            "q25": float(np.quantile(x, 0.25)),
            "q75": float(np.quantile(x, 0.75)),
            "ci95_low": float(np.mean(x) - 1.96 * se) if np.isfinite(se) else np.nan,
            "ci95_high": float(np.mean(x) + 1.96 * se) if np.isfinite(se) else np.nan,
        })
    order = {g: i for i, g in enumerate(GROUP_ORDER)}
    return pd.DataFrame(rows).sort_values("group", key=lambda s: s.map(lambda x: order.get(x, 99)))


def _cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    # O(n*m) can be large; use Mann-Whitney identity instead.
    u, _ = stats.mannwhitneyu(x, y, alternative="two-sided", method="auto")
    return float((2 * u) / (len(x) * len(y)) - 1)


def robust_two_group_tests(df: pd.DataFrame, treatment_col: str, outcome_col: str, seed: int = 42) -> pd.DataFrame:
    d = df[[treatment_col, outcome_col]].dropna()
    x = d.loc[d[treatment_col] == 1, outcome_col].to_numpy(float)
    y = d.loc[d[treatment_col] == 0, outcome_col].to_numpy(float)
    if len(x) < 2 or len(y) < 2:
        return pd.DataFrame([{"status": "insufficient_data"}])

    t_stat, p_t = stats.ttest_ind(x, y, equal_var=False)
    u, p_mw = stats.mannwhitneyu(x, y, alternative="two-sided", method="auto")
    bm, p_bm = stats.brunnermunzel(x, y, alternative="two-sided")
    cl = float(u / (len(x) * len(y)))  # P(X>Y)+.5 P(tie), oriented treated vs control
    r_rb = 2 * cl - 1
    delta = _cliffs_delta(x, y)

    rng = np.random.default_rng(seed)
    B = 2000
    med = np.empty(B)
    mean = np.empty(B)
    for b in range(B):
        xb = rng.choice(x, len(x), replace=True)
        yb = rng.choice(y, len(y), replace=True)
        med[b] = np.median(xb) - np.median(yb)
        mean[b] = np.mean(xb) - np.mean(yb)

    return pd.DataFrame([{
        "status": "ok",
        "n_treated": len(x),
        "n_control": len(y),
        "mean_treated": np.mean(x),
        "mean_control": np.mean(y),
        "mean_diff": np.mean(x) - np.mean(y),
        "mean_diff_ci95_low": np.quantile(mean, 0.025),
        "mean_diff_ci95_high": np.quantile(mean, 0.975),
        "welch_t": t_stat,
        "welch_p": p_t,
        "median_treated": np.median(x),
        "median_control": np.median(y),
        "median_diff": np.median(x) - np.median(y),
        "median_diff_ci95_low": np.quantile(med, 0.025),
        "median_diff_ci95_high": np.quantile(med, 0.975),
        "mann_whitney_u": u,
        "mann_whitney_p": p_mw,
        "brunner_munzel_stat": bm,
        "brunner_munzel_p": p_bm,
        "common_language_superiority": cl,
        "rank_biserial": r_rb,
        "cliffs_delta": delta,
    }])


def _coef_table(result, model_name: str, keep_terms: tuple[str, ...] | None = None) -> pd.DataFrame:
    rows = []
    ci = result.conf_int()
    for term in result.params.index:
        if keep_terms is not None and not any(k in term for k in keep_terms):
            continue
        rows.append({
            "model": model_name,
            "term": term,
            "estimate": float(result.params[term]),
            "std_error": float(result.bse[term]),
            "p_value": float(result.pvalues[term]),
            "ci95_low": float(ci.loc[term, 0]),
            "ci95_high": float(ci.loc[term, 1]),
            "n": int(result.nobs),
        })
    return pd.DataFrame(rows)


def primary_fixed_effect_models(df: pd.DataFrame, outcome_col: str, treatment_col: str) -> pd.DataFrame:
    d = df.dropna(subset=[outcome_col, treatment_col, "CLASSROOM_ID"]).copy()
    model1 = smf.ols(f"{outcome_col} ~ {treatment_col} + C(CLASSROOM_ID)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]}
    )
    tables = [_coef_table(model1, "classroom_FE", keep_terms=(treatment_col,))]

    # Career is a pre-course characteristic in the supplied academic file.
    d2 = d.dropna(subset=["CLAVECARRERA"]).copy()
    if len(d2):
        model2 = smf.ols(
            f"{outcome_col} ~ {treatment_col} + C(CLASSROOM_ID) + C(CLAVECARRERA)",
            data=d2,
        ).fit(cov_type="cluster", cov_kwds={"groups": d2["CLASSROOM_ID"]})
        tables.append(_coef_table(model2, "classroom_FE_plus_career", keep_terms=(treatment_col,)))
    return pd.concat(tables, ignore_index=True)


def dose_group_fixed_effect_model(df: pd.DataFrame, outcome_col: str, group_col: str) -> pd.DataFrame:
    d = df.dropna(subset=[outcome_col, group_col, "CLASSROOM_ID"]).copy()
    d[group_col] = pd.Categorical(d[group_col], categories=GROUP_ORDER, ordered=True)
    model = smf.ols(
        f"{outcome_col} ~ C({group_col}, Treatment(reference='0')) + C(CLASSROOM_ID)",
        data=d,
    ).fit(cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]})
    return _coef_table(model, "dose_groups_classroom_FE", keep_terms=(f"C({group_col}",))


def secondary_pass_model(df: pd.DataFrame, treatment_col: str) -> pd.DataFrame:
    """Secondary pass/fail sensitivity using a linear probability model.

    The primary paper outcome is continuous performance. For the secondary
    binary outcome we favor a stable classroom-fixed-effect LPM with clustered
    standard errors over a high-dimensional fixed-effect logit, which can suffer
    separation/undefined covariance in small professor-period cells.
    """
    d = df.dropna(subset=["PASS", treatment_col, "CLASSROOM_ID", "CLAVECARRERA"]).copy()
    if d["PASS"].nunique() < 2:
        return pd.DataFrame([{"model": "pass_LPM_classroom_FE", "status": "single_outcome_level"}])
    model = smf.ols(
        f"PASS ~ {treatment_col} + C(CLASSROOM_ID) + C(CLAVECARRERA)", data=d
    ).fit(cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]})
    tab = _coef_table(model, "pass_LPM_classroom_FE_plus_career", keep_terms=(treatment_col,))
    tab["interpretation"] = "absolute probability-point difference; secondary outcome"
    return tab

def visit_distribution(df: pd.DataFrame, visits_col: str, course_label: str, max_exact: int = 15) -> pd.DataFrame:
    v = df[visits_col].dropna().astype(int)
    rows = []
    n = len(v)
    for k in range(0, max_exact + 1):
        rows.append({
            "course": course_label,
            "visits": k,
            "n": int((v == k).sum()),
            "proportion": float((v == k).mean()) if n else np.nan,
            "tail_proportion_ge_k": float((v >= k).mean()) if n else np.nan,
        })
    rows.append({
        "course": course_label,
        "visits": f">{max_exact}",
        "n": int((v > max_exact).sum()),
        "proportion": float((v > max_exact).mean()) if n else np.nan,
        "tail_proportion_ge_k": np.nan,
    })
    return pd.DataFrame(rows)


def continuation_curve(df: pd.DataFrame, visits_col: str, course_label: str, max_k: int = 10) -> pd.DataFrame:
    v = df[visits_col].dropna().astype(int).to_numpy()
    rows = []
    for k in range(0, max_k + 1):
        denom = np.sum(v >= k)
        num = np.sum(v >= k + 1)
        p = num / denom if denom else np.nan
        se = math.sqrt(p * (1 - p) / denom) if denom and np.isfinite(p) else np.nan
        rows.append({
            "course": course_label,
            "k": k,
            "n_at_risk": int(denom),
            "continuation_probability": float(p) if np.isfinite(p) else np.nan,
            "ci95_low": max(0.0, p - 1.96 * se) if np.isfinite(se) else np.nan,
            "ci95_high": min(1.0, p + 1.96 * se) if np.isfinite(se) else np.nan,
        })
    return pd.DataFrame(rows)


def bunching_metrics(df: pd.DataFrame, visits_col: str, threshold: int, course_label: str) -> pd.DataFrame:
    v = df[visits_col].dropna().astype(int)
    p_t = float((v == threshold).mean())
    p_l = float((v == threshold - 1).mean())
    p_r = float((v == threshold + 1).mean())
    local_expected = (p_l + p_r) / 2
    return pd.DataFrame([{
        "course": course_label,
        "threshold": threshold,
        "n": len(v),
        "p_exact_threshold": p_t,
        "p_threshold_minus_1": p_l,
        "p_threshold_plus_1": p_r,
        "local_bunching_ratio": p_t / local_expected if local_expected > 0 else np.nan,
        "share_gt_threshold": float((v > threshold).mean()),
        "share_any_visit": float((v > 0).mean()),
        "mean_visits": float(v.mean()),
        "median_visits": float(v.median()),
    }])


def longitudinal_summary(longitudinal: pd.DataFrame, *, mu_group_col: str, calc_visits_col: str, coverage_col: str) -> pd.DataFrame:
    d = longitudinal.loc[longitudinal[coverage_col]].copy()
    rows = []
    for group, g in d.groupby(mu_group_col, observed=True):
        v = g[calc_visits_col].astype(int)
        rows.append({
            "mu_visit_group": group,
            "n": len(g),
            "any_calc_visit_proportion": float((v > 0).mean()),
            "mean_calc_visits": float(v.mean()),
            "median_calc_visits": float(v.median()),
            "q75_calc_visits": float(v.quantile(0.75)),
        })
    order = {g: i for i, g in enumerate(GROUP_ORDER)}
    return pd.DataFrame(rows).sort_values("mu_visit_group", key=lambda s: s.map(lambda x: order.get(x, 99)))



def temporal_regularity_performance_models(
    df: pd.DataFrame,
    *,
    outcome_col: str,
    visits_col: str,
    regularity_col: str = "REGULARITY_MONTHLY_4",
    min_visits: int = 3,
) -> pd.DataFrame:
    """RQ2b: regularity-performance association conditional on visit intensity.

    Primary RQ2b specification is restricted to students with >=3 visits and a
    numeric final grade (the caller selects the complete-case outcome).  This
    avoids mechanically giving withdrawal cases less time in which to spread
    visits. Visit intensity is flexibly controlled using capped exact-count
    categories (3,4,5,6,7,8+), alongside professor-period fixed effects and
    career, with clustered standard errors by professor-period.
    """
    req = [outcome_col, visits_col, regularity_col, "CLASSROOM_ID", "CLAVECARRERA"]
    d = df.dropna(subset=req).copy()
    d = d.loc[d[visits_col] >= int(min_visits)].copy()
    if len(d) < 30 or d[regularity_col].nunique() < 2:
        return pd.DataFrame([{"model": "temporal_regularity", "status": "insufficient_data", "n": len(d)}])
    d["VISITS_CAPPED_8"] = d[visits_col].clip(upper=8).astype(int)
    model = smf.ols(
        f"{outcome_col} ~ {regularity_col} + C(VISITS_CAPPED_8) + C(CLASSROOM_ID) + C(CLAVECARRERA)",
        data=d,
    ).fit(cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]})
    tab = _coef_table(model, "regularity_ge3_classroom_FE_plus_career", keep_terms=(regularity_col,))
    tab["population"] = f"students with {visits_col}>={min_visits}"
    tab["visit_intensity_control"] = "categorical exact counts 3-7; 8+ capped"
    return tab


def exact_visit_count_regularity_summary(
    df: pd.DataFrame,
    *,
    visits_col: str,
    outcome_col: str,
    exact_visits: int = 3,
) -> pd.DataFrame:
    """Descriptive regularity-performance comparison at exactly V=3."""
    d = df.loc[df[visits_col] == int(exact_visits)].dropna(subset=[outcome_col, "ACTIVE_CALENDAR_MONTHS"]).copy()
    if d.empty:
        return pd.DataFrame()
    rows = []
    for months, g in d.groupby("ACTIVE_CALENDAR_MONTHS", observed=True):
        x = g[outcome_col].dropna().to_numpy(float)
        if not len(x):
            continue
        se = np.std(x, ddof=1) / np.sqrt(len(x)) if len(x) > 1 else np.nan
        rows.append({
            "exact_visits": int(exact_visits),
            "active_calendar_months": int(months),
            "n": int(len(x)),
            "mean_z": float(np.mean(x)),
            "median_z": float(np.median(x)),
            "ci95_low": float(np.mean(x)-1.96*se) if np.isfinite(se) else np.nan,
            "ci95_high": float(np.mean(x)+1.96*se) if np.isfinite(se) else np.nan,
        })
    return pd.DataFrame(rows).sort_values("active_calendar_months")
