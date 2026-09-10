#!/usr/bin/env python3
"""Build the Paper 2 manuscript from retained or freshly generated aggregate tables."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys


PAPER_DIR = Path(__file__).resolve().parent
REPO_ROOT = PAPER_DIR.parent
TEX = PAPER_DIR / "main.tex"
BIB = PAPER_DIR / "references.bib"
FIGURE_SCRIPT = REPO_ROOT / "code" / "figures.py"
FIGURE_SOURCE = os.environ.get("PAPER2_FIGURE_SOURCE", "retained").strip().lower()


def _run(command: list[str], *, cwd: Path = PAPER_DIR) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def _generate_figures() -> None:
    if FIGURE_SOURCE not in {"retained", "generated"}:
        raise RuntimeError(
            "PAPER2_FIGURE_SOURCE must be either 'retained' or 'generated'."
        )
    _run(
        [sys.executable, str(FIGURE_SCRIPT), "--source", FIGURE_SOURCE],
        cwd=REPO_ROOT,
    )


def _compile_latex() -> Path:
    latexmk = shutil.which("latexmk")
    if latexmk:
        _run(
            [
                latexmk,
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                TEX.name,
            ]
        )
    else:
        pdflatex = shutil.which("pdflatex")
        bibtex = shutil.which("bibtex")
        if not pdflatex or not bibtex:
            raise RuntimeError(
                "Compilation requires latexmk, or both pdflatex and bibtex."
            )
        _run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", TEX.name])
        _run([bibtex, TEX.stem])
        _run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", TEX.name])
        _run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", TEX.name])

    pdf = PAPER_DIR / "main.pdf"
    if not pdf.is_file():
        raise RuntimeError("LaTeX completed without creating paper/main.pdf")
    return pdf


def main() -> int:
    for path in (TEX, BIB, FIGURE_SCRIPT):
        if not path.is_file():
            raise FileNotFoundError(f"Required Paper 2 build input is missing: {path}")
    _generate_figures()
    pdf = _compile_latex()
    print(f"Paper 2 figure source: {FIGURE_SOURCE}")
    print(f"Compiled: {pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
