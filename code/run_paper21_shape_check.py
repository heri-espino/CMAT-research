#!/usr/bin/env python3
"""Fast Paper 2.1 shape check: Gaussian, skew-normal, and two-Gaussian mixture."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from run_paper21_mixture import GROUP_ORDER, TABLES_DIR, _gmm_starts, _load_cohort

try:
    from cmat_analysis.statistics import (
        gaussian_mixture_model_selection,
        skew_normal_fit_summary,
    )
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

        selection, _ = gaussian_mixture_model_selection(
            values,
            component_counts=(1, 2),
            random_state=42,
            n_init=30,
            two_component_mean_starts=_gmm_starts(values),
        )
        normal = selection.loc[selection["n_components"].eq(1)].iloc[0]
        gmm2 = selection.loc[selection["n_components"].eq(2)].iloc[0]
        skew = skew_normal_fit_summary(values).iloc[0]

        bic = {
            "gaussian_k1": float(normal["bic"]),
            "skew_normal_k1": float(skew["bic"]),
            "gaussian_mixture_k2": float(gmm2["bic"]),
        }
        aic = {
            "gaussian_k1": float(normal["aic"]),
            "skew_normal_k1": float(skew["aic"]),
            "gaussian_mixture_k2": float(gmm2["aic"]),
        }
        rows.append(
            {
                "outcome_specification": outcome_specification,
                "group": group,
                "n": int(len(values)),
                "gaussian_k1_log_likelihood": float(normal["log_likelihood"]),
                "gaussian_k1_aic": float(normal["aic"]),
                "gaussian_k1_bic": float(normal["bic"]),
                "skew_normal_k1_shape": float(skew["shape"]),
                "skew_normal_k1_loc": float(skew["loc"]),
                "skew_normal_k1_scale": float(skew["scale"]),
                "skew_normal_k1_log_likelihood": float(skew["log_likelihood"]),
                "skew_normal_k1_aic": float(skew["aic"]),
                "skew_normal_k1_bic": float(skew["bic"]),
                "gaussian_mixture_k2_log_likelihood": float(gmm2["log_likelihood"]),
                "gaussian_mixture_k2_aic": float(gmm2["aic"]),
                "gaussian_mixture_k2_bic": float(gmm2["bic"]),
                "bic_advantage_skew_normal_over_gaussian_k1": (
                    float(normal["bic"]) - float(skew["bic"])
                ),
                "bic_advantage_gmm_k2_over_skew_normal": (
                    float(skew["bic"]) - float(gmm2["bic"])
                ),
                "aic_advantage_skew_normal_over_gaussian_k1": (
                    float(normal["aic"]) - float(skew["aic"])
                ),
                "aic_advantage_gmm_k2_over_skew_normal": (
                    float(skew["aic"]) - float(gmm2["aic"])
                ),
                "bic_preferred_model": min(bic, key=bic.get),
                "aic_preferred_model": min(aic, key=aic.get),
            }
        )

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
