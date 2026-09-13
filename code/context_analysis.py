#!/usr/bin/env python3
"""Run Paper 1 classroom-outcome and degree-programme context analyses.

Reusable cohort construction and estimators live in :mod:`cmat_analysis`. This
branch-local module only orchestrates the validated shared functions and writes
publication-safe aggregate outputs; it never writes student- or instructor-level
microdata.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pandas as pd

from cmat_analysis.cohorts import load_and_clean_inputs
from cmat_analysis.config.study_config import get_study_config
from cmat_analysis.ppa import (
    build_mu_classroom_outcome_context,
    build_ppa_mu_baseline_cohort,
    clustered_academic_context_uptake_models,
    leave_period_out_professor_academic_context,
    leave_period_out_professor_propensity,
    major_uptake_increment,
    major_visit_group_multinomial_increment,
    major_visit_group_summary,
    professor_period_context_correlations,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "results" / "tables"


def _save(frame: pd.DataFrame, filename: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES_DIR / filename, index=False)


def _classroom_context_summary(context: pd.DataFrame) -> pd.DataFrame:
    """Reduce classroom outcomes to distributional summaries without identifiers."""
    classrooms = context.drop_duplicates("MU_CONTEXT_CLASSROOM_ID")
    rows: list[dict[str, object]] = []
    for column in (
        "MU_CLASSROOM_ATTEMPT_N",
        "MU_CLASSROOM_MEAN_GRADE",
        "MU_CLASSROOM_PASS_RATE",
        "MU_CLASSROOM_FAIL_RATE",
    ):
        values = pd.to_numeric(classrooms[column], errors="coerce").dropna()
        if values.empty:
            continue
        quantiles = values.quantile([0.10, 0.25, 0.50, 0.75, 0.90])
        rows.append({
            "measure": column,
            "classrooms": int(len(values)),
            "mean": float(values.mean()),
            "sd": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
            "min": float(values.min()),
            "p10": float(quantiles.loc[0.10]),
            "p25": float(quantiles.loc[0.25]),
            "median": float(quantiles.loc[0.50]),
            "p75": float(quantiles.loc[0.75]),
            "p90": float(quantiles.loc[0.90]),
            "max": float(values.max()),
        })
    return pd.DataFrame(rows)


def main() -> int:
    base_config = get_study_config(REPO_ROOT)
    config = replace(base_config, output_dir=REPO_ROOT / "results")
    data = load_and_clean_inputs(config)

    mu_baseline = build_ppa_mu_baseline_cohort(data, config)
    classroom = build_mu_classroom_outcome_context(data, config)

    attach_columns = [
        "SOURCE_ROW",
        "MU_CONTEXT_CLASSROOM_ID",
        "MU_CLASSROOM_ATTEMPT_N",
        "MU_CLASSROOM_NUMERIC_N",
        "MU_CLASSROOM_ADVERSE_N",
        "MU_CLASSROOM_MEAN_GRADE",
        "MU_CLASSROOM_MEDIAN_GRADE",
        "MU_CLASSROOM_SD_GRADE",
        "MU_CLASSROOM_PASS_RATE",
        "MU_CLASSROOM_FAIL_RATE",
        "MU_LOO_CLASSROOM_MEAN_GRADE",
        "MU_LOO_CLASSROOM_PASS_RATE",
        "MU_LOO_CLASSROOM_FAIL_RATE",
    ]
    mu_augmented = mu_baseline.merge(
        classroom[attach_columns], on="SOURCE_ROW", how="left", validate="one_to_one"
    )

    academic_history = leave_period_out_professor_academic_context(
        classroom,
        professor_col="CLAVEPROFESOR",
        period_col="PERIOD_LABEL",
        grade_col="GRADE_NUMERIC",
        pass_col="MU_ATTEMPT_PASS",
        min_other_n=30,
        prefix="MU_PROF_ACAD",
    )
    historical_columns = [
        "SOURCE_ROW",
        "MU_PROF_ACAD_LEAVE_PERIOD_OUT_PASS_RATE",
        "MU_PROF_ACAD_LEAVE_PERIOD_OUT_FAIL_RATE",
        "MU_PROF_ACAD_LEAVE_PERIOD_OUT_MEAN_GRADE",
        "MU_PROF_ACAD_LEAVE_PERIOD_OUT_ATTEMPT_N",
        "MU_PROF_ACAD_LEAVE_PERIOD_OUT_GRADE_N",
        "MU_PROF_ACAD_LEAVE_PERIOD_OUT_PASS_Z",
        "MU_PROF_ACAD_LEAVE_PERIOD_OUT_GRADE_Z",
    ]
    mu_augmented = mu_augmented.merge(
        academic_history[historical_columns],
        on="SOURCE_ROW",
        how="left",
        validate="one_to_one",
    )

    professor_uptake = leave_period_out_professor_propensity(
        mu_baseline,
        professor_col="MU_PROFESSOR",
        period_col="MU_PERIOD_LABEL",
        outcome_col="MU_ANY_VISIT",
        min_other_n=30,
        prefix="MU_PROF",
    )
    uptake_columns = [
        "SOURCE_ROW",
        "MU_PROF_LEAVE_PERIOD_OUT_RATE",
        "MU_PROF_LEAVE_PERIOD_OUT_N",
        "MU_PROF_LEAVE_PERIOD_OUT_Z",
    ]
    mu_augmented = mu_augmented.merge(
        professor_uptake[uptake_columns],
        on="SOURCE_ROW",
        how="left",
        validate="one_to_one",
    )

    major_summary = major_visit_group_summary(
        mu_baseline,
        min_n=config.min_career_n_for_inference,
    )
    major_binary = major_uptake_increment(
        mu_baseline,
        min_major_n=config.min_career_n_for_inference,
    )
    major_multinomial = major_visit_group_multinomial_increment(
        mu_baseline,
        min_major_n=config.min_career_n_for_inference,
    )

    observed_context = clustered_academic_context_uptake_models(
        mu_augmented,
        outcome_col="MU_ANY_VISIT",
        context_cols=[
            "MU_LOO_CLASSROOM_MEAN_GRADE",
            "MU_LOO_CLASSROOM_PASS_RATE",
        ],
        period_col="MU_PERIOD_LABEL",
        cluster_col="MU_CONTEXT_CLASSROOM_ID",
        major_col="MU_CAREER_OFFICIAL",
        professor_col="MU_PROFESSOR",
        min_major_n=config.min_career_n_for_inference,
    )
    historical_context = clustered_academic_context_uptake_models(
        mu_augmented,
        outcome_col="MU_ANY_VISIT",
        context_cols=[
            "MU_PROF_ACAD_LEAVE_PERIOD_OUT_MEAN_GRADE",
            "MU_PROF_ACAD_LEAVE_PERIOD_OUT_PASS_RATE",
        ],
        period_col="MU_PERIOD_LABEL",
        cluster_col="MU_PROFESSOR",
        major_col="MU_CAREER_OFFICIAL",
        professor_col="MU_PROFESSOR",
        min_major_n=config.min_career_n_for_inference,
    )
    context_correlations = professor_period_context_correlations(
        mu_augmented,
        professor_col="MU_PROFESSOR",
        period_col="MU_PERIOD_LABEL",
        uptake_col="MU_PROF_LEAVE_PERIOD_OUT_RATE",
        academic_cols=[
            "MU_PROF_ACAD_LEAVE_PERIOD_OUT_MEAN_GRADE",
            "MU_PROF_ACAD_LEAVE_PERIOD_OUT_PASS_RATE",
        ],
    )

    outputs = {
        "140_mu_major_visit_group_summary.csv": major_summary,
        "141_mu_major_any_use_increment.csv": major_binary,
        "142_mu_major_visit_group_multinomial_increment.csv": major_multinomial,
        "143_mu_classroom_outcome_context_summary.csv": _classroom_context_summary(classroom),
        "144_mu_observed_classroom_context_uptake_models.csv": observed_context,
        "145_mu_historical_professor_academic_context_uptake_models.csv": historical_context,
        "146_mu_professor_uptake_vs_academic_context_correlations.csv": context_correlations,
    }
    for filename, frame in outputs.items():
        _save(frame, filename)

    print(f"Paper 1 MU baseline: N={len(mu_baseline):,}")
    print(f"Real MU classroom context rows: N={len(classroom):,}")
    print(f"Degree programmes retained: {len(major_summary):,}")
    print(f"Aggregate context tables written: {len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
