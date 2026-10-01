#!/usr/bin/env python3
"""Generate a local observation-level audit for a Paper 2.1 visit group.

Stored student/professor/classroom identifiers are replaced by document-local
labels. Generated observation-level material is written only to the ignored
paper/docs/observations/generated/ directory.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_academic_outcome_states, add_primary_outcomes
    from cmat_analysis.statistics import add_topcoded_visit_group
except ModuleNotFoundError as exc:
    raise SystemExit(
        'Install the shared library first: python -m pip install -e "./cmat_analysis[dev]"'
    ) from exc

OBS_DIR = Path(__file__).resolve().parent
PAPER_DIR = OBS_DIR.parents[1]
REPO_ROOT = PAPER_DIR.parent
DEFAULT_OUTPUT = OBS_DIR / "generated"
DEFAULT_MATERIAS = REPO_ROOT / "data" / "controlled" / "Materias_pseudonymized.csv"
DEFAULT_ASESORIAS = REPO_ROOT / "data" / "controlled" / "Asesorias_pseudonymized.csv"
PASS_MARK = 7.5
STATE_LABELS = {
    "pass": "Numeric pass",
    "numeric_nonpass": "Numeric below 7.5",
    "BV": "BV",
    "RT": "RT",
    "BA": "BA",
}
STATE_ORDER = {"numeric_nonpass": 0, "BV": 1, "RT": 2, "BA": 3, "pass": 4}


def esc(value: object) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "--"
    text = str(value)
    for old, new in {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
    }.items():
        text = text.replace(old, new)
    return text


def num(value: float | None, digits: int = 2) -> str:
    if value is None or not np.isfinite(float(value)):
        return "--"
    return f"{float(value):.{digits}f}"


def class_stats(classroom: pd.DataFrame, grade: float | None) -> dict[str, float | int]:
    numeric = pd.to_numeric(
        classroom.loc[classroom["GRADE_CLASS"].eq("numeric"), "GRADE_NUMERIC"],
        errors="coerce",
    ).dropna()
    percentile = np.nan
    if grade is not None and len(numeric):
        percentile = 100.0 * float((numeric <= grade).mean())
    return {
        "n_total": len(classroom),
        "n_numeric": len(numeric),
        "n_admin": int(classroom["GRADE_CLASS"].eq("adverse").sum()),
        "mean": numeric.mean(),
        "median": numeric.median(),
        "q25": numeric.quantile(0.25),
        "q75": numeric.quantile(0.75),
        "pass_rate": classroom["PASS"].mean(),
        "percentile": percentile,
    }


def visits_for(advisories: pd.DataFrame, row: pd.Series) -> pd.DataFrame:
    out = advisories.loc[
        advisories["STUDENT_ID"].astype(str).eq(str(row["STUDENT_ID"]))
        & advisories["YEAR"].astype("Int64").eq(int(row["YEAR"]))
        & advisories["SESSION"].astype(str).eq(str(row["SESSION"]))
    ].copy()
    return out.sort_values("VISIT_DATETIME", kind="stable")


def plot_classroom(classroom: pd.DataFrame, grade: float | None, title: str, path: Path) -> None:
    numeric = pd.to_numeric(
        classroom.loc[classroom["GRADE_CLASS"].eq("numeric"), "GRADE_NUMERIC"],
        errors="coerce",
    ).dropna().to_numpy(float)
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    counts, _, _ = ax.hist(numeric, bins=np.arange(0, 10.5, 0.5), alpha=0.55,
                           edgecolor="0.25", linewidth=0.5)
    ymax = max(float(np.max(counts)) if len(counts) else 0.0, 1.0)
    if len(numeric):
        ax.scatter(numeric, np.full_like(numeric, -0.03 * ymax), marker="|", s=70,
                   linewidths=0.8, clip_on=False)
    ax.axvline(PASS_MARK, linestyle="--", linewidth=1.0, color="0.35")
    if grade is not None:
        ax.axvline(grade, linewidth=1.4, color="0.15")
        ax.scatter([grade], [0.82 * ymax], marker="*", s=90, color="0.15", zorder=5)
    ax.set(xlim=(0, 10), ylim=(-0.08 * ymax, None), xlabel="Observed numeric MU final grade",
           ylabel="Students", title=title)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_overview(group: pd.DataFrame, path: Path, label: str) -> None:
    x = pd.to_numeric(group.loc[group["GRADE_CLASS"].eq("numeric"), "GRADE_NUMERIC"],
                      errors="coerce").dropna().sort_values().to_numpy(float)
    below = x < PASS_MARK
    fig, ax = plt.subplots(figsize=(8.0, 2.8))
    ax.scatter(x[~below], np.zeros((~below).sum()), s=35, label="numeric pass")
    ax.scatter(x[below], np.zeros(below.sum()), s=55, marker="D", label="numeric <7.5")
    ax.axvline(PASS_MARK, linestyle="--", linewidth=1.0, color="0.35")
    ax.set(xlim=(0, 10), yticks=[], xlabel="Observed numeric MU final grade",
           title=f"Exact observed numeric grades: {label} visits")
    ax.legend(frameon=False, ncol=2, loc="upper left")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def build_fragment(group: pd.DataFrame, cohort: pd.DataFrame, advisories: pd.DataFrame,
                   output: Path, label: str) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    figdir = output / "figures"
    figdir.mkdir(parents=True, exist_ok=True)

    work = group.copy()
    work["_rank"] = work["ACADEMIC_OUTCOME_STATE_5"].map(STATE_ORDER).fillna(99)
    work["_grade"] = pd.to_numeric(work["GRADE_NUMERIC"], errors="coerce").fillna(999)
    work = work.sort_values(["_rank", "PERIOD_INDEX", "CLASSROOM_ID", "_grade"], kind="stable").reset_index(drop=True)
    work["OBS"] = [f"O{i:02d}" for i in range(1, len(work) + 1)]

    instructors = {v: f"I{i:02d}" for i, v in enumerate(dict.fromkeys(work["CLAVEPROFESOR"].astype(str)), 1)}
    classrooms = {v: f"C{i:02d}" for i, v in enumerate(dict.fromkeys(work["CLASSROOM_ID"].astype(str)), 1)}

    overview = output / f"group{label}_exact_numeric_grades.pdf"
    plot_overview(work, overview, label)
    lines = [
        r"\subsection{Exact numeric grades in the selected group}",
        "The next plot shows each observed numeric grade directly, without kernel smoothing.",
        r"\begin{figure}[H]", r"\centering",
        rf"\includegraphics[width=0.92\textwidth]{{generated/{overview.name}}}",
        rf"\caption{{Exact observed numeric grades for students with {esc(label)} visits.}}",
        r"\end{figure}",
    ]

    for state in ["numeric_nonpass", "BV", "RT", "BA", "pass"]:
        subset = work.loc[work["ACADEMIC_OUTCOME_STATE_5"].eq(state)]
        if subset.empty:
            continue
        lines.append(rf"\section{{{esc(STATE_LABELS[state])} observations}}")
        for _, row in subset.iterrows():
            obs = row["OBS"]
            cid = str(row["CLASSROOM_ID"])
            clabel = classrooms[cid]
            ilabel = instructors[str(row["CLAVEPROFESOR"])]
            period = str(row["PERIOD_LABEL"])
            grade = float(row["GRADE_NUMERIC"]) if pd.notna(row["GRADE_NUMERIC"]) else None
            classroom = cohort.loc[cohort["CLASSROOM_ID"].astype(str).eq(cid)].copy()
            stats = class_stats(classroom, grade)
            visits = visits_for(advisories, row)
            plot_path = figdir / f"{obs}_classroom.pdf"
            plot_classroom(classroom, grade, f"{obs} | {clabel} | {period}", plot_path)

            visit_text = []
            for _, v in visits.iterrows():
                date = pd.Timestamp(v["VISIT_DATE"]).date().isoformat()
                subject = v.get("SUBJECT")
                visit_text.append(f"{esc(date)} ({esc(subject)})" if subject else esc(date))
            outcome = STATE_LABELS[state] + (f" (grade {grade:.2f})" if grade is not None else "")

            lines += [
                rf"\subsection{{Observation {obs}}}",
                r"\begin{description}[leftmargin=3.8cm,style=nextline]",
                rf"\item[Period] {esc(period)}",
                rf"\item[Outcome] {esc(outcome)}",
                rf"\item[Document-local context] Instructor {ilabel}; classroom {clabel}",
                rf"\item[Recorded CMAT visits] {'; '.join(visit_text) if visit_text else '--'}",
                rf"\item[Classroom composition] {stats['n_total']} students total; {stats['n_numeric']} numeric grades; {stats['n_admin']} adverse administrative outcomes.",
                rf"\item[Numeric classroom distribution] mean {num(stats['mean'])}; median {num(stats['median'])}; IQR [{num(stats['q25'])}, {num(stats['q75'])}].",
                rf"\item[Observed classroom pass share] {num(100.0 * float(stats['pass_rate']), 1)}\%.",
            ]
            if grade is not None:
                side = "below" if grade < PASS_MARK else "above"
                distance = abs(grade - PASS_MARK)
                lines.append(rf"\item[Within-classroom position] empirical percentile {num(stats['percentile'], 1)} among observed numeric grades; {num(distance, 2)} grade points {side} the pass mark.")
            lines += [
                r"\end{description}", r"\begin{figure}[H]", r"\centering",
                rf"\includegraphics[width=0.88\textwidth]{{generated/figures/{plot_path.name}}}",
                rf"\caption{{Observed numeric-grade distribution in {clabel} for observation {obs}. The dashed line marks 7.5; for numeric outcomes the star and solid line mark the focal grade.}}",
                r"\end{figure}",
            ]

    fragment = output / f"group{label}_observations.tex"
    fragment.write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    return fragment


def load_group(args: argparse.Namespace):
    base = get_study_config(REPO_ROOT)
    config = replace(base, materias_path=args.materias.expanduser().resolve(),
                     asesorias_path=args.asesorias.expanduser().resolve())
    data = load_and_clean_inputs(config)
    cohort = build_study_cohorts(data, config)["mu_primary"].copy()
    cohort = add_primary_outcomes(cohort, config)
    cohort["PASS"] = cohort["PASS"].astype(float)
    cohort = add_academic_outcome_states(cohort)
    cohort = add_topcoded_visit_group(cohort, visits_col="VISITS_CMAT_PERIOD", top_exact=5,
                                      include_zero=True, output_col="P21_GROUP_WITH_ZERO")
    group = cohort.loc[cohort["P21_GROUP_WITH_ZERO"].astype("string").eq(args.group)].copy()
    if group.empty:
        raise SystemExit(f"No Paper 2.1 observations found for group {args.group!r}.")
    return group, cohort, data.advisories.copy()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a local observation-level audit for Paper 2.1.")
    p.add_argument("--materias", type=Path, default=DEFAULT_MATERIAS)
    p.add_argument("--asesorias", type=Path, default=DEFAULT_ASESORIAS)
    p.add_argument("--group", default="5", choices=["0", "1", "2", "3", "4", "5", "6+"])
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--compile", action="store_true")
    p.add_argument("--check", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.check:
        required = [REPO_ROOT / "cmat_analysis" / "pyproject.toml", OBS_DIR / "group5_observation_audit.tex"]
        missing = [str(p.relative_to(REPO_ROOT)) for p in required if not p.is_file()]
        if missing:
            raise SystemExit("Missing observation-audit paths: " + ", ".join(missing))
        print("Paper 2.1 observation-audit recipe: OK")
        print("Generated observation-level material is local-only and ignored by Git.")
        return 0

    group, cohort, advisories = load_group(args)
    fragment = build_fragment(group, cohort, advisories, args.output_dir.expanduser().resolve(), args.group)
    counts = group["ACADEMIC_OUTCOME_STATE_5"].value_counts().reindex(
        ["pass", "numeric_nonpass", "BV", "RT", "BA"], fill_value=0)
    print(f"Paper 2.1 group {args.group}: N={len(group)}")
    print("Outcome counts: " + ", ".join(f"{k}={int(v)}" for k, v in counts.items()))
    print(f"Generated local fragment: {fragment.relative_to(REPO_ROOT)}")

    if args.compile:
        if args.group != "5":
            raise SystemExit("--compile currently targets group5_observation_audit.tex only.")
        latexmk = shutil.which("latexmk")
        if not latexmk:
            raise SystemExit("latexmk is required for --compile.")
        subprocess.run([latexmk, "-g", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                        "group5_observation_audit.tex"], cwd=OBS_DIR, check=True)
        print("Compiled local PDF: paper/docs/observations/group5_observation_audit.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
