#!/usr/bin/env python3
"""Paper 2.1 outcome-blind visit-frequency support audit.

Paper-specific orchestration delegates reusable grouping and support diagnostics
to cmat_analysis. No academic outcome variable is read in this runner.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

import pandas as pd

try:
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.statistics import (
        add_topcoded_visit_group,
        visit_frequency_cut_frontier,
        visit_frequency_support_audit,
        visit_group_pair_overlap,
    )
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2.1 requires the shared editable library. From the repository root run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"\n'
        f"Original import error: {exc}"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "results" / "paper21" / "tables"


def _save(frame: pd.DataFrame, name: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES_DIR / name, index=False)


def check_environment() -> int:
    required = [
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
        REPO_ROOT / "paper" / "ANALYSIS_PLAN.md",
        REPO_ROOT / "paper" / "PROJECT_CONTEXT.md",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing Paper 2.1 paths: " + ", ".join(missing))
    print("Paper 2.1 support-audit check: OK")
    print("Reusable support diagnostics: cmat_analysis.statistics")
    print("No academic outcome variables are read by this runner.")
    return 0


def run(args: argparse.Namespace) -> int:
    base = get_study_config(REPO_ROOT)
    config = replace(
        base,
        materias_path=(args.materias or base.materias_path).expanduser().resolve(),
        asesorias_path=(args.asesorias or base.asesorias_path).expanduser().resolve(),
    )
    data = load_and_clean_inputs(config)
    mu = build_study_cohorts(data, config)["mu_primary"].copy()
    visits_col = "VISITS_CMAT_PERIOD"
    users = mu.loc[mu[visits_col].gt(0)].copy()

    support = visit_frequency_support_audit(
        mu,
        visits_col=visits_col,
        cluster_col="CLASSROOM_ID",
        instructor_col="CLAVEPROFESOR",
    ).rename(
        columns={
            "n_clusters": "n_instructor_period_groups",
            "median_students_per_cluster": "median_students_per_instructor_period",
            "max_students_per_cluster": "max_students_per_instructor_period",
            "clusters_with_another_positive_frequency": "groups_with_another_positive_frequency",
            "clusters_with_zero_visit_students": "groups_with_zero_visit_students",
        }
    )
    _save(support, "01_exact_positive_visit_support.csv")

    max_visits = int(users[visits_col].max())
    frontier = visit_frequency_cut_frontier(
        mu,
        visits_col=visits_col,
        cluster_col="CLASSROOM_ID",
        min_top_exact=1,
        max_top_exact=max_visits - 1,
    )
    frontier["tail_instructors"] = [
        int(users.loc[users[visits_col].gt(int(k)), "CLAVEPROFESOR"].nunique())
        for k in frontier["top_exact_visit_count"]
    ]
    tail_support = frontier.rename(
        columns={
            "minimum_exact_group_clusters": "minimum_exact_group_instructor_periods",
            "tail_clusters": "tail_instructor_periods",
        }
    )[
        [
            "top_exact_visit_count",
            "tail_label",
            "n_frequency_groups",
            "minimum_exact_group_n",
            "minimum_exact_group_instructor_periods",
            "tail_n",
            "tail_instructor_periods",
            "tail_instructors",
        ]
    ]
    _save(tail_support, "02_candidate_tail_support.csv")

    top_exact = int(args.candidate_top_exact)
    grouped = add_topcoded_visit_group(
        users,
        visits_col=visits_col,
        top_exact=top_exact,
        output_col="CANDIDATE_GROUP",
    )
    candidate_summary = (
        grouped.groupby("CANDIDATE_GROUP", observed=True)
        .agg(
            n_students=("STUDENT_ID", "size"),
            n_instructor_period_groups=("CLASSROOM_ID", "nunique"),
            n_instructors=("CLAVEPROFESOR", "nunique"),
        )
        .reset_index()
    )
    candidate_summary["group"] = candidate_summary["CANDIDATE_GROUP"].astype(str)
    _save(candidate_summary.drop(columns="CANDIDATE_GROUP"), "03_candidate_group_support.csv")

    order = [str(value) for value in range(1, top_exact + 1)] + [f"{top_exact + 1}+"]
    overlap = visit_group_pair_overlap(
        grouped,
        group_col="CANDIDATE_GROUP",
        group_order=order,
        cluster_col="CLASSROOM_ID",
    ).rename(columns={"clusters_with_both": "instructor_period_groups_with_both"})
    _save(overlap.drop(columns="adjacent_groups"), "04_candidate_pair_overlap.csv")

    overlap_frontier = frontier.loc[frontier["top_exact_visit_count"].ge(2)].rename(
        columns={
            "minimum_adjacent_pair_overlap_clusters": "minimum_adjacent_pair_overlap_groups",
            "median_adjacent_pair_overlap_clusters": "median_adjacent_pair_overlap_groups",
            "minimum_all_pair_overlap_clusters": "minimum_all_pair_overlap_groups",
            "median_all_pair_overlap_clusters": "median_all_pair_overlap_groups",
        }
    )[
        [
            "top_exact_visit_count",
            "tail_label",
            "n_frequency_groups",
            "minimum_adjacent_pair_overlap_groups",
            "median_adjacent_pair_overlap_groups",
            "minimum_all_pair_overlap_groups",
            "median_all_pair_overlap_groups",
        ]
    ]
    _save(overlap_frontier, "05_cut_overlap_frontier.csv")

    print(f"Paper 2.1 positive-attendance students: N={len(users):,}")
    print(f"Maximum observed same-period visits: {max_visits}")
    print(f"Candidate grouping audit: 1..{top_exact}, {top_exact + 1}+")
    print(f"Outputs: {TABLES_DIR}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Paper 2.1 outcome-blind visit-frequency support audit."
    )
    parser.add_argument("--materias", type=Path)
    parser.add_argument("--asesorias", type=Path)
    parser.add_argument("--candidate-top-exact", type=int, default=5)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return check_environment() if args.check else run(args)


if __name__ == "__main__":
    raise SystemExit(main())
