"""Build Paper 2.1 aggregate tables and publication figures.

This module centralises the dependency chain used by the manuscript build:

    controlled data -> aggregate tables -> vector figures

Explicit requests rebuild the selected stage. Automatic dependency resolution
only rebuilds an upstream stage when a required file is missing, so a normal PDF
compile does not rerun expensive analyses unnecessarily.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterable

PAPER_DIR = Path(__file__).resolve().parent
REPO_ROOT = PAPER_DIR.parent
TABLES_DIR = REPO_ROOT / "results" / "paper21" / "tables"
FIGURES_DIR = REPO_ROOT / "results" / "paper21" / "figures"

MATERIAS = REPO_ROOT / "data" / "controlled" / "Materias_pseudonymized.csv"
ASESORIAS = REPO_ROOT / "data" / "controlled" / "Asesorias_pseudonymized.csv"

SUPPORT_RUNNER = REPO_ROOT / "code" / "run_paper21.py"
OUTCOME_RUNNER = REPO_ROOT / "code" / "run_paper21_outcomes.py"
MIXTURE_RUNNER = REPO_ROOT / "code" / "run_paper21_mixture.py"
FIGURE_RUNNER = REPO_ROOT / "code" / "figures_paper21.py"

# Canonical validation settings used by the verified Paper 2.1 analysis.
GMM_BOOTSTRAP = 199
SHAPE_BOOTSTRAP = 199
SHAPE_CV_FOLDS = 5
SHAPE_CV_REPEATS = 10

TABLE_SENTINELS = (
    TABLES_DIR / "01_exact_positive_visit_support.csv",
    TABLES_DIR / "05_cut_overlap_frontier.csv",
    TABLES_DIR / "10_benchmark_0_vs_1plus.csv",
    TABLES_DIR / "10d_zero_inclusive_exact_administrative_composition.csv",
    TABLES_DIR / "10g_zero_inclusive_stacked_ridgeline_density.csv",
    TABLES_DIR / "10l_zero_inclusive_observed_numeric_grade_density.csv",
    TABLES_DIR / "18_primary_z_heatmap_matrix.csv",
    TABLES_DIR / "19_primary_pass_heatmap_matrix.csv",
    TABLES_DIR / "29_instructor_cluster_benchmark_0_vs_1plus.csv",
    TABLES_DIR / "30_numeric_failure_descriptives.csv",
    TABLES_DIR / "38_complete_case_gmm_two_component_parameters.csv",
    TABLES_DIR / "42_imputed_gmm_two_component_parameters.csv",
    TABLES_DIR / "46_complete_case_gmm_ridgeline_density.csv",
    TABLES_DIR / "52_imputed_skewnormal_vs_gmm_cross_validation.csv",
)

FIGURE_INPUTS = (
    TABLES_DIR / "10b_zero_inclusive_descriptives.csv",
    TABLES_DIR / "10d_zero_inclusive_exact_administrative_composition.csv",
    TABLES_DIR / "10g_zero_inclusive_stacked_ridgeline_density.csv",
    TABLES_DIR / "10l_zero_inclusive_observed_numeric_grade_density.csv",
    TABLES_DIR / "18_primary_z_heatmap_matrix.csv",
    TABLES_DIR / "19_primary_pass_heatmap_matrix.csv",
    TABLES_DIR / "38_complete_case_gmm_two_component_parameters.csv",
    TABLES_DIR / "42_imputed_gmm_two_component_parameters.csv",
    TABLES_DIR / "46_complete_case_gmm_ridgeline_density.csv",
    TABLES_DIR / "10j_zero_inclusive_z_heatmap_matrix.csv",
    TABLES_DIR / "10k_zero_inclusive_pass_heatmap_matrix.csv",
)

FIGURE_OUTPUTS = (
    FIGURES_DIR / "fig01a_observed_pre_imputation_structure.pdf",
    FIGURES_DIR / "fig01_distribution_composition_ridgeline.pdf",
    FIGURES_DIR / "fig02_pairwise_z_heatmap.pdf",
    FIGURES_DIR / "fig03_pairwise_pass_heatmap.pdf",
    FIGURES_DIR / "fig04_complete_case_gmm_ridgeline.pdf",
    FIGURES_DIR / "fig05_lower_component_weight.pdf",
    FIGURES_DIR / "figS01_zero_inclusive_z_heatmap.pdf",
    FIGURES_DIR / "figS02_zero_inclusive_pass_heatmap.pdf",
)


def _missing(paths: Iterable[Path]) -> list[Path]:
    return [path for path in paths if not path.is_file() or path.stat().st_size == 0]


def _relative(paths: Iterable[Path]) -> str:
    return ", ".join(str(path.relative_to(REPO_ROOT)) for path in paths)


def _require(paths: Iterable[Path], *, label: str) -> None:
    missing = _missing(paths)
    if missing:
        raise SystemExit(f"Missing {label}: {_relative(missing)}")


def _run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def build_tables(*, force: bool = False) -> None:
    """Build the complete Paper 2.1 aggregate table family.

    When force is false, existing complete outputs are reused. Explicit
    paper_build.py --tables calls pass force=True.
    """
    if not force and not _missing(TABLE_SENTINELS):
        print("Paper 2.1 tables: present; reusing existing aggregate outputs.")
        return

    _require(
        (MATERIAS, ASESORIAS, SUPPORT_RUNNER, OUTCOME_RUNNER, MIXTURE_RUNNER),
        label="inputs required to build Paper 2.1 tables",
    )
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    common = [
        "--materias",
        str(MATERIAS),
        "--asesorias",
        str(ASESORIAS),
    ]

    _run(
        [
            sys.executable,
            str(SUPPORT_RUNNER),
            *common,
            "--candidate-top-exact",
            "5",
        ]
    )
    _run([sys.executable, str(OUTCOME_RUNNER), *common])
    _run(
        [
            sys.executable,
            str(MIXTURE_RUNNER),
            *common,
            "--gmm-bootstrap",
            str(GMM_BOOTSTRAP),
            "--shape-bootstrap",
            str(SHAPE_BOOTSTRAP),
            "--shape-cv-folds",
            str(SHAPE_CV_FOLDS),
            "--shape-cv-repeats",
            str(SHAPE_CV_REPEATS),
        ]
    )

    _require(TABLE_SENTINELS, label="expected Paper 2.1 table outputs")
    print(f"Paper 2.1 tables: built in {TABLES_DIR.relative_to(REPO_ROOT)}")


def build_figures(*, force: bool = False, auto_tables: bool = True) -> None:
    """Build every Paper 2.1 vector figure.

    Missing figure inputs trigger the table build automatically when auto_tables
    is true. Existing figures are reused unless force is requested explicitly.
    """
    if not force and not _missing(FIGURE_OUTPUTS):
        print("Paper 2.1 figures: present; reusing existing vector figures.")
        return

    missing_inputs = _missing(FIGURE_INPUTS)
    if missing_inputs:
        if not auto_tables:
            raise SystemExit(
                "Missing aggregate inputs required for figures: "
                + _relative(missing_inputs)
            )
        print(
            "Paper 2.1 figures: required aggregate inputs are missing; "
            "building tables first."
        )
        build_tables(force=True)

    _require((FIGURE_RUNNER,), label="Paper 2.1 figure recipe")
    _require(FIGURE_INPUTS, label="aggregate inputs required for figures")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    _run([sys.executable, str(FIGURE_RUNNER)])
    _require(FIGURE_OUTPUTS, label="expected Paper 2.1 figure outputs")
    print(f"Paper 2.1 figures: built in {FIGURES_DIR.relative_to(REPO_ROOT)}")


def ensure_figures() -> None:
    """Ensure figures exist, rebuilding only missing dependencies."""
    if _missing(FIGURE_OUTPUTS):
        build_figures(force=True, auto_tables=True)


def status() -> dict[str, list[str]]:
    """Return missing table, figure-input, and figure-output paths."""
    return {
        "tables": [str(p.relative_to(REPO_ROOT)) for p in _missing(TABLE_SENTINELS)],
        "figure_inputs": [
            str(p.relative_to(REPO_ROOT)) for p in _missing(FIGURE_INPUTS)
        ],
        "figures": [str(p.relative_to(REPO_ROOT)) for p in _missing(FIGURE_OUTPUTS)],
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Build Paper 2.1 aggregate tables and/or vector figures."
    )
    parser.add_argument(
        "--tables",
        action="store_true",
        help="Force regeneration of the canonical aggregate tables.",
    )
    parser.add_argument(
        "--figures",
        action="store_true",
        help="Force regeneration of vector figures; missing tables are built automatically.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report missing table/figure dependencies without building them.",
    )
    args = parser.parse_args()

    if args.check:
        state = status()
        for key, missing in state.items():
            print(f"{key}: {'OK' if not missing else ', '.join(missing)}")
        return 0 if not any(state.values()) else 1

    # Standalone helper defaults to figures, with automatic table resolution.
    if not args.tables and not args.figures:
        args.figures = True

    if args.tables:
        build_tables(force=True)
    if args.figures:
        build_figures(force=True, auto_tables=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
