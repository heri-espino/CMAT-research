from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CMATStudyConfig:
    """Pre-specified choices shared by the reproducible CMAT study runners."""

    project_root: Path
    materias_path: Path
    asesorias_path: Path
    output_dir: Path

    primary_subject_code: str = "MAT1012"
    primary_subject_name: str = "MATEMATICAS UNIVERSITARIAS"
    followup_subject_code: str = "MAT1022"
    followup_subject_name: str = "CALCULO I"

    ppa_threshold: int = 3
    assume_mu_is_first_semester_ppa1_context: bool = True
    assume_calc_has_no_same_ppa1_cmat_incentive: bool = True
    passing_grade: float = 7.5

    adverse_grade_tokens: tuple[str, ...] = ("BV", "RT", "BA")
    administrative_non_attempt_tokens: tuple[str, ...] = ("EQV", "REV", "AC")
    primary_visit_measure: str = "period_wide"

    # Canonical methodology-report imputation rule: use numeric grades strictly
    # below passing_grade and scipy.stats.gaussian_kde(..., bw_method=None),
    # SciPy's default Scott factor. Non-empty degenerate pools use empirical
    # resampling; uniform is reserved for empty sub-pass pools. These two fields
    # remain for backward config compatibility; add_primary_outcomes() uses
    # passing_grade directly.
    imputation_upper_bound: float = 7.5
    imputation_min_kde_n: int = 2
    random_seed: int = 42
    min_classroom_n_for_z: int = 5

    baseline_categorical_covariates: tuple[str, ...] = (
        "CLAVECARRERA",
        "YEAR",
        "SESSION",
        "CLAVEPROFESOR",
    )
    extra_covariates_path: Path | None = None

    one_two_equivalence_margin_z: float = 0.20
    min_career_n_for_inference: int = 30
    min_career_n_for_interaction: int = 100
    min_career_visit_cell_n_interaction: int = 5
    exact_visit_index_max: int = 12
    career_usage_permutation_reps: int = 3000


def get_study_config(project_root: Path | None = None) -> CMATStudyConfig:
    root = project_root or Path(__file__).resolve().parents[1]
    data = root / "data"
    extra = data / "pre_treatment_covariates.xlsx"
    raw_materias = data / "Materias estudiantes-profesores 2019-2025 P y O.xlsx"
    raw_asesorias = data / "Asesorias2024.xlsx"
    anon_materias = data / "Materias_anonymized.csv"
    anon_asesorias = data / "Asesorias_anonymized.csv"
    materias_path = raw_materias if raw_materias.exists() else anon_materias
    asesorias_path = raw_asesorias if raw_asesorias.exists() else anon_asesorias
    return CMATStudyConfig(
        project_root=root,
        materias_path=materias_path,
        asesorias_path=asesorias_path,
        output_dir=root / "outputs" / "study",
        extra_covariates_path=extra if extra.exists() else None,
    )
