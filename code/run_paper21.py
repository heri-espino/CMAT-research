#!/usr/bin/env python3
"""Paper 2.1 outcome-blind support audit for positive CMAT visit frequencies.

This runner intentionally does not construct grades, PASS, means, effect sizes,
or p-values. Its first job is to determine how finely positive visit frequency
can be represented before outcome analysis begins.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

import pandas as pd

try:
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Paper 2.1 requires the shared editable library. From the repository root run:\n"
        '  python -m pip install -e "./cmat_analysis[dev]"\n'
        f"Original import error: {exc}"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "results" / "paper21"
TABLES_DIR = RESULTS_DIR / "tables"


def _save(frame: pd.DataFrame, name: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES_DIR / name, index=False)


def check_environment() -> int:
    required = [
        REPO_ROOT / "cmat_analysis" / "pyproject.toml",
        REPO_ROOT / "paper" / "ANALYSIS_PLAN.md",
        REPO_ROOT / "paper" / "PROJECT_CONTEXT.md",
    ]
    missing = [str(p.relative_to(REPO_ROOT)) for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing Paper 2.1 paths: " + ", ".join(missing))
    print("Paper 2.1 support-audit check: OK")
    print("No academic outcome variables are read by this support audit.")
    return 0


def _candidate_group(visits: pd.Series, top_exact: int) -> pd.Series:
    labels = visits.astype(int).astype(str)
    labels = labels.where(visits <= top_exact, f"{top_exact + 1}+")
    order = [str(k) for k in range(1, top_exact + 1)] + [f"{top_exact + 1}+"]
    return pd.Categorical(labels, categories=order, ordered=True)


def run(args: argparse.Namespace) -> int:
    base = get_study_config(REPO_ROOT)
    materias = (args.materias or base.materias_path).expanduser().resolve()
    asesorias = (args.asesorias or base.asesorias_path).expanduser().resolve()
    config = replace(base, materias_path=materias, asesorias_path=asesorias)

    data = load_and_clean_inputs(config)
    cohorts = build_study_cohorts(data, config)
    mu = cohorts["mu_primary"].copy()

    visits_col = "VISITS_CMAT_PERIOD"
    users = mu.loc[mu[visits_col] > 0].copy()
    users[visits_col] = users[visits_col].astype(int)

    classroom_positive_sets = (
        users.groupby("CLASSROOM_ID", observed=True)[visits_col]
        .agg(lambda s: set(int(x) for x in s))
        .to_dict()
    )
    classroom_all_sets = (
        mu.groupby("CLASSROOM_ID", observed=True)[visits_col]
        .agg(lambda s: set(int(x) for x in s))
        .to_dict()
    )

    rows = []
    n_users = len(users)
    for k, g in users.groupby(visits_col, sort=True):
        classroom_counts = g.groupby("CLASSROOM_ID", observed=True).size()
        classrooms = set(g["CLASSROOM_ID"])
        rows.append(
            {
                "visits_exact": int(k),
                "n_students": int(len(g)),
                "share_of_positive_users": float(len(g) / n_users),
                "n_instructor_period_groups": int(g["CLASSROOM_ID"].nunique()),
                "n_instructors": int(g["CLAVEPROFESOR"].nunique()),
                "median_students_per_instructor_period": float(classroom_counts.median()),
                "max_students_per_instructor_period": int(classroom_counts.max()),
                "groups_with_another_positive_frequency": int(
                    sum(len(classroom_positive_sets[c] - {int(k)}) > 0 for c in classrooms)
                ),
                "groups_with_zero_visit_students": int(
                    sum(0 in classroom_all_sets[c] for c in classrooms)
                ),
                "tail_n_ge_k": int((users[visits_col] >= int(k)).sum()),
            }
        )
    exact_support = pd.DataFrame(rows)
    _save(exact_support, "01_exact_positive_visit_support.csv")

    max_k = int(users[visits_col].max())
    tail_rows = []
    for top_exact in range(1, max_k):
        exact_levels = list(range(1, top_exact + 1))
        exact_stats = exact_support.loc[exact_support["visits_exact"].isin(exact_levels)]
        tail = users.loc[users[visits_col] > top_exact]
        if tail.empty or len(exact_stats) != len(exact_levels):
            continue
        tail_rows.append(
            {
                "top_exact_visit_count": top_exact,
                "tail_label": f"{top_exact + 1}+",
                "n_frequency_groups": top_exact + 1,
                "minimum_exact_group_n": int(exact_stats["n_students"].min()),
                "minimum_exact_group_instructor_periods": int(
                    exact_stats["n_instructor_period_groups"].min()
                ),
                "tail_n": int(len(tail)),
                "tail_instructor_periods": int(tail["CLASSROOM_ID"].nunique()),
                "tail_instructors": int(tail["CLAVEPROFESOR"].nunique()),
            }
        )
    _save(pd.DataFrame(tail_rows), "02_candidate_tail_support.csv")

    top_exact = int(args.candidate_top_exact)
    users["CANDIDATE_GROUP"] = _candidate_group(users[visits_col], top_exact)
    candidate_summary = (
        users.groupby("CANDIDATE_GROUP", observed=True)
        .agg(
            n_students=("STUDENT_ID", "size"),
            n_instructor_period_groups=("CLASSROOM_ID", "nunique"),
            n_instructors=("CLAVEPROFESOR", "nunique"),
        )
        .reset_index()
    )
    candidate_summary["group"] = candidate_summary["CANDIDATE_GROUP"].astype(str)
    candidate_summary = candidate_summary.drop(columns="CANDIDATE_GROUP")
    _save(candidate_summary, "03_candidate_group_support.csv")

    presence = (
        users[["CLASSROOM_ID", "CANDIDATE_GROUP"]]
        .drop_duplicates()
        .assign(group=lambda d: d["CANDIDATE_GROUP"].astype(str))
        .drop(columns="CANDIDATE_GROUP")
    )
    group_order = [str(k) for k in range(1, top_exact + 1)] + [f"{top_exact + 1}+"]
    overlap_rows = []
    for i, a in enumerate(group_order):
        ca = set(presence.loc[presence["group"] == a, "CLASSROOM_ID"])
        for b in group_order[i + 1 :]:
            cb = set(presence.loc[presence["group"] == b, "CLASSROOM_ID"])
            overlap_rows.append(
                {
                    "group1": a,
                    "group2": b,
                    "instructor_period_groups_with_both": int(len(ca & cb)),
                }
            )
    _save(pd.DataFrame(overlap_rows), "04_candidate_pair_overlap.csv")

    print(f"Paper 2.1 positive-attendance students: N={n_users:,}")
    print(f"Maximum observed same-period visits: {max_k}")
    print(f"Candidate grouping audit: 1..{top_exact}, {top_exact + 1}+")
    print(f"Outputs: {TABLES_DIR}")
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Paper 2.1 outcome-blind visit-frequency support audit.")
    p.add_argument("--materias", type=Path)
    p.add_argument("--asesorias", type=Path)
    p.add_argument("--candidate-top-exact", type=int, default=6)
    p.add_argument("--check", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.check:
        return check_environment()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
