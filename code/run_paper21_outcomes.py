#!/usr/bin/env python3
"""Paper 2.1 dual-outcome analysis using the shared cmat_analysis library.

Paper-specific code constructs the cohort, freezes the documented grouping, and
formats publication outputs. Reusable grouping, outcome-state construction,
clustered fixed-effect comparisons, distribution profiles, and effect matrices
live in cmat_analysis on main.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_academic_outcome_states, add_primary_outcomes
    from cmat_analysis.statistics import (
        add_topcoded_visit_group,
        distribution_profile,
        fixed_effect_group_comparisons,
        group_outcome_summary,
        mixture_component_density,
        outcome_state_composition,
        pairwise_effect_matrix,
    )
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


def _format_descriptives(
    frame: pd.DataFrame,
    *,
    specification: str,
) -> pd.DataFrame:
    out = frame.rename(
        columns={
            "outcome_mean": "mean_z",
            "outcome_sd": "sd_z",
            "outcome_ci95_low": "z_ci95_low",
            "outcome_ci95_high": "z_ci95_high",
            "binary_rate": "pass_rate",
            "binary_ci95_low": "pass_ci95_low",
            "binary_ci95_high": "pass_ci95_high",
        }
    ).copy()
    out.insert(0, "specification", specification)
    return out


def _format_pairwise(
    pairwise: pd.DataFrame,
    info: pd.DataFrame,
    *,
    outcome: str,
    specification: str,
) -> pd.DataFrame:
    out = pairwise.rename(
        columns={
            "estimate_group1_minus_group2": "adjusted_difference_group1_minus_group2",
            "ci_low": "ci95_low",
            "ci_high": "ci95_high",
            "p_adjusted": "p_holm",
            "reject_adjusted": "reject_holm_0_05",
        }
    ).copy()
    out.insert(0, "outcome", outcome)
    out.insert(0, "specification", specification)
    out["n_instructor_period_groups"] = int(info.loc[0, "n_fixed_effect_levels"])
    return out


def _format_omnibus(
    omnibus: pd.DataFrame,
    info: pd.DataFrame,
    *,
    outcome: str,
    specification: str,
) -> pd.DataFrame:
    out = omnibus.copy()
    out.insert(0, "outcome", outcome)
    out.insert(0, "specification", specification)
    out["n_instructor_period_groups"] = int(info.loc[0, "n_fixed_effect_levels"])
    out["covariance"] = f"cluster-robust by {info.loc[0, 'cluster_col']}"
    out["adjustment"] = "instructor-period fixed effects + degree-programme indicators"
    return out


def _fit(
    data: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    outcome_col: str,
    outcome_label: str,
    specification: str,
    cluster_col: str = "CLASSROOM_ID",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    pairwise, omnibus, info = fixed_effect_group_comparisons(
        data,
        group_col=group_col,
        group_order=group_order,
        outcome_col=outcome_col,
        fixed_effect_col="CLASSROOM_ID",
        cluster_col=cluster_col,
        categorical_covariates=["CLAVECARRERA"],
        multiplicity_method="holm",
    )
    return (
        _format_pairwise(
            pairwise, info, outcome=outcome_label, specification=specification
        ),
        _format_omnibus(
            omnibus, info, outcome=outcome_label, specification=specification
        ),
    )


def _benchmark(
    data: pd.DataFrame,
    outcome_col: str,
    outcome_label: str,
    *,
    cluster_col: str = "CLASSROOM_ID",
) -> dict[str, object]:
    x = data.copy()
    x["ATTENDANCE_BINARY_GROUP"] = np.where(
        x["VISITS_CMAT_PERIOD"].gt(0), "1+", "0"
    )
    pairwise, _, info = fixed_effect_group_comparisons(
        x,
        group_col="ATTENDANCE_BINARY_GROUP",
        group_order=["0", "1+"],
        outcome_col=outcome_col,
        fixed_effect_col="CLASSROOM_ID",
        cluster_col=cluster_col,
        categorical_covariates=["CLAVECARRERA"],
    )
    row = pairwise.iloc[0]
    return {
        "outcome": outcome_label,
        "comparison": "1+ visits minus 0 visits",
        "adjusted_difference": -float(row["estimate_group1_minus_group2"]),
        "cluster_robust_se": float(row["cluster_robust_se"]),
        "ci95_low": -float(row["ci_high"]),
        "ci95_high": -float(row["ci_low"]),
        "p_value": float(row["p_raw"]),
        "n": int(row["n"]),
        "n_instructor_period_groups": int(info.loc[0, "n_fixed_effect_levels"]),
        "cluster_col": cluster_col,
        "n_clusters": int(info.loc[0, "n_clusters"]),
    }


def _composition(
    data: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    state_col: str,
    state_order: list[str],
    specification: str,
) -> pd.DataFrame:
    out = outcome_state_composition(
        data,
        group_col=group_col,
        group_order=group_order,
        state_col=state_col,
        state_order=state_order,
    ).rename(columns={"state": "outcome_state"})
    out["outcome_state"] = out["outcome_state"].replace(
        {"numeric_nonpass": "numeric_grade_below_7.5"}
    )
    out.insert(0, "specification", specification)
    return out


def _profile(
    data: pd.DataFrame,
    *,
    group_col: str,
    group_order: list[str],
    outcome_col: str,
    outcome_label: str,
    specification: str,
) -> pd.DataFrame:
    out = distribution_profile(
        data,
        group_col=group_col,
        group_order=group_order,
        outcome_col=outcome_col,
        pass_col="PASS",
    )
    out = out.rename(
        columns={
            "q10": "z_q10",
            "q25": "z_q25",
            "q50": "z_median",
            "q75": "z_q75",
            "q90": "z_q90",
            "mean_outcome_among_pass": "mean_z_among_pass",
            "mean_outcome_among_nonpass": "mean_z_among_nonpass",
        }
    )
    out.insert(0, "outcome", outcome_label)
    out.insert(0, "specification", specification)
    out["interpretation"] = (
        "descriptive distribution profile; conditional means are not causal subgroup effects"
    )
    return out


def _matrix(
    pairwise: pd.DataFrame,
    *,
    group_order: list[str],
    outcome: str,
) -> pd.DataFrame:
    out = pairwise_effect_matrix(
        pairwise,
        group_order=group_order,
        estimate_col="adjusted_difference_group1_minus_group2",
    )
    out.insert(0, "outcome", outcome)
    return out


def _nonpass_management_summary(data: pd.DataFrame) -> pd.DataFrame:
    x = data.loc[data["PASS"].eq(0)].copy()
    x["attendance"] = np.where(x["VISITS_CMAT_PERIOD"].gt(0), "1+", "0")
    token = x["GRADE_TOKEN"].fillna("").astype(str).str.upper()
    rows = []
    for attendance in ["0", "1+"]:
        group = x.loc[x["attendance"].eq(attendance)]
        group_token = token.loc[group.index]
        numeric_n = int(group["GRADE_CLASS"].eq("numeric").sum())
        bv_n = int(group_token.eq("BV").sum())
        rt_n = int(group_token.eq("RT").sum())
        ba_n = int(group_token.eq("BA").sum())
        admin_n = bv_n + rt_n + ba_n
        n = int(len(group))
        rows.append(
            {
                "attendance": attendance,
                "nonpass_n": n,
                "numeric_below_7_5_n": numeric_n,
                "BV_n": bv_n,
                "RT_n": rt_n,
                "BA_n": ba_n,
                "administrative_n": admin_n,
                "administrative_share_among_nonpass": admin_n / n if n else np.nan,
                "BV_RT_share_among_numeric_or_BV_RT": (
                    (bv_n + rt_n) / (numeric_n + bv_n + rt_n)
                    if numeric_n + bv_n + rt_n
                    else np.nan
                ),
                "BV_share_among_numeric_or_BV": (
                    bv_n / (numeric_n + bv_n) if numeric_n + bv_n else np.nan
                ),
                "RT_share_among_numeric_or_RT": (
                    rt_n / (numeric_n + rt_n) if numeric_n + rt_n else np.nan
                ),
            }
        )
    return pd.DataFrame(rows)


def check_environment() -> int:
    required = [
        REPO_ROOT / "paper" / "VISIT_GROUPING_DECISION.md",
        GROUP_SPEC,
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing Paper 2.1 outcome-analysis paths: " + ", ".join(missing))
    spec = json.loads(GROUP_SPEC.read_text(encoding="utf-8"))
    if spec["positive_user_primary_groups"] != ["1", "2", "3", "4", "5", "6+"]:
        raise SystemExit("Paper 2.1 primary visit grouping differs from frozen decision.")
    print("Paper 2.1 dual-outcome analysis check: OK")
    print("Reusable estimators: cmat_analysis 0.3 attendance-frequency API")
    print("Frozen primary groups: 1, 2, 3, 4, 5, 6+")
    return 0


def run(args: argparse.Namespace) -> int:
    base = get_study_config(REPO_ROOT)
    config = replace(
        base,
        materias_path=(args.materias or base.materias_path).expanduser().resolve(),
        asesorias_path=(args.asesorias or base.asesorias_path).expanduser().resolve(),
    )
    data = load_and_clean_inputs(config)
    mu = add_primary_outcomes(build_study_cohorts(data, config)["mu_primary"], config)
    mu["PASS"] = mu["PASS"].astype(float)
    mu = add_academic_outcome_states(mu)

    benchmark = pd.DataFrame(
        [
            _benchmark(mu, "Z_GRADE_PRIMARY", "continuous_standardised_grade"),
            _benchmark(mu, "PASS", "pass_probability"),
        ]
    )
    _save(benchmark, "10_benchmark_0_vs_1plus.csv")

    zero_order = ["0", "1", "2", "3", "4", "5", "6+"]
    zero_plus = add_topcoded_visit_group(
        mu,
        top_exact=5,
        include_zero=True,
        output_col="P21_GROUP_WITH_ZERO",
    )
    zero_desc = group_outcome_summary(
        zero_plus,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=zero_order,
        outcome_col="Z_GRADE_PRIMARY",
        pass_col="PASS",
    )
    _save(
        _format_descriptives(
            zero_desc, specification="zero_inclusive_primary_0_1_2_3_4_5_6plus"
        ),
        "10b_zero_inclusive_descriptives.csv",
    )
    _save(
        _composition(
            zero_plus,
            group_col="P21_GROUP_WITH_ZERO",
            group_order=zero_order,
            state_col="ACADEMIC_OUTCOME_STATE_4",
            state_order=["pass", "numeric_nonpass", "BV_RT", "BA"],
            specification="zero_inclusive_primary_0_1_2_3_4_5_6plus",
        ),
        "10c_zero_inclusive_outcome_state_composition.csv",
    )
    _save(
        _composition(
            zero_plus,
            group_col="P21_GROUP_WITH_ZERO",
            group_order=zero_order,
            state_col="ACADEMIC_OUTCOME_STATE_5",
            state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            specification="zero_inclusive_primary_0_1_2_3_4_5_6plus",
        ),
        "10d_zero_inclusive_exact_administrative_composition.csv",
    )

    ridge_density = mixture_component_density(
        zero_plus,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=zero_order,
        outcome_col="Z_GRADE_PRIMARY",
        component_col="ACADEMIC_OUTCOME_STATE_5",
        component_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
        grid_size=400,
    )
    _save(ridge_density, "10g_zero_inclusive_stacked_ridgeline_density.csv")

    nonpass = mu.loc[mu["PASS"].eq(0)].copy()
    management_benchmark = pd.DataFrame(
        [
            _benchmark(
                nonpass,
                "ADMINISTRATIVE_VS_NUMERIC_NONPASS",
                "administrative_outcome_vs_numeric_failure_among_nonpass",
            ),
            _benchmark(
                nonpass,
                "BVRT_VS_NUMERIC_NONPASS",
                "BV_RT_vs_numeric_failure_among_nonpass_excluding_BA",
            ),
            _benchmark(
                nonpass,
                "BV_VS_NUMERIC_NONPASS",
                "BV_vs_numeric_failure_among_nonpass_excluding_RT_BA",
            ),
            _benchmark(
                nonpass,
                "RT_VS_NUMERIC_NONPASS",
                "RT_vs_numeric_failure_among_nonpass_excluding_BV_BA",
            ),
        ]
    )
    _save(management_benchmark, "10e_nonpass_management_benchmark_0_vs_1plus.csv")
    _save(_nonpass_management_summary(mu), "10f_nonpass_management_descriptives_0_vs_1plus.csv")

    users = mu.loc[mu["VISITS_CMAT_PERIOD"].gt(0)].copy()
    primary_order = ["1", "2", "3", "4", "5", "6+"]
    users = add_topcoded_visit_group(
        users, top_exact=5, output_col="P21_GROUP"
    )
    primary_desc = group_outcome_summary(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_PRIMARY",
        pass_col="PASS",
    )
    _save(
        _format_descriptives(primary_desc, specification="primary_1_2_3_4_5_6plus"),
        "11_primary_group_descriptives.csv",
    )

    z_pair, z_omni = _fit(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="primary_1_2_3_4_5_6plus",
    )
    p_pair, p_omni = _fit(
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

    _save(
        _composition(
            users,
            group_col="P21_GROUP",
            group_order=primary_order,
            state_col="ACADEMIC_OUTCOME_STATE_4",
            state_order=["pass", "numeric_nonpass", "BV_RT", "BA"],
            specification="primary_1_2_3_4_5_6plus",
        ),
        "15_primary_outcome_state_composition.csv",
    )
    _save(
        _composition(
            users,
            group_col="P21_GROUP",
            group_order=primary_order,
            state_col="ACADEMIC_OUTCOME_STATE_5",
            state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            specification="primary_1_2_3_4_5_6plus",
        ),
        "15a_primary_exact_administrative_composition.csv",
    )
    _save(
        _profile(
            users,
            group_col="P21_GROUP",
            group_order=primary_order,
            outcome_col="Z_GRADE_PRIMARY",
            outcome_label="continuous_standardised_grade",
            specification="primary_1_2_3_4_5_6plus",
        ),
        "15b_primary_distribution_profile.csv",
    )
    _save(
        _profile(
            users,
            group_col="P21_GROUP",
            group_order=primary_order,
            outcome_col="Z_GRADE_COMPLETE_CASE",
            outcome_label="numeric_complete_case_standardised_grade",
            specification="primary_1_2_3_4_5_6plus_complete_case",
        ),
        "15c_primary_complete_case_distribution_profile.csv",
    )

    nonpass_users = users.loc[users["PASS"].eq(0)].copy()
    admin_pair, admin_omni = _fit(
        nonpass_users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="ADMINISTRATIVE_VS_NUMERIC_NONPASS",
        outcome_label="administrative_outcome_vs_numeric_failure_among_nonpass",
        specification="primary_1_2_3_4_5_6plus_nonpass",
    )
    bvrt_pair, bvrt_omni = _fit(
        nonpass_users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="BVRT_VS_NUMERIC_NONPASS",
        outcome_label="BV_RT_vs_numeric_failure_among_nonpass_excluding_BA",
        specification="primary_1_2_3_4_5_6plus_nonpass",
    )
    bv_pair, bv_omni = _fit(
        nonpass_users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="BV_VS_NUMERIC_NONPASS",
        outcome_label="BV_vs_numeric_failure_among_nonpass_excluding_RT_BA",
        specification="primary_1_2_3_4_5_6plus_nonpass",
    )
    _save(
        pd.concat([admin_omni, bvrt_omni, bv_omni], ignore_index=True),
        "15d_nonpass_management_omnibus.csv",
    )
    _save(admin_pair, "15e_nonpass_administrative_pairwise.csv")
    _save(bvrt_pair, "15f_nonpass_BVRT_pairwise.csv")
    _save(bv_pair, "15g_nonpass_BV_pairwise.csv")

    cc_pair, cc_omni = _fit(
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
        _matrix(z_pair, group_order=primary_order, outcome="continuous_standardised_grade"),
        "18_primary_z_heatmap_matrix.csv",
    )
    _save(
        _matrix(p_pair, group_order=primary_order, outcome="pass_probability"),
        "19_primary_pass_heatmap_matrix.csv",
    )

    sensitivity_order = ["1", "2", "3", "4", "5", "6", "7+"]
    sensitivity = add_topcoded_visit_group(
        users.drop(columns=["P21_GROUP"]),
        top_exact=6,
        output_col="P21_GROUP_7P",
    )
    sensitivity_desc = group_outcome_summary(
        sensitivity,
        group_col="P21_GROUP_7P",
        group_order=sensitivity_order,
        outcome_col="Z_GRADE_PRIMARY",
        pass_col="PASS",
    )
    _save(
        _format_descriptives(
            sensitivity_desc, specification="sensitivity_1_to_6_7plus"
        ),
        "20_sensitivity_7plus_group_descriptives.csv",
    )
    sz_pair, sz_omni = _fit(
        sensitivity,
        group_col="P21_GROUP_7P",
        group_order=sensitivity_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="sensitivity_1_to_6_7plus",
    )
    sp_pair, sp_omni = _fit(
        sensitivity,
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
        _composition(
            sensitivity,
            group_col="P21_GROUP_7P",
            group_order=sensitivity_order,
            state_col="ACADEMIC_OUTCOME_STATE_4",
            state_order=["pass", "numeric_nonpass", "BV_RT", "BA"],
            specification="sensitivity_1_to_6_7plus",
        ),
        "24_sensitivity_7plus_outcome_state_composition.csv",
    )
    _save(
        _composition(
            sensitivity,
            group_col="P21_GROUP_7P",
            group_order=sensitivity_order,
            state_col="ACADEMIC_OUTCOME_STATE_5",
            state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
            specification="sensitivity_1_to_6_7plus",
        ),
        "24a_sensitivity_7plus_exact_administrative_composition.csv",
    )
    _save(
        _profile(
            sensitivity,
            group_col="P21_GROUP_7P",
            group_order=sensitivity_order,
            outcome_col="Z_GRADE_PRIMARY",
            outcome_label="continuous_standardised_grade",
            specification="sensitivity_1_to_6_7plus",
        ),
        "25_sensitivity_7plus_distribution_profile.csv",
    )

    z_prof_pair, z_prof_omni = _fit(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_label="continuous_standardised_grade",
        specification="primary_instructor_cluster_sensitivity",
        cluster_col="CLAVEPROFESOR",
    )
    p_prof_pair, p_prof_omni = _fit(
        users,
        group_col="P21_GROUP",
        group_order=primary_order,
        outcome_col="PASS",
        outcome_label="pass_probability",
        specification="primary_instructor_cluster_sensitivity",
        cluster_col="CLAVEPROFESOR",
    )
    _save(z_prof_pair, "26_instructor_cluster_pairwise_continuous.csv")
    _save(p_prof_pair, "27_instructor_cluster_pairwise_pass.csv")
    _save(
        pd.concat([z_prof_omni, p_prof_omni], ignore_index=True),
        "28_instructor_cluster_omnibus.csv",
    )
    _save(
        pd.DataFrame(
            [
                _benchmark(
                    mu,
                    "Z_GRADE_PRIMARY",
                    "continuous_standardised_grade",
                    cluster_col="CLAVEPROFESOR",
                ),
                _benchmark(
                    mu,
                    "PASS",
                    "pass_probability",
                    cluster_col="CLAVEPROFESOR",
                ),
            ]
        ),
        "29_instructor_cluster_benchmark_0_vs_1plus.csv",
    )

    print(f"Paper 2.1 study cohort: N={len(mu):,}")
    print(f"Positive-attendance analysis: N={len(users):,}")
    print("Primary groups: 1, 2, 3, 4, 5, 6+")
    print("Sensitivity groups: 1, 2, 3, 4, 5, 6, 7+")
    print("Shared methods: cmat_analysis 0.3 public API")
    print(f"Outputs: {TABLES_DIR}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Paper 2.1 dual-outcome frequency analysis."
    )
    parser.add_argument("--materias", type=Path)
    parser.add_argument("--asesorias", type=Path)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return check_environment() if args.check else run(args)


if __name__ == "__main__":
    raise SystemExit(main())
