"""Reusable methodology diagnostics for visit-dose and subgroup analyses.

The functions in this module originated in the methodology report but implement
scientific comparisons that are reusable across CMAT analyses. The architectural
move changes import paths only; statistical formulas, cohort definitions,
thresholds, and estimands are unchanged.

Notes
-----
These procedures analyze observational service-use data. Unless an individual
function documents an identifying design, reported associations must not be
interpreted as causal effects.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from scipy.stats import studentized_range
from statsmodels.stats.multitest import multipletests

from cmat_analysis.cohorts import attach_visits
from cmat_analysis.measures import add_primary_outcomes


EXACT_GROUP_ORDER = ["0", "1", "2", "3", "4+"]


def exact_visit_group(v: int | float) -> str:
    x = int(v)
    if x <= 0:
        return "0"
    if x == 1:
        return "1"
    if x == 2:
        return "2"
    if x == 3:
        return "3"
    return "4+"


def add_exact_visit_group(df: pd.DataFrame, visits_col: str = "VISITS_CMAT_PERIOD") -> pd.DataFrame:
    d = df.copy()
    d["EXACT_VISIT_GROUP_0_1_2_3_4P"] = pd.Categorical(
        d[visits_col].map(exact_visit_group), categories=EXACT_GROUP_ORDER, ordered=True
    )
    return d


def exact_visit_group_summary(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    population: str,
) -> pd.DataFrame:
    d = add_exact_visit_group(df, visits_col).dropna(subset=[outcome_col]).copy()
    rows = []
    for group in EXACT_GROUP_ORDER:
        g = d.loc[d["EXACT_VISIT_GROUP_0_1_2_3_4P"] == group, outcome_col].dropna().astype(float)
        n = len(g)
        mean = float(g.mean()) if n else np.nan
        sd = float(g.std(ddof=1)) if n > 1 else np.nan
        se = sd / math.sqrt(n) if n > 1 else np.nan
        rows.append({
            "population": population,
            "group": group,
            "n": n,
            "mean_z": mean,
            "sd_z": sd,
            "se_z": se,
            "ci95_low": mean - 1.96 * se if np.isfinite(se) else np.nan,
            "ci95_high": mean + 1.96 * se if np.isfinite(se) else np.nan,
        })
    return pd.DataFrame(rows)


def exact_visit_count_summary(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    population: str,
    max_visits: int = 12,
) -> pd.DataFrame:
    """Descriptive outcome summary for each exact visit count from 0 to max_visits."""
    d = df.dropna(subset=[visits_col, outcome_col]).copy()
    d = d.loc[d[visits_col].between(0, max_visits)].copy()
    rows = []
    for v in range(0, max_visits + 1):
        x = d.loc[d[visits_col] == v, outcome_col].dropna().astype(float)
        n = len(x)
        mean = float(x.mean()) if n else np.nan
        sd = float(x.std(ddof=1)) if n > 1 else np.nan
        se = sd / math.sqrt(n) if n > 1 else np.nan
        rows.append({
            "population": population,
            "visits_exact": v,
            "n": n,
            "mean_z": mean,
            "sd_z": sd,
            "se_z": se,
            "ci95_low": mean - 1.96 * se if np.isfinite(se) else np.nan,
            "ci95_high": mean + 1.96 * se if np.isfinite(se) else np.nan,
        })
    return pd.DataFrame(rows)


def exact_visit_count_trend_diagnostics(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    population: str,
    max_visits: int = 12,
    stable_max_visits: int = 7,
) -> pd.DataFrame:
    """Student-level monotonic/linear diagnostics over exact positive counts."""
    d = df.dropna(subset=[visits_col, outcome_col, "CLASSROOM_ID"]).copy()
    rows = []
    for label, upper in [("full_1_to_12", max_visits), ("stable_1_to_7", stable_max_visits)]:
        g = d.loc[d[visits_col].between(1, upper)].copy()
        if len(g) < 3:
            continue
        rho, p_rho = stats.spearmanr(g[visits_col], g[outcome_col])
        model = smf.ols(f"{outcome_col} ~ {visits_col}", data=g).fit(
            cov_type="cluster", cov_kwds={"groups": g["CLASSROOM_ID"]}
        )
        rows.append({
            "population": population,
            "specification": label,
            "visit_min": 1,
            "visit_max": upper,
            "n_students": int(len(g)),
            "n_classrooms": int(g["CLASSROOM_ID"].nunique()),
            "spearman_rho": float(rho),
            "spearman_p": float(p_rho),
            "linear_slope_z_per_visit": float(model.params[visits_col]),
            "cluster_robust_se": float(model.bse[visits_col]),
            "linear_p": float(model.pvalues[visits_col]),
            "r2_ols_point_estimate": float(model.rsquared),
            "interpretation": "descriptive trend only; no causal dose-response identification",
        })
    return pd.DataFrame(rows)


def welch_anova_exact_groups(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    population: str,
) -> pd.DataFrame:
    """Welch one-way ANOVA plus Brown--Forsythe variance diagnostic."""
    d = add_exact_visit_group(df, visits_col).dropna(subset=[outcome_col]).copy()
    groups = []
    for label in EXACT_GROUP_ORDER:
        x = d.loc[d["EXACT_VISIT_GROUP_0_1_2_3_4P"] == label, outcome_col].dropna().to_numpy(float)
        if len(x) >= 2 and np.var(x, ddof=1) > 0:
            groups.append((label, x))
    k = len(groups)
    if k < 2:
        return pd.DataFrame([{"population": population, "status": "insufficient_groups"}])
    n = np.array([len(x) for _, x in groups], dtype=float)
    means = np.array([np.mean(x) for _, x in groups], dtype=float)
    vars_ = np.array([np.var(x, ddof=1) for _, x in groups], dtype=float)
    w = n / vars_
    W = w.sum()
    xw = float(np.sum(w * means) / W)
    numerator = float(np.sum(w * (means - xw) ** 2) / (k - 1))
    term = float(np.sum(((1 - w / W) ** 2) / (n - 1)))
    correction = 1 + (2 * (k - 2) / (k**2 - 1)) * term
    F = numerator / correction
    df1 = k - 1
    df2 = (k**2 - 1) / (3 * term) if term > 0 else np.inf
    p = float(stats.f.sf(F, df1, df2))
    bf_stat, bf_p = stats.levene(*[x for _, x in groups], center="median")
    return pd.DataFrame([{
        "population": population,
        "k_groups": k,
        "F_welch": F,
        "df_num": df1,
        "df_denom": df2,
        "p_value": p,
        "brown_forsythe_F": float(bf_stat),
        "brown_forsythe_p": float(bf_p),
    }])


def games_howell_exact_groups(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    population: str,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """All pairwise Games--Howell contrasts for 0,1,2,3,4+ visit groups."""
    d = add_exact_visit_group(df, visits_col).dropna(subset=[outcome_col]).copy()
    stats_by = {}
    for label in EXACT_GROUP_ORDER:
        x = d.loc[d["EXACT_VISIT_GROUP_0_1_2_3_4P"] == label, outcome_col].dropna().to_numpy(float)
        if len(x) >= 2:
            stats_by[label] = (len(x), float(np.mean(x)), float(np.var(x, ddof=1)))
    k = len(stats_by)
    rows = []
    for i, g1 in enumerate(EXACT_GROUP_ORDER):
        if g1 not in stats_by:
            continue
        for g2 in EXACT_GROUP_ORDER[i + 1:]:
            if g2 not in stats_by:
                continue
            n1, m1, v1 = stats_by[g1]
            n2, m2, v2 = stats_by[g2]
            a = v1 / n1
            b = v2 / n2
            se_mean_diff = math.sqrt(a + b)
            gh_se = math.sqrt(0.5 * (a + b))
            df = (a + b) ** 2 / (a * a / (n1 - 1) + b * b / (n2 - 1))
            diff = m1 - m2
            q = abs(diff) / gh_se if gh_se > 0 else np.nan
            p = float(studentized_range.sf(q, k, df)) if np.isfinite(q) else np.nan
            qcrit = float(studentized_range.ppf(1 - alpha, k, df))
            half = qcrit * gh_se
            t = diff / se_mean_diff if se_mean_diff > 0 else np.nan
            p_welch = float(2 * stats.t.sf(abs(t), df)) if np.isfinite(t) else np.nan
            rows.append({
                "population": population,
                "group1": g1,
                "group2": g2,
                "n1": n1,
                "n2": n2,
                "mean1": m1,
                "mean2": m2,
                "mean_diff_group1_minus_group2": diff,
                "games_howell_ci95_low": diff - half,
                "games_howell_ci95_high": diff + half,
                "games_howell_q": q,
                "games_howell_df": df,
                "games_howell_p": p,
                "welch_t_reference": t,
                "welch_p_reference": p_welch,
            })
    return pd.DataFrame(rows)


def fixed_effect_pairwise_exact_groups(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    population: str,
    include_career: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """All pairwise adjusted contrasts from one additive classroom-FE model."""
    d = add_exact_visit_group(df, visits_col).dropna(
        subset=[outcome_col, "EXACT_VISIT_GROUP_0_1_2_3_4P", "CLASSROOM_ID"]
    ).copy()
    if include_career:
        d = d.dropna(subset=["CLAVECARRERA"])
    group_term = "C(EXACT_VISIT_GROUP_0_1_2_3_4P, Treatment(reference='0'))"
    formula = f"{outcome_col} ~ {group_term} + C(CLASSROOM_ID)"
    if include_career:
        formula += " + C(CLAVECARRERA)"
    model = smf.ols(formula, data=d).fit(cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]})

    names = list(model.params.index)
    def coef_name(group: str) -> str | None:
        if group == "0":
            return None
        prefix = f"{group_term}[T.{group}]"
        return prefix if prefix in names else None

    rows = []
    R_list = []
    labels = []
    for i, g1 in enumerate(EXACT_GROUP_ORDER):
        for g2 in EXACT_GROUP_ORDER[i + 1:]:
            R = np.zeros(len(names), dtype=float)
            n1 = coef_name(g1)
            n2 = coef_name(g2)
            if n1 is not None:
                R[names.index(n1)] += 1.0
            if n2 is not None:
                R[names.index(n2)] -= 1.0
            R_list.append(R)
            labels.append((g1, g2))
    raw_ps = []
    tmp = []
    for (g1, g2), R in zip(labels, R_list):
        test = model.t_test(R)
        est = float(np.asarray(test.effect).reshape(-1)[0])
        se = float(np.asarray(test.sd).reshape(-1)[0])
        p = float(np.asarray(test.pvalue).reshape(-1)[0])
        ci = np.asarray(test.conf_int(alpha=0.05)).reshape(-1, 2)[0]
        raw_ps.append(p)
        tmp.append((g1, g2, est, se, p, float(ci[0]), float(ci[1])))
    holm = multipletests(raw_ps, alpha=0.05, method="holm") if raw_ps else ([], [], [], [])
    for j, vals in enumerate(tmp):
        g1, g2, est, se, p, lo, hi = vals
        rows.append({
            "population": population,
            "model": "classroom_FE_plus_official_career" if include_career else "classroom_FE",
            "group1": g1,
            "group2": g2,
            "adjusted_mean_difference_group1_minus_group2": est,
            "cluster_robust_se": se,
            "ci95_low": lo,
            "ci95_high": hi,
            "p_raw": p,
            "p_holm_10_pairwise": float(holm[1][j]),
            "reject_holm_0_05": bool(holm[0][j]),
            "n": int(model.nobs),
            "n_classrooms": int(d["CLASSROOM_ID"].nunique()),
        })
    model_info = pd.DataFrame([{
        "population": population,
        "formula": formula,
        "n": int(model.nobs),
        "n_classrooms": int(d["CLASSROOM_ID"].nunique()),
        "n_careers": int(d["CLAVECARRERA"].nunique()) if include_career else np.nan,
        "covariance": "cluster-robust by CLASSROOM_ID",
        "multiple_testing": "Holm adjustment across 10 pre-specified pairwise visit-group contrasts",
    }])
    return pd.DataFrame(rows), model_info


def _coverage_set(data) -> set[tuple[int, str]]:
    c = data.data_quality["coverage"]
    return set(zip(c["YEAR"].astype(int), c["SESSION"]))


def build_all_math_attempts_with_outcomes(data, config) -> pd.DataFrame:
    """Build all eligible observed math-course attempts in CMAT-covered periods."""
    d = data.academics.loc[data.academics["GRADE_CLASS"].isin(["numeric", "adverse"])].copy()
    cov = _coverage_set(data)
    d = d.loc[[(int(y), s) in cov for y, s in zip(d["YEAR"], d["SESSION"])]].copy()
    d = attach_visits(d, data.advisories, threshold=config.ppa_threshold)
    d["CLASSROOM_ID"] = (
        d["CLAVEPROFESOR"].astype(str)
        + "|" + d["SUBJECT_CODE"].astype(str)
        + "|" + d["YEAR"].astype(str)
        + "|" + d["SESSION"].astype(str)
    )
    return add_primary_outcomes(d, config)


def career_summary(
    df: pd.DataFrame,
    *,
    population: str,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    min_n: int = 30,
) -> pd.DataFrame:
    d = df.dropna(subset=["CLAVECARRERA", visits_col, outcome_col]).copy()
    out = (
        d.groupby("CLAVECARRERA", observed=True)
        .agg(
            n=("STUDENT_ID", "size"),
            unique_students=("STUDENT_ID", "nunique"),
            any_visit_rate=(visits_col, lambda x: float((pd.Series(x) > 0).mean())),
            mean_visits=(visits_col, "mean"),
            mean_z=(outcome_col, "mean"),
            sd_z=(outcome_col, "std"),
        )
        .reset_index()
    )
    out.insert(0, "population", population)
    out["included_n_ge_min"] = out["n"] >= int(min_n)
    out["min_n_rule"] = int(min_n)
    return out.sort_values(["included_n_ge_min", "n", "CLAVECARRERA"], ascending=[False, False, True])


def career_ecological_association(summary: pd.DataFrame) -> pd.DataFrame:
    """Descriptive career-level association between CMAT use rate and mean Z."""
    rows = []
    for population, g in summary.groupby("population", observed=True):
        d = g.loc[g["included_n_ge_min"]].dropna(subset=["any_visit_rate", "mean_z", "n"]).copy()
        if len(d) < 3:
            continue
        pear = stats.pearsonr(d["any_visit_rate"], d["mean_z"])
        spear = stats.spearmanr(d["any_visit_rate"], d["mean_z"])
        wls = smf.wls("mean_z ~ any_visit_rate", data=d, weights=d["n"]).fit()
        rows.append({
            "population": population,
            "n_careers": len(d),
            "pearson_r_unweighted": float(pear.statistic),
            "pearson_p": float(pear.pvalue),
            "spearman_rho_unweighted": float(spear.statistic),
            "spearman_p": float(spear.pvalue),
            "weighted_slope_mean_z_per_unit_visit_rate": float(wls.params["any_visit_rate"]),
            "weighted_slope_se": float(wls.bse["any_visit_rate"]),
            "weighted_slope_p": float(wls.pvalues["any_visit_rate"]),
            "weighted_r2": float(wls.rsquared),
            "interpretation": "ecological/descriptive; not an individual-level causal association",
        })
    return pd.DataFrame(rows)


def calc_progressor_mu_cohort(mu_with_outcomes: pd.DataFrame, longitudinal: pd.DataFrame) -> pd.DataFrame:
    """MU rows for students whose first later Calculus attempt has CMAT coverage."""
    ids = set(longitudinal.loc[longitudinal["CALC_VISIT_COVERAGE"], "STUDENT_ID"].astype(str))
    return mu_with_outcomes.loc[mu_with_outcomes["STUDENT_ID"].astype(str).isin(ids)].copy().reset_index(drop=True)


def calc_progressor_followup_cohort(longitudinal_with_outcomes: pd.DataFrame) -> pd.DataFrame:
    return longitudinal_with_outcomes.loc[longitudinal_with_outcomes["CALC_VISIT_COVERAGE"]].copy().reset_index(drop=True)
