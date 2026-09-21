"""Reusable attendance-frequency and grouped-outcome analysis.

Support audits in this module do not read academic outcomes, allowing exposure
groups to be chosen before outcome means or significance tests are inspected.
Regression helpers remain observational estimators.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests


def _require(df: pd.DataFrame, columns: Sequence[str]) -> None:
    missing = sorted(set(columns).difference(df.columns))
    if missing:
        raise KeyError(f"Missing required columns: {missing}")


def _formula_name(name: str) -> str:
    if not isinstance(name, str) or not name.isidentifier():
        raise ValueError(f"Rename non-identifier column before modelling: {name!r}")
    return name


def add_topcoded_visit_group(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    top_exact: int = 5,
    include_zero: bool = False,
    output_col: str = "VISIT_FREQUENCY_GROUP",
) -> pd.DataFrame:
    """Add an ordered exact-plus-tail attendance-frequency grouping.

    Parameters
    ----------
    df : pandas.DataFrame
        Table containing non-negative visit counts.
    visits_col : str, default='VISITS_CMAT_PERIOD'
        Visit-count column.
    top_exact : int, default=5
        Largest positive count retained exactly; larger counts are pooled.
    include_zero : bool, default=False
        Whether zero visits is retained as the first ordered category.
    output_col : str, default='VISIT_FREQUENCY_GROUP'
        Name of the added ordered categorical column.

    Returns
    -------
    pandas.DataFrame
        Copy of the table with the grouped attendance column.
    """
    if top_exact < 1:
        raise ValueError("top_exact must be at least 1")
    _require(df, [visits_col])
    out = df.copy()
    visits = pd.to_numeric(out[visits_col], errors="coerce")
    labels = pd.Series(pd.NA, index=out.index, dtype="string")
    if include_zero:
        labels.loc[visits.eq(0)] = "0"
    for value in range(1, top_exact + 1):
        labels.loc[visits.eq(value)] = str(value)
    labels.loc[visits.gt(top_exact)] = f"{top_exact + 1}+"
    categories = (["0"] if include_zero else []) + [
        str(value) for value in range(1, top_exact + 1)
    ] + [f"{top_exact + 1}+"]
    out[output_col] = pd.Categorical(labels, categories=categories, ordered=True)
    return out


def visit_frequency_support_audit(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    cluster_col: str = "CLASSROOM_ID",
    instructor_col: str | None = None,
) -> pd.DataFrame:
    """Audit exact positive visit counts without using academic outcomes.

    Parameters
    ----------
    df : pandas.DataFrame
        Cohort table containing visits and comparison-cluster identifiers.
    visits_col : str, default='VISITS_CMAT_PERIOD'
        Visit-count column.
    cluster_col : str, default='CLASSROOM_ID'
        Context/cluster used for later comparisons.
    instructor_col : str or None, default=None
        Optional instructor identifier for coverage counts.

    Returns
    -------
    pandas.DataFrame
        Exact-count sample size, cluster support, overlap, and upper-tail size.
    """
    required = [visits_col, cluster_col]
    if instructor_col is not None:
        required.append(instructor_col)
    _require(df, required)
    d = df.dropna(subset=[visits_col, cluster_col]).copy()
    d[visits_col] = pd.to_numeric(d[visits_col], errors="coerce")
    users = d.loc[d[visits_col].gt(0)].copy()
    if users.empty:
        return pd.DataFrame()

    positive_sets = users.groupby(cluster_col)[visits_col].agg(
        lambda x: set(int(v) for v in x)
    ).to_dict()
    all_sets = d.groupby(cluster_col)[visits_col].agg(
        lambda x: set(int(v) for v in x)
    ).to_dict()
    rows = []
    for value, group in users.groupby(visits_col, sort=True):
        exact = int(value)
        cluster_counts = group.groupby(cluster_col).size()
        clusters = set(group[cluster_col])
        row = {
            "visits_exact": exact,
            "n_students": int(len(group)),
            "share_of_positive_users": float(len(group) / len(users)),
            "n_clusters": int(group[cluster_col].nunique()),
            "median_students_per_cluster": float(cluster_counts.median()),
            "max_students_per_cluster": int(cluster_counts.max()),
            "clusters_with_another_positive_frequency": int(
                sum(len(positive_sets[c] - {exact}) > 0 for c in clusters)
            ),
            "clusters_with_zero_visit_students": int(
                sum(0 in all_sets[c] for c in clusters)
            ),
            "tail_n_ge_k": int(users[visits_col].ge(exact).sum()),
        }
        if instructor_col is not None:
            row["n_instructors"] = int(group[instructor_col].nunique())
        rows.append(row)
    return pd.DataFrame(rows)


def visit_group_pair_overlap(
    df: pd.DataFrame,
    *,
    group_col: str,
    group_order: Sequence[str],
    cluster_col: str = "CLASSROOM_ID",
) -> pd.DataFrame:
    """Count cluster overlap for every pair of attendance groups.

    Parameters
    ----------
    df : pandas.DataFrame
        Table containing grouped attendance and cluster identifiers.
    group_col : str
        Attendance-group column.
    group_order : sequence of str
        Ordered group labels.
    cluster_col : str, default='CLASSROOM_ID'
        Context/cluster identifier.

    Returns
    -------
    pandas.DataFrame
        Pairwise cluster overlap and adjacency flags.
    """
    _require(df, [group_col, cluster_col])
    order = [str(group) for group in group_order]
    presence = df[[cluster_col, group_col]].dropna().drop_duplicates().copy()
    presence[group_col] = presence[group_col].astype(str)
    clusters = {
        group: set(presence.loc[presence[group_col].eq(group), cluster_col])
        for group in order
    }
    rows = []
    for i, group1 in enumerate(order):
        for j in range(i + 1, len(order)):
            group2 = order[j]
            rows.append({
                "group1": group1,
                "group2": group2,
                "clusters_with_both": int(len(clusters[group1] & clusters[group2])),
                "adjacent_groups": bool(j == i + 1),
            })
    return pd.DataFrame(rows)


def visit_frequency_cut_frontier(
    df: pd.DataFrame,
    *,
    visits_col: str = "VISITS_CMAT_PERIOD",
    cluster_col: str = "CLASSROOM_ID",
    min_top_exact: int = 1,
    max_top_exact: int = 10,
) -> pd.DataFrame:
    """Compare candidate exact-plus-tail cuts using outcome-blind support.

    Parameters
    ----------
    df : pandas.DataFrame
        Cohort table containing visits and comparison clusters.
    visits_col : str, default='VISITS_CMAT_PERIOD'
        Visit-count column.
    cluster_col : str, default='CLASSROOM_ID'
        Context/cluster identifier.
    min_top_exact : int, default=1
        Smallest candidate exact upper count.
    max_top_exact : int, default=10
        Largest candidate exact upper count.

    Returns
    -------
    pandas.DataFrame
        Candidate-cut support and minimum/median pair-overlap diagnostics.

    Notes
    -----
    The function supplies a support frontier and intentionally does not choose
    an automatic optimal cut.
    """
    if min_top_exact < 1 or max_top_exact < min_top_exact:
        raise ValueError("Require 1 <= min_top_exact <= max_top_exact")
    _require(df, [visits_col, cluster_col])
    d = df.dropna(subset=[visits_col, cluster_col]).copy()
    d[visits_col] = pd.to_numeric(d[visits_col], errors="coerce")
    users = d.loc[d[visits_col].gt(0)].copy()
    if users.empty:
        return pd.DataFrame()
    exact = users.groupby(visits_col).agg(
        n_students=(cluster_col, "size"),
        n_clusters=(cluster_col, "nunique"),
    ).reset_index()
    observed = set(int(v) for v in users[visits_col].unique())
    rows = []
    upper = min(max_top_exact, int(users[visits_col].max()) - 1)
    for top_exact in range(min_top_exact, upper + 1):
        if not set(range(1, top_exact + 1)).issubset(observed):
            continue
        grouped = add_topcoded_visit_group(
            users, visits_col=visits_col, top_exact=top_exact, output_col="_CUT"
        )
        order = [str(v) for v in range(1, top_exact + 1)] + [f"{top_exact + 1}+"]
        overlap = visit_group_pair_overlap(
            grouped, group_col="_CUT", group_order=order, cluster_col=cluster_col
        )
        adjacent = overlap.loc[overlap["adjacent_groups"], "clusters_with_both"]
        all_pairs = overlap["clusters_with_both"]
        tail = users.loc[users[visits_col].gt(top_exact)]
        exact_rows = exact.loc[exact[visits_col].le(top_exact)]
        rows.append({
            "top_exact_visit_count": top_exact,
            "tail_label": f"{top_exact + 1}+",
            "n_frequency_groups": len(order),
            "minimum_exact_group_n": int(exact_rows["n_students"].min()),
            "minimum_exact_group_clusters": int(exact_rows["n_clusters"].min()),
            "tail_n": int(len(tail)),
            "tail_clusters": int(tail[cluster_col].nunique()),
            "minimum_adjacent_pair_overlap_clusters": int(adjacent.min()),
            "median_adjacent_pair_overlap_clusters": float(adjacent.median()),
            "minimum_all_pair_overlap_clusters": int(all_pairs.min()),
            "median_all_pair_overlap_clusters": float(all_pairs.median()),
        })
    return pd.DataFrame(rows)


def group_outcome_summary(
    df: pd.DataFrame,
    *,
    group_col: str,
    group_order: Sequence[str],
    outcome_col: str,
    pass_col: str | None = None,
) -> pd.DataFrame:
    """Summarise continuous and optional binary outcomes by ordered group.

    Parameters
    ----------
    df : pandas.DataFrame
        Analytical table.
    group_col : str
        Group column.
    group_order : sequence of str
        Ordered labels to report.
    outcome_col : str
        Continuous outcome.
    pass_col : str or None, default=None
        Optional binary outcome coded 0/1.

    Returns
    -------
    pandas.DataFrame
        Sample sizes, continuous moments/95 percent CIs, and optional rates.
    """
    required = [group_col, outcome_col] + ([pass_col] if pass_col else [])
    _require(df, required)
    labels = df[group_col].astype("string")
    rows = []
    for group in [str(value) for value in group_order]:
        subset = df.loc[labels.eq(group)]
        outcome = pd.to_numeric(subset[outcome_col], errors="coerce").dropna()
        mean = float(outcome.mean()) if len(outcome) else np.nan
        sd = float(outcome.std(ddof=1)) if len(outcome) > 1 else np.nan
        se = sd / math.sqrt(len(outcome)) if len(outcome) > 1 else np.nan
        row = {
            "group": group,
            "n": int(len(subset)),
            "n_outcome": int(len(outcome)),
            "outcome_mean": mean,
            "outcome_sd": sd,
            "outcome_ci95_low": mean - 1.96 * se if np.isfinite(se) else np.nan,
            "outcome_ci95_high": mean + 1.96 * se if np.isfinite(se) else np.nan,
        }
        if pass_col:
            binary = pd.to_numeric(subset[pass_col], errors="coerce").dropna()
            rate = float(binary.mean()) if len(binary) else np.nan
            bse = math.sqrt(rate * (1 - rate) / len(binary)) if len(binary) else np.nan
            row.update({
                "n_binary": int(len(binary)),
                "binary_rate": rate,
                "binary_ci95_low": max(0.0, rate - 1.96 * bse) if np.isfinite(bse) else np.nan,
                "binary_ci95_high": min(1.0, rate + 1.96 * bse) if np.isfinite(bse) else np.nan,
            })
        rows.append(row)
    return pd.DataFrame(rows)


def fixed_effect_group_comparisons(
    df: pd.DataFrame,
    *,
    group_col: str,
    group_order: Sequence[str],
    outcome_col: str,
    fixed_effect_col: str,
    cluster_col: str,
    categorical_covariates: Sequence[str] = (),
    alpha: float = 0.05,
    multiplicity_method: str = "holm",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Estimate omnibus and all-pair contrasts from one clustered FE model.

    Parameters
    ----------
    df : pandas.DataFrame
        Table containing model variables.
    group_col : str
        Categorical exposure/group column.
    group_order : sequence of str
        Ordered labels; the first is the reference category.
    outcome_col : str
        Continuous or 0/1 outcome analysed with OLS.
    fixed_effect_col : str
        Categorical fixed-effect context.
    cluster_col : str
        Cluster-robust covariance identifier.
    categorical_covariates : sequence of str, default=()
        Additional categorical adjustment variables.
    alpha : float, default=0.05
        Two-sided confidence/rejection level.
    multiplicity_method : str, default='holm'
        statsmodels multiplicity-adjustment method.

    Returns
    -------
    tuple of pandas.DataFrame
        Pairwise contrasts, omnibus joint test, and model metadata.

    Notes
    -----
    A 0/1 outcome yields a linear-probability model. Fixed effects and clustered
    covariance do not address unmeasured confounding.
    """
    order = [str(group) for group in group_order]
    if len(order) < 2 or len(order) != len(set(order)):
        raise ValueError("group_order must contain at least two unique labels")
    names = [group_col, outcome_col, fixed_effect_col, cluster_col, *categorical_covariates]
    for name in names:
        _formula_name(name)
    _require(df, names)
    d = df.dropna(subset=names).copy()
    d[group_col] = d[group_col].astype(str)
    missing = [group for group in order if group not in set(d[group_col])]
    if missing:
        raise ValueError(f"group_order contains unobserved groups: {missing}")
    d = d.loc[d[group_col].isin(order)].copy()
    d[group_col] = pd.Categorical(d[group_col], categories=order, ordered=True)

    reference = order[0]
    group_term = f"C({group_col}, Treatment(reference='{reference}'))"
    formula = f"{outcome_col} ~ {group_term} + C({fixed_effect_col})"
    if categorical_covariates:
        formula += " + " + " + ".join(f"C({name})" for name in categorical_covariates)
    model = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d[cluster_col]}
    )
    param_names = list(model.params.index)

    def coefficient(group: str) -> str | None:
        if group == reference:
            return None
        name = f"{group_term}[T.{group}]"
        return name if name in param_names else None

    rows, raw_p = [], []
    for i, group1 in enumerate(order):
        for j in range(i + 1, len(order)):
            group2 = order[j]
            contrast = np.zeros(len(param_names))
            name1, name2 = coefficient(group1), coefficient(group2)
            if name1:
                contrast[param_names.index(name1)] += 1
            if name2:
                contrast[param_names.index(name2)] -= 1
            test = model.t_test(contrast)
            ci = np.asarray(test.conf_int(alpha=alpha)).reshape(-1, 2)[0]
            p_value = float(np.asarray(test.pvalue).reshape(-1)[0])
            raw_p.append(p_value)
            rows.append({
                "group1": group1,
                "group2": group2,
                "estimate_group1_minus_group2": float(np.asarray(test.effect).reshape(-1)[0]),
                "cluster_robust_se": float(np.asarray(test.sd).reshape(-1)[0]),
                "ci_low": float(ci[0]),
                "ci_high": float(ci[1]),
                "p_raw": p_value,
                "adjacent_groups": bool(j == i + 1),
            })
    reject, adjusted, _, _ = multipletests(raw_p, alpha=alpha, method=multiplicity_method)
    for index, row in enumerate(rows):
        row["p_adjusted"] = float(adjusted[index])
        row["reject_adjusted"] = bool(reject[index])
        row["n"] = int(model.nobs)
        row["n_clusters"] = int(d[cluster_col].nunique())

    coefficient_names = [coefficient(group) for group in order[1:]]
    coefficient_names = [name for name in coefficient_names if name]
    restriction = np.zeros((len(coefficient_names), len(param_names)))
    for index, name in enumerate(coefficient_names):
        restriction[index, param_names.index(name)] = 1
    joint = model.f_test(restriction)
    omnibus = pd.DataFrame([{
        "null_hypothesis": "equal adjusted outcomes across listed groups",
        "test_statistic": float(np.asarray(joint.fvalue).reshape(-1)[0]),
        "df_num": int(len(coefficient_names)),
        "p_value": float(np.asarray(joint.pvalue).reshape(-1)[0]),
        "n": int(model.nobs),
        "n_clusters": int(d[cluster_col].nunique()),
    }])
    info = pd.DataFrame([{
        "formula": formula,
        "reference_group": reference,
        "n": int(model.nobs),
        "n_groups": int(len(order)),
        "n_fixed_effect_levels": int(d[fixed_effect_col].nunique()),
        "n_clusters": int(d[cluster_col].nunique()),
        "cluster_col": cluster_col,
        "multiplicity_method": multiplicity_method,
        "alpha": float(alpha),
    }])
    return pd.DataFrame(rows), omnibus, info



def fixed_effect_logistic_group_comparisons(
    df: pd.DataFrame,
    *,
    group_col: str,
    group_order: Sequence[str],
    outcome_col: str,
    fixed_effect_col: str,
    cluster_col: str,
    categorical_covariates: Sequence[str] = (),
    alpha: float = 0.05,
    multiplicity_method: str = "holm",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Estimate pairwise odds ratios from a clustered fixed-effect logit.

    Parameters
    ----------
    df : pandas.DataFrame
        Analytical table containing a binary 0/1 outcome and model variables.
    group_col : str
        Categorical exposure/group column.
    group_order : sequence of str
        Ordered labels; the first is the regression reference category.
    outcome_col : str
        Binary outcome coded 0/1.
    fixed_effect_col : str
        Categorical fixed-effect context.
    cluster_col : str
        Cluster identifier for the sandwich covariance estimator.
    categorical_covariates : sequence of str, default=()
        Additional categorical adjustment variables.
    alpha : float, default=0.05
        Two-sided confidence and rejection level.
    multiplicity_method : str, default='holm'
        Method passed to statsmodels multipletests for pairwise p-values.

    Returns
    -------
    tuple of pandas.DataFrame
        Pairwise log-odds differences and odds ratios, omnibus group test, and
        model metadata.

    Notes
    -----
    Odds ratios are conditional model contrasts and are not risk ratios. Sparse
    or separated outcome patterns can make logistic estimates unstable; callers
    should inspect counts and confidence intervals before interpretation.
    """
    order = [str(group) for group in group_order]
    if len(order) < 2 or len(order) != len(set(order)):
        raise ValueError("group_order must contain at least two unique labels")
    names = [group_col, outcome_col, fixed_effect_col, cluster_col, *categorical_covariates]
    for name in names:
        _formula_name(name)
    _require(df, names)

    d = df.dropna(subset=names).copy()
    y = pd.to_numeric(d[outcome_col], errors="coerce")
    valid = y.isin([0, 1])
    d = d.loc[valid].copy()
    d[outcome_col] = y.loc[valid].astype(float)
    d[group_col] = d[group_col].astype(str)
    missing = [group for group in order if group not in set(d[group_col])]
    if missing:
        raise ValueError(f"group_order contains unobserved groups: {missing}")
    d = d.loc[d[group_col].isin(order)].copy()
    d[group_col] = pd.Categorical(d[group_col], categories=order, ordered=True)

    reference = order[0]
    group_term = f"C({group_col}, Treatment(reference='{reference}'))"
    formula = f"{outcome_col} ~ {group_term} + C({fixed_effect_col})"
    if categorical_covariates:
        formula += " + " + " + ".join(f"C({name})" for name in categorical_covariates)

    model = smf.glm(formula, data=d, family=sm.families.Binomial()).fit(
        cov_type="cluster",
        cov_kwds={"groups": d[cluster_col]},
        maxiter=200,
    )
    param_names = list(model.params.index)

    def coefficient(group: str) -> str | None:
        if group == reference:
            return None
        name = f"{group_term}[T.{group}]"
        return name if name in param_names else None

    rows: list[dict[str, object]] = []
    raw_p: list[float] = []
    for i, group1 in enumerate(order):
        for j in range(i + 1, len(order)):
            group2 = order[j]
            contrast = np.zeros(len(param_names))
            name1, name2 = coefficient(group1), coefficient(group2)
            if name1:
                contrast[param_names.index(name1)] += 1
            if name2:
                contrast[param_names.index(name2)] -= 1
            test = model.t_test(contrast)
            log_or = float(np.asarray(test.effect).reshape(-1)[0])
            se = float(np.asarray(test.sd).reshape(-1)[0])
            p_value = float(np.asarray(test.pvalue).reshape(-1)[0])
            ci = np.asarray(test.conf_int(alpha=alpha)).reshape(-1, 2)[0]
            raw_p.append(p_value)
            rows.append(
                {
                    "group1": group1,
                    "group2": group2,
                    "log_odds_difference_group1_minus_group2": log_or,
                    "odds_ratio_group1_vs_group2": float(np.exp(log_or)),
                    "cluster_robust_se_log_odds": se,
                    "or_ci_low": float(np.exp(ci[0])),
                    "or_ci_high": float(np.exp(ci[1])),
                    "p_raw": p_value,
                    "adjacent_groups": bool(j == i + 1),
                }
            )

    reject, adjusted, _, _ = multipletests(
        raw_p, alpha=alpha, method=multiplicity_method
    )
    for index, row in enumerate(rows):
        row["p_adjusted"] = float(adjusted[index])
        row["reject_adjusted"] = bool(reject[index])
        row["n"] = int(model.nobs)
        row["n_clusters"] = int(d[cluster_col].nunique())

    coefficient_names = [coefficient(group) for group in order[1:]]
    coefficient_names = [name for name in coefficient_names if name]
    restriction = np.zeros((len(coefficient_names), len(param_names)))
    for index, name in enumerate(coefficient_names):
        restriction[index, param_names.index(name)] = 1
    joint = model.wald_test(restriction, scalar=True)

    omnibus = pd.DataFrame(
        [
            {
                "null_hypothesis": "equal adjusted log odds across listed groups",
                "test_statistic": float(np.asarray(joint.statistic).reshape(-1)[0]),
                "df_num": int(len(coefficient_names)),
                "p_value": float(np.asarray(joint.pvalue).reshape(-1)[0]),
                "n": int(model.nobs),
                "n_clusters": int(d[cluster_col].nunique()),
            }
        ]
    )
    info = pd.DataFrame(
        [
            {
                "formula": formula,
                "reference_group": reference,
                "n": int(model.nobs),
                "n_groups": int(len(order)),
                "n_fixed_effect_levels": int(d[fixed_effect_col].nunique()),
                "n_clusters": int(d[cluster_col].nunique()),
                "cluster_col": cluster_col,
                "multiplicity_method": multiplicity_method,
                "alpha": float(alpha),
                "converged": bool(model.converged),
            }
        ]
    )
    return pd.DataFrame(rows), omnibus, info



def fixed_effect_logistic_adjusted_probabilities(
    df: pd.DataFrame,
    *,
    group_col: str,
    group_order: Sequence[str],
    outcome_col: str,
    fixed_effect_col: str,
    cluster_col: str,
    categorical_covariates: Sequence[str] = (),
) -> pd.DataFrame:
    """Estimate model-standardized probabilities from a clustered FE logit.

    Parameters
    ----------
    df : pandas.DataFrame
        Analytical table containing a binary 0/1 outcome and model variables.
    group_col : str
        Categorical exposure/group column.
    group_order : sequence of str
        Ordered labels; the first is the regression reference category.
    outcome_col : str
        Binary outcome coded 0/1.
    fixed_effect_col : str
        Categorical fixed-effect context.
    cluster_col : str
        Cluster identifier for the sandwich covariance estimator.
    categorical_covariates : sequence of str, default=()
        Additional categorical adjustment variables.

    Returns
    -------
    pandas.DataFrame
        One row per group with the observed probability and the
        model-standardized adjusted probability.

    Notes
    -----
    Standardization uses the empirical distribution of fixed-effect levels and
    covariates in the fitted model sample. For each group, all observations are
    counterfactually assigned that group while every other observed model
    variable is retained, and the resulting fitted probabilities are averaged.
    The estimates are descriptive model-adjusted associations, not causal risks.
    """
    order = [str(group) for group in group_order]
    if len(order) < 2 or len(order) != len(set(order)):
        raise ValueError("group_order must contain at least two unique labels")
    names = [group_col, outcome_col, fixed_effect_col, cluster_col, *categorical_covariates]
    for name in names:
        _formula_name(name)
    _require(df, names)

    d = df.dropna(subset=names).copy()
    y = pd.to_numeric(d[outcome_col], errors="coerce")
    valid = y.isin([0, 1])
    d = d.loc[valid].copy()
    d[outcome_col] = y.loc[valid].astype(float)
    d[group_col] = d[group_col].astype(str)
    missing = [group for group in order if group not in set(d[group_col])]
    if missing:
        raise ValueError(f"group_order contains unobserved groups: {missing}")
    d = d.loc[d[group_col].isin(order)].copy()
    d[group_col] = pd.Categorical(d[group_col], categories=order, ordered=True)

    reference = order[0]
    group_term = f"C({group_col}, Treatment(reference='{reference}'))"
    formula = f"{outcome_col} ~ {group_term} + C({fixed_effect_col})"
    if categorical_covariates:
        formula += " + " + " + ".join(f"C({name})" for name in categorical_covariates)

    model = smf.glm(formula, data=d, family=sm.families.Binomial()).fit(
        cov_type="cluster",
        cov_kwds={"groups": d[cluster_col]},
        maxiter=200,
    )

    rows: list[dict[str, object]] = []
    observed_labels = d[group_col].astype("string")
    for group in order:
        counterfactual = d.copy()
        counterfactual[group_col] = pd.Categorical(
            [group] * len(counterfactual),
            categories=order,
            ordered=True,
        )
        fitted = np.asarray(model.predict(counterfactual), dtype=float)
        observed = pd.to_numeric(
            d.loc[observed_labels.eq(group), outcome_col], errors="coerce"
        ).dropna()
        rows.append(
            {
                "group": group,
                "observed_probability": float(observed.mean()),
                "adjusted_probability": float(np.mean(fitted)),
                "n_observed_group": int(len(observed)),
                "n_standardization_sample": int(model.nobs),
                "n_clusters": int(d[cluster_col].nunique()),
                "converged": bool(model.converged),
                "formula": formula,
            }
        )
    return pd.DataFrame(rows)

def outcome_state_composition(
    df: pd.DataFrame,
    *,
    group_col: str,
    group_order: Sequence[str],
    state_col: str,
    state_order: Sequence[str],
) -> pd.DataFrame:
    """Tabulate academic-result state composition within exposure groups.

    Parameters
    ----------
    df : pandas.DataFrame
        Table containing group and state columns.
    group_col : str
        Exposure/group column.
    group_order : sequence of str
        Ordered group labels.
    state_col : str
        Academic-result state column.
    state_order : sequence of str
        Ordered states to report.

    Returns
    -------
    pandas.DataFrame
        Long-format counts and within-group shares.
    """
    _require(df, [group_col, state_col])
    groups = df[group_col].astype("string")
    states = df[state_col].astype("string")
    rows = []
    for group in [str(value) for value in group_order]:
        mask = groups.eq(group)
        counts = states.loc[mask].value_counts()
        denominator = int(mask.sum())
        for state in [str(value) for value in state_order]:
            n = int(counts.get(state, 0))
            rows.append({
                "group": group,
                "state": state,
                "n": n,
                "group_n": denominator,
                "share_within_group": float(n / denominator) if denominator else np.nan,
            })
    return pd.DataFrame(rows)


def distribution_profile(
    df: pd.DataFrame,
    *,
    group_col: str,
    group_order: Sequence[str],
    outcome_col: str,
    pass_col: str | None = None,
    quantiles: Sequence[float] = (0.10, 0.25, 0.50, 0.75, 0.90),
) -> pd.DataFrame:
    """Describe where a continuous outcome distribution differs by group.

    Parameters
    ----------
    df : pandas.DataFrame
        Analytical table.
    group_col : str
        Exposure/group column.
    group_order : sequence of str
        Ordered group labels.
    outcome_col : str
        Continuous outcome column.
    pass_col : str or None, default=None
        Optional 0/1 pass indicator for descriptive conditional means.
    quantiles : sequence of float, default=(0.10, 0.25, 0.50, 0.75, 0.90)
        Quantile probabilities strictly between zero and one.

    Returns
    -------
    pandas.DataFrame
        One row per group with requested quantiles and optional conditional means.
    """
    required = [group_col, outcome_col] + ([pass_col] if pass_col else [])
    _require(df, required)
    q_values = [float(value) for value in quantiles]
    if not q_values or any(value <= 0 or value >= 1 for value in q_values):
        raise ValueError("quantiles must be strictly between 0 and 1")
    labels = df[group_col].astype("string")
    rows = []
    for group in [str(value) for value in group_order]:
        subset = df.loc[labels.eq(group)]
        outcome = pd.to_numeric(subset[outcome_col], errors="coerce").dropna()
        row = {"group": group, "n": int(len(subset)), "n_outcome": int(len(outcome))}
        for value in q_values:
            row[f"q{int(round(value * 100)):02d}"] = (
                float(outcome.quantile(value)) if len(outcome) else np.nan
            )
        if pass_col:
            passed = pd.to_numeric(subset[pass_col], errors="coerce")
            pass_y = pd.to_numeric(
                subset.loc[passed.eq(1), outcome_col], errors="coerce"
            ).dropna()
            nonpass_y = pd.to_numeric(
                subset.loc[passed.eq(0), outcome_col], errors="coerce"
            ).dropna()
            row["mean_outcome_among_pass"] = float(pass_y.mean()) if len(pass_y) else np.nan
            row["mean_outcome_among_nonpass"] = (
                float(nonpass_y.mean()) if len(nonpass_y) else np.nan
            )
        rows.append(row)
    return pd.DataFrame(rows)


def pairwise_effect_matrix(
    pairwise: pd.DataFrame,
    *,
    group_order: Sequence[str],
    estimate_col: str = "estimate_group1_minus_group2",
    group1_col: str = "group1",
    group2_col: str = "group2",
) -> pd.DataFrame:
    """Convert long pairwise contrasts into a signed symmetric matrix.

    Parameters
    ----------
    pairwise : pandas.DataFrame
        Long-format pairwise contrasts using a group1-minus-group2 convention.
    group_order : sequence of str
        Ordered group labels for rows and columns.
    estimate_col : str, default='estimate_group1_minus_group2'
        Signed contrast-estimate column.
    group1_col : str, default='group1'
        First group-label column.
    group2_col : str, default='group2'
        Second group-label column.

    Returns
    -------
    pandas.DataFrame
        Wide signed matrix with a leading group column and zero diagonal.
    """
    _require(pairwise, [estimate_col, group1_col, group2_col])
    order = [str(group) for group in group_order]
    matrix = pd.DataFrame(np.nan, index=order, columns=order)
    for group in order:
        matrix.loc[group, group] = 0.0
    for _, row in pairwise.iterrows():
        group1, group2 = str(row[group1_col]), str(row[group2_col])
        if group1 in order and group2 in order:
            estimate = float(row[estimate_col])
            matrix.loc[group1, group2] = estimate
            matrix.loc[group2, group1] = -estimate
    return matrix.reset_index(names="group")



def mixture_component_density(
    df: pd.DataFrame,
    *,
    group_col: str,
    group_order: Sequence[str],
    outcome_col: str,
    component_col: str,
    component_order: Sequence[str],
    grid_size: int = 256,
    cut: float = 3.0,
    min_bandwidth: float = 1e-3,
) -> pd.DataFrame:
    """Build stacked KDE components whose areas equal observed group shares.

    A common Gaussian-kernel bandwidth is used for all components within each
    group. Each component density is divided by the full group size rather than
    the component size, so integrating a component over the x-axis yields its
    observed within-group share and summing components reconstructs the group's
    total kernel density.

    Parameters
    ----------
    df : pandas.DataFrame
        Analytical table containing group, continuous outcome, and component
        state columns.
    group_col : str
        Column identifying the ridgeline/exposure groups.
    group_order : sequence of str
        Ordered group labels to include.
    outcome_col : str
        Continuous variable whose distribution is estimated.
    component_col : str
        Column identifying stacked outcome components.
    component_order : sequence of str
        Ordered component labels to include.
    grid_size : int, default=256
        Number of common x-grid points used for every group.
    cut : float, default=3.0
        Number of maximum group bandwidths added beyond the observed global
        minimum and maximum.
    min_bandwidth : float, default=1e-3
        Lower bound for the Gaussian kernel bandwidth.

    Returns
    -------
    pandas.DataFrame
        Long-format density grid containing group, component, x,
        density_component, density_total, component_share, n_group,
        n_component, and bandwidth.

    Notes
    -----
    This is a descriptive visualization transform. Administrative or imputed
    values retain whatever meaning they have in the supplied outcome column.
    """
    if grid_size < 32:
        raise ValueError("grid_size must be at least 32")
    if cut < 0:
        raise ValueError("cut must be non-negative")
    if min_bandwidth <= 0:
        raise ValueError("min_bandwidth must be positive")
    _require(df, [group_col, outcome_col, component_col])

    groups = [str(value) for value in group_order]
    components = [str(value) for value in component_order]
    work = df[[group_col, outcome_col, component_col]].copy()
    work[group_col] = work[group_col].astype("string")
    work[component_col] = work[component_col].astype("string")
    work[outcome_col] = pd.to_numeric(work[outcome_col], errors="coerce")
    work = work.loc[
        work[group_col].isin(groups)
        & work[component_col].isin(components)
        & work[outcome_col].notna()
    ].copy()
    if work.empty:
        return pd.DataFrame(
            columns=[
                "group", "component", "x", "density_component",
                "density_total", "component_share", "n_group",
                "n_component", "bandwidth",
            ]
        )

    bandwidths: dict[str, float] = {}
    for group in groups:
        values = work.loc[work[group_col].eq(group), outcome_col].to_numpy(float)
        if len(values) == 0:
            continue
        sd = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
        if not np.isfinite(sd) or sd <= 0:
            iqr = (
                float(np.subtract(*np.percentile(values, [75, 25])))
                if len(values) > 1
                else 0.0
            )
            scale = iqr / 1.349 if np.isfinite(iqr) and iqr > 0 else 1.0
        else:
            scale = sd
        bandwidths[group] = max(
            float(scale * len(values) ** (-0.2)), min_bandwidth
        )

    maximum_bandwidth = max(bandwidths.values())
    global_values = work[outcome_col].to_numpy(float)
    x_min = float(np.min(global_values) - cut * maximum_bandwidth)
    x_max = float(np.max(global_values) + cut * maximum_bandwidth)
    grid = np.linspace(x_min, x_max, int(grid_size))
    normalizer = math.sqrt(2.0 * math.pi)

    rows: list[pd.DataFrame] = []
    for group in groups:
        subset = work.loc[work[group_col].eq(group)]
        if subset.empty:
            continue
        n_group = int(len(subset))
        bandwidth = bandwidths[group]
        component_density: dict[str, np.ndarray] = {}
        for component in components:
            values = subset.loc[
                subset[component_col].eq(component), outcome_col
            ].to_numpy(float)
            if len(values):
                z = (grid[:, None] - values[None, :]) / bandwidth
                density = np.exp(-0.5 * z**2).sum(axis=1)
                density /= n_group * bandwidth * normalizer
            else:
                density = np.zeros_like(grid)
            component_density[component] = density

        total_density = np.sum(
            np.vstack([component_density[c] for c in components]), axis=0
        )
        for component in components:
            n_component = int(subset[component_col].eq(component).sum())
            rows.append(
                pd.DataFrame(
                    {
                        "group": group,
                        "component": component,
                        "x": grid,
                        "density_component": component_density[component],
                        "density_total": total_density,
                        "component_share": n_component / n_group,
                        "n_group": n_group,
                        "n_component": n_component,
                        "bandwidth": bandwidth,
                    }
                )
            )
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
