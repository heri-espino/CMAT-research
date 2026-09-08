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
from .extended_methodology import (
    build_all_math_attempts_with_outcomes,
    calc_progressor_followup_cohort,
    calc_progressor_mu_cohort,
    career_ecological_association,
    career_summary,
    exact_visit_count_summary,
    exact_visit_count_trend_diagnostics,
    exact_visit_group_summary,
    fixed_effect_pairwise_exact_groups,
    games_howell_exact_groups,
    welch_anova_exact_groups,
)
from .extended_plots import (
    plot_career_mean_z,
    plot_career_use_vs_z,
    plot_exact_visit_count_curve,
    plot_pairwise_exact_group_means,
    plot_peak_spacing_by_population,
    plot_periodicity_acf_by_population,
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
    mu_imputation_audit = mu.attrs.get("imputation_summary", pd.DataFrame()).copy()
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
    monthly_acf_all, monthly_periods_all = monthly_periodicity_diagnostics(
        data.advisories, population="All CMAT"
    )
    monthly_acf_mu, monthly_periods_mu = monthly_periodicity_diagnostics(
        mu_visit_events, population="First-MU cohort during MU term"
    )
    monthly_acf = pd.concat([monthly_acf_all, monthly_acf_mu], ignore_index=True)
    monthly_periods = pd.concat([monthly_periods_all, monthly_periods_mu], ignore_index=True)
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

    # Extended methodology requested for statistical review: every pairwise
    # contrast among exact visit groups 0,1,2,3,4+, both unadjusted
    # (Games--Howell) and adjusted in one classroom-FE + official-career model.
    exact_full_summary = exact_visit_group_summary(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population="All first-MU attempts with CMAT coverage"
    )
    exact_full_welch = welch_anova_exact_groups(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population="All first-MU attempts with CMAT coverage"
    )
    exact_full_gh = games_howell_exact_groups(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population="All first-MU attempts with CMAT coverage"
    )
    exact_full_fe, exact_full_fe_info = fixed_effect_pairwise_exact_groups(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population="All first-MU attempts with CMAT coverage", include_career=True
    )
    _save_csv(exact_full_summary, tables / "80_exact_visit_groups_0_1_2_3_4plus_summary.csv")
    _save_csv(exact_full_welch, tables / "81_exact_visit_groups_welch_anova.csv")
    _save_csv(exact_full_gh, tables / "82_exact_visit_groups_games_howell_all_pairs.csv")
    _save_csv(exact_full_fe, tables / "83_exact_visit_groups_FE_career_all_pairs.csv")
    _save_csv(exact_full_fe_info, tables / "84_exact_visit_groups_FE_model_info.csv")

    # N=4,211 students who have a first later Calculus attempt with advisory
    # coverage. Z_MU is computed in the full MU classroom before subsetting.
    # This is a selected future-progressor population and therefore changes the
    # estimand; it is reported as a separate analysis rather than silently
    # replacing the full N=6,627 MU cohort.
    mu_progressors = calc_progressor_mu_cohort(mu, cohorts["longitudinal"])
    progressor_summary = exact_visit_group_summary(
        mu_progressors, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population="MU students with later Calculus and CMAT coverage"
    )
    progressor_welch = welch_anova_exact_groups(
        mu_progressors, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population="MU students with later Calculus and CMAT coverage"
    )
    progressor_gh = games_howell_exact_groups(
        mu_progressors, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population="MU students with later Calculus and CMAT coverage"
    )
    progressor_fe, progressor_fe_info = fixed_effect_pairwise_exact_groups(
        mu_progressors, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population="MU students with later Calculus and CMAT coverage", include_career=True
    )
    _save_csv(progressor_summary, tables / "85_progressor4211_exact_visit_summary.csv")
    _save_csv(progressor_welch, tables / "86_progressor4211_welch_anova.csv")
    _save_csv(progressor_gh, tables / "87_progressor4211_games_howell_all_pairs.csv")
    _save_csv(progressor_fe, tables / "88_progressor4211_FE_career_all_pairs.csv")
    _save_csv(progressor_fe_info, tables / "89_progressor4211_FE_model_info.csv")

    # Career-level descriptive analyses in three explicitly different
    # populations, always using the official career from the academic row.
    all_math_attempts = build_all_math_attempts_with_outcomes(data, config)
    calc_progressors = calc_progressor_followup_cohort(longitudinal)
    career_all = career_summary(
        all_math_attempts, population="All observed math-course attempts with CMAT coverage",
        visits_col="VISITS_CMAT_PERIOD", outcome_col="Z_GRADE_PRIMARY", min_n=30
    )
    career_mu = career_summary(
        mu, population="First-MU attempts with CMAT coverage",
        visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", min_n=30
    )
    career_calc = career_summary(
        calc_progressors, population="Linked later-Calculus attempts (N=4211 risk set)",
        visits_col=calc_visits_long, outcome_col="Z_GRADE_PRIMARY", min_n=30
    )
    career_populations = pd.concat([career_all, career_mu, career_calc], ignore_index=True)
    _save_csv(career_populations, tables / "90_career_summary_three_populations.csv")
    omitted_mu = career_mu.loc[~career_mu["included_n_ge_min"]].copy()
    _save_csv(omitted_mu, tables / "91_omitted_careers_first_mu_n_lt30.csv")
    ecological = career_ecological_association(career_populations)
    _save_csv(ecological, tables / "92_career_use_vs_mean_z_ecological.csv")

    # Exact visit-count descriptive tail (0--12), retained to show the sparse
    # high-visit cells explicitly. Inferential conclusions remain based on the
    # 0/1/2/3/4+ specification above.
    exact_count = exact_visit_count_summary(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY",
        population="All first-MU attempts with CMAT coverage", max_visits=12
    )
    exact_count_trends = exact_visit_count_trend_diagnostics(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY",
        population="All first-MU attempts with CMAT coverage", max_visits=12, stable_max_visits=7
    )
    _save_csv(exact_count, tables / "93_exact_visit_counts_0_to_12_summary.csv")
    _save_csv(exact_count_trends, tables / "94_exact_visit_counts_trend_diagnostics.csv")

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
    _save_csv(mu_imputation_audit, tables / "50_imputation_audit.csv")

    # Figures.
    plot_visit_distribution(mu, calc, figures, visits_col)
    plot_continuation(continuation, figures)
    plot_primary_group_means(primary_summary, figures)
    plot_longitudinal_persistence(long_summary, figures)
    plot_daily_cmat_timeline(daily_all, figures)
    plot_term_peak_profiles(
        all_profiles, all_peaks, figures,
        filename="06a_term_temporal_peaks_all_cmat.png",
        title="Picos de actividad: todos los registros CMAT",
    )
    plot_term_peak_profiles(
        mu_profiles, mu_peaks, figures,
        filename="06b_term_temporal_peaks_first_mu.png",
        title="Picos de actividad: cohorte de primer MU durante su periodo de MU",
    )
    # Backward-compatible old plot name remains generated from all-CMAT only.
    plot_term_peak_profiles(all_profiles, all_peaks, figures)
    plot_same_day_ppa_behavior(max_daily_dist, figures)
    plot_peak_spacing(all_intervals, temporal_peak_summary, figures)
    plot_peak_spacing_by_population(temporal_intervals, figures)
    plot_monthly_periodicity_acf(monthly_acf_all, figures)
    plot_periodicity_acf_by_population(monthly_acf, figures)
    plot_exact3_regularity_performance(exact3_regularity, figures)
    plot_pairwise_exact_group_means(
        exact_full_summary, figures, "11_exact_visit_groups_0_1_2_3_4plus.png",
        "Desempeño por visitas exactas: cohorte completa de primer MU"
    )
    plot_pairwise_exact_group_means(
        progressor_summary, figures, "12_progressor4211_exact_visit_groups.png",
        "Desempeño por visitas exactas: estudiantes de MU que posteriormente llegan a Cálculo"
    )
    plot_exact_visit_count_curve(exact_count, figures, "13_exact_visit_counts_0_to_12.png")
    for population, stem in [
        ("All observed math-course attempts with CMAT coverage", "all_math_attempts"),
        ("First-MU attempts with CMAT coverage", "first_mu"),
        ("Linked later-Calculus attempts (N=4211 risk set)", "linked_calculus4211"),
    ]:
        plot_career_mean_z(career_populations, population, figures, f"career_mean_z_{stem}.png")
        plot_career_use_vs_z(career_populations, population, figures, f"career_use_vs_z_{stem}.png")

    same_day_metrics = same_day_summary.set_index("metric")["count"].to_dict()
    same_day_props = same_day_summary.set_index("metric")["proportion"].to_dict()
    all_peak_summary = temporal_peak_summary.loc[temporal_peak_summary["population"] == "All CMAT"]

    pooled_acf = monthly_acf.loc[(monthly_acf["SESSION"] == "POOLED") & (monthly_acf["population"] == "All CMAT")].dropna(subset=["autocorrelation"]) if not monthly_acf.empty else pd.DataFrame()
    if len(pooled_acf):
        best_acf = pooled_acf.loc[pooled_acf["autocorrelation"].idxmax()]
        best_acf_lag = int(best_acf["lag_days"])
        best_acf_value = float(best_acf["autocorrelation"])
    else:
        best_acf_lag = None
        best_acf_value = np.nan
    median_periodogram_cycle = (
        float(monthly_periods.loc[monthly_periods["population"] == "All CMAT", "dominant_period_days_21_42"].median())
        if len(monthly_periods.loc[monthly_periods["population"] == "All CMAT"]) else np.nan
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
        "extended_methodology": {
            "n_mu_full": int(len(mu)),
            "n_mu_future_calc_progressors": int(len(mu_progressors)),
            "exact_visit_pairwise_groups": ["0", "1", "2", "3", "4+"],
            "career_populations": career_populations.groupby("population")["CLAVECARRERA"].nunique().to_dict(),
            "note": "The 4211 cohort conditions on observed future progression to Calculus and is reported separately from the full first-MU cohort."
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
