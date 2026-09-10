"""Build the Paper 1 manuscript from any working directory.

This is packaging/build orchestration only. It does not implement scientific
calculations. The script checks that Git LFS assets needed by the manuscript are
materialized, then compiles in the manuscript directory so relative LaTeX and
BibTeX paths are stable.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

MANUSCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = MANUSCRIPT_DIR.parents[2]
MAIN_TEX = MANUSCRIPT_DIR / "main.tex"
BIB_FILE = MANUSCRIPT_DIR / "references.bib"
FIGURE = (
    REPO_ROOT
    / "reports"
    / "methodology_report"
    / "figures"
    / "refined_longitudinal_persistence_3241.png"
)

LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message: str) -> None:
    print(f"Paper 1 build error: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_inputs() -> None:
    if not MAIN_TEX.is_file():
        fail(f"missing LaTeX source: {MAIN_TEX}")
    if not BIB_FILE.is_file():
        fail(f"missing bibliography: {BIB_FILE}")
    if not FIGURE.is_file():
        fail(
            "missing retained figure. Run `git lfs pull` from the repository "
            f"root and verify: {FIGURE}"
        )

    header = FIGURE.read_bytes()[:64]
    if header.startswith(LFS_POINTER_PREFIX):
        fail(
            "the required figure is still a Git LFS pointer, not the PNG. "
            "Run `git lfs install` once, then `git lfs pull`, and rerun this "
            "builder."
        )
    if not header.startswith(PNG_SIGNATURE):
        fail(f"required figure is not a valid PNG: {FIGURE}")


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=MANUSCRIPT_DIR, check=True)


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
