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
        build_ppa_mu_baseline_cohort,
        build_ppa_progression_cohort,
        familiarization_professor_persistence_models,
        later_performance_models,
        leave_period_out_professor_propensity,
        persistence_by_mu_group,
        persistence_logistic_models,
        piecewise_threshold_persistence_model,
        ppa_behavior_profiles,
        ppa_persistence_association_tests,
        professor_familiarization_interaction_model,
        professor_uptake_increment,
        professor_visit_group_distribution,
        professor_visit_group_multinomial_increment,
    )
    from cmat_analysis.reporting import write_run_log
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


def _summarize_professor_group_distribution(frame: pd.DataFrame) -> pd.DataFrame:
    """Reduce controlled instructor-level group shares to publication-safe quantiles."""
    share_columns = [
        column for column in frame.columns if column.startswith("share_")
    ]
    rows: list[dict[str, object]] = []
    for column in share_columns:
        values = frame[column].dropna().astype(float)
        if values.empty:
            continue
        q = values.quantile([0.10, 0.25, 0.50, 0.75, 0.90])
        rows.append({
            "visit_group_share": column.removeprefix("share_"),
            "professors": int(len(values)),
            "min": float(values.min()),
            "p10": float(q.loc[0.10]),
            "p25": float(q.loc[0.25]),
            "median": float(q.loc[0.50]),
            "p75": float(q.loc[0.75]),
            "p90": float(q.loc[0.90]),
            "max": float(values.max()),
            "sd": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
        })
    return pd.DataFrame(rows)


def _professor_propensity_by_familiarity(pair: pd.DataFrame) -> pd.DataFrame:
    """Aggregate later-use rates by prior familiarity and current-instructor propensity."""
    augmented = leave_period_out_professor_propensity(
        pair,
        professor_col="CALC_PROFESSOR",
        period_col="CALC_PERIOD_LABEL",
        outcome_col="CALC_ANY_VISIT",
        min_other_n=30,
        prefix="CALC_PROF",
    )
    d = augmented.dropna(
        subset=[
            "CALC_PROF_LEAVE_PERIOD_OUT_RATE",
            "CALC_ANY_VISIT",
            "MU_VISIT_GROUP",
        ]
    ).copy()
    if d.empty:
        return pd.DataFrame(columns=[
            "mu_visit_group", "professor_propensity_quartile", "n",
            "calc_any_visit_rate", "mean_professor_leaveout_rate",
        ])
    quartile = pd.qcut(
        d["CALC_PROF_LEAVE_PERIOD_OUT_RATE"],
        q=4,
        labels=False,
        duplicates="drop",
    )
    d["professor_propensity_quartile"] = quartile.map(
        lambda value: f"Q{int(value) + 1}" if pd.notna(value) else None
    )
    out = (
        d.groupby(
            ["MU_VISIT_GROUP", "professor_propensity_quartile"],
            observed=False,
            dropna=True,
        )
        .agg(
            n=("CALC_ANY_VISIT", "size"),
            calc_any_visit_rate=("CALC_ANY_VISIT", "mean"),
            mean_professor_leaveout_rate=(
                "CALC_PROF_LEAVE_PERIOD_OUT_RATE", "mean"
            ),
        )
        .reset_index()
    )
    out["mu_visit_group"] = out["MU_VISIT_GROUP"].astype(str)
    return out.drop(columns="MU_VISIT_GROUP")


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
        REPO_ROOT / "cmat_analysis" / "src" / "cmat_analysis" / "ppa" / "encouragement.py",
        REPO_ROOT / "cmat_analysis" / "src" / "cmat_analysis" / "ppa" / "baseline.py",
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
    print("Initial uptake analysis: eligible MU baseline, not conditioned on later Calculus")
    print("Persistence analysis: strict next-regular-term MU -> Calculus progression cohort")
    print("Primary later outcome: any CMAT use in the eligible Calculus I period")
    print("Prior familiarity groups: 0 / 1-2 / exactly 3 / 4+")
    print("Instructor-linked uptake is observational and is not treated as an instrument")
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
            "Administrative raw microdata must not be committed to Git."
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
    mu_baseline = build_ppa_mu_baseline_cohort(data, config)
    progression = build_ppa_progression_cohort(data, config)
    pair = progression.paired_primary_next_term
    pair_all = progression.paired_all_subsequent

    if pair.empty:
        raise RuntimeError("The primary Paper 1 progression cohort is empty.")
    if mu_baseline.empty:
        raise RuntimeError("The Paper 1 MU baseline cohort is empty.")

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

    # Instructor-linked uptake at the initial MU stage is estimated in the full
    # eligible MU baseline rather than only among students who later reach Calculus.
    mu_professor_distribution = professor_visit_group_distribution(
        mu_baseline,
        professor_col="MU_PROFESSOR",
        group_col="MU_VISIT_GROUP",
        min_professor_n=30,
    )
    mu_professor_distribution_summary = _summarize_professor_group_distribution(
        mu_professor_distribution
    )
    mu_professor_multinomial = professor_visit_group_multinomial_increment(
        mu_baseline,
        group_col="MU_VISIT_GROUP",
        professor_col="MU_PROFESSOR",
        period_col="MU_PERIOD_LABEL",
        career_col="MU_CAREER_OFFICIAL",
        min_career_n=config.min_career_n_for_inference,
    )
    mu_professor_any = professor_uptake_increment(
        mu_baseline,
        outcome_col="MU_ANY_VISIT",
        professor_col="MU_PROFESSOR",
        period_col="MU_PERIOD_LABEL",
        career_col="MU_CAREER_OFFICIAL",
        min_career_n=config.min_career_n_for_inference,
    )

    # In the later Calculus setting, compare prior CMAT familiarity with the
    # current instructor-linked implementation context.
    calc_professor_any = professor_uptake_increment(
        pair,
        outcome_col="CALC_ANY_VISIT",
        professor_col="CALC_PROFESSOR",
        period_col="CALC_PERIOD_LABEL",
        career_col="CALC_CAREER_OFFICIAL",
        min_career_n=config.min_career_n_for_inference,
    )
    familiarity_professor = familiarization_professor_persistence_models(
        pair,
        min_career_n=config.min_career_n_for_inference,
    )
    interaction_coef, interaction_slopes, interaction_diag = (
        professor_familiarization_interaction_model(
            pair,
            min_career_n=config.min_career_n_for_inference,
            min_other_n=30,
        )
    )
    propensity_cells = _professor_propensity_by_familiarity(pair)

    # Broader all-subsequent-Calculus sensitivity for the two-mechanism result.
    familiarity_professor_all = familiarization_professor_persistence_models(
        pair_all,
        min_career_n=config.min_career_n_for_inference,
    )
    interaction_coef_all, interaction_slopes_all, interaction_diag_all = (
        professor_familiarization_interaction_model(
            pair_all,
            min_career_n=config.min_career_n_for_inference,
            min_other_n=30,
        )
    )

    generated = {
        "101_ppa_behavior_profiles.csv": profiles,
        "102_ppa_persistence_by_mu_group.csv": persistence,
        "103_ppa_persistence_omnibus.csv": omnibus,
        "104_ppa_exact3_vs_4plus_persistence.csv": exact3_vs_4plus,
        "105_ppa_persistence_logistic_models.csv": logit,
        "106_ppa_piecewise_threshold_persistence.csv": piecewise,
        "107_ppa_later_performance_models.csv": later_perf,
        "120_mu_professor_visit_group_distribution_summary.csv": mu_professor_distribution_summary,
        "121_mu_professor_visit_group_multinomial_increment.csv": mu_professor_multinomial,
        "122_mu_professor_any_use_increment.csv": mu_professor_any,
        "123_calc_professor_any_use_increment.csv": calc_professor_any,
        "124_familiarization_with_calc_professor_models.csv": familiarity_professor,
        "125_professor_familiarization_interaction_coefficients.csv": interaction_coef,
        "126_professor_familiarization_group_slopes.csv": interaction_slopes,
        "127_professor_familiarization_diagnostics.csv": interaction_diag,
        "128_professor_propensity_by_prior_familiarity.csv": propensity_cells,
        "129_familiarization_with_calc_professor_models_all_subsequent.csv": familiarity_professor_all,
        "130_professor_familiarization_group_slopes_all_subsequent.csv": interaction_slopes_all,
        "131_professor_familiarization_diagnostics_all_subsequent.csv": interaction_diag_all,
        "132_professor_familiarization_interaction_coefficients_all_subsequent.csv": interaction_coef_all,
    }
    for filename, frame in generated.items():
        _save_csv(frame, TABLES_DIR / filename)

    figure_paths = generate_paper_figures(TABLES_DIR, FIGURES_DIR)

    summary = {
        "paper": "paper1-ppa-persistence",
        "cmat_analysis_version": _package_version(),
        "mu_baseline_n": int(len(mu_baseline)),
        "mu_baseline_professors": int(mu_baseline["MU_PROFESSOR"].nunique()),
        "primary_cohort_n": int(len(pair)),
        "primary_calc_professors": int(pair["CALC_PROFESSOR"].nunique()),
        "all_subsequent_sensitivity_n": int(len(pair_all)),
        "interpretation": (
            "observational instructor-linked uptake and prior-familiarity associations; "
            "neither instructor propensity nor prior CMAT use is randomized"
        ),
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
            "mu_baseline_n": int(len(mu_baseline)),
            "primary_cohort_n": int(len(pair)),
            "all_subsequent_sensitivity_n": int(len(pair_all)),
            "generated_table_count": len(generated) + 3,
        },
    )

    print(f"Paper 1 MU baseline cohort: N={len(mu_baseline):,}")
    print(f"Paper 1 primary progression cohort: N={len(pair):,}")
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
            "Reproduce Paper 1 PPA-persistence and instructor/familiarity results "
            "using the installed cmat_analysis library."
        )
    )
    parser.add_argument(
        "--materias",
        type=Path,
        help="Controlled academic-record input file.",
    )
    parser.add_argument(
        "--asesorias",
        type=Path,
        help="Controlled CMAT advisory-record input file.",
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
        help="Validate imports and repository structure without reading controlled data.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check:
        return check_environment()
    return run_analysis(args)


if __name__ == "__main__":
    raise SystemExit(main())
