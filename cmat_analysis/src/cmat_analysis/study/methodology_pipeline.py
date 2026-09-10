"""Methodology-report-specific orchestration.

The broad publication pipeline remains canonical for shared/base outputs. This
module adds the methodology-review analyses restored from the validated
methodology snapshot without duplicating their estimators.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .cohort import build_study_cohorts, load_and_clean_inputs
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
from .methodology_plots import (
    plot_career_mean_z,
    plot_career_use_vs_z,
    plot_exact_visit_count_curve,
    plot_pairwise_exact_group_means,
    plot_peak_spacing_by_population,
    plot_periodicity_acf_by_population,
)
from .outcomes import add_primary_outcomes
from .pipeline import run_study_pipeline


def _save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def run_methodology_pipeline(config) -> dict[str, object]:
    """Run shared study outputs, then add the methodology-report extensions.

    The methodology branch is a report profile, not a second implementation of
    shared cohort/statistical logic. The existing broad study runner creates
    the base outputs. This function then recreates the methodology snapshot's
    exact-group, progressor, career and exact-count outputs 80--94 from the same
    canonical cohort/outcome functions.
    """
    result = run_study_pipeline(config)
    out = Path(config.output_dir)
    tables = out / "tables"
    figures = out / "figures"

    data = load_and_clean_inputs(config)
    cohorts = build_study_cohorts(data, config)
    mu = add_primary_outcomes(cohorts["mu_primary"], config)
    longitudinal = add_primary_outcomes(cohorts["longitudinal"], config)

    if config.primary_visit_measure == "course_specific":
        visits_col = "VISITS_COURSE"
        calc_visits_long = "VISITS_COURSE"
    else:
        visits_col = "VISITS_CMAT_PERIOD"
        calc_visits_long = "VISITS_CMAT_PERIOD"

    population_full = "All first-MU attempts with CMAT coverage"
    exact_full_summary = exact_visit_group_summary(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population=population_full
    )
    exact_full_welch = welch_anova_exact_groups(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population=population_full
    )
    exact_full_gh = games_howell_exact_groups(
        mu, visits_col=visits_col, outcome_col="Z_GRADE_PRIMARY", population=population_full
    )
    exact_full_fe, exact_full_fe_info = fixed_effect_pairwise_exact_groups(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population_full,
        include_career=True,
    )
    _save_csv(exact_full_summary, tables / "80_exact_visit_groups_0_1_2_3_4plus_summary.csv")
    _save_csv(exact_full_welch, tables / "81_exact_visit_groups_welch_anova.csv")
    _save_csv(exact_full_gh, tables / "82_exact_visit_groups_games_howell_all_pairs.csv")
    _save_csv(exact_full_fe, tables / "83_exact_visit_groups_FE_career_all_pairs.csv")
    _save_csv(exact_full_fe_info, tables / "84_exact_visit_groups_FE_model_info.csv")

    mu_progressors = calc_progressor_mu_cohort(mu, cohorts["longitudinal"])
    population_progressors = "MU students with later Calculus and CMAT coverage"
    progressor_summary = exact_visit_group_summary(
        mu_progressors,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population_progressors,
    )
    progressor_welch = welch_anova_exact_groups(
        mu_progressors,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population_progressors,
    )
    progressor_gh = games_howell_exact_groups(
        mu_progressors,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population_progressors,
    )
    progressor_fe, progressor_fe_info = fixed_effect_pairwise_exact_groups(
        mu_progressors,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population_progressors,
        include_career=True,
    )
    _save_csv(progressor_summary, tables / "85_progressor4211_exact_visit_summary.csv")
    _save_csv(progressor_welch, tables / "86_progressor4211_welch_anova.csv")
    _save_csv(progressor_gh, tables / "87_progressor4211_games_howell_all_pairs.csv")
    _save_csv(progressor_fe, tables / "88_progressor4211_FE_career_all_pairs.csv")
    _save_csv(progressor_fe_info, tables / "89_progressor4211_FE_model_info.csv")

    all_math_attempts = build_all_math_attempts_with_outcomes(data, config)
    calc_progressors = calc_progressor_followup_cohort(longitudinal)
    career_all = career_summary(
        all_math_attempts,
        population="All observed math-course attempts with CMAT coverage",
        visits_col="VISITS_CMAT_PERIOD",
        outcome_col="Z_GRADE_PRIMARY",
        min_n=30,
    )
    career_mu = career_summary(
        mu,
        population="First-MU attempts with CMAT coverage",
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        min_n=30,
    )
    career_calc = career_summary(
        calc_progressors,
        population="Linked later-Calculus attempts (N=4211 risk set)",
        visits_col=calc_visits_long,
        outcome_col="Z_GRADE_PRIMARY",
        min_n=30,
    )
    career_populations = pd.concat([career_all, career_mu, career_calc], ignore_index=True)
    _save_csv(career_populations, tables / "90_career_summary_three_populations.csv")
    _save_csv(
        career_mu.loc[~career_mu["included_n_ge_min"]].copy(),
        tables / "91_omitted_careers_first_mu_n_lt30.csv",
    )
    _save_csv(
        career_ecological_association(career_populations),
        tables / "92_career_use_vs_mean_z_ecological.csv",
    )

    exact_count = exact_visit_count_summary(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population_full,
        max_visits=12,
    )
    exact_count_trends = exact_visit_count_trend_diagnostics(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population_full,
        max_visits=12,
        stable_max_visits=7,
    )
    _save_csv(exact_count, tables / "93_exact_visit_counts_0_to_12_summary.csv")
    _save_csv(exact_count_trends, tables / "94_exact_visit_counts_trend_diagnostics.csv")

    plot_pairwise_exact_group_means(
        exact_full_summary,
        figures,
        "11_exact_visit_groups_0_1_2_3_4plus.png",
        "Desempeño por visitas exactas: cohorte completa de primer MU",
    )
    plot_pairwise_exact_group_means(
        progressor_summary,
        figures,
        "12_progressor4211_exact_visit_groups.png",
        "Desempeño por visitas exactas: estudiantes de MU que posteriormente llegan a Cálculo",
    )
    plot_exact_visit_count_curve(exact_count, figures, "13_exact_visit_counts_0_to_12.png")

    for population, stem in [
        ("All observed math-course attempts with CMAT coverage", "all_math_attempts"),
        ("First-MU attempts with CMAT coverage", "first_mu"),
        ("Linked later-Calculus attempts (N=4211 risk set)", "linked_calculus4211"),
    ]:
        plot_career_mean_z(career_populations, population, figures, f"career_mean_z_{stem}.png")
        plot_career_use_vs_z(career_populations, population, figures, f"career_use_vs_z_{stem}.png")

    intervals_path = tables / "67_peak_spacing_intervals.csv"
    acf_path = tables / "69_monthly_cycle_autocorrelation.csv"
    if intervals_path.exists():
        plot_peak_spacing_by_population(pd.read_csv(intervals_path), figures)
    if acf_path.exists():
        plot_periodicity_acf_by_population(pd.read_csv(acf_path), figures)

    return {
        **result,
        "methodology_profile": True,
        "methodology_exact_group_table": tables / "80_exact_visit_groups_0_1_2_3_4plus_summary.csv",
        "methodology_career_table": tables / "90_career_summary_three_populations.csv",
        "methodology_exact_count_table": tables / "93_exact_visit_counts_0_to_12_summary.csv",
    }
