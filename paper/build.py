"""Build the official and commented Paper 4 LaTeX manuscripts.

This builder performs no scientific calculations. ``main.tex`` is the official
clean wrapper and ``main_commented.tex`` exposes development TODO annotations;
both include the single shared source ``manuscript.tex``.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

MANUSCRIPT_DIR = Path(__file__).resolve().parent
TARGETS = ("main", "main_commented")
REQUIRED_FILES = (
    MANUSCRIPT_DIR / "main.tex",
    MANUSCRIPT_DIR / "main_commented.tex",
    MANUSCRIPT_DIR / "manuscript.tex",
    MANUSCRIPT_DIR / "references.bib",
)


def fail(message: str) -> None:
    print(f"Paper 4 build error: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=MANUSCRIPT_DIR, check=True)


def build_target(stem: str) -> None:
    latexmk = shutil.which("latexmk")
    if latexmk:
        run([latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"])
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
    for stem in TARGETS:
        build_target(stem)


if __name__ == "__main__":
    build()
