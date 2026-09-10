#!/usr/bin/env python3
"""Reproduce the Paper 2 MU-performance analysis from controlled local inputs.

This branch-local entry point fixes the publication specification and execution
order while delegating cohort construction, outcome definitions, estimators,
confidence intervals, and tests to the public :mod:`cmat_analysis` API.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import replace
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import pandas as pd

from figures import generate_paper_figures, validate_figure_inputs

try:
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_primary_outcomes
    from cmat_analysis.reporting import write_run_log
    from cmat_analysis.statistics import (
        dose_group_fixed_effect_model,
        group_summary,
        one_two_pooling_analysis,
        primary_fixed_effect_models,
        robust_two_group_tests,
        secondary_pass_model,
        visit_distribution,
        welch_anova_visit_groups,
    )
    from cmat_analysis.visualization import set_style
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2 requires the shared editable library. From the repository root run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"\n'
        f"Original import error: {exc}"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = REPO_ROOT / "results"
TABLES_DIR = RESULTS_ROOT / "tables"
FIGURES_DIR = RESULTS_ROOT / "figures"
LOGS_DIR = RESULTS_ROOT / "logs"
PAPER_DIR = REPO_ROOT / "paper"
RETAINED_TABLES_DIR = (
    REPO_ROOT / "brainstorm" / "shared" / "historical_outputs" / "study" / "tables"
)

RETAINED_COMPARISON_FILES = (
    "10_primary_outcome_by_visit_group.csv",
    "11_primary_robust_gt3_vs_le3.csv",
    "12_primary_fixed_effect_models.csv",
    "13_primary_dose_group_model.csv",
    "14_continuous_outcome_sensitivity.csv",
    "80_justify_pooling_exact_1_vs_2.csv",
    "81_visit_groups_welch_anova.csv",
    "82_visit_groups_welch_summary.csv",
    "83_visit_groups_games_howell.csv",
)


def _save_csv(frame: pd.DataFrame, path: Path) -> None:
    """Write one aggregate Paper 2 output table."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def _package_version() -> str:
    try:
        return version("cmat-analysis")
    except PackageNotFoundError:
        return "editable/unknown"


def _compare_retained() -> None:
    """Require regenerated core tables to reproduce the retained shared snapshot."""
    mismatches: list[str] = []
    for filename in RETAINED_COMPARISON_FILES:
        generated_path = TABLES_DIR / filename
        retained_path = RETAINED_TABLES_DIR / filename
        if not generated_path.exists():
            mismatches.append(f"{filename}: generated file missing")
            continue
        if not retained_path.exists():
            mismatches.append(f"{filename}: retained reference missing")
            continue
        generated = pd.read_csv(generated_path)
        retained = pd.read_csv(retained_path)
        try:
            pd.testing.assert_frame_equal(
                generated,
                retained,
                check_dtype=False,
                check_exact=False,
                rtol=1e-9,
                atol=1e-12,
            )
        except AssertionError as exc:
            mismatches.append(f"{filename}: {str(exc).splitlines()[0]}")

    if mismatches:
        joined = "\n  - ".join(mismatches)
        raise RuntimeError(
            "Generated Paper 2 tables do not reproduce the retained canonical snapshot:\n"
            f"  - {joined}\n"
            "Do not update manuscript numbers until the discrepancy is reviewed."
        )
    print(
        "Retained-output comparison passed for "
        f"{len(RETAINED_COMPARISON_FILES)} Paper 2 tables."
    )


def check_environment() -> int:
    """Validate imports and publication-local structure without private data."""
    required_paths = [
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
        REPO_ROOT / "code" / "figures.py",
        PAPER_DIR / "main.tex",
        PAPER_DIR / "references.bib",
        PAPER_DIR / "DECOMPOSITION_FROM_PROYECTO_VISITAS.md",
        RETAINED_TABLES_DIR / "01_cohort_flow.csv",
        RETAINED_TABLES_DIR / "02_visit_distribution_mu_vs_calculus.csv",
        *[RETAINED_TABLES_DIR / name for name in RETAINED_COMPARISON_FILES],
    ]
    missing = [
        str(path.relative_to(REPO_ROOT)) for path in required_paths if not path.exists()
    ]
    if missing:
        print("Paper 2 check failed; missing required repository paths:", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 1

    try:
        validate_figure_inputs(RETAINED_TABLES_DIR, source="retained")
    except (FileNotFoundError, ValueError) as exc:
        print(f"Paper 2 retained figure-input check failed: {exc}", file=sys.stderr)
        return 1

    print("Paper 2 recipe check: OK")
    print(f"cmat-analysis version: {_package_version()}")
    print("Population: first eligible MU attempt in a period with CMAT coverage")
    print("Exposure: same-period CMAT registrations")
    print("Primary outcome: classroom-relative continuous final performance")
    print("Historical proyecto_visitas exposure is provenance only, not the estimand")
    print("No private data were read.")
    return 0


def run_analysis(args: argparse.Namespace) -> int:
    """Execute the Paper 2 recipe with the canonical shared scientific functions."""
    base_config = get_study_config(REPO_ROOT)
    materias_path = (args.materias or base_config.materias_path).expanduser().resolve()
    asesorias_path = (args.asesorias or base_config.asesorias_path).expanduser().resolve()

    missing_inputs = [path for path in (materias_path, asesorias_path) if not path.is_file()]
    if missing_inputs:
        paths = "\n".join(f"  - {path}" for path in missing_inputs)
        raise FileNotFoundError(
            "Controlled local inputs were not found:\n"
            f"{paths}\n"
            "Pass them explicitly with --materias and --asesorias. "
            "Administrative microdata must not be committed to Git."
        )

    config = replace(
        base_config,
        materias_path=materias_path,
        asesorias_path=asesorias_path,
        output_dir=RESULTS_ROOT,
    )
    set_style()
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    data = load_and_clean_inputs(config)
    cohorts = build_study_cohorts(data, config)
    mu = add_primary_outcomes(cohorts["mu_primary"], config)

    if config.primary_visit_measure == "course_specific":
        visits_col = "VISITS_COURSE"
        group_col = "VISIT_GROUP_COURSE"
        treatment_col = "PERSISTENT_GT3_COURSE"
        reached_col = "PPA_REACHED_COURSE"
    else:
        visits_col = "VISITS_CMAT_PERIOD"
        group_col = "VISIT_GROUP_PERIOD"
        treatment_col = "PERSISTENT_GT3_PERIOD"
        reached_col = "PPA_REACHED_PERIOD"

    flow = pd.DataFrame(
        [
            {
                "stage": "eligible first MU attempts, all academic periods",
                "n": len(cohorts["mu_all_first_attempts"]),
            },
            {
                "stage": "primary MU cohort with advisory coverage",
                "n": len(mu),
            },
            {
                "stage": "first Calculus I attempts with advisory coverage (comparator)",
                "n": len(cohorts["calc_comparator"]),
            },
            {
                "stage": "students progressing from MU to later Calculus I",
                "n": len(cohorts["longitudinal"]),
            },
            {
                "stage": "longitudinal pairs with Calculus advisory coverage",
                "n": int(cohorts["longitudinal"]["CALC_VISIT_COVERAGE"].sum()),
            },
        ]
    )
    _save_csv(flow, TABLES_DIR / "01_cohort_flow.csv")
    _save_csv(
        visit_distribution(mu, visits_col, "Matemáticas Universitarias"),
        TABLES_DIR / "02_mu_visit_distribution.csv",
    )

    primary_summary = group_summary(mu, group_col, "Z_GRADE_PRIMARY")
    robust = robust_two_group_tests(
        mu, treatment_col, "Z_GRADE_PRIMARY", seed=config.random_seed
    )
    fixed_effect = primary_fixed_effect_models(mu, "Z_GRADE_PRIMARY", treatment_col)
    dose = dose_group_fixed_effect_model(mu, "Z_GRADE_PRIMARY", group_col)

    sensitivity_rows: list[pd.DataFrame] = []
    for outcome in ("Z_GRADE_UNIFORM_SENS", "Z_GRADE_COMPLETE_CASE"):
        frame = robust_two_group_tests(
            mu, treatment_col, outcome, seed=config.random_seed
        )
        frame.insert(0, "outcome", outcome)
        sensitivity_rows.append(frame)
    sensitivity = pd.concat(sensitivity_rows, ignore_index=True)

    reached_robust = robust_two_group_tests(
        mu, reached_col, "Z_GRADE_PRIMARY", seed=config.random_seed
    )
    reached_fixed_effect = primary_fixed_effect_models(
        mu, "Z_GRADE_PRIMARY", reached_col
    )
    pass_model = secondary_pass_model(mu, treatment_col)

    one_two = one_two_pooling_analysis(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        equivalence_margin_z=config.one_two_equivalence_margin_z,
    )
    welch, welch_summary, games_howell = welch_anova_visit_groups(
        mu, group_col=group_col, outcome_col="Z_GRADE_PRIMARY"
    )

    generated = {
        "10_primary_outcome_by_visit_group.csv": primary_summary,
        "11_primary_robust_gt3_vs_le3.csv": robust,
        "12_primary_fixed_effect_models.csv": fixed_effect,
        "13_primary_dose_group_model.csv": dose,
        "14_continuous_outcome_sensitivity.csv": sensitivity,
        "15_ppa_reached_ge3_vs_lt3_robust.csv": reached_robust,
        "16_ppa_reached_ge3_vs_lt3_fixed_effect.csv": reached_fixed_effect,
        "20_secondary_pass_model.csv": pass_model,
        "80_justify_pooling_exact_1_vs_2.csv": one_two,
        "81_visit_groups_welch_anova.csv": welch,
        "82_visit_groups_welch_summary.csv": welch_summary,
        "83_visit_groups_games_howell.csv": games_howell,
    }
    for filename, frame in generated.items():
        _save_csv(frame, TABLES_DIR / filename)

    figure_paths = generate_paper_figures(TABLES_DIR, FIGURES_DIR, source="generated")

    summary = {
        "paper": "paper2-mu-performance",
        "cmat_analysis_version": _package_version(),
        "primary_mu_n": int(len(mu)),
        "same_period_any_cmat_use_n": int((mu[visits_col] > 0).sum()),
        "primary_visit_measure": config.primary_visit_measure,
        "tables": sorted(
            str(path.relative_to(REPO_ROOT)) for path in TABLES_DIR.glob("*.csv")
        ),
        "figures": [str(path.relative_to(REPO_ROOT)) for path in figure_paths],
    }
    (RESULTS_ROOT / "run_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    write_run_log(
        logs_dir=LOGS_DIR,
        materias_path=materias_path,
        asesorias_path=asesorias_path,
        mode="paper2_mu_performance",
        status="success",
        details={
            "primary_mu_n": int(len(mu)),
            "same_period_any_cmat_use_n": int((mu[visits_col] > 0).sum()),
            "primary_visit_measure": config.primary_visit_measure,
        },
    )

    print(f"Paper 2 primary first-MU cohort: N={len(mu):,}")
    print(f"Generated tables: {TABLES_DIR}")
    print("Generated figures:")
    for path in figure_paths:
        print(f"  - {path}")

    if args.compare_retained:
        _compare_retained()

    if args.compile:
        build_env = os.environ.copy()
        build_env["PAPER2_FIGURE_SOURCE"] = "generated"
        subprocess.run(
            [sys.executable, str(PAPER_DIR / "build.py")],
            check=True,
            env=build_env,
        )

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reproduce Paper 2 CMAT-use/performance results using the installed "
            "cmat_analysis library."
        )
    )
    parser.add_argument("--materias", type=Path, help="Controlled academic-record input file.")
    parser.add_argument("--asesorias", type=Path, help="Controlled CMAT advisory-record input file.")
    parser.add_argument(
        "--compare-retained",
        action="store_true",
        help="Require regenerated core tables to reproduce the retained shared snapshot.",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile paper/main.tex using freshly generated figure inputs.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate imports and repository structure without reading private data.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check:
        return check_environment()
    return run_analysis(args)


if __name__ == "__main__":
    raise SystemExit(main())
