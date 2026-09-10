from __future__ import annotations

from pathlib import Path


FIGURE_OUTPUTS = {
    "visits_histogram": "02_01_visits_histogram.pdf",
    "visits_histogram_low_counts": "02_02_visits_histogram_low_counts.pdf",
    "visits_ecdf": "02_03_visits_ecdf.pdf",
    "visits_tail_curve": "02_04_visits_tail_curve.pdf",
    "visits_continuation_curve": "02_05_visits_continuation_curve.pdf",
    "visits_lorenz_curve": "02_06_visits_lorenz_curve.pdf",
    "visits_by_year": "02_07_visits_by_year.pdf",
    "classroom_size_distribution": "02_08_classroom_size_distribution.pdf",
    "visit_histogram_main": "03_01.pdf",
    "visit_histogram_low_ylim": "03_02.pdf",
    "imputation_comparison": "05_01.pdf",
    "imputation_comparison_standardized": "05_02.pdf",
    "imputation_outlier_phase1": "05_03.pdf",
    "imputation_outlier_phase2": "05_04.pdf",
    "global_imputation_phase2": "05_05.pdf",
    "reported_professors_split": "05_06.pdf",
    "imputed_professors_split": "05_07.pdf",
    "cluster_heatmap": "05_08.pdf",
    "cluster_selection": "05_09.pdf",
    "cluster_distributions": "05_10.pdf",
    "cluster_distributions_with_ci": "05_11.pdf",
    "yearly_professor_variance": "06_00.pdf",
    "salon_scatter": "07_00.pdf",
    "salon_ecdf": "07_00_ecdf.pdf",
    "salon_parametric": "07_01.pdf",
    "salon_nonparametric": "07_02.pdf",
    "student_scatter": "08_00.pdf",
    "student_ecdf": "08_00_ecdf.pdf",
    "student_parametric": "08_01.pdf",
    "student_nonparametric": "08_02.pdf",
    "mean_z_by_visits": "09_01.pdf",
}


REPORT_FIGURE_KEYS = (
    "visits_histogram",
    "visits_histogram_low_counts",
    "visits_ecdf",
    "visits_tail_curve",
    "visits_continuation_curve",
    "visits_lorenz_curve",
    "visits_by_year",
    "classroom_size_distribution",
    "visit_histogram_main",
    "visit_histogram_low_ylim",
    "imputation_comparison",
    "imputation_outlier_phase1",
    "imputation_outlier_phase2",
    "global_imputation_phase2",
    "reported_professors_split",
    "imputed_professors_split",
    "cluster_heatmap",
    "cluster_selection",
    "cluster_distributions",
    "cluster_distributions_with_ci",
    "yearly_professor_variance",
    "salon_scatter",
    "salon_ecdf",
    "salon_parametric",
    "salon_nonparametric",
    "student_scatter",
    "student_ecdf",
    "student_parametric",
    "student_nonparametric",
    "mean_z_by_visits",
)


def figure_name(key: str) -> str:
    return FIGURE_OUTPUTS[key]


def figure_path(figures_dir: Path, key: str) -> Path:
    return figures_dir / figure_name(key)


def figure_stem(key: str) -> str:
    return Path(figure_name(key)).stem


def report_figure_names() -> list[str]:
    return [FIGURE_OUTPUTS[key] for key in REPORT_FIGURE_KEYS]
