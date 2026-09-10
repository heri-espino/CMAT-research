"""Build the Paper 1 manuscript from any working directory.

The builder generates the paper-owned figures from reviewed aggregate tables
before compiling LaTeX. Direct builds use the retained aggregate snapshot;
``code/run_paper.py --compile`` selects freshly generated aggregate tables after
an empirical run. No scientific calculations are implemented here.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

MANUSCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = MANUSCRIPT_DIR.parent
MAIN_TEX = MANUSCRIPT_DIR / "main.tex"
BIB_FILE = MANUSCRIPT_DIR / "references.bib"
FIGURES_DIR = REPO_ROOT / "results" / "figures"
FIGURE_FILES = (
    "figure_01_cohort_flow.png",
    "figure_02_main_persistence.png",
    "figure_03_threshold_piecewise.png",
    "figure_04_adjusted_persistence_or.png",
)

LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message: str) -> None:
    print(f"Paper 1 build error: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(command: list[str], *, cwd: Path = MANUSCRIPT_DIR) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def generate_figures() -> None:
    source = os.environ.get("PAPER1_FIGURE_SOURCE", "retained")
    if source not in {"retained", "generated", "auto"}:
        fail(
            "PAPER1_FIGURE_SOURCE must be one of retained, generated, or auto; "
            f"received {source!r}."
        )
    run(
        [sys.executable, str(REPO_ROOT / "code" / "figures.py"), "--source", source],
        cwd=REPO_ROOT,
    )


def check_inputs() -> None:
    if not MAIN_TEX.is_file():
        fail(f"missing LaTeX source: {MAIN_TEX}")
    if not BIB_FILE.is_file():
        fail(f"missing bibliography: {BIB_FILE}")

    generate_figures()
    for filename in FIGURE_FILES:
        figure = FIGURES_DIR / filename
        if not figure.is_file():
            fail(f"missing generated Paper 1 figure: {figure}")
        header = figure.read_bytes()[:64]
        if header.startswith(LFS_POINTER_PREFIX):
            fail(
                "generated figure path is an unresolved Git LFS pointer: "
                f"{figure}"
            )
        if not header.startswith(PNG_SIGNATURE):
            fail(f"generated figure is not a valid PNG: {figure}")


def build() -> None:
    check_inputs()

    latexmk = shutil.which("latexmk")
    if latexmk:
        run([latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
        return

    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if not pdflatex or not bibtex:
        fail(
            "no usable LaTeX toolchain found. Install latexmk (recommended) "
            "or both pdflatex and bibtex, then rerun."
        )

    latex = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    run(latex)
    run([bibtex, "main"])
    run(latex)
    run(latex)


if __name__ == "__main__":
    build()
