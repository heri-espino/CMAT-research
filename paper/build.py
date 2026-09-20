"""Build the official and commented Paper 2.1 manuscripts with the IMA class."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

MANUSCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = MANUSCRIPT_DIR.parent
TEMPLATE_DIR = MANUSCRIPT_DIR / "ima-authoring-template"
FIGURE_SCRIPT = REPO_ROOT / "code" / "figures_paper21.py"
TARGETS = ("main", "main_commented")
OUTPUT_STEM = "espino_2026_beyond_first_attendance"
REQUIRED_FILES = (
    MANUSCRIPT_DIR / "main.tex",
    MANUSCRIPT_DIR / "main_commented.tex",
    MANUSCRIPT_DIR / "manuscript.tex",
    MANUSCRIPT_DIR / "references.bib",
    TEMPLATE_DIR / "ima-authoring-template.cls",
)
FIGURE_INPUTS = (
    REPO_ROOT / "results" / "paper21" / "tables" / "10b_zero_inclusive_descriptives.csv",
    REPO_ROOT / "results" / "paper21" / "tables" / "10g_zero_inclusive_stacked_ridgeline_density.csv",
    REPO_ROOT / "results" / "paper21" / "tables" / "18_primary_z_heatmap_matrix.csv",
    REPO_ROOT / "results" / "paper21" / "tables" / "19_primary_pass_heatmap_matrix.csv",
)


def fail(message: str) -> None:
    print(f"Paper 2.1 build error: {message}", file=sys.stderr)
    raise SystemExit(1)


def build_env() -> dict[str, str]:
    env = os.environ.copy()
    current = env.get("TEXINPUTS", "")
    env["TEXINPUTS"] = f"{TEMPLATE_DIR}//{os.pathsep}{current}"
    return env


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=MANUSCRIPT_DIR, check=True, env=build_env())


def regenerate_figures() -> None:
    if not FIGURE_SCRIPT.is_file():
        fail(f"missing figure recipe: {FIGURE_SCRIPT}")
    missing = [str(path.relative_to(REPO_ROOT)) for path in FIGURE_INPUTS if not path.is_file()]
    if missing:
        fail("missing aggregate Paper 2.1 figure inputs: " + ", ".join(missing))
    subprocess.run(
        [sys.executable, str(FIGURE_SCRIPT)],
        cwd=REPO_ROOT,
        check=True,
        env=os.environ.copy(),
    )


def clean_legacy_bibliography(stem: str) -> None:
    for suffix in ("aux", "bbl", "bcf", "blg", "fdb_latexmk", "fls", "run.xml"):
        path = MANUSCRIPT_DIR / f"{stem}.{suffix}"
        if path.exists():
            path.unlink()


def build_target(stem: str) -> None:
    clean_legacy_bibliography(stem)
    latexmk = shutil.which("latexmk")
    if latexmk:
        run([latexmk, "-g", "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"])
        return

    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if not pdflatex or not bibtex:
        fail("install latexmk or both pdflatex and bibtex, then rerun")
    latex = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"]
    run(latex)
    run([bibtex, stem])
    run(latex)
    run(latex)


def build() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("missing required source files: " + ", ".join(missing))

    regenerate_figures()
    for stem in TARGETS:
        build_target(stem)

    outputs = {
        "main": f"{OUTPUT_STEM}.pdf",
        "main_commented": f"{OUTPUT_STEM}_commented.pdf",
    }
    for stem, output_name in outputs.items():
        shutil.copy2(MANUSCRIPT_DIR / f"{stem}.pdf", MANUSCRIPT_DIR / output_name)


if __name__ == "__main__":
    build()
