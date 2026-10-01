#!/usr/bin/env python3
"""Fast Paper 2.1 shape check: Gaussian, skew-normal, and two-Gaussian mixture."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from run_paper21_mixture import GROUP_ORDER, TABLES_DIR, _gmm_starts, _load_cohort

try:
    from cmat_analysis.statistics import (
        compare_univariate_shape_models,
        cross_validated_skew_normal_vs_gmm,
        parametric_bootstrap_skew_normal_vs_gmm,
    )
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2.1 shape check requires the shared editable library. Run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"\n'
        f"Original import error: {exc}"
    ) from exc


def _shape_tables(
    cohort: pd.DataFrame,
    *,
    outcome_col: str,
    outcome_specification: str,
    shape_bootstrap: int,
    cv_folds: int,
    cv_repeats: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    comparison_rows: list[dict[str, object]] = []
    bootstrap_rows: list[dict[str, object]] = []
    predictive_rows: list[dict[str, object]] = []
    labels = cohort["P21_GROUP_WITH_ZERO"].astype("string")

    for group in GROUP_ORDER:
        g = cohort.loc[labels.eq(group)].copy()
        values = pd.to_numeric(g[outcome_col], errors="coerce").dropna().to_numpy(float)
        if len(values) < 30:
            continue

        comparison = compare_univariate_shape_models(
            values,
            random_state=42,
            n_init=30,
            two_component_mean_starts=_gmm_starts(values),
        ).iloc[0].to_dict()
        comparison["outcome_specification"] = outcome_specification
        comparison["group"] = group
        comparison_rows.append(comparison)

        bootstrap = parametric_bootstrap_skew_normal_vs_gmm(
            values,
            n_bootstrap=shape_bootstrap,
            random_state=42,
            n_init=8,
            two_component_mean_starts=((-1.1, 0.5),),
        ).iloc[0].to_dict()
        bootstrap["outcome_specification"] = outcome_specification
        bootstrap["group"] = group
        bootstrap_rows.append(bootstrap)

        predictive = cross_validated_skew_normal_vs_gmm(
            values,
            n_splits=cv_folds,
            n_repeats=cv_repeats,
            random_state=42,
            n_init=6,
            two_component_mean_starts=((-1.1, 0.5),),
        ).iloc[0].to_dict()
        predictive["outcome_specification"] = outcome_specification
        predictive["group"] = group
        predictive_rows.append(predictive)

    return (
        pd.DataFrame(comparison_rows),
        pd.DataFrame(bootstrap_rows),
        pd.DataFrame(predictive_rows),
    )


def _save_and_print(frame: pd.DataFrame, filename: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    path = TABLES_DIR / filename
    frame.to_csv(path, index=False)
    print(f"\n=== {filename} ===")
    print(frame.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fast Paper 2.1 skew-normal versus Gaussian-mixture shape check."
    )
    parser.add_argument("--materias", type=Path)
    parser.add_argument("--asesorias", type=Path)
    parser.add_argument("--shape-bootstrap", type=int, default=199)
    parser.add_argument("--shape-cv-folds", type=int, default=5)
    parser.add_argument("--shape-cv-repeats", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cohort = _load_cohort(args)
    complete, complete_bootstrap, complete_cv = _shape_tables(
        cohort,
        outcome_col="Z_GRADE_COMPLETE_CASE",
        outcome_specification="numeric_complete_case",
        shape_bootstrap=args.shape_bootstrap,
        cv_folds=args.shape_cv_folds,
        cv_repeats=args.shape_cv_repeats,
    )
    imputed, imputed_bootstrap, imputed_cv = _shape_tables(
        cohort,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_specification="primary_imputed_sensitivity",
        shape_bootstrap=args.shape_bootstrap,
        cv_folds=args.shape_cv_folds,
        cv_repeats=args.shape_cv_repeats,
    )
    _save_and_print(complete, "47_complete_case_skewnormal_vs_gmm.csv")
    _save_and_print(imputed, "48_imputed_skewnormal_vs_gmm.csv")
    _save_and_print(
        complete_bootstrap,
        "49_complete_case_skewnormal_bootstrap_vs_gmm.csv",
    )
    _save_and_print(
        complete_cv,
        "50_complete_case_skewnormal_vs_gmm_cross_validation.csv",
    )
    _save_and_print(
        imputed_bootstrap,
        "51_imputed_skewnormal_bootstrap_vs_gmm.csv",
    )
    _save_and_print(
        imputed_cv,
        "52_imputed_skewnormal_vs_gmm_cross_validation.csv",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
