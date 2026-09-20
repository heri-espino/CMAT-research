#!/usr/bin/env python3
"""Paper 2.1 dual-outcome analysis after the visit grouping has been frozen.

Primary positive-attendance groups are read conceptually from the documented
Paper 2.1 decision: 1, 2, 3, 4, 5, 6+. A more granular 1..6, 7+ grouping is
retained as an exploratory sensitivity.

The analysis is observational. Reported contrasts are associations, not causal
effects of additional CMAT visits.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

try:
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_primary_outcomes
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2.1 requires the shared editable library. From the repository root run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"\n'
        f"Original import error: {exc}"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "results" / "paper21" / "tables"
GROUP_SPEC = REPO_ROOT / "paper" / "visit_grouping_spec.json"


def _save(frame: pd.DataFrame, name: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES_DIR / name, index=False)


def _group_positive(visits: pd.Series, top_exact: int) -> pd.Categorical:
    labels = visits.astype(int).astype(str)
    labels = labels.where(visits <= top_exact, f"{top_exact + 1}+")
    order = [str(k) for k in range(1, top_exact + 1)] + [f"{top_exact + 1}+"]
    return pd.Categorical(labels, categories=order, ordered=True)


def _descriptives(d: pd.DataFrame, group_col: str, group_order: list[str], spec: str) -> pd.DataFrame:
    rows = []
    for group in group_order:
        g = d.loc[d[group_col].astype(str) == group].copy()
        z = g["Z_GRADE_PRIMARY"].dropna().astype(float)
        n_z = len(z)
        sd = float(z.std(ddof=1)) if n_z > 1 else np.nan
        se = sd / math.sqrt(n_z) if n_z > 1 else np.nan
        p = g["PASS"].dropna().astype(float)
        pass_rate = float(p.mean()) if len(p) else np.nan
        pass_se = math.sqrt(pass_rate * (1 - pass_rate) / len(p)) if len(p) and np.isfinite(pass_rate) else np.nan
        rows.append({
            "specification": spec,
            "group": group,
            "n": int(len(g)),
            "mean_z": float(z.mean()) if n_z else np.nan,
            "sd_z": sd,
            "z_ci95_low": float(z.mean() - 1.96 * se) if np.isfinite(se) else np.nan,
            "z_ci95_high": float(z.mean() + 1.96 * se) if np.isfinite(se) else np.nan,
            "pass_rate": pass_rate,
            "pass_ci95_low": max(0.0, pass_rate - 1.96 * pass_se) if np.isfinite(pass_se) else np.nan,
            "pass_ci95_high": min(1.0, pass_rate + 1.96 * pass_se) if np.isfinite(pass_se) else np.nan,
        })
    return pd.DataFrame(rows)


def _fit_pairwise(
    d: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    outcome_col: str,
    outcome_label: str,
    specification: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    x = d.dropna(subset=[group_col, outcome_col, "CLASSROOM_ID", "CLAVECARRERA"]).copy()
    x[group_col] = pd.Categorical(x[group_col].astype(str), categories=group_order, ordered=True)
    reference = group_order[0]
    term = f"C({group_col}, Treatment(reference='{reference}'))"
    formula = f"{outcome_col} ~ {term} + C(CLASSROOM_ID) + C(CLAVECARRERA)"
    model = smf.ols(formula, data=x).fit(
        cov_type="cluster",
        cov_kwds={"groups": x["CLASSROOM_ID"]},
    )

    names = list(model.params.index)

    def coef_name(group: str) -> str | None:
        if group == reference:
            return None
        candidate = f"{term}[T.{group}]"
        return candidate if candidate in names else None

    tmp = []
    raw_ps = []
    for i, g1 in enumerate(group_order):
        for g2 in group_order[i + 1:]:
            R = np.zeros(len(names), dtype=float)
            n1 = coef_name(g1)
            n2 = coef_name(g2)
            if n1 is not None:
                R[names.index(n1)] += 1.0
            if n2 is not None:
                R[names.index(n2)] -= 1.0
            test = model.t_test(R)
            est = float(np.asarray(test.effect).reshape(-1)[0])
            se = float(np.asarray(test.sd).reshape(-1)[0])
            p = float(np.asarray(test.pvalue).reshape(-1)[0])
            ci = np.asarray(test.conf_int(alpha=0.05)).reshape(-1, 2)[0]
            raw_ps.append(p)
            tmp.append((g1, g2, est, se, p, float(ci[0]), float(ci[1])))

    holm = multipletests(raw_ps, alpha=0.05, method="holm")
    rows = []
    for j, (g1, g2, est, se, p, lo, hi) in enumerate(tmp):
        rows.append({
            "specification": specification,
            "outcome": outcome_label,
            "group1": g1,
            "group2": g2,
            "adjusted_difference_group1_minus_group2": est,
            "cluster_robust_se": se,
            "ci95_low": lo,
            "ci95_high": hi,
            "p_raw": p,
            "p_holm": float(holm[1][j]),
            "reject_holm_0_05": bool(holm[0][j]),
            "adjacent_groups": bool(j is not None and group_order.index(g2) - group_order.index(g1) == 1),
            "n": int(model.nobs),
            "n_instructor_period_groups": int(x["CLASSROOM_ID"].nunique()),
        })

    # Joint null: every non-reference frequency coefficient is zero.
    coefficient_names = [coef_name(g) for g in group_order[1:]]
    coefficient_names = [n for n in coefficient_names if n is not None]
    R = np.zeros((len(coefficient_names), len(names)), dtype=float)
    for row_i, n in enumerate(coefficient_names):
        R[row_i, names.index(n)] = 1.0
    omnibus = model.f_test(R)
    omnibus_frame = pd.DataFrame([{
        "specification": specification,
        "outcome": outcome_label,
        "null_hypothesis": "equal adjusted outcomes across all positive attendance-frequency groups",
        "test_statistic": float(np.asarray(omnibus.fvalue).reshape(-1)[0]),
        "df_num": int(len(coefficient_names)),
        "p_value": float(np.asarray(omnibus.pvalue).reshape(-1)[0]),
        "n": int(model.nobs),
        "n_instructor_period_groups": int(x["CLASSROOM_ID"].nunique()),
        "covariance": "cluster-robust by instructor-period group",
        "adjustment": "instructor-period fixed effects + degree-programme indicators",
    }])
    return pd.DataFrame(rows), omnibus_frame


def _benchmark(d: pd.DataFrame, outcome_col: str, outcome_label: str) -> dict[str, object]:
    x = d.dropna(subset=[outcome_col, "CLASSROOM_ID", "CLAVECARRERA"]).copy()
    x["ANY_CMAT"] = (x["VISITS_CMAT_PERIOD"] > 0).astype(int)
    formula = f"{outcome_col} ~ ANY_CMAT + C(CLASSROOM_ID) + C(CLAVECARRERA)"
    model = smf.ols(formula, data=x).fit(
        cov_type="cluster", cov_kwds={"groups": x["CLASSROOM_ID"]}
    )
    return {
        "outcome": outcome_label,
        "comparison": "1+ visits minus 0 visits",
        "adjusted_difference": float(model.params["ANY_CMAT"]),
        "cluster_robust_se": float(model.bse["ANY_CMAT"]),
        "ci95_low": float(model.conf_int().loc["ANY_CMAT", 0]),
        "ci95_high": float(model.conf_int().loc["ANY_CMAT", 1]),
        "p_value": float(model.pvalues["ANY_CMAT"]),
        "n": int(model.nobs),
        "n_instructor_period_groups": int(x["CLASSROOM_ID"].nunique()),
    }


def _nonpass_composition(d: pd.DataFrame, group_col: str, group_order: list[str], spec: str) -> pd.DataFrame:
    x = d.copy()
    x["OUTCOME_STATE"] = np.select(
        [
            x["PASS"].eq(1),
            x["GRADE_CLASS"].eq("numeric") & x["PASS"].eq(0),
            x["GRADE_CLASS"].eq("adverse"),
        ],
        [
            "pass",
            "numeric_grade_below_7.5",
            "BA_BV_RT",
        ],
        default="other",
    )
    rows = []
    for group in group_order:
        g = x.loc[x[group_col].astype(str) == group].copy()
        denom = len(g)
        counts = g["OUTCOME_STATE"].value_counts()
        for state in ["pass", "numeric_grade_below_7.5", "BA_BV_RT"]:
            n = int(counts.get(state, 0))
            rows.append({
                "specification": spec,
                "group": group,
                "outcome_state": state,
                "n": n,
                "group_n": int(denom),
                "share_within_group": float(n / denom) if denom else np.nan,
            })
    return pd.DataFrame(rows)


def _distribution_profile(
    d: pd.DataFrame,
    group_col: str,
    group_order: list[str],
    spec: str,
) -> pd.DataFrame:
    """Describe where the continuous outcome distribution moves, not only its mean."""
    rows = []
    for group in group_order:
        g = d.loc[d[group_col].astype(str) == group].copy()
        z = g["Z_GRADE_PRIMARY"].dropna().astype(float)
        passing_z = g.loc[g["PASS"].eq(1), "Z_GRADE_PRIMARY"].dropna().astype(float)
        nonpassing_z = g.loc[g["PASS"].eq(0), "Z_GRADE_PRIMARY"].dropna().astype(float)
        rows.append({
            "specification": spec,
            "group": group,
            "n": int(len(g)),
            "z_q10": float(z.quantile(0.10)) if len(z) else np.nan,
            "z_q25": float(z.quantile(0.25)) if len(z) else np.nan,
            "z_median": float(z.quantile(0.50)) if len(z) else np.nan,
            "z_q75": float(z.quantile(0.75)) if len(z) else np.nan,
            "z_q90": float(z.quantile(0.90)) if len(z) else np.nan,
            "mean_z_among_pass": float(passing_z.mean()) if len(passing_z) else np.nan,
            "mean_z_among_nonpass": float(nonpassing_z.mean()) if len(nonpassing_z) else np.nan,
            "n_pass": int(g["PASS"].eq(1).sum()),
            "n_nonpass": int(g["PASS"].eq(0).sum()),
            "interpretation": "descriptive distribution profile; conditional means are not causal subgroup effects",
        })
    return pd.DataFrame(rows)


def _effect_matrix(pairwise: pd.DataFrame, group_order: list[str], value_col: str, outcome: str) -> pd.DataFrame:
    mat = pd.DataFrame(np.nan, index=group_order, columns=group_order)
    for g in group_order:
        mat.loc[g, g] = 0.0
    for row in pairwise.itertuples(index=False):
        est = float(getattr(row, value_col))
        mat.loc[str(row.group1), str(row.group2)] = est
        mat.loc[str(row.group2), str(row.group1)] = -est
    out = mat.reset_index().rename(columns={"index": "group"})
    out.insert(0, "outcome", outcome)
    return out


def check_environment() -> int:
    required = [
        REPO_ROOT / "paper" / "VISIT_GROUPING_DECISION.md",
        GROUP_SPEC,
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
    ]
    missing = [str(p.relative_to(REPO_ROOT)) for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing Paper 2.1 outcome-analysis paths: " + ", ".join(missing))
    spec = json.loads(GROUP_SPEC.read_text(encoding="utf-8"))
    if spec["positive_user_primary_groups"] != ["1", "2", "3", "4", "5", "6+"]:
        raise SystemExit("Paper 2.1 primary visit grouping differs from the frozen decision.")
    print("Paper 2.1 dual-outcome analysis check: OK")
    print("Frozen primary groups: 1, 2, 3, 4, 5, 6+")
    print("Exploratory sensitivity: 1, 2, 3, 4, 5, 6, 7+")
    return 0


def run(args: argparse.Namespace) -> int:
    base = get_study_config(REPO_ROOT)
    materias = (args.materias or base.materias_path).expanduser().resolve()
    asesorias = (args.asesorias or base.asesorias_path).expanduser().resolve()
    config = replace(base, materias_path=materias, asesorias_path=asesorias)

    data = load_and_clean_inputs(config)
    cohorts = build_study_cohorts(data, config)
    mu = add_primary_outcomes(cohorts["mu_primary"], config)
    mu["PASS"] = mu["PASS"].astype(float)

    benchmark = pd.DataFrame([
        _benchmark(mu, "Z_GRADE_PRIMARY", "continuous_standardised_grade"),
        _benchmark(mu, "PASS", "pass_probability"),
    ])
    _save(benchmark, "10_benchmark_0_vs_1plus.csv")

    users = mu.loc[mu["VISITS_CMAT_PERIOD"] > 0].copy()

    # Primary: 1, 2, 3, 4, 5, 6+
    primary_order = ["1", "2", "3", "4", "5", "6+"]
    users["P21_GROUP"] = _group_positive(users["VISITS_CMAT_PERIOD"], 5)
    primary_desc = _descriptives(users, "P21_GROUP", primary_order, "primary_1_2_3_4_5_6plus")
    _save(primary_desc, "11_primary_group_descriptives.csv")

    z_pair, z_omni = _fit_pairwise(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="primary_1_2_3_4_5_6plus",
    )
    p_pair, p_omni = _fit_pairwise(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="PASS",
        outcome_label="pass_probability",
        specification="primary_1_2_3_4_5_6plus",
    )
    _save(pd.concat([z_omni, p_omni], ignore_index=True), "12_primary_omnibus.csv")
    _save(z_pair, "13_primary_pairwise_continuous.csv")
    _save(p_pair, "14_primary_pairwise_pass.csv")
    _save(_nonpass_composition(users, "P21_GROUP", primary_order, "primary_1_2_3_4_5_6plus"),
          "15_primary_outcome_state_composition.csv")
    _save(
        _distribution_profile(users, "P21_GROUP", primary_order, "primary_1_2_3_4_5_6plus"),
        "15b_primary_distribution_profile.csv",
    )

    cc_pair, cc_omni = _fit_pairwise(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_COMPLETE_CASE",
        outcome_label="numeric_complete_case_standardised_grade",
        specification="primary_1_2_3_4_5_6plus",
    )
    _save(cc_pair, "16_complete_case_pairwise_continuous.csv")
    _save(cc_omni, "17_complete_case_omnibus.csv")

    _save(
        _effect_matrix(z_pair, primary_order, "adjusted_difference_group1_minus_group2",
                       "continuous_standardised_grade"),
        "18_primary_z_heatmap_matrix.csv",
    )
    _save(
        _effect_matrix(p_pair, primary_order, "adjusted_difference_group1_minus_group2",
                       "pass_probability"),
        "19_primary_pass_heatmap_matrix.csv",
    )

    # Exploratory sensitivity: 1, 2, 3, 4, 5, 6, 7+
    sensitivity_order = ["1", "2", "3", "4", "5", "6", "7+"]
    users["P21_GROUP_7P"] = _group_positive(users["VISITS_CMAT_PERIOD"], 6)
    _save(
        _descriptives(users, "P21_GROUP_7P", sensitivity_order, "sensitivity_1_to_6_7plus"),
        "20_sensitivity_7plus_group_descriptives.csv",
    )
    sz_pair, sz_omni = _fit_pairwise(
        users,
        group_col="P21_GROUP_7P",
        group_order=sensitivity_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="sensitivity_1_to_6_7plus",
    )
    sp_pair, sp_omni = _fit_pairwise(
        users,
        group_col="P21_GROUP_7P",
        group_order=sensitivity_order,
        outcome_col="PASS",
        outcome_label="pass_probability",
        specification="sensitivity_1_to_6_7plus",
    )
    _save(pd.concat([sz_omni, sp_omni], ignore_index=True), "21_sensitivity_7plus_omnibus.csv")
    _save(sz_pair, "22_sensitivity_7plus_pairwise_continuous.csv")
    _save(sp_pair, "23_sensitivity_7plus_pairwise_pass.csv")
    _save(
        _nonpass_composition(users, "P21_GROUP_7P", sensitivity_order, "sensitivity_1_to_6_7plus"),
        "24_sensitivity_7plus_outcome_state_composition.csv",
    )
    _save(
        _distribution_profile(users, "P21_GROUP_7P", sensitivity_order, "sensitivity_1_to_6_7plus"),
        "25_sensitivity_7plus_distribution_profile.csv",
    )

    print(f"Paper 2.1 study cohort: N={len(mu):,}")
    print(f"Positive-attendance analysis: N={len(users):,}")
    print("Primary frequency groups: 1, 2, 3, 4, 5, 6+")
    print("Sensitivity groups: 1, 2, 3, 4, 5, 6, 7+")
    print(f"Outputs: {TABLES_DIR}")
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Paper 2.1 dual-outcome frequency analysis.")
    p.add_argument("--materias", type=Path)
    p.add_argument("--asesorias", type=Path)
    p.add_argument("--check", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.check:
        return check_environment()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
