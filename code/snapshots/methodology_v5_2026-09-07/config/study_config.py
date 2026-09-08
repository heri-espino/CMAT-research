from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CMATStudyConfig:
    """Pre-specified choices for the redesigned CMAT study.

    The defaults encode the roadmap agreed for the project. Administrative
    assumptions that still need confirmation are documented in
    ADMINISTRATIVE_QUESTIONS.md and are deliberately centralized here.
    """

    project_root: Path
    materias_path: Path
    asesorias_path: Path
    output_dir: Path

    primary_subject_code: str = "MAT1012"
    primary_subject_name: str = "MATEMATICAS UNIVERSITARIAS"
    followup_subject_code: str = "MAT1022"
    followup_subject_name: str = "CALCULO I"

    # Confirmed institutional rule: the PPA point is obtained once a student
    # reaches >=3 CMAT visits during the first attempt at Matemáticas
    # Universitarias. The point is not part of the course grade.
    ppa_threshold: int = 3
    passing_grade: float = 7.5

    adverse_grade_tokens: tuple[str, ...] = ("BV", "RT", "BA")
    # These do not represent a standard graded attempt and therefore are not
    # treated as failures or imputed grades.
    administrative_non_attempt_tokens: tuple[str, ...] = ("EQV", "REV", "AC")

    # Confirmed PPA exposure: ANY CMAT visit during the same academic term as
    # the student's first attempt at Matemáticas Universitarias. Course-tagged
    # visits are retained only as a sensitivity/description.
    primary_visit_measure: str = "period_wide"

    # Primary continuous outcome uses adverse-outcome imputation below the
    # passing threshold, followed by professor x period standardization.
    # Adverse outcomes are imputed from the observed within-classroom grade
    # distribution strictly below passing_grade using scipy.stats.gaussian_kde
    # with its default bw_method=None (Scott factor). A uniform fallback is used
    # only when the classroom has no observed numeric grade below 7.5.
    imputation_upper_bound: float = 7.5  # retained for backward config compatibility
    imputation_min_kde_n: int = 2       # deprecated: KDE is attempted whenever non-degenerate
    random_seed: int = 42
    min_classroom_n_for_z: int = 5

    # Observed-at/before-course covariates available in the current files.
    # No individual-level pre-treatment achievement measure is currently
    # available; therefore selection adjustment remains limited/sensitivity
    # analysis rather than a causal identification strategy.
    baseline_categorical_covariates: tuple[str, ...] = (
        "CLAVECARRERA",
        "YEAR",
        "SESSION",
        "CLAVEPROFESOR",
    )
    extra_covariates_path: Path | None = None


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
