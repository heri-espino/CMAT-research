#!/usr/bin/env python3
"""Fast Paper 2.1 shape check: Gaussian, skew-normal, and two-Gaussian mixture."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from run_paper21_mixture import GROUP_ORDER, TABLES_DIR, _gmm_starts, _load_cohort

try:
    from cmat_analysis.statistics import compare_univariate_shape_models
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2.1 shape check requires the shared editable library. Run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"\n'
        f"Original import error: {exc}"
    ) from exc


def _shape_table(
    cohort: pd.DataFrame,
    *,
    outcome_col: str,
    outcome_specification: str,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
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
        ).iloc[0]

        row = comparison.to_dict()
        row["outcome_specification"] = outcome_specification
        row["group"] = group
        rows.append(row)

    return pd.DataFrame(rows)


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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cohort = _load_cohort(args)
    complete = _shape_table(
        cohort,
        outcome_col="Z_GRADE_COMPLETE_CASE",
        outcome_specification="numeric_complete_case",
    )
    imputed = _shape_table(
        cohort,
        outcome_col="Z_GRADE_PRIMARY",
        outcome_specification="primary_imputed_sensitivity",
    )
    _save_and_print(complete, "47_complete_case_skewnormal_vs_gmm.csv")
    _save_and_print(imputed, "48_imputed_skewnormal_vs_gmm.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
