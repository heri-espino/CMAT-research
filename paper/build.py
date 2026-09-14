"""Build the Paper 4 LaTeX manuscript from any working directory.

This builder performs no scientific calculations. It compiles the manuscript from
the reviewed aggregate results already versioned in the Paper 4 branch.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

MANUSCRIPT_DIR = Path(__file__).resolve().parent
MAIN_TEX = MANUSCRIPT_DIR / "main.tex"
BIB_FILE = MANUSCRIPT_DIR / "references.bib"


def fail(message: str) -> None:
    print(f"Paper 4 build error: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=MANUSCRIPT_DIR, check=True)


def build() -> None:
    if not MAIN_TEX.is_file():
        fail(f"missing LaTeX source: {MAIN_TEX}")
    if not BIB_FILE.is_file():
        fail(f"missing bibliography: {BIB_FILE}")

    latexmk = shutil.which("latexmk")
    if latexmk:
        run([latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
        return

    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if not pdflatex or not bibtex:
        fail("install latexmk or both pdflatex and bibtex, then rerun")

    latex = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    run(latex)
    run([bibtex, "main"])
    run(latex)
    run(latex)


if __name__ == "__main__":
    build()
