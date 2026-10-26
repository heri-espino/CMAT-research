#!/usr/bin/env python3
"""Generate and optionally publish ALL outstanding CMAT Paper 2.1 follow-up outputs.

Runs the original follow-up analysis and the new curve analysis against the
same authorized local institutional inputs. The inputs are NEVER copied into
the repository; only expected aggregate reports, tables, and figures are
exported. Historical Holm, EM and Shapley outputs already live in Git history.

Usage from the separate research-branch checkout on the Windows VM:
  python scripts/generate_all_results.py --source "C:\\Users\\175199\\CMAT-research" --publish

If data have moved:
  python scripts/generate_all_results.py --source "..." --materias "..." --asesorias "..." --publish
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parents[1]
FOLLOWUP_FILES = (
    "notes/22_FOLLOWUP_QUESTIONS_RESULTS.md",
    "results/paper21/tables/followup_questions/degree_professor_period_overlap.csv",
    "results/paper21/tables/followup_questions/two_part_attendance_z_pass.csv",
    "results/paper21/tables/followup_questions/observed_numeric_grade_quantiles.csv",
    "results/paper21/tables/followup_questions/numeric_vs_administrative_composition.csv",
)
CURVE_FILES = (
    "notes/24_ATTENDANCE_CURVE_RESULTS.md",
    "results/paper21/tables/attendance_curves/unadjusted_means_cluster_ci.csv",
    "results/paper21/tables/attendance_curves/model_comparison_in_sample.csv",
    "results/paper21/tables/attendance_curves/adjusted_curves_cluster_ci.csv",
    "results/paper21/tables/attendance_curves/adjacent_differences_holm.csv",
    "results/paper21/tables/attendance_curves/group_heldout_shape_cv.csv",
    "results/paper21/figures/attendance_curves/imputed_z_attendance_curve.png",
    "results/paper21/figures/attendance_curves/pass_lpm_attendance_curve.png",
    "results/paper21/figures/attendance_curves/numeric_only_z_attendance_curve.png",
    "results/paper21/figures/attendance_curves/observed_numeric_grade_attendance_curve.png",
)
ALL_FILES = FOLLOWUP_FILES + CURVE_FILES

INPUT_NAMES = {
    "materias": (
        "Materias estudiantes-profesores 2019-2025 P y O.xlsx",
        "Materias.xlsx",
        "Materias_pseudonymized.csv",
        "Materias_anonymized.csv",
    ),
    "asesorias": (
        "Asesorias2024.xlsx",
        "Asesorias.xlsx",
        "Asesorias_pseudonymized.csv",
        "Asesorias_anonymized.csv",
    ),
}
SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules",
    "AppData", "miniconda3", "anaconda3", "site-packages", ".cache",
    "Library", "Temporary Internet Files", "Program Files",
}


def find_inputs(search_roots: list[Path]) -> dict[str, list[Path]]:
    """Find config-supported filenames without opening institutional records.

    Prevent following symlinked directories and skip application environments.
    Search roots are limited to the user's existing project/home paths.
    """
    found: dict[str, list[Path]] = {"materias": [], "asesorias": []}
    target = {
        k: {name.casefold() for name in names}
        for k, names in INPUT_NAMES.items()
    }
    seen: set[str] = set()
    for root in search_roots:
        if not root.is_dir():
            continue
        for current, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = [
                d for d in dirs
                if d not in SKIP_DIRS and not d.startswith(".")
            ]
            for name in files:
                key = name.casefold()
                if not any(key in choices for choices in target.values()):
                    continue
                path = Path(current) / name
                real = str(path.resolve()).casefold()
                if real in seen:
                    continue
                seen.add(real)
                for kind, names in target.items():
                    if key in names:
                        found[kind].append(path.resolve())
    return found


def discover_pair(source: Path, search_root: Path | None) -> tuple[Path, Path]:
    roots = [source, source.parent]
    if search_root is not None:
        roots.append(search_root)
    # Deduplicate and prefer source-local data before other locations.
    roots = list(dict.fromkeys(p.resolve() for p in roots))
    found = find_inputs(roots)
    if not found["materias"] or not found["asesorias"]:
        raise SystemExit(
            "Cannot generate new institutional estimates: the academic/CMAT "
            "input files were not found in the original project or nearby "
            "workspace. No results were fabricated or pushed. Restore the "
            "authorized source files locally or pass --materias and --asesorias "
            "with their full file paths."
        )

    def priority(p: Path, kind: str) -> tuple[int, int, int, str]:
        # Prioritize the original checkout, preferred config names, and raw
        # before controlled inputs; break ties deterministically by path.
        p_string = str(p).casefold()
        local = int(source.resolve() == p or source.resolve() in p.parents)
        lower_names = [v.casefold() for v in INPUT_NAMES[kind]]
        named = lower_names.index(p.name.casefold())
        raw = int(any(part.casefold() == "raw" for part in p.parts))
        return (-local, named, -raw, p_string)

    academic = sorted(found["materias"], key=lambda p: priority(p, "materias"))
    advice = sorted(found["asesorias"], key=lambda p: priority(p, "asesorias"))
    # Prefer paired files in the same folder; the cohort guard in both
    # official runners rejects wrong-population matches before publication.
    for m in academic:
        matching = [a for a in advice if a.parent == m.parent]
        if matching:
            return m, matching[0]
    return academic[0], advice[0]


def execute(*args: str, cwd: Path = REPO) -> None:
    print("\nRUN:", " ".join(args[:3]), flush=True)
    result = subprocess.run(list(args), cwd=cwd, check=False)
    if result.returncode != 0:
        raise SystemExit(f"Stopped: command failed with exit code {result.returncode}. "
                         "No publication was initiated.")


def validate_outputs() -> None:
    missing = [str(p) for p in ALL_FILES if not (REPO / p).is_file()]
    if missing:
        raise SystemExit("Required analysis outputs are missing; nothing pushed:\n"
                         + "\n".join(missing))
    # Privacy gate: expected schema and no suspicious row-level identifiers.
    import pandas as pd

    for path in ALL_FILES:
        filename = REPO / path
        if filename.stat().st_size == 0:
            raise SystemExit(f"Empty result file: {path}. No push.")
        if path.endswith(".csv"):
            df = pd.read_csv(filename, nrows=100)
            prohibited = {"student_id", "matricula", "nomina", "student_name",
                          "clavematricula", "source_row", "clavaprofesor",
                          "claveprofesor", "email", "correo", "classroom_id"}
            exposed = prohibited.intersection(c.casefold() for c in df.columns)
            if exposed:
                raise SystemExit(f"Unsafe output column(s) in {path}: {sorted(exposed)}")
    print("\nSUCCESS: verified all 15 expected aggregate outputs.", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path,
                        help="Original CMAT-research folder (left unchanged).")
    parser.add_argument("--search-root", type=Path,
                        help="Optional other local directory to search for inputs.")
    parser.add_argument("--materias", type=Path,
                        help="Explicit path to authorized academic input.")
    parser.add_argument("--asesorias", type=Path,
                        help="Explicit path to authorized CMAT input.")
    parser.add_argument("--publish", action="store_true",
                        help="After successful tests/output verification, invoke guarded Git publisher.")
    parser.add_argument("--no-historical-figures", action="store_true",
                        help="Do not reimport the 16 historical PNGs.")
    args = parser.parse_args()
    original = args.source.expanduser().resolve()
    if not original.is_dir():
        parser.error(f"Original repository folder not found: {original}")
    if original == REPO:
        parser.error("Use the separate publication clone, not the original repository.")
    if bool(args.materias) != bool(args.asesorias):
        parser.error("Specify both --materias and --asesorias, or neither.")
    if args.materias:
        materias = args.materias.expanduser().resolve()
        asesorias = args.asesorias.expanduser().resolve()
    else:
        materias, asesorias = discover_pair(original, args.search_root)

    for file in (materias, asesorias):
        if not file.is_file():
            parser.error(f"Input not found: {file}")
    # Install this checkout's local analysis library without downloading raw data
    # or resolving dependencies from the network. The Conda environment already
    # contains the pinned scientific Python dependencies.
    execute(sys.executable, "-m", "pip", "install", "--no-deps",
            "-e", "./cmat_analysis")

    print("Found authorized candidate inputs locally; source files remain private.")
    print("Analyses must pass the established N=6,627 / 190-context cohort checks.")

    execute(sys.executable, "-m", "pytest", "-q",
            "cmat_analysis/tests/test_paper21_followup_questions.py",
            "cmat_analysis/tests/test_paper21_attendance_curves.py",
            "cmat_analysis/tests/test_generate_all_results.py")
    execute(sys.executable, "code/run_paper21_followup_questions.py", "--check")
    execute(sys.executable, "code/run_paper21_attendance_curves.py", "--check")

    for script in ("code/run_paper21_followup_questions.py",
                   "code/run_paper21_attendance_curves.py"):
        execute(sys.executable, script, "--materias", str(materias),
                "--asesorias", str(asesorias))

    validate_outputs()
    if args.publish:
        powershell = "powershell.exe" if os.name == "nt" else "pwsh"
        arguments = [powershell, "-NoProfile", "-File",
                     str(REPO / "scripts/publish_cmat_results.ps1"),
                     "-Source", str(original), "-Publish"]
        if not args.no_historical_figures:
            arguments.append("-IncludeHistoricalFigures")
        execute(*arguments)
    else:
        print("Outputs generated locally. Pass --publish for the GitHub publication step.")


if __name__ == "__main__":
    main()
