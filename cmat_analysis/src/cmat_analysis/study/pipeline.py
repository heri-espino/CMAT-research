from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .cohort import build_study_cohorts, load_and_clean_inputs
from .outcomes import add_primary_outcomes
from .plots import (
    plot_continuation,
    plot_longitudinal_persistence,
    plot_primary_group_means,
    plot_visit_distribution,
    plot_daily_cmat_timeline,
    plot_term_peak_profiles,
    plot_same_day_ppa_behavior,
    plot_peak_spacing,
    plot_monthly_periodicity_acf,
    plot_exact3_regularity_performance,
)
from .selection import propensity_att_sensitivity
from .extended_analysis import (
    one_two_pooling_analysis,
    welch_anova_visit_groups,
    career_usage_association,
    career_performance_analysis,
    career_visit_interaction_model,
    clustered_visit_group_omnibus,
    clustered_career_omnibus,
    exact_visit_performance_index,
    longitudinal_any_visit_transition,
    clustered_omnibus_visit_group_test,
    clustered_omnibus_career_test,
    exact_visit_index_trend,
)
from .extended_plots import (
    plot_exact_visit_performance_index,
    plot_career_performance,
    plot_longitudinal_any_visit_transition,
    plot_career_usage_rates,
)
from .ppa_progression import (
    build_ppa_progression_cohort,
    ppa_behavior_profiles,
    persistence_by_mu_group,
    ppa_persistence_association_tests,
    persistence_logistic_models,
    piecewise_threshold_persistence_model,
    later_performance_models,
    major_persistence_summary,
    course_specific_transition,
    form_career_crosswalk,
    major_persistence_joint_test,
    major_delta_z_welch,
)
from .ppa_plots import (
    plot_ppa_persistence_by_mu_group,
    plot_ppa_academic_trajectory_profiles,
)
from .temporal import (
    TemporalPeakConfig,
    daily_service_counts,
    detect_period_peaks,
    peak_spacing_summary,
    primary_period_visit_events,
    same_day_ppa_behavior,
    top_daily_dates,
    student_temporal_regularity,
    monthly_periodicity_diagnostics,
)
from .statistics import (
    bunching_metrics,
    continuation_curve,
    dose_group_fixed_effect_model,
    group_summary,
    longitudinal_summary,
    primary_fixed_effect_models,
    robust_two_group_tests,
    secondary_pass_model,
    visit_distribution,
    temporal_regularity_performance_models,
    exact_visit_count_regularity_summary,
)


def _json_default(obj):
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (pd.Timestamp,)):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(type(obj).__name__)


def _save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _merge_extra_covariates(mu: pd.DataFrame, config) -> tuple[pd.DataFrame, list[str], str]:
    d = mu.copy()
    extras: list[str] = []
    if config.extra_covariates_path is None or not Path(config.extra_covariates_path).exists():
        return d, extras, "No optional pre-treatment covariate file found. Current adjustment is limited to variables already available in the academic file."
    extra = pd.read_excel(config.extra_covariates_path)
    if "CLAVEALUMNO" not in extra.columns:
        return d, extras, "Optional covariate file found but CLAVEALUMNO is missing; file was not joined."
    extra = extra.rename(columns={"CLAVEALUMNO": "STUDENT_ID"})
    extra["STUDENT_ID"] = pd.to_numeric(extra["STUDENT_ID"], errors="coerce").astype("Int64")
    extras = [c for c in extra.columns if c != "STUDENT_ID"]
    d = d.merge(extra, on="STUDENT_ID", how="left")
    return d, extras, f"Joined optional covariate file with {len(extras)} additional columns."


def run_study_pipeline(config) -> dict[str, object]:
    out = Path(config.output_dir)
    tables = out / "tables"
    figures = out / "figures"
    out.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    data = load_and_clean_inputs(config)
    cohorts = build_study_cohorts(data, config)

    mu = add_primary_outcomes(cohorts["mu_primary"], config)
    calc = add_primary_outcomes(cohorts["calc_comparator"], config)
    longitudinal = add_primary_outcomes(cohorts["longitudinal"], config)

    # Choose the primary exposure centrally; both measures are always retained.
    if config.primary_visit_measure == "course_specific":
        visits_col = "VISITS_COURSE"
        group_col = "VISIT_GROUP_COURSE"
        treatment_col = "PERSISTENT_GT3_COURSE"
        mu_group_long = "MU_VISIT_GROUP_COURSE"
        calc_visits_long = "VISITS_COURSE"
    else:
        visits_col = "VISITS_CMAT_PERIOD"
        group_col = "VISIT_GROUP_PERIOD"
        treatment_col = "PERSISTENT_GT3_PERIOD"
        mu_group_long = "MU_VISIT_GROUP_PERIOD"
        calc_visits_long = "VISITS_CMAT_PERIOD"

    # Cohort flow / quality.
    coverage = data.data_quality["coverage"].copy()
    _save_csv(coverage, tables / "00_advisory_period_coverage.csv")
    quality = {k: v for k, v in data.data_quality.items() if k != "coverage"}
    with open(out / "data_quality.json", "w", encoding="utf-8") as f:
        json.dump(quality, f, ensure_ascii=False, indent=2, default=_json_default)

    flow = pd.DataFrame([
        {"stage": "eligible first MU attempts, all academic periods", "n": len(cohorts["mu_all_first_attempts"])},
        {"stage": "primary MU cohort with advisory coverage", "n": len(mu)},
        {"stage": "first Calculus I attempts with advisory coverage (comparator)", "n": len(calc)},
        {"stage": "students progressing from MU to later Calculus I", "n": len(cohorts["longitudinal"])},
        {"stage": "longitudinal pairs with Calculus advisory coverage", "n": int(cohorts["longitudinal"]["CALC_VISIT_COVERAGE"].sum())},
    ])
    _save_csv(flow, tables / "01_cohort_flow.csv")

    # RQ1: incentive-associated visit distribution and comparator without PPA.
    dist = pd.concat([
        visit_distribution(mu, visits_col, "Matemáticas Universitarias"),
        visit_distribution(calc, visits_col, "Cálculo I"),
    ], ignore_index=True)
    _save_csv(dist, tables / "02_visit_distribution_mu_vs_calculus.csv")
    continuation = pd.concat([
        continuation_curve(mu, visits_col, "Matemáticas Universitarias"),
        continuation_curve(calc, visits_col, "Cálculo I"),
    ], ignore_index=True)
    _save_csv(continuation, tables / "03_continuation_probability.csv")
    bunching = pd.concat([
        bunching_metrics(mu, visits_col, config.ppa_threshold, "Matemáticas Universitarias"),
        bunching_metrics(calc, visits_col, config.ppa_threshold, "Cálculo I"),
    ], ignore_index=True)
    _save_csv(bunching, tables / "04_bunching_metrics.csv")

    # Confirmed PPA rule counts any CMAT visit in the period. Course-tagged
    # visits are retained as a sensitivity/description only.
    course_specific_bunching = pd.concat([
        bunching_metrics(mu, "VISITS_COURSE", config.ppa_threshold, "Matemáticas Universitarias"),
        bunching_metrics(calc, "VISITS_COURSE", config.ppa_threshold, "Cálculo I"),
    ], ignore_index=True)
    _save_csv(course_specific_bunching, tables / "05_bunching_metrics_course_specific_sensitivity.csv")

    cohort_period = (
        mu.groupby(["YEAR", "SESSION"], observed=True)
        .agg(
            n=("STUDENT_ID", "size"),
            any_cmat_visit=("VISITS_CMAT_PERIOD", lambda x: float((x > 0).mean())),
            reached_ppa_ge3=("VISITS_CMAT_PERIOD", lambda x: float((x >= config.ppa_threshold).mean())),
            exact_3_visits=("VISITS_CMAT_PERIOD", lambda x: float((x == config.ppa_threshold).mean())),
            beyond_ppa_gt3=("VISITS_CMAT_PERIOD", lambda x: float((x > config.ppa_threshold).mean())),
            mean_cmat_visits=("VISITS_CMAT_PERIOD", "mean"),
        )
        .reset_index()
        .sort_values(["YEAR", "SESSION"])
    )
    _save_csv(cohort_period, tables / "06_primary_cohort_visits_by_period.csv")

    # Temporal attendance module: calendar-day concentration, same-day PPA
    # completion behavior, and recurring service-load peaks.  Exact times are
    # used only to order visits; all exported temporal tables are day-level.
    mu_visit_events = primary_period_visit_events(mu, data.advisories)
    daily_all = daily_service_counts(data.advisories, "All CMAT")
    daily_mu = daily_service_counts(mu_visit_events, "First-MU cohort during MU term")
    _save_csv(daily_all, tables / "60_daily_visit_counts_all_cmat.csv")
    _save_csv(daily_mu, tables / "61_daily_visit_counts_mu_cohort.csv")

    temporal_students, same_day_summary, max_daily_dist, ppa_completion_dates = same_day_ppa_behavior(
        mu, mu_visit_events, threshold=config.ppa_threshold
    )
    _save_csv(same_day_summary, tables / "62_mu_same_day_ppa_behavior_summary.csv")
    _save_csv(max_daily_dist, tables / "63_mu_max_same_day_visit_distribution.csv")
    _save_csv(ppa_completion_dates, tables / "64_ppa_completion_dates.csv")

    top_dates = pd.concat([
        top_daily_dates(daily_all, 30),
        top_daily_dates(daily_mu, 30),
    ], ignore_index=True)
    _save_csv(top_dates, tables / "65_top_cmat_dates.csv")

    peak_cfg = TemporalPeakConfig()
    all_peaks, all_profiles, all_intervals = detect_period_peaks(
        data.advisories, peak_cfg, population="All CMAT"
    )
    mu_peaks, mu_profiles, mu_intervals = detect_period_peaks(
        mu_visit_events, peak_cfg, population="First-MU cohort during MU term"
    )
    temporal_peaks = pd.concat([all_peaks, mu_peaks], ignore_index=True)
    temporal_profiles = pd.concat([all_profiles, mu_profiles], ignore_index=True)
    temporal_intervals = pd.concat([all_intervals, mu_intervals], ignore_index=True)
    temporal_peak_summary = peak_spacing_summary(temporal_peaks, temporal_intervals, peak_cfg)
    _save_csv(temporal_peaks, tables / "66_detected_temporal_peaks.csv")
    _save_csv(temporal_intervals, tables / "67_peak_spacing_intervals.csv")
    _save_csv(temporal_peak_summary, tables / "68_peak_spacing_summary.csv")

    # Formal descriptive cycle diagnostics for RQ1b. Exact professor exam dates
    # are not observed, so these estimate recurrence consistent with an
    # approximately monthly assessment rhythm without labeling peaks as exams.
    monthly_acf, monthly_periods = monthly_periodicity_diagnostics(
        data.advisories, population="All CMAT"
    )
    _save_csv(monthly_acf, tables / "69_monthly_cycle_autocorrelation.csv")
    _save_csv(monthly_periods, tables / "70_monthly_cycle_periodogram_by_term.csv")

    # Student-level temporal distribution. Calendar-month spread is the primary
    # RQ2b regularity measure because exact exam dates differ by professor and
    # are unobserved. Week/day metrics are retained as sensitivity measures.
    temporal_regularity = student_temporal_regularity(
        mu, mu_visit_events, visits_col=visits_col, assessment_cycles=4
    )
    reg_cols = [
        "STUDENT_ID", "ACTIVE_DAYS", "ACTIVE_WEEKS", "ACTIVE_CALENDAR_MONTHS",
        "VISIT_SPAN_DAYS", "MAX_VISITS_ONE_DAY", "MAX_SAME_DAY_SHARE",
        "WEEK_ENTROPY", "EFFECTIVE_WEEKS", "EFFECTIVE_WEEKS_PER_VISIT",
        "ACTIVE_MONTHS_CAPPED4", "REGULARITY_MONTHLY_4", "VISITS_CAPPED_8",
    ]
    mu = mu.merge(temporal_regularity[reg_cols], on="STUDENT_ID", how="left")
    regularity_distribution = (
        mu.loc[mu[visits_col] >= config.ppa_threshold]
        .groupby(["ACTIVE_MONTHS_CAPPED4"], observed=True)
        .agg(
            students=("STUDENT_ID", "size"),
            mean_visits=(visits_col, "mean"),
            mean_regularity=("REGULARITY_MONTHLY_4", "mean"),
            mean_effective_weeks=("EFFECTIVE_WEEKS", "mean"),
        )
        .reset_index()
    )
    _save_csv(regularity_distribution, tables / "71_ppa_temporal_regularity_distribution.csv")

    # Primary outcome: continuous performance.
    primary_summary = group_summary(mu, group_col, "Z_GRADE_PRIMARY")
    _save_csv(primary_summary, tables / "10_primary_outcome_by_visit_group.csv")
    robust = robust_two_group_tests(mu, treatment_col, "Z_GRADE_PRIMARY", seed=config.random_seed)
    _save_csv(robust, tables / "11_primary_robust_gt3_vs_le3.csv")
    fe = primary_fixed_effect_models(mu, "Z_GRADE_PRIMARY", treatment_col)
    _save_csv(fe, tables / "12_primary_fixed_effect_models.csv")
    dose = dose_group_fixed_effect_model(mu, "Z_GRADE_PRIMARY", group_col)
    _save_csv(dose, tables / "13_primary_dose_group_model.csv")

    # Complementary institutional-threshold contrast: reached PPA (>=3) vs <3.
    reached_col = "PPA_REACHED_PERIOD" if config.primary_visit_measure != "course_specific" else "PPA_REACHED_COURSE"
    reached_robust = robust_two_group_tests(mu, reached_col, "Z_GRADE_PRIMARY", seed=config.random_seed)
    _save_csv(reached_robust, tables / "15_ppa_reached_ge3_vs_lt3_robust.csv")
    reached_fe = primary_fixed_effect_models(mu, "Z_GRADE_PRIMARY", reached_col)
    _save_csv(reached_fe, tables / "16_ppa_reached_ge3_vs_lt3_fixed_effect.csv")

    # Sensitivity: continuous outcome under complete cases / uniform adverse imputation.
    sens_rows = []
    for outcome in ["Z_GRADE_UNIFORM_SENS", "Z_GRADE_COMPLETE_CASE"]:
        tmp = robust_two_group_tests(mu, treatment_col, outcome, seed=config.random_seed)
        tmp.insert(0, "outcome", outcome)
        sens_rows.append(tmp)
    sensitivity = pd.concat(sens_rows, ignore_index=True)
    _save_csv(sensitivity, tables / "14_continuous_outcome_sensitivity.csv")

    # RQ2b: conditional on overall utilization, is temporally distributed use
    # associated with continuous performance? The primary regularity model uses
    # numeric final grades only, because withdrawals have less opportunity to
    # distribute visits across a full term and exact withdrawal dates are absent.
    regularity_primary = temporal_regularity_performance_models(
        mu, outcome_col="Z_GRADE_COMPLETE_CASE", visits_col=visits_col,
        regularity_col="REGULARITY_MONTHLY_4", min_visits=config.ppa_threshold,
    )
    regularity_primary.insert(0, "specification", "primary_complete_case_monthly_spread")
    regularity_imputed = temporal_regularity_performance_models(
        mu, outcome_col="Z_GRADE_PRIMARY", visits_col=visits_col,
        regularity_col="REGULARITY_MONTHLY_4", min_visits=config.ppa_threshold,
    )
    regularity_imputed.insert(0, "specification", "sensitivity_imputed_adverse_monthly_spread")
    regularity_effective_weeks = temporal_regularity_performance_models(
        mu, outcome_col="Z_GRADE_COMPLETE_CASE", visits_col=visits_col,
        regularity_col="EFFECTIVE_WEEKS_PER_VISIT", min_visits=config.ppa_threshold,
    )
    regularity_effective_weeks.insert(0, "specification", "sensitivity_complete_case_effective_weeks")
    regularity_models = pd.concat(
        [regularity_primary, regularity_imputed, regularity_effective_weeks],
        ignore_index=True, sort=False,
    )
    _save_csv(regularity_models, tables / "72_temporal_regularity_performance_models.csv")

    exact3_regularity = exact_visit_count_regularity_summary(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_COMPLETE_CASE", exact_visits=config.ppa_threshold
    )
    _save_csv(exact3_regularity, tables / "73_exact3_regularity_performance.csv")

    # ------------------------------------------------------------------
    # Additive working-draft experiments (legacy/extended questions).
    # These do NOT replace the pre-specified primary analyses above.
    # ------------------------------------------------------------------
    one_two = one_two_pooling_analysis(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY",
        equivalence_margin_z=config.one_two_equivalence_margin_z,
    )
    _save_csv(one_two, tables / "80_justify_pooling_exact_1_vs_2.csv")

    visit_welch, visit_welch_summary, visit_games = welch_anova_visit_groups(
        mu, group_col=group_col, outcome_col="Z_GRADE_PRIMARY"
    )
    _save_csv(visit_welch, tables / "81_visit_groups_welch_anova.csv")
    _save_csv(visit_welch_summary, tables / "82_visit_groups_welch_summary.csv")
    _save_csv(visit_games, tables / "83_visit_groups_games_howell.csv")
    visit_clustered = clustered_visit_group_omnibus(
        mu, group_col=group_col, outcome_col="Z_GRADE_PRIMARY"
    )
    _save_csv(visit_clustered, tables / "83b_visit_groups_clustered_omnibus.csv")

    career_usage, career_any_usage, career_usage_long = career_usage_association(
        mu, career_col="CLAVECARRERA", group_col=group_col,
        min_career_n=config.min_career_n_for_inference,
        permutation_reps=config.career_usage_permutation_reps,
        seed=config.random_seed,
    )
    _save_csv(career_usage, tables / "84_career_visit_group_association.csv")
    _save_csv(career_any_usage, tables / "85_career_any_visit_association.csv")
    _save_csv(career_usage_long, tables / "86_career_visit_group_distribution.csv")

    career_summary, career_welch, career_games = career_performance_analysis(
        mu, career_col="CLAVECARRERA", outcome_col="Z_GRADE_PRIMARY", visits_col=visits_col,
        min_career_n=config.min_career_n_for_inference,
    )
    _save_csv(career_summary, tables / "87_career_performance_and_use_summary.csv")
    _save_csv(career_welch, tables / "88_career_performance_welch_anova.csv")
    _save_csv(career_games, tables / "89_career_performance_games_howell.csv")
    career_clustered = clustered_career_omnibus(
        mu, career_col="CLAVECARRERA", outcome_col="Z_GRADE_PRIMARY",
        min_career_n=config.min_career_n_for_inference,
    )
    _save_csv(career_clustered, tables / "89b_career_clustered_omnibus.csv")

    career_interaction = career_visit_interaction_model(
        mu, career_col="CLAVECARRERA", group_col=group_col, outcome_col="Z_GRADE_PRIMARY",
        min_career_n=config.min_career_n_for_interaction,
        min_cell_n=config.min_career_visit_cell_n_interaction,
    )
    _save_csv(career_interaction, tables / "90_career_by_visit_group_interaction.csv")

    exact_index, exact_index_career = exact_visit_performance_index(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", career_col="CLAVECARRERA",
        min_visit=1, max_visit=config.exact_visit_index_max,
        min_career_n_for_standardization=config.min_career_n_for_inference,
    )
    _save_csv(exact_index, tables / "91_exact_1_to_12_visit_performance_index.csv")
    _save_csv(exact_index_career, tables / "92_exact_1_to_12_visit_index_by_career.csv")

    transition_combos, transition_stats = longitudinal_any_visit_transition(
        longitudinal, mu_visits_col="MU_VISITS_CMAT_PERIOD", calc_visits_col="VISITS_CMAT_PERIOD",
        calc_coverage_col="CALC_VISIT_COVERAGE", mu_coverage_col="MU_VISIT_COVERAGE",
    )
    _save_csv(transition_combos, tables / "93_mu_calculus_any_visit_2x2.csv")
    _save_csv(transition_stats, tables / "94_mu_calculus_any_visit_statistics.csv")

    visit_clustered = clustered_omnibus_visit_group_test(
        mu, group_col=group_col, outcome_col="Z_GRADE_PRIMARY"
    )
    career_clustered = clustered_omnibus_career_test(
        mu, career_col="CLAVECARRERA", outcome_col="Z_GRADE_PRIMARY",
        min_career_n=config.min_career_n_for_inference,
    )
    _save_csv(visit_clustered, tables / "95_visit_groups_clustered_omnibus.csv")
    _save_csv(career_clustered, tables / "96_career_clustered_omnibus.csv")
    index_trend = exact_visit_index_trend(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", career_col="CLAVECARRERA",
        min_visit=1, max_visit=config.exact_visit_index_max,
        min_career_n=config.min_career_n_for_inference,
    )
    _save_csv(index_trend, tables / "97_exact_visit_index_trend.csv")

    # ------------------------------------------------------------------
    # PPA1 progression chapter (v8): strict MU-pass -> numeric Calculus pair.
    # This is additive and does not replace the earlier full-MU analyses.
    # ------------------------------------------------------------------
    ppa_cohorts = build_ppa_progression_cohort(data, config)
    ppa_pair = ppa_cohorts.paired_primary_next_term
    ppa_pair_all = ppa_cohorts.paired_all_subsequent
    _save_csv(ppa_cohorts.cohort_flow, tables / "98_ppa_progression_cohort_flow.csv")
    _save_csv(ppa_cohorts.revalidation_audit, tables / "99_revalidation_audit.csv")
    _save_csv(ppa_cohorts.career_count_distribution, tables / "100_student_official_career_count_distribution.csv")

    ppa_profiles = ppa_behavior_profiles(ppa_pair)
    ppa_persistence = persistence_by_mu_group(ppa_pair)
    ppa_omnibus, ppa_3_vs_4 = ppa_persistence_association_tests(ppa_pair)
    ppa_logit = persistence_logistic_models(
        ppa_pair, min_career_n=config.min_career_n_for_inference
    )
    ppa_piecewise = piecewise_threshold_persistence_model(
        ppa_pair, cap_visits=config.exact_visit_index_max
    )
    ppa_later_perf = later_performance_models(
        ppa_pair, min_career_n=config.min_career_n_for_inference
    )
    ppa_major = major_persistence_summary(
        ppa_pair, min_n=config.min_career_n_for_inference
    )
    ppa_specific_combo, ppa_specific_stats = course_specific_transition(ppa_pair)
    ppa_crosswalk = form_career_crosswalk(ppa_pair)
    ppa_major_joint = major_persistence_joint_test(
        ppa_pair, min_career_n=config.min_career_n_for_inference
    )
    ppa_major_delta = major_delta_z_welch(
        ppa_pair, min_n=config.min_career_n_for_inference
    )

    _save_csv(ppa_profiles, tables / "101_ppa_behavior_profiles.csv")
    _save_csv(ppa_persistence, tables / "102_ppa_persistence_by_mu_group.csv")
    _save_csv(ppa_omnibus, tables / "103_ppa_persistence_omnibus.csv")
    _save_csv(ppa_3_vs_4, tables / "104_ppa_exact3_vs_4plus_persistence.csv")
    _save_csv(ppa_logit, tables / "105_ppa_persistence_logistic_models.csv")
    _save_csv(ppa_piecewise, tables / "106_ppa_piecewise_threshold_persistence.csv")
    _save_csv(ppa_later_perf, tables / "107_ppa_later_performance_models.csv")
    _save_csv(ppa_major, tables / "108_ppa_major_persistence_summary.csv")
    _save_csv(ppa_specific_combo, tables / "109_course_specific_mu_calc_transition.csv")
    _save_csv(ppa_specific_stats, tables / "110_course_specific_mu_calc_transition_stats.csv")
    _save_csv(ppa_crosswalk, tables / "111_observed_official_vs_form_career_crosswalk.csv")
    _save_csv(ppa_major_joint, tables / "113_ppa_major_persistence_joint_test.csv")
    _save_csv(ppa_major_delta, tables / "114_ppa_major_delta_z_welch.csv")

    # Sensitivity: allow delayed first Calculus after MU, still requiring numeric
    # outcomes, coverage and valid classroom Z in both courses.
    ppa_persistence_all_subseq = persistence_by_mu_group(ppa_pair_all)
    _save_csv(ppa_persistence_all_subseq, tables / "112_ppa_persistence_all_subsequent_calc_sensitivity.csv")

    plot_ppa_persistence_by_mu_group(ppa_persistence, figures)
    plot_ppa_academic_trajectory_profiles(ppa_profiles, figures)

    # Secondary outcome: passing/completion-like academic success.
    pass_summary = (
        mu.groupby(group_col, observed=True)
        .agg(n=("PASS", "size"), pass_rate=("PASS", "mean"))
        .reset_index()
        .rename(columns={group_col: "group"})
    )
    _save_csv(pass_summary, tables / "20_secondary_pass_rate_by_group.csv")
    pass_model = secondary_pass_model(mu, treatment_col)
    _save_csv(pass_model, tables / "21_secondary_pass_model.csv")

    # RQ3: persistence into Calculus I once the PPA incentive is absent.
    long_summary = longitudinal_summary(
        longitudinal,
        mu_group_col=mu_group_long,
        calc_visits_col=calc_visits_long,
        coverage_col="CALC_VISIT_COVERAGE",
    )
    _save_csv(long_summary, tables / "30_longitudinal_persistence_to_calculus.csv")
    lag = (
        longitudinal.groupby("SEMESTER_LAG")
        .size().rename("n").reset_index().sort_values("SEMESTER_LAG")
    )
    _save_csv(lag, tables / "31_longitudinal_semester_lag.csv")

    # Observed-covariate selection adjustment sensitivity.
    mu_ps, extra_cols, cov_note = _merge_extra_covariates(mu, config)
    categorical = [c for c in config.baseline_categorical_covariates if c in mu_ps.columns]
    categorical += [c for c in extra_cols if c in mu_ps.columns and (mu_ps[c].dtype == object or str(mu_ps[c].dtype).startswith("category"))]
    numeric_extra = [
        c for c in extra_cols
        if c in mu_ps.columns and pd.api.types.is_numeric_dtype(mu_ps[c])
    ]
    ps_rows, balance, ps_meta = propensity_att_sensitivity(
        mu_ps,
        treatment_col=treatment_col,
        outcome_col="Z_GRADE_PRIMARY",
        categorical_covariates=categorical,
        numeric_covariates=numeric_extra,
    )
    _save_csv(balance, tables / "40_propensity_balance_sensitivity.csv")
    with open(out / "selection_adjustment.json", "w", encoding="utf-8") as f:
        json.dump({"note": cov_note, **ps_meta}, f, ensure_ascii=False, indent=2, default=_json_default)

    # Imputation audit (aggregated, no student identifiers).
    imp = mu.attrs.get("imputation_summary", pd.DataFrame())
    _save_csv(imp, tables / "50_imputation_audit.csv")

    # Figures.
    plot_visit_distribution(mu, calc, figures, visits_col)
    plot_continuation(continuation, figures)
    plot_primary_group_means(primary_summary, figures)
    plot_longitudinal_persistence(long_summary, figures)
    plot_daily_cmat_timeline(daily_all, figures)
    plot_term_peak_profiles(all_profiles, all_peaks, figures)
    plot_same_day_ppa_behavior(max_daily_dist, figures)
    plot_peak_spacing(all_intervals, temporal_peak_summary, figures)
    plot_monthly_periodicity_acf(monthly_acf, figures)
    plot_exact3_regularity_performance(exact3_regularity, figures)
    plot_exact_visit_performance_index(exact_index, figures)
    plot_career_performance(career_summary, figures, min_n=config.min_career_n_for_inference)
    plot_longitudinal_any_visit_transition(transition_combos, transition_stats, figures)
    plot_career_usage_rates(career_summary, figures, min_n=config.min_career_n_for_inference)

    same_day_metrics = same_day_summary.set_index("metric")["count"].to_dict()
    same_day_props = same_day_summary.set_index("metric")["proportion"].to_dict()
    all_peak_summary = temporal_peak_summary.loc[temporal_peak_summary["population"] == "All CMAT"]

    pooled_acf = monthly_acf.loc[monthly_acf["SESSION"] == "POOLED"].dropna(subset=["autocorrelation"]) if not monthly_acf.empty else pd.DataFrame()
    if len(pooled_acf):
        best_acf = pooled_acf.loc[pooled_acf["autocorrelation"].idxmax()]
        best_acf_lag = int(best_acf["lag_days"])
        best_acf_value = float(best_acf["autocorrelation"])
    else:
        best_acf_lag = None
        best_acf_value = np.nan
    median_periodogram_cycle = (
        float(monthly_periods["dominant_period_days_21_42"].median())
        if len(monthly_periods) else np.nan
    )
    reg_primary_row = regularity_primary.iloc[0].to_dict() if len(regularity_primary) else {}

    summary = {
        "study_title": "From Incentivized Attendance to Persistent Help-Seeking: Longitudinal Use of a University Mathematics Support Center and Academic Performance",
        "primary_outcome": "Z_GRADE_PRIMARY (continuous performance, professor x period standardized)",
        "secondary_outcome": "PASS",
        "primary_visit_measure": config.primary_visit_measure,
        "ppa_rule": "PPA reached at >=3 ANY CMAT visits during first MU attempt term",
        "ppa_threshold": config.ppa_threshold,
        "n_primary_mu": len(mu),
        "n_mu_gt3": int(mu[treatment_col].sum()),
        "n_mu_le3": int((mu[treatment_col] == 0).sum()),
        "n_mu_ppa_reached_ge3": int(mu[reached_col].sum()),
        "n_mu_below_ppa_lt3": int((mu[reached_col] == 0).sum()),
        "n_longitudinal_with_calc_visit_coverage": int(longitudinal["CALC_VISIT_COVERAGE"].sum()),
        "primary_unadjusted": robust.iloc[0].to_dict() if len(robust) else {},
        "primary_fixed_effect": fe.to_dict(orient="records"),
        "ppa_reached_threshold_robust": reached_robust.iloc[0].to_dict() if len(reached_robust) else {},
        "ppa_reached_threshold_fixed_effect": reached_fe.to_dict(orient="records"),
        "bunching": bunching.to_dict(orient="records"),
        "temporal_attendance": {
            "mu_term_visit_events": int(len(mu_visit_events)),
            "mu_students_with_any_visit": int(same_day_metrics.get("students_with_any_visit", 0)),
            "ppa_achievers": int(same_day_metrics.get("students_reaching_ppa_ge3", 0)),
            "ppa_achievers_any_3plus_same_day": int(same_day_metrics.get("ppa_achievers_with_any_3plus_same_day", 0)),
            "ppa_achievers_any_3plus_same_day_proportion": float(same_day_props.get("ppa_achievers_with_any_3plus_same_day", np.nan)),
            "ppa_achievers_first_3_same_day": int(same_day_metrics.get("ppa_achievers_first_3_visits_same_day", 0)),
            "ppa_achievers_first_3_same_day_proportion": float(same_day_props.get("ppa_achievers_first_3_visits_same_day", np.nan)),
            "ppa_achievers_completion_day_3plus": int(same_day_metrics.get("ppa_achievers_completion_day_3plus", 0)),
            "ppa_achievers_completion_day_3plus_proportion": float(same_day_props.get("ppa_achievers_completion_day_3plus", np.nan)),
            "all_cmat_peak_summary": all_peak_summary.to_dict(orient="records"),
            "pooled_acf_best_lag_days": best_acf_lag,
            "pooled_acf_best_value": best_acf_value,
            "median_periodogram_cycle_days_21_42": median_periodogram_cycle,
        },
        "temporal_regularity_rq2b": {
            "primary_metric": "REGULARITY_MONTHLY_4 = min(active calendar months,4) / min(total visits,4)",
            "primary_population": "students with >=3 visits and numeric final grades",
            "primary_model": reg_primary_row,
            "exact3_descriptive": exact3_regularity.to_dict(orient="records"),
        },
        "ppa1_progression_chapter_v8": {
            "study_assumption": "MU is treated as first semester/PPA1 context; primary paired cohort progresses to numeric Calculus grade in next regular term",
            "n_primary_paired": int(len(ppa_pair)),
            "n_all_subsequent_sensitivity": int(len(ppa_pair_all)),
            "persistence_by_mu_group": ppa_persistence.to_dict(orient="records"),
            "exact3_vs_4plus": ppa_3_vs_4.iloc[0].to_dict() if len(ppa_3_vs_4) else {},
            "omnibus": ppa_omnibus.iloc[0].to_dict() if len(ppa_omnibus) else {},
            "piecewise": ppa_piecewise.to_dict(orient="records"),
            "note": "Behavioral profiles are observable patterns compatible with incentive-limited or persistent use; they are not latent motivation labels.",
        },
        "extended_working_draft_analyses": {
            "one_vs_two_pooling": one_two.iloc[0].to_dict() if len(one_two) else {},
            "visit_group_welch_anova": visit_welch.iloc[0].to_dict() if len(visit_welch) else {},
            "visit_group_clustered_omnibus": visit_clustered.iloc[0].to_dict() if len(visit_clustered) else {},
            "career_usage_association": career_usage.iloc[0].to_dict() if len(career_usage) else {},
            "career_performance_welch_anova": career_welch.iloc[0].to_dict() if len(career_welch) else {},
            "career_clustered_omnibus": career_clustered.iloc[0].to_dict() if len(career_clustered) else {},
            "career_visit_interaction": career_interaction.iloc[0].to_dict() if len(career_interaction) else {},
            "mu_calculus_any_visit": transition_stats.iloc[0].to_dict() if len(transition_stats) else {},
        },
        "selection_sensitivity": ps_meta,
    }
    with open(out / "study_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=_json_default)

    peak_row = all_peak_summary.iloc[0] if len(all_peak_summary) else pd.Series(dtype=float)
    readme = f"""# CMAT publication-oriented study outputs

Primary outcome: continuous standardized performance (`Z_GRADE_PRIMARY`).  
Secondary outcome: pass/adverse academic result (`PASS`).  
Primary exposure: **all CMAT visits during the same academic term** as the student's first attempt at Matemáticas Universitarias.  
Confirmed PPA rule: the point is reached at **≥{config.ppa_threshold} visits**; `{config.ppa_threshold + 1}+` is interpreted only as **use beyond the incentive threshold**, not as intrinsic motivation.

## Current cohort
- First standard attempt at Matemáticas Universitarias, all periods: {len(cohorts['mu_all_first_attempts']):,}
- Primary cohort with advisory-record coverage: {len(mu):,}
- Students in primary cohort with >{config.ppa_threshold} course-period visits: {int(mu[treatment_col].sum()):,}
- Longitudinal MU→Cálculo pairs with visit coverage in Cálculo: {int(longitudinal['CALC_VISIT_COVERAGE'].sum()):,}

## Temporal attendance findings
- Calendar day of every advisory is preserved for analysis; exact clock time is used internally only to order repeated same-day visits.
- PPA achievers (≥{config.ppa_threshold} visits): {int(same_day_metrics.get('students_reaching_ppa_ge3', 0)):,}.
- PPA achievers with ≥{config.ppa_threshold} visits on at least one single day: {int(same_day_metrics.get('ppa_achievers_with_any_3plus_same_day', 0)):,} ({100*float(same_day_props.get('ppa_achievers_with_any_3plus_same_day', np.nan)):.2f}%).
- PPA achievers whose first {config.ppa_threshold} visits all occurred on one calendar day: {int(same_day_metrics.get('ppa_achievers_first_3_visits_same_day', 0)):,} ({100*float(same_day_props.get('ppa_achievers_first_3_visits_same_day', np.nan)):.2f}%).
- Detected CMAT service-load peaks are separated by a median of {float(peak_row.get('peak_gap_median_days', np.nan)):.1f} days (IQR {float(peak_row.get('peak_gap_q25_days', np.nan)):.1f}–{float(peak_row.get('peak_gap_q75_days', np.nan)):.1f}); {100*float(peak_row.get('monthly_like_interval_proportion', np.nan)):.1f}% of detected inter-peak gaps fall between 24 and 38 days. This is compatible with a roughly monthly academic cycle, but peaks must not be labeled as exams without professor-level exam calendars.
- ACF/periodogram diagnostics are exported as independent descriptive checks of the approximately monthly cycle.

## RQ2b — temporal regularity and performance
- Primary temporal-spread metric: `REGULARITY_MONTHLY_4 = min(active calendar months, 4) / min(total visits, 4)`.
- Primary RQ2b population: students with ≥{config.ppa_threshold} visits and a numeric final grade, to avoid mechanically shortening the opportunity window for withdrawal cases.
- The model adjusts flexibly for visit intensity (3, 4, 5, 6, 7, 8+), professor×period fixed effects and career; it remains observational.
- Effective-number-of-weeks and adverse-outcome-imputed specifications are sensitivity analyses.

## Interpretation guardrails
1. The study is observational. Fixed effects and propensity weighting address observed structure, not unmeasured motivation/need.
2. The current academic file has no exact withdrawal date, so visits are linked by year/session rather than truncated on a student's withdrawal date.
3. `BV`, `RT`, and `BA` are treated as adverse academic outcomes below 7.5. `EQV`, `REV`, and `AC` are confirmed external/equivalent passing records and are excluded because the relevant instructor/classroom is not observed.
4. Every advisory row is one confirmed visit.
5. Cálculo I is a descriptive/no-PPA comparator and a longitudinal follow-up; it is not treated as a causal control for the PPA policy.

See `STUDY_PROTOCOL.md` and `ADMINISTRATIVE_QUESTIONS.md` at the project root before publication use.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")

    return {
        "output_dir": out,
        "summary_path": out / "study_summary.json",
        "primary_n": len(mu),
        "longitudinal_n": int(longitudinal["CALC_VISIT_COVERAGE"].sum()),
    }
