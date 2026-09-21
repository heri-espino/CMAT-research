#!/usr/bin/env python3
"""Paper 2.1 observed-failure and Gaussian-mixture analysis.

The analysis deliberately separates:
1. observed numeric failure among students with a numeric final grade;
2. Gaussian-mixture structure in the numeric complete-case Z outcome;
3. the same Gaussian-mixture analysis on the primary imputed Z outcome only as
   a sensitivity to administrative-outcome imputation.

Reusable estimation is delegated to cmat_analysis 0.4.1.
"""

from __future__ import annotations

import argparse
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
        fixed_effect_logistic_group_comparisons,
        fixed_effect_logistic_adjusted_probabilities,
        gaussian_mixture_component_summary,
        gaussian_mixture_model_selection,
        gaussian_mixture_responsibilities,
        parametric_bootstrap_gmm_lrt,
        mixture_component_density,
        soft_component_composition,
    )
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2.1 mixture analysis requires the shared editable library. Run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"\n'
        f"Original import error: {exc}"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "results" / "paper21" / "tables"
GROUP_ORDER = ["0", "1", "2", "3", "4", "5", "6+"]
USER_GROUP_ORDER = ["1", "2", "3", "4", "5", "6+"]
STATE_ORDER = ["pass", "numeric_nonpass", "BV", "RT", "BA"]


def _save(frame: pd.DataFrame, name: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES_DIR / name, index=False)


def _load_cohort(args: argparse.Namespace) -> pd.DataFrame:
    base = get_study_config(REPO_ROOT)
    config = replace(
        base,
        materias_path=(args.materias or base.materias_path).expanduser().resolve(),
        asesorias_path=(args.asesorias or base.asesorias_path).expanduser().resolve(),
    )
    data = load_and_clean_inputs(config)
    cohort = build_study_cohorts(data, config)["mu_primary"].copy()
    cohort = add_primary_outcomes(cohort, config)
    cohort["PASS"] = cohort["PASS"].astype(float)
    cohort = add_academic_outcome_states(cohort)
    cohort = add_topcoded_visit_group(
        cohort,
        visits_col="VISITS_CMAT_PERIOD",
        top_exact=5,
        include_zero=True,
        output_col="P21_GROUP_WITH_ZERO",
    )
    return cohort


def _numeric_failure_descriptives(cohort: pd.DataFrame) -> pd.DataFrame:
    numeric = cohort.loc[cohort["GRADE_CLASS"].eq("numeric")].copy()
    numeric["NUMERIC_FAIL"] = 1.0 - numeric["PASS"]
    labels = numeric["P21_GROUP_WITH_ZERO"].astype("string")
    rows = []
    for group in GROUP_ORDER:
        g = numeric.loc[labels.eq(group)]
        n = int(len(g))
        fail_n = int(g["NUMERIC_FAIL"].sum())
        pass_n = int(g["PASS"].sum())
        rate = fail_n / n if n else np.nan
        odds = fail_n / pass_n if pass_n else np.inf
        rows.append(
            {
                "group": group,
                "n_numeric_final_grade": n,
                "numeric_fail_n": fail_n,
                "numeric_pass_n": pass_n,
                "numeric_failure_probability": rate,
                "numeric_failure_odds": odds,
            }
        )
    return pd.DataFrame(rows)


def _logit_outputs(
    numeric: pd.DataFrame,
    *,
    group_order: list[str],
    specification: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    adjusted = fixed_effect_logistic_adjusted_probabilities(
        numeric,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=group_order,
        outcome_col="NUMERIC_FAIL",
        fixed_effect_col="CLASSROOM_ID",
        cluster_col="CLASSROOM_ID",
        categorical_covariates=["CLAVECARRERA"],
    )
    pairwise, omnibus, info = fixed_effect_logistic_group_comparisons(
        numeric,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=group_order,
        outcome_col="NUMERIC_FAIL",
        fixed_effect_col="CLASSROOM_ID",
        cluster_col="CLASSROOM_ID",
        categorical_covariates=["CLAVECARRERA"],
        multiplicity_method="holm",
    )
    adjusted.insert(0, "specification", specification)
    pairwise.insert(0, "specification", specification)
    omnibus.insert(0, "specification", specification)
    info.insert(0, "specification", specification)
    return adjusted, pairwise, omnibus, info


def _gmm_starts(values: np.ndarray) -> tuple[tuple[float, float], ...]:
    q25, q75 = np.quantile(values, [0.25, 0.75])
    starts = [(-1.1, 0.5)]
    if np.isfinite(q25) and np.isfinite(q75) and q25 < q75:
        starts.append((float(q25), float(q75)))
    return tuple(starts)


def _run_gmm_family(
    cohort: pd.DataFrame,
    *,
    outcome_col: str,
    outcome_spec: str,
    n_bootstrap: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    selection_rows: list[pd.DataFrame] = []
    component_rows: list[pd.DataFrame] = []
    bootstrap_rows: list[pd.DataFrame] = []
    composition_rows: list[pd.DataFrame] = []

    labels = cohort["P21_GROUP_WITH_ZERO"].astype("string")
    for group in GROUP_ORDER:
        g = cohort.loc[labels.eq(group)].copy()
        finite = pd.to_numeric(g[outcome_col], errors="coerce").notna()
        g = g.loc[finite].copy()
        values = pd.to_numeric(g[outcome_col], errors="coerce").to_numpy(float)
        if len(values) < 30:
            continue

        starts = _gmm_starts(values)
        selection, models = gaussian_mixture_model_selection(
            values,
            component_counts=(1, 2, 3),
            random_state=42,
            n_init=30,
            two_component_mean_starts=starts,
        )
        selection.insert(0, "group", group)
        selection.insert(0, "outcome_specification", outcome_spec)
        bic1 = float(selection.loc[selection["n_components"].eq(1), "bic"].iloc[0])
        icl1 = float(selection.loc[selection["n_components"].eq(1), "icl"].iloc[0])
        selection["delta_bic_vs_1_component"] = selection["bic"] - bic1
        selection["delta_icl_vs_1_component"] = selection["icl"] - icl1
        selection_rows.append(selection)

        components = gaussian_mixture_component_summary(models[2])
        components.insert(0, "group", group)
        components.insert(0, "outcome_specification", outcome_spec)
        component_rows.append(components)

        responsibilities = gaussian_mixture_responsibilities(models[2], values)
        composition = soft_component_composition(
            g["ACADEMIC_OUTCOME_STATE_5"].astype(str).tolist(),
            responsibilities,
            state_order=STATE_ORDER,
        )
        composition.insert(0, "group", group)
        composition.insert(0, "outcome_specification", outcome_spec)
        composition_rows.append(composition)

        bootstrap = parametric_bootstrap_gmm_lrt(
            values,
            n_bootstrap=n_bootstrap,
            random_state=42,
            n_init=20,
            two_component_mean_starts=starts,
        )
        bootstrap.insert(0, "group", group)
        bootstrap.insert(0, "outcome_specification", outcome_spec)
        bootstrap_rows.append(bootstrap)

    return (
        pd.concat(selection_rows, ignore_index=True),
        pd.concat(component_rows, ignore_index=True),
        pd.concat(bootstrap_rows, ignore_index=True),
        pd.concat(composition_rows, ignore_index=True),
    )


def check_environment() -> int:
    required = [
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
        REPO_ROOT / "paper" / "VISIT_GROUPING_DECISION.md",
        REPO_ROOT / "paper" / "OUTCOME_FRAMEWORK.md",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing Paper 2.1 mixture-analysis paths: " + ", ".join(missing))
    print("Paper 2.1 mixture-analysis check: OK")
    print("Primary mixture outcome: numeric complete-case instructor-period Z")
    print("Imputed primary Z: sensitivity only")
    print("Two-component proposed start (-1.1, 0.5) is one of multiple EM starts")
    return 0


def run(args: argparse.Namespace) -> int:
    cohort = _load_cohort(args)

    numeric = cohort.loc[cohort["GRADE_CLASS"].eq("numeric")].copy()
    numeric["NUMERIC_FAIL"] = 1.0 - numeric["PASS"]

    _save(_numeric_failure_descriptives(cohort), "30_numeric_failure_descriptives.csv")

    adjusted_all, pairwise_all, omnibus_all, info_all = _logit_outputs(
        numeric,
        group_order=GROUP_ORDER,
        specification="numeric_final_grade_zero_inclusive",
    )
    _save(adjusted_all, "31a_numeric_failure_adjusted_probabilities_zero_inclusive.csv")
    _save(pairwise_all, "31_numeric_failure_logit_pairwise_zero_inclusive.csv")
    _save(omnibus_all, "32_numeric_failure_logit_omnibus_zero_inclusive.csv")
    _save(info_all, "33_numeric_failure_logit_model_info_zero_inclusive.csv")

    numeric_users = numeric.loc[numeric["VISITS_CMAT_PERIOD"].gt(0)].copy()
    adjusted_users, pairwise_users, omnibus_users, info_users = _logit_outputs(
        numeric_users,
        group_order=USER_GROUP_ORDER,
        specification="numeric_final_grade_positive_attendance",
    )
    _save(adjusted_users, "34a_numeric_failure_adjusted_probabilities_users.csv")
    _save(pairwise_users, "34_numeric_failure_logit_pairwise_users.csv")
    _save(omnibus_users, "35_numeric_failure_logit_omnibus_users.csv")
    _save(info_users, "36_numeric_failure_logit_model_info_users.csv")

    cc_selection, cc_components, cc_bootstrap, cc_composition = _run_gmm_family(
        cohort,
        outcome_col="Z_GRADE_COMPLETE_CASE",
        outcome_spec="numeric_complete_case",
        n_bootstrap=args.gmm_bootstrap,
    )
    _save(cc_selection, "37_complete_case_gmm_selection.csv")
    _save(cc_components, "38_complete_case_gmm_two_component_parameters.csv")
    _save(cc_bootstrap, "39_complete_case_gmm_bootstrap_1_vs_2.csv")
    _save(cc_composition, "40_complete_case_gmm_soft_component_composition.csv")

    imp_selection, imp_components, imp_bootstrap, imp_composition = _run_gmm_family(
        cohort,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_spec="primary_imputed_sensitivity",
        n_bootstrap=args.gmm_bootstrap,
    )
    _save(imp_selection, "41_imputed_gmm_selection.csv")
    _save(imp_components, "42_imputed_gmm_two_component_parameters.csv")
    _save(imp_bootstrap, "43_imputed_gmm_bootstrap_1_vs_2.csv")
    _save(imp_composition, "44_imputed_gmm_soft_component_composition.csv")

    comparison = pd.concat(
        [
            cc_components,
            imp_components,
        ],
        ignore_index=True,
    )
    _save(comparison, "45_gmm_component_comparison_complete_vs_imputed.csv")

    density_source = cohort.copy()
    density_source["_GMM_DENSITY_COMPONENT"] = "all"
    cc_density = mixture_component_density(
        density_source,
        group_col="P21_GROUP_WITH_ZERO",
        group_order=GROUP_ORDER,
        outcome_col="Z_GRADE_COMPLETE_CASE",
        component_col="_GMM_DENSITY_COMPONENT",
        component_order=["all"],
        grid_size=512,
    )
    _save(cc_density, "46_complete_case_gmm_ridgeline_density.csv")

    print(f"Paper 2.1 study cohort: N={len(cohort):,}")
    print(f"Numeric final grades: N={len(numeric):,}")
    print(f"GMM bootstrap replicates per group/specification: {args.gmm_bootstrap}")
    print("GMM hierarchy: complete-case primary; imputed outcome sensitivity")
    print(f"Outputs: {TABLES_DIR}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Paper 2.1 observed-failure and Gaussian-mixture analysis."
    )
    parser.add_argument("--materias", type=Path)
    parser.add_argument("--asesorias", type=Path)
    parser.add_argument("--gmm-bootstrap", type=int, default=999)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return check_environment() if args.check else run(args)


if __name__ == "__main__":
    raise SystemExit(main())
