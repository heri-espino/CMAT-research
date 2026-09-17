#!/usr/bin/env python3
"""Reproduce the Paper 2 MU-performance analysis from controlled inputs.

Paper 2 treats exact same-term visit groups (0, 1, 2, 3, 4+) as the primary
exposure presentation. The historical 1--2 pooling and threshold-oriented
contrasts are retained only as secondary/provenance outputs. Reusable cohort,
outcome, and estimation logic lives in ``cmat_analysis``.
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

from figures import generate_paper_figures

try:
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_primary_outcomes
    from cmat_analysis.reporting import write_run_log
    from cmat_analysis.statistics import (
        exact_visit_group_summary,
        fixed_effect_pairwise_exact_groups,
        games_howell_exact_groups,
        one_two_pooling_analysis,
        primary_fixed_effect_models,
        robust_two_group_tests,
        secondary_pass_model,
        visit_distribution,
        welch_anova_exact_groups,
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


def _save_csv(frame: pd.DataFrame, path: Path) -> None:
    """Write one aggregate Paper 2 output table."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def _package_version() -> str:
    try:
        return version("cmat-analysis")
    except PackageNotFoundError:
        return "editable/unknown"


def check_environment() -> int:
    """Validate imports and publication-local structure without reading microdata."""
    required_paths = [
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
        REPO_ROOT / "code" / "figures.py",
        PAPER_DIR / "main.tex",
        PAPER_DIR / "main_commented.tex",
        PAPER_DIR / "manuscript.tex",
        PAPER_DIR / "references.bib",
        PAPER_DIR / "ima-authoring-template" / "ima-authoring-template.cls",
    ]
    missing = [
        str(path.relative_to(REPO_ROOT)) for path in required_paths if not path.exists()
    ]
    if missing:
        print("Paper 2 check failed; missing required repository paths:", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 1

    print("Paper 2 recipe check: OK")
    print(f"cmat-analysis version: {_package_version()}")
    print("Population: first eligible MU attempt in a period with CMAT coverage")
    print("Exposure: exact same-period CMAT groups 0, 1, 2, 3, 4+")
    print("Primary outcome: classroom-relative continuous final performance")
    print("No diagnostic-test adjustment is used in Paper 2.")
    print("No private row-level data were read.")
    return 0


def run_analysis(args: argparse.Namespace) -> int:
    """Execute the Paper 2 recipe with canonical shared scientific functions."""
    base_config = get_study_config(REPO_ROOT)
    materias_path = (args.materias or base_config.materias_path).expanduser().resolve()
    asesorias_path = (args.asesorias or base_config.asesorias_path).expanduser().resolve()

    missing_inputs = [path for path in (materias_path, asesorias_path) if not path.is_file()]
    if missing_inputs:
        paths = "\n".join(f"  - {path}" for path in missing_inputs)
        raise FileNotFoundError(
            "Controlled inputs were not found:\n"
            f"{paths}\n"
            "Pass academic and advisory files explicitly. "
            "Row-level administrative outputs must not be committed as publication results."
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
        historical_treatment_col = "PERSISTENT_GT3_COURSE"
    else:
        visits_col = "VISITS_CMAT_PERIOD"
        historical_treatment_col = "PERSISTENT_GT3_PERIOD"

    population = "First eligible MU attempt with CMAT coverage"

    flow = pd.DataFrame(
        [
            {
                "stage": "eligible first MU attempts, all academic periods",
                "n": len(cohorts["mu_all_first_attempts"]),
            },
            {
                "stage": "primary MU cohort with CMAT coverage",
                "n": len(mu),
            },
        ]
    )
    _save_csv(flow, TABLES_DIR / "01_cohort_flow.csv")
    _save_csv(
        visit_distribution(mu, visits_col, "Matemáticas Universitarias"),
        TABLES_DIR / "02_mu_visit_distribution.csv",
    )

    # Primary transparent exposure specification: 0, 1, 2, 3, 4+.
    exact_summary = exact_visit_group_summary(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population,
    )
    exact_welch = welch_anova_exact_groups(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population,
    )
    exact_gh = games_howell_exact_groups(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population,
    )
    exact_fe, exact_fe_info = fixed_effect_pairwise_exact_groups(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        population=population,
        include_career=True,
    )

    primary_exact = {
        "30_exact_visit_groups_summary.csv": exact_summary,
        "31_exact_visit_groups_welch_anova.csv": exact_welch,
        "32_exact_visit_groups_games_howell.csv": exact_gh,
        "33_exact_visit_groups_fe_pairwise.csv": exact_fe,
        "34_exact_visit_groups_fe_model_info.csv": exact_fe_info,
    }
    for filename, frame in primary_exact.items():
        _save_csv(frame, TABLES_DIR / filename)

    # Identification diagnostics for the within-classroom comparisons. These are
    # aggregate publication outputs only and do not expose student identifiers.
    classroom_sizes = mu.groupby("CLASSROOM_ID", observed=True).size().astype(int)
    any_use = mu[visits_col].fillna(0).astype(float).gt(0)
    overlap = (
        pd.DataFrame({"CLASSROOM_ID": mu["CLASSROOM_ID"], "any_use": any_use})
        .groupby("CLASSROOM_ID", observed=True)["any_use"]
        .agg(["size", "sum"])
        .rename(columns={"size": "n", "sum": "users"})
    )
    overlap["nonusers"] = overlap["n"] - overlap["users"]
    overlap["has_user_nonuser_overlap"] = (overlap["users"] > 0) & (overlap["nonusers"] > 0)

    exact_labels = pd.Series("4+", index=mu.index, dtype="object")
    v = mu[visits_col].fillna(0).astype(float)
    exact_labels.loc[v.eq(0)] = "0"
    exact_labels.loc[v.eq(1)] = "1"
    exact_labels.loc[v.eq(2)] = "2"
    exact_labels.loc[v.eq(3)] = "3"
    exact_overlap_rows = []
    for group in ("1", "2", "3", "4+"):
        tmp = pd.DataFrame({"CLASSROOM_ID": mu["CLASSROOM_ID"], "group": exact_labels})
        present = tmp.groupby("CLASSROOM_ID", observed=True)["group"].agg(lambda x: set(x.astype(str)))
        n_overlap = int(present.map(lambda groups: "0" in groups and group in groups).sum())
        exact_overlap_rows.append({"comparison": f"0_vs_{group}", "classrooms_with_both_groups": n_overlap})

    diagnostics = pd.DataFrame(
        [
            {"metric": "n_classrooms", "value": float(classroom_sizes.size)},
            {"metric": "classroom_size_mean", "value": float(classroom_sizes.mean())},
            {"metric": "classroom_size_median", "value": float(classroom_sizes.median())},
            {"metric": "classroom_size_q1", "value": float(classroom_sizes.quantile(0.25))},
            {"metric": "classroom_size_q3", "value": float(classroom_sizes.quantile(0.75))},
            {"metric": "classroom_size_min", "value": float(classroom_sizes.min())},
            {"metric": "classroom_size_max", "value": float(classroom_sizes.max())},
            {
                "metric": "classrooms_with_any_user_and_nonuser",
                "value": float(overlap["has_user_nonuser_overlap"].sum()),
            },
        ]
    )
    _save_csv(diagnostics, TABLES_DIR / "35_classroom_identification_diagnostics.csv")
    _save_csv(pd.DataFrame(exact_overlap_rows), TABLES_DIR / "36_exact_group_classroom_overlap.csv")

    # Sensitivity of the adjusted 0-vs-positive contrasts to excluding very
    # small classrooms. Thresholds are reported together rather than selected
    # after inspecting one preferred result.
    small_class_rows: list[pd.DataFrame] = []
    classroom_n = mu.groupby("CLASSROOM_ID", observed=True)["CLASSROOM_ID"].transform("size")
    for min_n in (1, 10, 20):
        sub = mu.loc[classroom_n >= min_n].copy()
        pairwise, info = fixed_effect_pairwise_exact_groups(
            sub,
            visits_col=visits_col,
            outcome_col="Z_GRADE_PRIMARY",
            population=f"{population}; classrooms n>={min_n}",
            include_career=True,
        )
        pairwise = pairwise.loc[
            (pairwise["group1"].astype(str) == "0")
            & pairwise["group2"].astype(str).isin(["1", "2", "3", "4+"])
        ].copy()
        pairwise.insert(0, "minimum_classroom_n", min_n)
        pairwise.insert(1, "analysis_n", int(len(sub)))
        pairwise.insert(2, "analysis_classrooms", int(sub["CLASSROOM_ID"].nunique()))
        small_class_rows.append(pairwise)
    _save_csv(
        pd.concat(small_class_rows, ignore_index=True),
        TABLES_DIR / "38_small_classroom_fe_sensitivity.csv",
    )

    # Outcome-construction sensitivity using the same transparent visit groups.
    outcome_sensitivity_frames: list[pd.DataFrame] = []
    for outcome_col, outcome_label in [
        ("Z_GRADE_PRIMARY", "primary_adverse_outcome_rule"),
        ("Z_GRADE_UNIFORM_SENS", "uniform_adverse_imputation"),
        ("Z_GRADE_COMPLETE_CASE", "numeric_complete_case"),
    ]:
        frame = exact_visit_group_summary(
            mu,
            visits_col=visits_col,
            outcome_col=outcome_col,
            population=population,
        ).copy()
        frame.insert(1, "outcome_definition", outcome_label)
        outcome_sensitivity_frames.append(frame)
    outcome_sensitivity = pd.concat(outcome_sensitivity_frames, ignore_index=True)
    _save_csv(
        outcome_sensitivity,
        TABLES_DIR / "37_exact_visit_groups_outcome_sensitivity.csv",
    )

    # Secondary/provenance analyses retained so prior project claims remain
    # reproducible. They no longer define the main Paper 2 estimand.
    pooled_equivalence = one_two_pooling_analysis(
        mu,
        visits_col=visits_col,
        outcome_col="Z_GRADE_PRIMARY",
        equivalence_margin_z=config.one_two_equivalence_margin_z,
    )
    _save_csv(
        pooled_equivalence,
        TABLES_DIR / "80_secondary_pooling_exact_1_vs_2.csv",
    )

    historical_upper_tail = robust_two_group_tests(
        mu,
        historical_treatment_col,
        "Z_GRADE_PRIMARY",
        seed=config.random_seed,
    )
    _save_csv(
        historical_upper_tail,
        TABLES_DIR / "81_secondary_historical_upper_tail.csv",
    )
    _save_csv(
        primary_fixed_effect_models(
            mu, "Z_GRADE_PRIMARY", historical_treatment_col
        ),
        TABLES_DIR / "82_secondary_historical_upper_tail_fe.csv",
    )
    _save_csv(
        secondary_pass_model(mu, historical_treatment_col),
        TABLES_DIR / "83_secondary_historical_pass_model.csv",
    )

    figure_paths = generate_paper_figures(TABLES_DIR, FIGURES_DIR)

    summary = {
        "paper": "paper2-mu-performance",
        "cmat_analysis_version": _package_version(),
        "primary_mu_n": int(len(mu)),
        "same_period_any_cmat_use_n": int((mu[visits_col] > 0).sum()),
        "primary_visit_measure": config.primary_visit_measure,
        "primary_visit_groups": ["0", "1", "2", "3", "4+"],
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
        mode="paper2_mu_performance_exact_groups",
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

    if args.compile:
        build_env = os.environ.copy()
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
        "--compile",
        action="store_true",
        help="Compile the manuscript after generating current aggregate results and figures.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate imports and repository structure without reading row-level data.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check:
        return check_environment()
    return run_analysis(args)


if __name__ == "__main__":
    raise SystemExit(main())
