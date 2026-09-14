#!/usr/bin/env python3
"""Run reduced-dimensional Paper 4 confirmatory follow-ups.

This recipe replaces the over-parameterized career-by-state interaction and adds a
numeric-failure severity check. Shared estimators remain in ``cmat_analysis``.
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from cmat_analysis.cohorts import load_and_clean_inputs
from cmat_analysis.config.study_config import get_study_config
from cmat_analysis.ppa import build_engagement_trajectory_data
from cmat_analysis.ppa.adaptation_confirmatory import classify_experience_state
from cmat_analysis.ppa.adaptation_confirmatory_extra import (
    career_heterogeneity_reduced_interactions,
    post_failure_numeric_severity_models,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "results" / "tables"


def _save(frame: pd.DataFrame, filename: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES_DIR / filename, index=False)


def _coverage_mask(df: pd.DataFrame, coverage: set[tuple[int, str]]) -> pd.Series:
    return pd.Series(
        [(int(y), s) in coverage for y, s in zip(df["YEAR"], df["SESSION"])],
        index=df.index,
    )


def _primary_state_summary(mu_students: pd.DataFrame, calc_choices: pd.DataFrame) -> pd.DataFrame:
    d = mu_students.copy()
    d["state"] = classify_experience_state(
        d, performance_cut=-0.5, difficulty_quantile=0.25
    )
    calc = calc_choices[["STUDENT_ID", "CALC_FIRST_ANY_CMAT"]].copy()
    calc["observed_later_calc"] = 1
    d = d.merge(calc, on="STUDENT_ID", how="left", validate="one_to_one")
    d["observed_later_calc"] = d["observed_later_calc"].fillna(0).astype(int)
    rows = []
    for state, sub in d.groupby("state", dropna=False):
        later = sub.loc[sub["observed_later_calc"].eq(1)]
        rows.append({
            "state": state,
            "n": int(len(sub)),
            "first_cmat_use_rate": float((sub["MU_FIRST_CMAT_VISITS"] > 0).mean()),
            "mean_first_cmat_visits": float(sub["MU_FIRST_CMAT_VISITS"].mean()),
            "eventual_mu_pass_rate": float(sub["MU_EVER_PASSED"].mean()),
            "observed_later_calc_rate": float(sub["observed_later_calc"].mean()),
            "later_calc_cmat_use_rate": float(later["CALC_FIRST_ANY_CMAT"].mean()) if len(later) else np.nan,
        })
    return pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)


def _state_measurement_audit(mu_students: pd.DataFrame) -> pd.DataFrame:
    d = mu_students.copy()
    z = pd.to_numeric(d["MU_FIRST_Z"], errors="coerce")
    grade = pd.to_numeric(d["MU_FIRST_GRADE"], errors="coerce")
    context = pd.to_numeric(d["MU_FIRST_LOO_PASS_RATE"], errors="coerce")
    rows = [
        {"metric": "n_mu_students", "value": int(len(d))},
        {"metric": "share_missing_relative_z", "value": float(z.isna().mean())},
        {"metric": "share_missing_classroom_context", "value": float(context.isna().mean())},
        {"metric": "share_missing_z_with_numeric_grade", "value": float((z.isna() & grade.notna()).mean())},
        {"metric": "share_missing_z_without_numeric_grade", "value": float((z.isna() & grade.isna()).mean())},
    ]
    if z.isna().any():
        missing_z = z.isna()
        rows.extend([
            {
                "metric": "among_missing_z_share_numeric_grade",
                "value": float(grade.loc[missing_z].notna().mean()),
            },
            {
                "metric": "among_missing_z_share_no_numeric_grade",
                "value": float(grade.loc[missing_z].isna().mean()),
            },
        ])
    return pd.DataFrame(rows)


def main() -> int:
    config = replace(get_study_config(REPO_ROOT), output_dir=REPO_ROOT / "results")
    data = load_and_clean_inputs(config)
    trajectories = build_engagement_trajectory_data(data, config, min_history_n=20)
    coverage = set(zip(
        data.data_quality["coverage"]["YEAR"].astype(int),
        data.data_quality["coverage"]["SESSION"],
    ))
    covered_academic_rows = data.academics.loc[
        [(int(y), s) in coverage for y, s in zip(data.academics["YEAR"], data.academics["SESSION"])]
    ]
    covered_period_indices = set(
        pd.to_numeric(covered_academic_rows["PERIOD_INDEX"], errors="coerce").dropna().astype(int)
    )

    mu_students = trajectories.mu_students.loc[
        _coverage_mask(trajectories.mu_students, coverage)
    ].copy()
    calc_choices = trajectories.calc_choices.loc[
        _coverage_mask(trajectories.calc_choices, coverage)
        & trajectories.calc_choices["STUDENT_ID"].isin(mu_students["STUDENT_ID"])
    ].copy()
    repeats = trajectories.repeat_transitions.loc[
        trajectories.repeat_transitions["PREV_PERIOD_INDEX"].isin(covered_period_indices)
        & trajectories.repeat_transitions["NEXT_PERIOD_INDEX"].isin(covered_period_indices)
    ].copy()

    outputs = {
        "230_career_experience_interaction_reduced.csv": career_heterogeneity_reduced_interactions(
            mu_students, min_career_ns=(100, 150, 200)
        ),
        "231_post_failure_numeric_severity_models.csv": post_failure_numeric_severity_models(
            repeats, min_career_n=config.min_career_n_for_inference
        ),
        "232_primary_experience_state_summary.csv": _primary_state_summary(mu_students, calc_choices),
        "233_state_measurement_audit.csv": _state_measurement_audit(mu_students),
    }
    for filename, frame in outputs.items():
        _save(frame, filename)

    summary = {
        "mu_students": int(len(mu_students)),
        "covered_post_failure_transitions": int(len(repeats)),
        "outputs": list(outputs),
        "note": (
            "Career-by-state interaction uses aggressive pre-specified pooling thresholds; "
            "numeric-failure models exclude failures without a classroom-relative Z."
        ),
    }
    (REPO_ROOT / "results" / "confirmatory_extra_run_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
