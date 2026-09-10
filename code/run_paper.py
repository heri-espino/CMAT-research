#!/usr/bin/env python3
"""Reproduce the Paper 1 PPA-persistence analysis from controlled local inputs.

This file is intentionally a thin publication recipe. Scientific cohort
definitions, estimators, confidence intervals, and models are imported from the
shared :mod:`cmat_analysis` library. Do not reimplement reusable scientific
logic in this branch-local module.
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
    from cmat_analysis.cohorts import load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.ppa import (
        build_ppa_progression_cohort,
        later_performance_models,
        persistence_by_mu_group,
        persistence_logistic_models,
        piecewise_threshold_persistence_model,
        ppa_behavior_profiles,
        ppa_persistence_association_tests,
    )
    from cmat_analysis.reporting import write_run_log
    from cmat_analysis.visualization import set_style
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 1 requires the shared editable library. From the repository root run:\n"
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
    "101_ppa_behavior_profiles.csv",
    "102_ppa_persistence_by_mu_group.csv",
    "103_ppa_persistence_omnibus.csv",
    "104_ppa_exact3_vs_4plus_persistence.csv",
    "105_ppa_persistence_logistic_models.csv",
    "106_ppa_piecewise_threshold_persistence.csv",
    "107_ppa_later_performance_models.csv",
)


def _save_csv(frame: pd.DataFrame, path: Path) -> None:
    """Write one aggregate Paper 1 output table."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def _compare_retained() -> None:
    """Compare generated primary tables against the retained historical snapshot."""
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
            "Generated Paper 1 tables do not reproduce the retained snapshot:\n"
            f"  - {joined}\n"
            "Do not overwrite manuscript numbers until the discrepancy is reviewed."
        )

    print(
        "Retained-output comparison passed for "
        f"{len(RETAINED_COMPARISON_FILES)} Paper 1 tables."
    )


def _package_version() -> str:
    try:
        return version("cmat-analysis")
    except PackageNotFoundError:
        return "editable/unknown"


def check_environment() -> int:
    """Validate imports and branch-local structure without requiring private data."""
    required_paths = [
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
        REPO_ROOT / "code" / "figures.py",
        PAPER_DIR / "main.tex",
        PAPER_DIR / "references.bib",
        RETAINED_TABLES_DIR / "98_ppa_progression_cohort_flow.csv",
        RETAINED_TABLES_DIR / "102_ppa_persistence_by_mu_group.csv",
        RETAINED_TABLES_DIR / "105_ppa_persistence_logistic_models.csv",
        RETAINED_TABLES_DIR / "106_ppa_piecewise_threshold_persistence.csv",
    ]
    missing = [
        str(path.relative_to(REPO_ROOT)) for path in required_paths if not path.exists()
    ]
    if missing:
        print("Paper 1 check failed; missing required repository paths:", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 1

    try:
        validate_figure_inputs(RETAINED_TABLES_DIR)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Paper 1 figure-input check failed: {exc}", file=sys.stderr)
        return 1

    print("Paper 1 recipe check: OK")
    print(f"cmat-analysis version: {_package_version()}")
    print("Primary analysis: strict next-regular-term MU -> Calculus progression cohort")
    print("Primary outcome: any CMAT use in the eligible Calculus I period")
    print("Figure inputs: retained aggregate snapshot is complete")
    print("No private data were read.")
    return 0


def run_analysis(args: argparse.Namespace) -> int:
    """Execute the branch-local Paper 1 recipe using shared library functions."""
    base_config = get_study_config(REPO_ROOT)
    materias_path = (args.materias or base_config.materias_path).expanduser().resolve()
    asesorias_path = (args.asesorias or base_config.asesorias_path).expanduser().resolve()

    missing_inputs = [
        path for path in (materias_path, asesorias_path) if not path.is_file()
    ]
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

    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    data = load_and_clean_inputs(config)
    progression = build_ppa_progression_cohort(data, config)
    pair = progression.paired_primary_next_term

    if pair.empty:
        raise RuntimeError("The primary Paper 1 progression cohort is empty.")

    _save_csv(progression.cohort_flow, TABLES_DIR / "98_ppa_progression_cohort_flow.csv")
    _save_csv(progression.revalidation_audit, TABLES_DIR / "99_revalidation_audit.csv")
    _save_csv(
        progression.career_count_distribution,
        TABLES_DIR / "100_student_official_career_count_distribution.csv",
    )

    profiles = ppa_behavior_profiles(pair)
    persistence = persistence_by_mu_group(pair)
    omnibus, exact3_vs_4plus = ppa_persistence_association_tests(pair)
    logit = persistence_logistic_models(
        pair, min_career_n=config.min_career_n_for_inference
    )
    piecewise = piecewise_threshold_persistence_model(
        pair, cap_visits=config.exact_visit_index_max
    )
    later_perf = later_performance_models(
        pair, min_career_n=config.min_career_n_for_inference
    )

    generated = {
        "101_ppa_behavior_profiles.csv": profiles,
        "102_ppa_persistence_by_mu_group.csv": persistence,
        "103_ppa_persistence_omnibus.csv": omnibus,
        "104_ppa_exact3_vs_4plus_persistence.csv": exact3_vs_4plus,
        "105_ppa_persistence_logistic_models.csv": logit,
        "106_ppa_piecewise_threshold_persistence.csv": piecewise,
        "107_ppa_later_performance_models.csv": later_perf,
    }
    for filename, frame in generated.items():
        _save_csv(frame, TABLES_DIR / filename)

    figure_paths = generate_paper_figures(TABLES_DIR, FIGURES_DIR)

    summary = {
        "paper": "paper1-ppa-persistence",
        "cmat_analysis_version": _package_version(),
        "primary_cohort_n": int(len(pair)),
        "all_subsequent_sensitivity_n": int(len(progression.paired_all_subsequent)),
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
        mode="paper1_ppa_persistence",
        status="success",
        details={
            "primary_cohort_n": int(len(pair)),
            "all_subsequent_sensitivity_n": int(
                len(progression.paired_all_subsequent)
            ),
            "generated_table_count": len(generated) + 3,
        },
    )

    print(f"Paper 1 primary cohort: N={len(pair):,}")
    print(f"Generated tables: {TABLES_DIR}")
    print("Generated figures:")
    for path in figure_paths:
        print(f"  - {path}")

    if args.compare_retained:
        _compare_retained()

    if args.compile:
        build_env = os.environ.copy()
        build_env["PAPER1_FIGURE_SOURCE"] = "generated"
        subprocess.run(
            [sys.executable, str(PAPER_DIR / "build.py")],
            check=True,
            env=build_env,
        )

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reproduce Paper 1 PPA-persistence results using the installed "
            "cmat_analysis library."
        )
    )
    parser.add_argument(
        "--materias",
        type=Path,
        help="Controlled local academic-record input file.",
    )
    parser.add_argument(
        "--asesorias",
        type=Path,
        help="Controlled local CMAT advisory-record input file.",
    )
    parser.add_argument(
        "--compare-retained",
        action="store_true",
        help=(
            "Require generated tables 101-107 to match the retained historical "
            "Paper 1 snapshot within numerical tolerance."
        ),
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile paper/main.tex after the analysis finishes successfully.",
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
