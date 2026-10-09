"""Build Paper 2.1 Holm-only tables and figures.

Controlled inputs -> support audit and Wald/Holm outcomes -> pairwise plots.
Do not run unrelated distribution modelling during manuscript compilation.
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
FIGURE_RUNNER = REPO_ROOT / "code" / "figures_paper21.py"

TABLE_SENTINELS = (
    TABLES_DIR / "01_exact_positive_visit_support.csv",
    TABLES_DIR / "05_cut_overlap_frontier.csv",
    TABLES_DIR / "10_benchmark_0_vs_1plus.csv",
    TABLES_DIR / "11_primary_group_descriptives.csv",
    TABLES_DIR / "12_primary_omnibus.csv",
    TABLES_DIR / "13_primary_pairwise_continuous.csv",
    TABLES_DIR / "14_primary_pairwise_pass.csv",
    TABLES_DIR / "20_sensitivity_7plus_group_descriptives.csv",
    TABLES_DIR / "21_sensitivity_7plus_omnibus.csv",
    TABLES_DIR / "26b_zero_inclusive_7plus_z_effect_matrix.csv",
    TABLES_DIR / "26e_zero_inclusive_7plus_z_p_raw_matrix.csv",
    TABLES_DIR / "26f_zero_inclusive_7plus_z_p_holm_matrix.csv",
    TABLES_DIR / "26g_zero_inclusive_7plus_pass_p_raw_matrix.csv",
    TABLES_DIR / "26h_zero_inclusive_7plus_pass_p_holm_matrix.csv",
    TABLES_DIR / "26k_zero_inclusive_7plus_pairwise_pass_lpm.csv",
    TABLES_DIR / "28_instructor_cluster_omnibus.csv",
)

FIGURE_INPUTS = (
    TABLES_DIR / "26b_zero_inclusive_7plus_z_effect_matrix.csv",
    TABLES_DIR / "26e_zero_inclusive_7plus_z_p_raw_matrix.csv",
    TABLES_DIR / "26f_zero_inclusive_7plus_z_p_holm_matrix.csv",
    TABLES_DIR / "26g_zero_inclusive_7plus_pass_p_raw_matrix.csv",
    TABLES_DIR / "26h_zero_inclusive_7plus_pass_p_holm_matrix.csv",
    TABLES_DIR / "26k_zero_inclusive_7plus_pairwise_pass_lpm.csv",
)

FIGURE_OUTPUTS = (
    FIGURES_DIR / "fig03_04_pairwise_effect_dashboard.pdf",
    FIGURES_DIR / "fig05_pairwise_z_pvalue_dashboard.pdf",
    FIGURES_DIR / "fig06_pairwise_pass_pvalue_dashboard.pdf",
)


def _missing(paths: Iterable[Path]) -> list[Path]:
    return [p for p in paths if not p.is_file() or p.stat().st_size == 0]


def _relative(paths: Iterable[Path]) -> str:
    return ", ".join(str(p.relative_to(REPO_ROOT)) for p in paths)


def _require(paths: Iterable[Path], *, label: str) -> None:
    absent = _missing(paths)
    if absent:
        raise SystemExit(f"Missing {label}: {_relative(absent)}")


def _run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def build_tables(*, force: bool = False) -> None:
    """Produce the canonical support and outcome-contrast table family."""
    if not force and not _missing(TABLE_SENTINELS):
        print("Paper 2.1 Holm tables: present; reusing aggregate outputs.")
        return
    _require(
        (MATERIAS, ASESORIAS, SUPPORT_RUNNER, OUTCOME_RUNNER),
        label="inputs for Paper 2.1",
    )
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    common = ["--materias", str(MATERIAS), "--asesorias", str(ASESORIAS)]
    _run([sys.executable, str(SUPPORT_RUNNER), *common, "--candidate-top-exact", "5"])
    _run([sys.executable, str(OUTCOME_RUNNER), *common])
    _require(TABLE_SENTINELS, label="Holm aggregate tables")


def build_figures(*, force: bool = False, auto_tables: bool = True) -> None:
    """Regenerate only Z and PASS adjusted pairwise/Holm figures."""
    if not force and not _missing(FIGURE_OUTPUTS):
        print("Paper 2.1 Holm figures: present.")
        return
    if _missing(FIGURE_INPUTS):
        if not auto_tables:
            raise SystemExit("Missing Holm figure inputs: " + _relative(_missing(FIGURE_INPUTS)))
        build_tables(force=True)
    _require((FIGURE_RUNNER, *FIGURE_INPUTS), label="Holm figure inputs")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    _run([sys.executable, str(FIGURE_RUNNER)])
    _require(FIGURE_OUTPUTS, label="Holm publication figures")


def ensure_figures() -> None:
    # Pairwise dashboards are cheap and may have changed since a checked-in
    # older figure was built. Rebuild for every manuscript compilation.
    build_figures(force=True, auto_tables=True)


def status() -> dict[str, list[str]]:
    return {
        "tables": [str(p.relative_to(REPO_ROOT)) for p in _missing(TABLE_SENTINELS)],
        "figure_inputs": [str(p.relative_to(REPO_ROOT)) for p in _missing(FIGURE_INPUTS)],
        "figures": [str(p.relative_to(REPO_ROOT)) for p in _missing(FIGURE_OUTPUTS)],
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Build Paper 2.1 Wald/Holm tables or figures.")
    parser.add_argument("--tables", action="store_true")
    parser.add_argument("--figures", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        for label, missing in status().items():
            print(f"{label}: {'OK' if not missing else ', '.join(missing)}")
        return 0 if not any(status().values()) else 1
    if not args.tables and not args.figures:
        args.figures = True
    if args.tables:
        build_tables(force=True)
    if args.figures:
        build_figures(force=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
