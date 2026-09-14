#!/usr/bin/env python3
"""Run Paper 4 engagement-related adaptation analyses from shared CMAT helpers.

This is intentionally a thin publication recipe. Cohort reconstruction, historical
instructor context, choice-set ranking, experience profiles, and repeat-attempt
transitions live in :mod:`cmat_analysis.ppa`. This script writes only aggregate outputs.
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from cmat_analysis.cohorts import load_and_clean_inputs
from cmat_analysis.config.study_config import get_study_config
from cmat_analysis.ppa import (
    build_engagement_trajectory_data,
    calc_choice_association_models,
    experience_profile_summary,
    repeat_attempt_summary,
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


def _mu_outcome_summary(mu_students: pd.DataFrame) -> pd.DataFrame:
    rows = []
    total = len(mu_students)
    for profile, sub in mu_students.groupby("MU_ATTEMPT_OUTCOME_PROFILE", dropna=False):
        rows.append({
            "mu_attempt_outcome_profile": profile,
            "n": int(len(sub)),
            "share": float(len(sub) / total) if total else np.nan,
            "mean_first_cmat_visits": float(sub["MU_FIRST_CMAT_VISITS"].mean()),
            "any_first_cmat_rate": float((sub["MU_FIRST_CMAT_VISITS"] > 0).mean()),
            "mean_cumulative_cmat_visits": float(sub["MU_CUMULATIVE_CMAT_VISITS"].mean()),
            "mean_distinct_mu_professors": float(sub["MU_DISTINCT_PROFESSORS"].mean()),
        })
    return pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)


def _profile_progression_summary(mu_students: pd.DataFrame, calc_ids: set[str], min_n: int = 20) -> pd.DataFrame:
    d = mu_students.copy()
    d["OBSERVED_LATER_CALC"] = d["STUDENT_ID"].isin(calc_ids).astype(int)
    rows = []
    for profile, sub in d.groupby("MU_EXPERIENCE_PROFILE", dropna=False):
        if len(sub) < min_n:
            continue
        rows.append({
            "profile": profile,
            "n": int(len(sub)),
            "eventual_mu_pass_rate": float(sub["MU_EVER_PASSED"].mean()),
            "observed_later_calc_rate": float(sub["OBSERVED_LATER_CALC"].mean()),
            "mean_first_z": float(pd.to_numeric(sub["MU_FIRST_Z"], errors="coerce").mean()),
            "mean_first_classroom_pass_rate": float(sub["MU_FIRST_LOO_PASS_RATE"].mean()),
            "mean_first_cmat_visits": float(sub["MU_FIRST_CMAT_VISITS"].mean()),
            "mean_cumulative_cmat_visits": float(sub["MU_CUMULATIVE_CMAT_VISITS"].mean()),
        })
    return pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)


def _career_adaptation_summary(
    mu_students: pd.DataFrame,
    calc_choices: pd.DataFrame,
    *,
    min_n: int = 30,
) -> pd.DataFrame:
    mu_rows = []
    for career, sub in mu_students.groupby("MU_FIRST_CAREER", dropna=False):
        if len(sub) < min_n:
            continue
        mu_rows.append({
            "career": career,
            "n_mu": int(len(sub)),
            "first_attempt_fail_rate": float((sub["MU_ATTEMPT_OUTCOME_PROFILE"] != "pass_first").mean()),
            "eventual_mu_pass_rate": float(sub["MU_EVER_PASSED"].mean()),
            "first_cmat_use_rate": float((sub["MU_FIRST_CMAT_VISITS"] > 0).mean()),
            "mean_first_cmat_visits": float(sub["MU_FIRST_CMAT_VISITS"].mean()),
            "mean_cumulative_mu_cmat_visits": float(sub["MU_CUMULATIVE_CMAT_VISITS"].mean()),
        })
    out = pd.DataFrame(mu_rows)
    calc_rows = []
    for career, sub in calc_choices.groupby("MU_FIRST_CAREER", dropna=False):
        rank = pd.to_numeric(sub["CALC_CHOSEN_EASINESS_PERCENTILE"], errors="coerce")
        calc_rows.append({
            "career": career,
            "n_later_calc": int(len(sub)),
            "n_rankable_calc_choice": int(rank.notna().sum()),
            "mean_chosen_easiness_percentile": float(rank.mean()),
            "top_quartile_easiness_choice_rate": float((rank >= 0.75).mean()) if rank.notna().any() else np.nan,
            "calc_cmat_use_rate": float(sub["CALC_FIRST_ANY_CMAT"].mean()),
        })
    if len(calc_rows):
        out = out.merge(pd.DataFrame(calc_rows), on="career", how="left")
    return out.sort_values("n_mu", ascending=False).reset_index(drop=True)


def _repeat_by_career(transitions: pd.DataFrame, min_n: int = 20) -> pd.DataFrame:
    rows = []
    for career, sub in transitions.groupby("CAREER", dropna=False):
        if len(sub) < min_n:
            continue
        delta = pd.to_numeric(sub["DELTA_PROF_EASINESS_PERCENTILE"], errors="coerce")
        rows.append({
            "career": career,
            "n_repeat_transitions": int(len(sub)),
            "professor_change_rate": float(sub["CHANGED_PROFESSOR"].mean()),
            "prev_cmat_use_rate": float(sub["PREV_ANY_CMAT"].mean()),
            "next_cmat_use_rate": float(sub["NEXT_ANY_CMAT"].mean()),
            "mean_delta_cmat_visits": float(sub["DELTA_CMAT_VISITS"].mean()),
            "next_attempt_pass_rate": float(sub["NEXT_ATTEMPT_PASS"].mean()),
            "n_rankable_professor_changes": int(delta.notna().sum()),
            "mean_delta_prof_easiness_percentile": float(delta.mean()),
            "share_moving_to_higher_easiness_percentile": float((delta > 0).mean()) if delta.notna().any() else np.nan,
        })
    return pd.DataFrame(rows).sort_values("n_repeat_transitions", ascending=False).reset_index(drop=True)


def _experience_choice_interaction_model(calc_choices: pd.DataFrame, min_career_n: int = 30) -> pd.DataFrame:
    required = [
        "CALC_CHOSEN_EASINESS_PERCENTILE",
        "MU_FIRST_Z",
        "MU_FIRST_LOO_PASS_RATE",
        "MU_FIRST_VISIT_GROUP",
        "MU_ATTEMPT_OUTCOME_PROFILE",
        "MU_FIRST_CAREER",
        "CALC_FIRST_PERIOD_LABEL",
        "MU_FIRST_CLASSROOM_ID",
    ]
    d = calc_choices.dropna(subset=required).copy()
    if d.empty:
        return pd.DataFrame()
    counts = d["MU_FIRST_CAREER"].value_counts()
    keep = set(counts[counts >= min_career_n].index)
    d["_CAREER"] = d["MU_FIRST_CAREER"].where(d["MU_FIRST_CAREER"].isin(keep), "OTHER")
    for source, target in (("MU_FIRST_Z", "_Z"), ("MU_FIRST_LOO_PASS_RATE", "_PASSCTX")):
        values = pd.to_numeric(d[source], errors="coerce")
        sd = float(values.std(ddof=0))
        d[target] = (values - values.mean()) / sd if sd > 0 else np.nan
    formula = (
        "CALC_CHOSEN_EASINESS_PERCENTILE ~ _Z * _PASSCTX "
        "+ C(MU_FIRST_VISIT_GROUP) + C(MU_ATTEMPT_OUTCOME_PROFILE) "
        "+ C(_CAREER) + C(CALC_FIRST_PERIOD_LABEL)"
    )
    fit = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["MU_FIRST_CLASSROOM_ID"]}
    )
    focal = {"_Z", "_PASSCTX", "_Z:_PASSCTX"}
    rows = []
    for term in focal:
        rows.append({
            "term": term,
            "n": int(fit.nobs),
            "mu_classroom_clusters": int(d["MU_FIRST_CLASSROOM_ID"].nunique()),
            "estimate": float(fit.params[term]),
            "se_cluster": float(fit.bse[term]),
            "p_value": float(fit.pvalues[term]),
            "r2": float(fit.rsquared),
        })
    return pd.DataFrame(rows)


def main() -> int:
    base_config = get_study_config(REPO_ROOT)
    config = replace(base_config, output_dir=REPO_ROOT / "results")
    data = load_and_clean_inputs(config)
    trajectories = build_engagement_trajectory_data(data, config, min_history_n=20)

    coverage = set(zip(
        data.data_quality["coverage"]["YEAR"].astype(int),
        data.data_quality["coverage"]["SESSION"],
    ))
    mu_students = trajectories.mu_students.copy()
    mu_students = mu_students.loc[_coverage_mask(mu_students, coverage)].copy()
    calc_choices = trajectories.calc_choices.copy()
    calc_choices = calc_choices.loc[
        _coverage_mask(calc_choices, coverage)
        & calc_choices["STUDENT_ID"].isin(mu_students["STUDENT_ID"])
    ].copy()
    repeats = trajectories.repeat_transitions.copy()

    profile_all = _profile_progression_summary(
        mu_students,
        set(calc_choices["STUDENT_ID"].astype(str)),
        min_n=20,
    )
    calc_profile = experience_profile_summary(calc_choices, min_n=20)
    complete_choice = calc_choices.dropna(subset=[
        "CALC_CHOSEN_EASINESS_PERCENTILE",
        "MU_FIRST_Z",
        "MU_FIRST_LOO_PASS_RATE",
    ]).copy()
    choice_models = calc_choice_association_models(
        complete_choice,
        min_career_n=config.min_career_n_for_inference,
    )
    interaction = _experience_choice_interaction_model(
        calc_choices,
        min_career_n=config.min_career_n_for_inference,
    )
    repeat_summary = repeat_attempt_summary(repeats) if len(repeats) else pd.DataFrame()

    outputs = {
        "200_mu_attempt_outcome_summary.csv": _mu_outcome_summary(mu_students),
        "201_mu_experience_profile_progression.csv": profile_all,
        "202_calc_experience_profile_adaptation.csv": calc_profile,
        "203_calc_choice_association_models.csv": choice_models,
        "204_calc_choice_performance_difficulty_interaction.csv": interaction,
        "205_mu_repeat_attempt_summary.csv": repeat_summary,
        "206_mu_repeat_attempt_by_career.csv": _repeat_by_career(repeats) if len(repeats) else pd.DataFrame(),
        "207_career_adaptation_summary.csv": _career_adaptation_summary(
            mu_students,
            calc_choices,
            min_n=config.min_career_n_for_inference,
        ),
    }
    for filename, frame in outputs.items():
        _save(frame, filename)

    summary = {
        "mu_students_with_cmat_coverage": int(len(mu_students)),
        "mu_real_attempt_rows": int(len(trajectories.mu_attempts)),
        "students_with_first_later_calc_and_cmat_coverage": int(len(calc_choices)),
        "rankable_calc_choices": int(calc_choices["CALC_CHOSEN_EASINESS_PERCENTILE"].notna().sum()),
        "repeat_transitions_after_failed_mu_attempt": int(len(repeats)),
        "profiles_retained_all_mu": int(len(profile_all)),
        "profiles_retained_calc": int(len(calc_profile)),
        "outputs": list(outputs),
        "interpretation": (
            "Administrative traces of engagement-related adaptation; not direct latent engagement, "
            "causal professor difficulty, or causal instructor-choice effects."
        ),
    }
    (REPO_ROOT / "results" / "engagement_run_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
