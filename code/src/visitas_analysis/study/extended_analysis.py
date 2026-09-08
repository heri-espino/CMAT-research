from __future__ import annotations

"""Extended analyses for the CMAT publication draft.

These analyses are intentionally additive: they do not replace the pre-specified
publication-oriented pipeline.  They formalize several exploratory questions that
were part of earlier project iterations:

1. empirical/statistical justification for pooling exactly 1 and 2 visits;
2. association of degree programme (licenciatura) with CMAT use;
3. heteroskedastic one-way comparisons of the four visit cohorts;
4. exact-dose performance indices for 1,...,12 visits, including career-relative
   standardization;
5. differences in classroom-standardized performance across degree programmes;
6. paired longitudinal use patterns from Matemáticas Universitarias to Cálculo I.

The primary academic outcome remains Z_GRADE_PRIMARY, where the z-score is
computed within a 'salón' defined as professor x same course x same academic
period.  Because the primary cohort contains one course (MAT1012), CLASSROOM_ID
is professor x period there.
"""

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.libqsturng import psturng, qsturng
from statsmodels.stats.contingency_tables import Table2x2, mcnemar
from statsmodels.stats.oneway import anova_oneway
from statsmodels.stats.weightstats import ttost_ind
from statsmodels.stats.proportion import proportion_confint, confint_proportions_2indep
import statsmodels.formula.api as smf


VISIT_GROUP_ORDER = ["0", "1-2", "3", "4+"]


def _mean_ci_t(values: np.ndarray, alpha: float = 0.05) -> tuple[float, float, float, float]:
    """Student-t confidence interval for a sample mean.

    Returns mean, lower bound, upper bound and standard error.  The interval is
    intentionally t-based rather than a fixed 1.96 normal approximation because
    some exact-visit cohorts (especially 8--12 visits) are small.
    """
    x = np.asarray(values, float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n == 0:
        return np.nan, np.nan, np.nan, np.nan
    mean = float(np.mean(x))
    if n < 2:
        return mean, np.nan, np.nan, np.nan
    se = float(np.std(x, ddof=1) / math.sqrt(n))
    crit = float(stats.t.ppf(1 - alpha / 2, n - 1))
    return mean, mean - crit * se, mean + crit * se, se


def _welch_mean_ci(x: np.ndarray, y: np.ndarray, alpha: float = 0.05) -> tuple[float, float, float, float]:
    """Difference mean(x)-mean(y), Welch SE/df and two-sided CI."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    nx, ny = len(x), len(y)
    vx, vy = np.var(x, ddof=1), np.var(y, ddof=1)
    se2 = vx / nx + vy / ny
    se = math.sqrt(se2)
    df = se2**2 / ((vx / nx) ** 2 / (nx - 1) + (vy / ny) ** 2 / (ny - 1))
    diff = float(np.mean(x) - np.mean(y))
    crit = stats.t.ppf(1 - alpha / 2, df)
    return diff, float(diff - crit * se), float(diff + crit * se), float(df)


def one_two_pooling_analysis(
    df: pd.DataFrame,
    *,
    visits_col: str,
    outcome_col: str = "Z_GRADE_PRIMARY",
    equivalence_margin_z: float = 0.20,
) -> pd.DataFrame:
    """Formal justification for pooling V=1 and V=2.

    A non-significant difference is not evidence of similarity.  Therefore the
    primary similarity diagnostic is a two one-sided tests (TOST) equivalence
    test with a pre-specified smallest effect size of interest of +/-0.20 Z.
    Because Z is measured in classroom standard deviations, this margin has a
    direct substantive interpretation as a small standardized difference.

    Welch's test and Brunner-Munzel/Mann-Whitney are reported as complementary
    location/distribution checks, not as equivalence tests.
    """
    d = df.loc[df[visits_col].isin([1, 2]), [visits_col, outcome_col]].dropna().copy()
    x1 = d.loc[d[visits_col] == 1, outcome_col].to_numpy(float)
    x2 = d.loc[d[visits_col] == 2, outcome_col].to_numpy(float)
    if len(x1) < 2 or len(x2) < 2:
        return pd.DataFrame([{"status": "insufficient_data"}])

    # Orient every difference as V=2 minus V=1.
    diff, ci_lo, ci_hi, welch_df = _welch_mean_ci(x2, x1)
    t_stat, p_welch = stats.ttest_ind(x2, x1, equal_var=False)
    u, p_mw = stats.mannwhitneyu(x2, x1, alternative="two-sided", method="auto")
    bm_stat, p_bm = stats.brunnermunzel(x2, x1, alternative="two-sided")
    bf_stat, bf_p = stats.levene(x2, x1, center="median")
    cl = float(u / (len(x2) * len(x1)))
    cliff = 2 * cl - 1

    p_tost, lower_test, upper_test = ttost_ind(
        x2, x1,
        -float(equivalence_margin_z),
        float(equivalence_margin_z),
        usevar="unequal",
    )

    return pd.DataFrame([{
        "status": "ok",
        "comparison": "V=2 minus V=1",
        "n_v1": int(len(x1)),
        "n_v2": int(len(x2)),
        "mean_v1": float(np.mean(x1)),
        "mean_v2": float(np.mean(x2)),
        "mean_difference_v2_minus_v1": diff,
        "difference_ci95_low": ci_lo,
        "difference_ci95_high": ci_hi,
        "welch_df": welch_df,
        "welch_t": float(t_stat),
        "welch_p": float(p_welch),
        "mann_whitney_u": float(u),
        "mann_whitney_p": float(p_mw),
        "brunner_munzel_stat": float(bm_stat),
        "brunner_munzel_p": float(p_bm),
        "brown_forsythe_stat": float(bf_stat),
        "brown_forsythe_p": float(bf_p),
        "common_language_p_v2_gt_v1": cl,
        "cliffs_delta_v2_vs_v1": cliff,
        "equivalence_margin_z": float(equivalence_margin_z),
        "tost_p": float(p_tost),
        "tost_lower_t": float(lower_test[0]),
        "tost_lower_p": float(lower_test[1]),
        "tost_upper_t": float(upper_test[0]),
        "tost_upper_p": float(upper_test[1]),
        "equivalent_within_margin_at_05": bool(p_tost < 0.05),
        "academic_reason_for_pooling": "both 1 and 2 visits are below the institutional PPA threshold of 3",
    }])


def _games_howell(groups: dict[str, np.ndarray], alpha: float = 0.05) -> pd.DataFrame:
    """Games-Howell all-pairs comparisons for unequal variances/sample sizes."""
    names = list(groups)
    k = len(names)
    rows: list[dict[str, object]] = []
    for i in range(k):
        for j in range(i + 1, k):
            a_name, b_name = names[i], names[j]
            a, b = np.asarray(groups[a_name], float), np.asarray(groups[b_name], float)
            na, nb = len(a), len(b)
            if na < 2 or nb < 2:
                continue
            ma, mb = np.mean(a), np.mean(b)
            va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
            se2 = va / na + vb / nb
            se = math.sqrt(se2)
            df = se2**2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
            diff = ma - mb
            q = abs(diff) / se * math.sqrt(2)
            # statsmodels' qsturng implementation is substantially faster than
            # scipy's exact studentized_range integration for many career pairs.
            p = float(np.atleast_1d(psturng(q, k, df))[0])
            qcrit = float(qsturng(1 - alpha, k, df))
            half = qcrit / math.sqrt(2) * se
            rows.append({
                "group_a": a_name,
                "group_b": b_name,
                "n_a": na,
                "n_b": nb,
                "mean_a": float(ma),
                "mean_b": float(mb),
                "mean_difference_a_minus_b": float(diff),
                "df": float(df),
                "games_howell_q": float(q),
                "p_adjusted": p,
                "ci95_low": float(diff - half),
                "ci95_high": float(diff + half),
                "significant_05": bool(p < alpha),
            })
    return pd.DataFrame(rows)


def welch_anova_visit_groups(
    df: pd.DataFrame,
    *,
    group_col: str,
    outcome_col: str = "Z_GRADE_PRIMARY",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Welch one-way ANOVA + Brown-Forsythe + Games-Howell for visit cohorts."""
    d = df[[group_col, outcome_col]].dropna().copy()
    d[group_col] = pd.Categorical(d[group_col], categories=VISIT_GROUP_ORDER, ordered=True)
    groups = {
        g: d.loc[d[group_col] == g, outcome_col].to_numpy(float)
        for g in VISIT_GROUP_ORDER
        if (d[group_col] == g).sum() >= 2
    }
    arrs = list(groups.values())
    welch = anova_oneway(arrs, use_var="unequal", welch_correction=True)
    bf_stat, bf_p = stats.levene(*arrs, center="median")
    summary_rows = []
    for g, x in groups.items():
        se = np.std(x, ddof=1) / math.sqrt(len(x))
        summary_rows.append({
            "group": g, "n": len(x), "mean": np.mean(x), "sd": np.std(x, ddof=1),
            "median": np.median(x), "ci95_low": np.mean(x)-1.96*se, "ci95_high": np.mean(x)+1.96*se,
        })
    omnibus = pd.DataFrame([{
        "test": "Welch one-way ANOVA",
        "statistic": float(welch.statistic),
        "df_num": float(welch.df_num),
        "df_denom": float(welch.df_denom),
        "p_value": float(welch.pvalue),
        "brown_forsythe_levene_stat": float(bf_stat),
        "brown_forsythe_p": float(bf_p),
        "variance_assumption": "Welch ANOVA does not require homoscedasticity; Brown-Forsythe is diagnostic only",
        "independence_assumption": "one first-attempt observation per student; residual dependence within professor-period remains and is handled in FE models elsewhere",
    }])
    posthoc = _games_howell(groups)
    return omnibus, pd.DataFrame(summary_rows), posthoc


def _bias_corrected_cramers_v(table: np.ndarray) -> float:
    chi2 = stats.chi2_contingency(table, correction=False)[0]
    n = table.sum()
    if n <= 1:
        return np.nan
    phi2 = chi2 / n
    r, k = table.shape
    phi2corr = max(0.0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    denom = min(kcorr - 1, rcorr - 1)
    return float(math.sqrt(phi2corr / denom)) if denom > 0 else np.nan


def career_usage_association(
    df: pd.DataFrame,
    *,
    career_col: str = "CLAVECARRERA",
    group_col: str = "VISIT_GROUP_PERIOD",
    min_career_n: int = 30,
    permutation_reps: int = 3000,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Association between degree programme and use pattern.

    Rare careers are not combined into a misleading substantive category; they
    are excluded from the omnibus inferential table using a transparent minimum
    N rule and remain available in the descriptive career table.

    A permutation p-value is supplied because 4-level visit groups can yield
    sparse expected cells even after the minimum-N filter.
    """
    d = df[[career_col, group_col]].dropna().copy()
    counts = d[career_col].value_counts()
    keep = counts[counts >= min_career_n].index
    d = d.loc[d[career_col].isin(keep)].copy()
    d[group_col] = pd.Categorical(d[group_col], categories=VISIT_GROUP_ORDER, ordered=True)
    tab = pd.crosstab(d[career_col], d[group_col]).reindex(columns=VISIT_GROUP_ORDER, fill_value=0)
    chi2, p_chi, dof, expected = stats.chi2_contingency(tab.to_numpy(), correction=False)
    expected_lt5 = float((expected < 5).mean())

    rng = np.random.default_rng(seed)
    careers = d[career_col].to_numpy()
    labels = d[group_col].astype(str).to_numpy()
    career_levels = list(tab.index)
    group_levels = VISIT_GROUP_ORDER
    c_codes = pd.Categorical(careers, categories=career_levels).codes
    g_codes = pd.Categorical(labels, categories=group_levels).codes
    obs = float(chi2)
    ge = 0
    shape = (len(career_levels), len(group_levels))
    # Under label permutation row/column margins are fixed, hence expected
    # counts are constant. Computing Pearson's statistic directly avoids
    # thousands of repeated contingency-table decompositions.
    expected_const = expected
    for _ in range(int(permutation_reps)):
        pg = rng.permutation(g_codes)
        perm_table = np.zeros(shape, dtype=int)
        np.add.at(perm_table, (c_codes, pg), 1)
        stat = float(np.sum((perm_table - expected_const) ** 2 / expected_const))
        ge += stat >= obs - 1e-12
    p_perm = (ge + 1) / (permutation_reps + 1)

    omnibus = pd.DataFrame([{
        "test": "career x visit-group independence",
        "n": int(len(d)),
        "careers_included": int(len(career_levels)),
        "min_career_n": int(min_career_n),
        "chi_square": float(chi2),
        "df": int(dof),
        "asymptotic_p": float(p_chi),
        "expected_cells_lt5_proportion": expected_lt5,
        "permutation_reps": int(permutation_reps),
        "permutation_p": float(p_perm),
        "cramers_v_bias_corrected": _bias_corrected_cramers_v(tab.to_numpy()),
        "primary_p_for_sparse_table": "permutation_p",
    }])

    long = tab.reset_index().melt(id_vars=[career_col], var_name="visit_group", value_name="n")
    career_n = tab.sum(axis=1)
    long["career_n"] = long[career_col].map(career_n)
    long["within_career_proportion"] = long["n"] / long["career_n"]

    # Binary any-use association has much denser expected cells and an intuitive effect.
    binary = pd.crosstab(d[career_col], (d[group_col].astype(str) != "0").astype(int))
    binary = binary.reindex(columns=[0, 1], fill_value=0)
    bchi, bp, bdof, bexp = stats.chi2_contingency(binary.to_numpy(), correction=False)
    binary_omnibus = pd.DataFrame([{
        "test": "career x any-CMAT-use independence",
        "n": int(len(d)),
        "chi_square": float(bchi),
        "df": int(bdof),
        "p_value": float(bp),
        "expected_cells_lt5_proportion": float((bexp < 5).mean()),
        "cramers_v_bias_corrected": _bias_corrected_cramers_v(binary.to_numpy()),
    }])
    return omnibus, binary_omnibus, long


def career_performance_analysis(
    df: pd.DataFrame,
    *,
    career_col: str = "CLAVECARRERA",
    outcome_col: str = "Z_GRADE_PRIMARY",
    visits_col: str = "VISITS_CMAT_PERIOD",
    min_career_n: int = 30,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Career-specific classroom-relative performance and Welch comparisons."""
    d = df[[career_col, outcome_col, visits_col]].dropna(subset=[career_col, outcome_col]).copy()
    summary = (
        d.groupby(career_col)
        .agg(
            n=(outcome_col, "size"),
            mean_z=(outcome_col, "mean"),
            sd_z=(outcome_col, "std"),
            median_z=(outcome_col, "median"),
            mean_visits=(visits_col, "mean"),
            any_visit_rate=(visits_col, lambda s: float((s > 0).mean())),
            ppa_reached_rate=(visits_col, lambda s: float((s >= 3).mean())),
        )
        .reset_index()
    )
    summary["se_z"] = summary["sd_z"] / np.sqrt(summary["n"])
    summary["ci95_low"] = summary["mean_z"] - 1.96 * summary["se_z"]
    summary["ci95_high"] = summary["mean_z"] + 1.96 * summary["se_z"]
    summary["inferentially_included"] = summary["n"] >= min_career_n
    summary = summary.sort_values("mean_z", ascending=False)

    keep = summary.loc[summary["inferentially_included"], career_col]
    inf = d.loc[d[career_col].isin(keep)].copy()
    groups = {
        str(c): g[outcome_col].to_numpy(float)
        for c, g in inf.groupby(career_col)
        if len(g) >= 2
    }
    arrs = list(groups.values())
    welch = anova_oneway(arrs, use_var="unequal", welch_correction=True)
    bf_stat, bf_p = stats.levene(*arrs, center="median")
    omnibus = pd.DataFrame([{
        "test": "Welch ANOVA of classroom-standardized Z across careers",
        "n": int(len(inf)),
        "careers_included": len(groups),
        "min_career_n": int(min_career_n),
        "welch_F": float(welch.statistic),
        "df_num": float(welch.df_num),
        "df_denom": float(welch.df_denom),
        "p_value": float(welch.pvalue),
        "brown_forsythe_stat": float(bf_stat),
        "brown_forsythe_p": float(bf_p),
        "interpretation_of_z": "positive mean means the career's students are, on average, above their professor-period classroom mean in classroom SD units",
    }])
    posthoc = _games_howell(groups)
    return summary, omnibus, posthoc


def career_visit_interaction_model(
    df: pd.DataFrame,
    *,
    career_col: str = "CLAVECARRERA",
    group_col: str = "VISIT_GROUP_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    min_career_n: int = 100,
    min_cell_n: int = 5,
) -> pd.DataFrame:
    """Exploratory heterogeneity of the visit-performance association by career.

    To avoid a very sparse interaction model, only careers with at least
    ``min_career_n`` observations are retained.  The output reports a joint Wald
    test for all career x visit-group interaction coefficients.  This is a
    heterogeneity test, not a causal effect-modification claim.
    """
    req = [career_col, group_col, outcome_col, "CLASSROOM_ID"]
    d = df.dropna(subset=req).copy()
    counts = d[career_col].value_counts()
    keep = counts[counts >= min_career_n].index
    d = d.loc[d[career_col].isin(keep)].copy()
    d[group_col] = pd.Categorical(d[group_col], categories=VISIT_GROUP_ORDER, ordered=True)
    cell = pd.crosstab(d[career_col], d[group_col]).reindex(columns=VISIT_GROUP_ORDER, fill_value=0)
    keep_cells = cell.index[(cell >= int(min_cell_n)).all(axis=1)]
    d = d.loc[d[career_col].isin(keep_cells)].copy()
    if d[career_col].nunique() < 2:
        return pd.DataFrame([{"status": "insufficient_data"}])

    # Z is already standardized within professor-period classroom.  For this
    # exploratory effect-heterogeneity check we therefore avoid adding hundreds
    # of classroom dummy variables again; dependence within classroom is still
    # handled through cluster-robust covariance.
    formula = f"{outcome_col} ~ C({group_col}, Treatment(reference='0')) * C({career_col})"
    model = smf.ols(formula, data=d).fit(cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]})
    interaction_terms = [name for name in model.params.index if ":" in name and f"C({group_col}" in name]
    if not interaction_terms:
        return pd.DataFrame([{"status": "no_interaction_terms"}])
    idx = [model.params.index.get_loc(t) for t in interaction_terms]
    R = np.zeros((len(idx), len(model.params)))
    for r, j in enumerate(idx):
        R[r, j] = 1.0
    wt = model.wald_test(R, scalar=True)
    return pd.DataFrame([{
        "status": "ok",
        "model": "classroom-standardized Z ~ visit group x career",
        "n": int(model.nobs),
        "careers_included": int(d[career_col].nunique()),
        "min_career_n": int(min_career_n),
        "min_cell_n_each_visit_group": int(min_cell_n),
        "interaction_terms": int(len(interaction_terms)),
        "wald_statistic": float(wt.statistic),
        "df_constraints": int(len(interaction_terms)),
        "p_value": float(wt.pvalue),
        "covariance": "cluster-robust by professor-period classroom",
        "interpretation": "omnibus heterogeneity of association; not causal effect modification",
    }])



def clustered_visit_group_omnibus(
    df: pd.DataFrame,
    *,
    group_col: str = "VISIT_GROUP_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    classroom_col: str = "CLASSROOM_ID",
) -> pd.DataFrame:
    """Cluster-robust omnibus test for the four visit cohorts.

    Welch ANOVA is the requested heteroskedastic marginal comparison, but it
    treats students as independent. This model is a robustness check that adds
    professor-period classroom fixed effects and clusters the covariance matrix
    at the same classroom level. The joint Wald null is that every non-zero
    visit-group coefficient relative to V=0 equals zero.
    """
    req = [group_col, outcome_col, classroom_col]
    d = df.dropna(subset=req).copy()
    d[group_col] = pd.Categorical(d[group_col], categories=VISIT_GROUP_ORDER, ordered=True)
    if d[group_col].nunique() < 2:
        return pd.DataFrame([{"status": "insufficient_data"}])
    model = smf.ols(
        f"{outcome_col} ~ C({group_col}, Treatment(reference='0')) + C({classroom_col})",
        data=d,
    ).fit(cov_type="cluster", cov_kwds={"groups": d[classroom_col]})
    terms = [t for t in model.params.index if t.startswith(f"C({group_col}")]
    R = np.zeros((len(terms), len(model.params)))
    names = list(model.params.index)
    for i, term in enumerate(terms):
        R[i, names.index(term)] = 1.0
    wt = model.wald_test(R, scalar=True)
    return pd.DataFrame([{
        "status": "ok",
        "test": "joint Wald test of visit-group terms",
        "n": int(model.nobs),
        "classrooms": int(d[classroom_col].nunique()),
        "constraints": int(len(terms)),
        "wald_statistic": float(wt.statistic),
        "p_value": float(wt.pvalue),
        "fixed_effects": "professor x period classroom",
        "covariance": "cluster-robust by professor x period classroom",
    }])


def clustered_career_omnibus(
    df: pd.DataFrame,
    *,
    career_col: str = "CLAVECARRERA",
    outcome_col: str = "Z_GRADE_PRIMARY",
    classroom_col: str = "CLASSROOM_ID",
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Joint career test after classroom fixed effects with clustered covariance."""
    req = [career_col, outcome_col, classroom_col]
    d = df.dropna(subset=req).copy()
    counts = d[career_col].value_counts()
    keep = counts[counts >= int(min_career_n)].index
    d = d.loc[d[career_col].isin(keep)].copy()
    if d[career_col].nunique() < 2:
        return pd.DataFrame([{"status": "insufficient_data"}])
    base = smf.ols(f"{outcome_col} ~ C({classroom_col})", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d[classroom_col]}
    )
    model = smf.ols(
        f"{outcome_col} ~ C({classroom_col}) + C({career_col})", data=d
    ).fit(cov_type="cluster", cov_kwds={"groups": d[classroom_col]})
    terms = [t for t in model.params.index if t.startswith(f"C({career_col})")]
    R = np.zeros((len(terms), len(model.params)))
    names = list(model.params.index)
    for i, term in enumerate(terms):
        R[i, names.index(term)] = 1.0
    wt = model.wald_test(R, scalar=True)
    return pd.DataFrame([{
        "status": "ok",
        "test": "joint Wald test of career terms",
        "n": int(model.nobs),
        "careers_included": int(d[career_col].nunique()),
        "min_career_n": int(min_career_n),
        "classrooms": int(d[classroom_col].nunique()),
        "constraints": int(len(terms)),
        "wald_statistic": float(wt.statistic),
        "p_value": float(wt.pvalue),
        "r_squared_classroom_only": float(base.rsquared),
        "r_squared_classroom_plus_career": float(model.rsquared),
        "delta_r_squared_career": float(model.rsquared - base.rsquared),
        "fixed_effects": "professor x period classroom",
        "covariance": "cluster-robust by professor x period classroom",
    }])


def exact_visit_performance_index(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    career_col: str = "CLAVECARRERA",
    min_visit: int = 1,
    max_visit: int = 12,
    min_career_n_for_standardization: int = 30,
    min_cell_n_for_balanced: int = 2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Performance index by exact visit count (1..12), adjusted to career context.

    ``outcome_col`` is already standardized within professor x period classroom.
    We add a second standardization within degree programme:

        CAREER_REL_Z_i = (Z_i - mean(Z | career_i)) / sd(Z | career_i)

    Thus a value of +0.30 means that, after first expressing performance relative
    to the student's classroom, the student is 0.30 career-specific SD above the
    mean student in the same degree programme.  Exact-visit summaries are shown
    both student-weighted and career-balanced.  The latter gives each career with
    adequate cell size equal weight, preventing the largest degree programmes
    from mechanically dominating an exact-dose point.
    """
    req = [visits_col, outcome_col, career_col]
    d = df.dropna(subset=req).copy()
    career_stats = d.groupby(career_col)[outcome_col].agg(["count", "mean", "std"]).rename(
        columns={"count": "career_n", "mean": "career_mean_z", "std": "career_sd_z"}
    )
    eligible = career_stats.index[(career_stats["career_n"] >= min_career_n_for_standardization) & (career_stats["career_sd_z"] > 0)]
    d = d.loc[d[career_col].isin(eligible)].copy()
    d = d.join(career_stats, on=career_col)
    d["CAREER_REL_Z"] = (d[outcome_col] - d["career_mean_z"]) / d["career_sd_z"]
    d = d.loc[d[visits_col].between(min_visit, max_visit)].copy()

    rows: list[dict[str, object]] = []
    career_rows: list[dict[str, object]] = []
    for v in range(min_visit, max_visit + 1):
        g = d.loc[d[visits_col] == v].copy()
        if g.empty:
            rows.append({"visits": v, "n": 0})
            continue
        x = g[outcome_col].to_numpy(float)
        r = g["CAREER_REL_Z"].to_numpy(float)
        mean_x, x_lo, x_hi, _ = _mean_ci_t(x)
        mean_r, r_lo, r_hi, _ = _mean_ci_t(r)
        by_c = (
            g.groupby(career_col)
            .agg(n=("CAREER_REL_Z", "size"), mean_career_rel_z=("CAREER_REL_Z", "mean"), mean_classroom_z=(outcome_col, "mean"))
            .reset_index()
        )
        by_c["visits"] = v
        career_rows.extend(by_c.to_dict(orient="records"))
        bal = by_c.loc[by_c["n"] >= min_cell_n_for_balanced, "mean_career_rel_z"].to_numpy(float)
        bal_mean, bal_lo, bal_hi, _ = _mean_ci_t(bal)
        rows.append({
            "visits": v,
            "n": int(len(g)),
            "classrooms_represented": int(g["CLASSROOM_ID"].nunique()) if "CLASSROOM_ID" in g else np.nan,
            "careers_represented": int(g[career_col].nunique()),
            "mean_classroom_z": mean_x,
            "mean_classroom_z_ci95_low": x_lo,
            "mean_classroom_z_ci95_high": x_hi,
            "career_relative_index_student_weighted": mean_r,
            "career_relative_ci95_low": r_lo,
            "career_relative_ci95_high": r_hi,
            "career_balanced_index": bal_mean,
            "career_balanced_careers": int(len(bal)),
            "career_balanced_ci95_low": bal_lo,
            "career_balanced_ci95_high": bal_hi,
            "ci_method": "Student-t mean interval; descriptive and not cluster-adjusted",
            "stability_flag": "low_n" if len(g) < 20 else "ok",
        })
    return pd.DataFrame(rows), pd.DataFrame(career_rows)


def longitudinal_any_visit_transition(
    longitudinal: pd.DataFrame,
    *,
    mu_visits_col: str = "MU_VISITS_CMAT_PERIOD",
    calc_visits_col: str = "VISITS_CMAT_PERIOD",
    calc_coverage_col: str = "CALC_VISIT_COVERAGE",
    mu_coverage_col: str | None = "MU_VISIT_COVERAGE",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """2x2 longitudinal transition and association statistics for any CMAT use."""
    d = longitudinal.copy()
    mask = d[calc_coverage_col].astype(bool)
    if mu_coverage_col and mu_coverage_col in d.columns:
        mask &= d[mu_coverage_col].astype(bool)
    d = d.loc[mask].copy()
    d["MU_ANY"] = (d[mu_visits_col] > 0).astype(int)
    d["CALC_ANY"] = (d[calc_visits_col] > 0).astype(int)

    n00 = int(((d.MU_ANY == 0) & (d.CALC_ANY == 0)).sum())
    n01 = int(((d.MU_ANY == 0) & (d.CALC_ANY == 1)).sum())
    n10 = int(((d.MU_ANY == 1) & (d.CALC_ANY == 0)).sum())
    n11 = int(((d.MU_ANY == 1) & (d.CALC_ANY == 1)).sum())
    n = n00+n01+n10+n11

    combos = pd.DataFrame([
        {"mu_any_visit": 0, "calc_any_visit": 0, "pattern": "no MU / no Cálculo", "n": n00},
        {"mu_any_visit": 0, "calc_any_visit": 1, "pattern": "no MU / sí Cálculo", "n": n01},
        {"mu_any_visit": 1, "calc_any_visit": 0, "pattern": "sí MU / no Cálculo", "n": n10},
        {"mu_any_visit": 1, "calc_any_visit": 1, "pattern": "sí MU / sí Cálculo", "n": n11},
    ])
    combos["proportion"] = combos["n"] / n if n else np.nan

    # Exposed rows (MU users) vs unexposed rows; event = any Calculus use.
    exposed_table = np.array([[n11, n10], [n01, n00]], dtype=float)
    t2 = Table2x2(exposed_table, shift_zeros=True)
    fisher_or, fisher_p = stats.fisher_exact(exposed_table, alternative="two-sided")
    chi2, chi_p, chi_df, expected = stats.chi2_contingency(exposed_table, correction=False)
    p_calc_mu1 = n11 / (n11+n10) if (n11+n10) else np.nan
    p_calc_mu0 = n01 / (n01+n00) if (n01+n00) else np.nan
    rd = p_calc_mu1 - p_calc_mu0
    p1_ci = proportion_confint(n11, n11 + n10, alpha=0.05, method="wilson")
    p0_ci = proportion_confint(n01, n01 + n00, alpha=0.05, method="wilson")
    rd_ci = confint_proportions_2indep(
        n11, n11 + n10, n01, n01 + n00,
        compare="diff", method="newcomb", alpha=0.05, correction=True,
    )

    # McNemar asks a different question: whether marginal any-use prevalence
    # changed from MU to Calculus among the same students (discordant cells).
    paired = np.array([[n00, n01], [n10, n11]])
    mc = mcnemar(paired, exact=False, correction=True)
    phi = math.sqrt(chi2 / n) if n else np.nan

    stats_df = pd.DataFrame([{
        "n": n,
        "p_calc_visit_given_mu_visit": p_calc_mu1,
        "p_calc_visit_given_mu_visit_ci95_low": float(p1_ci[0]),
        "p_calc_visit_given_mu_visit_ci95_high": float(p1_ci[1]),
        "p_calc_visit_given_no_mu_visit": p_calc_mu0,
        "p_calc_visit_given_no_mu_visit_ci95_low": float(p0_ci[0]),
        "p_calc_visit_given_no_mu_visit_ci95_high": float(p0_ci[1]),
        "risk_difference": rd,
        "risk_difference_ci95_low": float(rd_ci[0]),
        "risk_difference_ci95_high": float(rd_ci[1]),
        "risk_difference_ci_method": "Newcombe-Wilson",
        "risk_ratio": float(t2.riskratio),
        "risk_ratio_ci95_low": float(t2.riskratio_confint()[0]),
        "risk_ratio_ci95_high": float(t2.riskratio_confint()[1]),
        "odds_ratio": float(t2.oddsratio),
        "odds_ratio_ci95_low": float(t2.oddsratio_confint()[0]),
        "odds_ratio_ci95_high": float(t2.oddsratio_confint()[1]),
        "fisher_exact_or": float(fisher_or),
        "fisher_exact_p": float(fisher_p),
        "pearson_chi_square": float(chi2),
        "pearson_chi_square_p": float(chi_p),
        "phi": float(phi),
        "min_expected_cell": float(np.min(expected)),
        "mcnemar_statistic": float(mc.statistic),
        "mcnemar_p": float(mc.pvalue),
        "mcnemar_interpretation": "tests marginal change in use prevalence, not MU->Calculus association",
        "association_interpretation": "RR/OR compare probability of Calculus use between prior MU users and non-users; observational, not causal",
    }])
    return combos, stats_df


def clustered_omnibus_visit_group_test(
    df: pd.DataFrame,
    *,
    group_col: str = "VISIT_GROUP_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
) -> pd.DataFrame:
    """Cluster-robust classroom-FE omnibus complement to marginal Welch ANOVA."""
    d = df.dropna(subset=[group_col, outcome_col, "CLASSROOM_ID"]).copy()
    d[group_col] = pd.Categorical(d[group_col], categories=VISIT_GROUP_ORDER, ordered=True)
    model = smf.ols(
        f"{outcome_col} ~ C({group_col}, Treatment(reference='0')) + C(CLASSROOM_ID)", data=d
    ).fit(cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]})
    terms = [t for t in model.params.index if t.startswith(f"C({group_col}")]
    idx = [model.params.index.get_loc(t) for t in terms]
    R = np.zeros((len(idx), len(model.params)))
    for r,j in enumerate(idx): R[r,j]=1
    wt = model.wald_test(R, scalar=True)
    return pd.DataFrame([{
        "test": "joint visit-group coefficients with professor-period FE",
        "n": int(model.nobs),
        "groups_tested": len(terms),
        "wald_statistic": float(wt.statistic),
        "df_constraints": len(terms),
        "p_value": float(wt.pvalue),
        "covariance": "cluster-robust by professor-period classroom",
    }])


def clustered_omnibus_career_test(
    df: pd.DataFrame,
    *,
    career_col: str = "CLAVECARRERA",
    outcome_col: str = "Z_GRADE_PRIMARY",
    min_career_n: int = 30,
) -> pd.DataFrame:
    """Classroom-FE, cluster-robust joint test of career coefficients."""
    d = df.dropna(subset=[career_col, outcome_col, "CLASSROOM_ID"]).copy()
    counts=d[career_col].value_counts(); keep=counts[counts>=min_career_n].index
    d=d.loc[d[career_col].isin(keep)].copy()
    model=smf.ols(f"{outcome_col} ~ C({career_col}) + C(CLASSROOM_ID)",data=d).fit(
        cov_type="cluster", cov_kwds={"groups":d["CLASSROOM_ID"]}
    )
    terms=[t for t in model.params.index if t.startswith(f"C({career_col})")]
    idx=[model.params.index.get_loc(t) for t in terms]
    R=np.zeros((len(idx),len(model.params)))
    for r,j in enumerate(idx): R[r,j]=1
    wt=model.wald_test(R,scalar=True)
    return pd.DataFrame([{
        "test":"joint career coefficients with professor-period FE",
        "n":int(model.nobs),"careers_included":int(d[career_col].nunique()),
        "min_career_n":int(min_career_n),"wald_statistic":float(wt.statistic),
        "df_constraints":len(terms),"p_value":float(wt.pvalue),
        "covariance":"cluster-robust by professor-period classroom",
    }])


def exact_visit_index_trend(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    outcome_col: str = "Z_GRADE_PRIMARY",
    career_col: str = "CLAVECARRERA",
    min_visit: int = 1,
    max_visit: int = 12,
    min_career_n: int = 30,
    min_exact_group_n_for_stable_trend: int = 20,
) -> pd.DataFrame:
    """Exploratory trend for the career-relative exact-dose index.

    Two specifications are returned.  The first uses every student with an
    exact count from 1..12.  The second excludes exact-count cells with fewer
    than ``min_exact_group_n_for_stable_trend`` students.  This protects the
    trend interpretation from being driven by the very sparse 8--12-visit
    tail while retaining those cohorts descriptively in table 91.

    Spearman's rho is a monotone, nonparametric summary.  The linear slope is
    intentionally secondary and uses professor-period cluster-robust standard
    errors; neither statistic identifies a causal dose-response relation.
    """
    d = df.dropna(subset=[visits_col, outcome_col, career_col, "CLASSROOM_ID"]).copy()
    cs = d.groupby(career_col)[outcome_col].agg(["count", "mean", "std"])
    keep = cs.index[(cs["count"] >= min_career_n) & (cs["std"] > 0)]
    d = d.loc[d[career_col].isin(keep) & d[visits_col].between(min_visit, max_visit)].copy()
    d = d.join(cs[["mean", "std"]], on=career_col)
    d["CAREER_REL_Z"] = (d[outcome_col] - d["mean"]) / d["std"]

    counts = d[visits_col].value_counts().sort_index()
    stable_counts = sorted(int(v) for v, n in counts.items() if n >= min_exact_group_n_for_stable_trend)

    specs: list[tuple[str, pd.DataFrame, str]] = [
        (f"all_exact_counts_{min_visit}_{max_visit}", d, ",".join(map(str, sorted(d[visits_col].unique().astype(int))))),
    ]
    if stable_counts:
        specs.append((
            f"stable_exact_cells_n_ge_{min_exact_group_n_for_stable_trend}",
            d.loc[d[visits_col].isin(stable_counts)].copy(),
            ",".join(map(str, stable_counts)),
        ))

    rows: list[dict[str, object]] = []
    for label, ds, included in specs:
        rho, p_rho = stats.spearmanr(ds[visits_col], ds["CAREER_REL_Z"])
        model = smf.ols(f"CAREER_REL_Z ~ {visits_col}", data=ds).fit(
            cov_type="cluster", cov_kwds={"groups": ds["CLASSROOM_ID"]}
        )
        ci = model.conf_int().loc[visits_col]
        rows.append({
            "specification": label,
            "n": int(len(ds)),
            "exact_visit_counts_included": included,
            "min_exact_group_n_rule": int(min_exact_group_n_for_stable_trend) if label.startswith("stable") else np.nan,
            "spearman_rho": float(rho),
            "spearman_p": float(p_rho),
            "linear_slope_per_visit": float(model.params[visits_col]),
            "linear_slope_se_clustered": float(model.bse[visits_col]),
            "linear_slope_ci95_low": float(ci.iloc[0]),
            "linear_slope_ci95_high": float(ci.iloc[1]),
            "linear_slope_p": float(model.pvalues[visits_col]),
            "classrooms": int(ds["CLASSROOM_ID"].nunique()),
            "covariance": "cluster-robust by professor-period classroom",
            "interpretation": "exploratory association; exact-dose relationship need not be linear and is not causal",
        })
    return pd.DataFrame(rows)

