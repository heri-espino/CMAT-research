#!/usr/bin/env python3
"""Run the pre-specified confirmatory design checks for Paper 4.

All reusable estimators live in ``cmat_analysis``. This publication recipe restricts
samples to the paper's controlled cohorts, composes the four confirmatory analysis
blocks, and writes aggregate outputs only.
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
from cmat_analysis.ppa.adaptation_audit import (
    attach_observed_choice_set_size,
    augment_repeat_transition_context,
    observed_course_instructor_counts,
)
from cmat_analysis.ppa.adaptation_confirmatory import (
    administrative_choice_constraint_audit,
    career_heterogeneity_tests,
    choice_set_audit,
    choice_set_sensitivity_models,
    continuous_challenge_response_model,
    experience_state_sensitivity,
    post_failure_response_models,
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


def _threshold_contrast_stability(sensitivity: pd.DataFrame) -> pd.DataFrame:
    rows = []
    keys = ["performance_cut", "difficulty_quantile", "difficulty_pass_rate_cut"]
    for values, sub in sensitivity.groupby(keys, dropna=False):
        indexed = sub.set_index("state")
        rates = indexed["first_cmat_use_rate"].to_dict()
        progression = indexed.get("observed_later_calc_rate", pd.Series(dtype=float)).to_dict()
        contextual = rates.get("contextual_challenge", np.nan)
        individual = rates.get("individual_strain", np.nan)
        compounded = rates.get("compounded_strain", np.nan)
        lower = rates.get("lower_strain", np.nan)
        rows.append({
            "performance_cut": values[0],
            "difficulty_quantile": values[1],
            "difficulty_pass_rate_cut": values[2],
            "contextual_minus_lower_cmat_pp": contextual - lower,
            "contextual_minus_individual_cmat_pp": contextual - individual,
            "contextual_minus_compounded_cmat_pp": contextual - compounded,
            "contextual_highest_of_four_cmat": bool(
                np.isfinite(contextual)
                and contextual >= np.nanmax([lower, individual, compounded])
            ),
            "individual_later_calc_rate": progression.get("individual_strain", np.nan),
            "compounded_later_calc_rate": progression.get("compounded_strain", np.nan),
        })
    return pd.DataFrame(rows).sort_values(["performance_cut", "difficulty_quantile"]).reset_index(drop=True)


def _post_failure_context_definition_summary(repeats: pd.DataFrame) -> pd.DataFrame:
    rows = []
    measures = {
        "within_period_percentile": "DELTA_PROF_EASINESS_PERCENTILE",
        "absolute_prior_pass_rate": "DELTA_PROF_PRIOR_PASS_RATE",
        "absolute_prior_mean_grade": "DELTA_PROF_PRIOR_MEAN_GRADE",
    }
    for attempt, sub in repeats.groupby("FAILED_ATTEMPT_NUMBER"):
        for definition, column in measures.items():
            values = pd.to_numeric(sub[column], errors="coerce").dropna()
            rows.append({
                "failed_attempt_number": int(attempt),
                "context_definition": definition,
                "n_comparable": int(len(values)),
                "mean_change": float(values.mean()) if len(values) else np.nan,
                "median_change": float(values.median()) if len(values) else np.nan,
                "share_moving_higher": float((values > 0).mean()) if len(values) else np.nan,
            })
    return pd.DataFrame(rows).sort_values(
        ["failed_attempt_number", "context_definition"]
    ).reset_index(drop=True)


def _attach_repeat_choice_set_support(
    repeats: pd.DataFrame,
    mu_attempts: pd.DataFrame,
    mu_period_counts: pd.DataFrame,
) -> pd.DataFrame:
    attempt_support = mu_attempts[[
        "STUDENT_ID",
        "MU_ATTEMPT_NUMBER",
        "MU_OFFER_ELIGIBLE_INSTRUCTORS",
    ]].drop_duplicates(["STUDENT_ID", "MU_ATTEMPT_NUMBER"])
    prev_support = attempt_support.rename(columns={
        "MU_ATTEMPT_NUMBER": "FAILED_ATTEMPT_NUMBER",
        "MU_OFFER_ELIGIBLE_INSTRUCTORS": "PREV_RANKABLE_INSTRUCTOR_N",
    })
    next_support = attempt_support.rename(columns={
        "MU_ATTEMPT_NUMBER": "NEXT_ATTEMPT_NUMBER",
        "MU_OFFER_ELIGIBLE_INSTRUCTORS": "NEXT_RANKABLE_INSTRUCTOR_N",
    })
    out = repeats.merge(
        prev_support,
        on=["STUDENT_ID", "FAILED_ATTEMPT_NUMBER"],
        how="left",
        validate="many_to_one",
    ).merge(
        next_support,
        on=["STUDENT_ID", "NEXT_ATTEMPT_NUMBER"],
        how="left",
        validate="many_to_one",
    )
    prev_counts = mu_period_counts.rename(columns={
        "PERIOD_INDEX": "PREV_PERIOD_INDEX",
        "OBSERVED_INSTRUCTOR_N": "PREV_OBSERVED_INSTRUCTOR_N",
    })
    next_counts = mu_period_counts.rename(columns={
        "PERIOD_INDEX": "NEXT_PERIOD_INDEX",
        "OBSERVED_INSTRUCTOR_N": "NEXT_OBSERVED_INSTRUCTOR_N",
    })
    return out.merge(prev_counts, on="PREV_PERIOD_INDEX", how="left", validate="many_to_one").merge(
        next_counts, on="NEXT_PERIOD_INDEX", how="left", validate="many_to_one"
    )


def _repeat_choice_set_audit(repeats: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for attempt, sub in repeats.groupby("FAILED_ATTEMPT_NUMBER"):
        next_rankable = pd.to_numeric(sub["NEXT_RANKABLE_INSTRUCTOR_N"], errors="coerce")
        next_observed = pd.to_numeric(sub["NEXT_OBSERVED_INSTRUCTOR_N"], errors="coerce")
        comparable = pd.to_numeric(sub["DELTA_PROF_EASINESS_PERCENTILE"], errors="coerce").notna()
        rows.append({
            "failed_attempt_number": int(attempt),
            "n_transitions": int(len(sub)),
            "share_with_comparable_professor_percentiles": float(comparable.mean()),
            "mean_next_observed_instructor_n": float(next_observed.mean()),
            "mean_next_rankable_instructor_n": float(next_rankable.mean()),
            "share_next_rankable_ge_2": float(next_rankable.ge(2).mean()),
            "share_next_rankable_ge_3": float(next_rankable.ge(3).mean()),
            "share_next_rankable_ge_4": float(next_rankable.ge(4).mean()),
            "mean_next_history_coverage": float(
                (next_rankable / next_observed.replace(0, np.nan)).mean()
            ),
        })
    return pd.DataFrame(rows).sort_values("failed_attempt_number").reset_index(drop=True)


def main() -> int:
    base_config = get_study_config(REPO_ROOT)
    config = replace(base_config, output_dir=REPO_ROOT / "results")
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
    repeats = augment_repeat_transition_context(repeats, trajectories.mu_attempts)

    calc_period_counts = observed_course_instructor_counts(
        data.academics,
        passing_grade=config.passing_grade,
        subject_code=config.followup_subject_code,
        subject_name=config.followup_subject_name,
    )
    calc_choices = attach_observed_choice_set_size(calc_choices, calc_period_counts)

    mu_period_counts = observed_course_instructor_counts(
        data.academics,
        passing_grade=config.passing_grade,
        subject_code=config.primary_subject_code,
        subject_name=config.primary_subject_name,
    )
    repeats = _attach_repeat_choice_set_support(repeats, trajectories.mu_attempts, mu_period_counts)

    threshold_sensitivity = experience_state_sensitivity(
        mu_students,
        later_calc_student_ids=set(calc_choices["STUDENT_ID"].astype(str)),
        performance_cuts=(-0.25, -0.5, -0.75),
        difficulty_quantiles=(0.20, 0.25, 1 / 3),
    )
    threshold_contrasts = _threshold_contrast_stability(threshold_sensitivity)
    continuous_model = continuous_challenge_response_model(
        mu_students,
        min_career_n=config.min_career_n_for_inference,
    )
    post_failure_models = post_failure_response_models(
        repeats,
        min_career_n=config.min_career_n_for_inference,
    )
    context_definition_summary = _post_failure_context_definition_summary(repeats)
    career_tests = career_heterogeneity_tests(
        mu_students,
        calc_choices,
        min_career_n=config.min_career_n_for_inference,
    )
    calc_set_audit = choice_set_audit(calc_choices)
    calc_set_sensitivity = choice_set_sensitivity_models(
        calc_choices,
        min_career_n=config.min_career_n_for_inference,
        rankable_thresholds=(2, 3, 4, 5),
        min_history_coverage=0.75,
    )
    constraint_audit = administrative_choice_constraint_audit(data.academics)
    repeat_set_audit = _repeat_choice_set_audit(repeats)

    outputs = {
        "220_difficulty_threshold_sensitivity.csv": threshold_sensitivity,
        "221_difficulty_contrast_stability.csv": threshold_contrasts,
        "222_continuous_challenge_cmat_model.csv": continuous_model,
        "223_post_failure_response_models.csv": post_failure_models,
        "224_post_failure_context_definition_sensitivity.csv": context_definition_summary,
        "225_career_heterogeneity_omnibus.csv": career_tests,
        "226_calc_choice_set_audit.csv": calc_set_audit,
        "227_calc_choice_set_model_sensitivity.csv": calc_set_sensitivity,
        "228_administrative_choice_constraint_audit.csv": constraint_audit,
        "229_post_failure_choice_set_audit.csv": repeat_set_audit,
    }
    for filename, frame in outputs.items():
        _save(frame, filename)

    summary = {
        "mu_students": int(len(mu_students)),
        "later_calc_choices": int(len(calc_choices)),
        "rankable_calc_choices": int(calc_choices["CALC_CHOSEN_EASINESS_PERCENTILE"].notna().sum()),
        "covered_post_failure_transitions": int(len(repeats)),
        "difficulty_threshold_specifications": int(
            threshold_sensitivity[["performance_cut", "difficulty_quantile"]].drop_duplicates().shape[0]
        ),
        "outputs": list(outputs),
        "interpretation": (
            "Confirmatory observational robustness checks. Historical instructor outcomes do not "
            "identify intrinsic professor difficulty or unconstrained student preference; observed "
            "period-wide instructor sets remain proxies when schedule/capacity constraints are absent."
        ),
    }
    (REPO_ROOT / "results" / "confirmatory_run_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
