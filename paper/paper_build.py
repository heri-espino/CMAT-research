"""Dependency-aware Paper 2.1 build entry point.

Examples
--------
python paper/paper_build.py
    Compile the manuscript PDFs, generating missing figures/tables only when
    required.

python paper/paper_build.py --tables
    Force regeneration of aggregate tables only.

python paper/paper_build.py --figures
    Force regeneration of vector figures only; missing table inputs are built
    automatically.

python paper/paper_build.py --tables --figures --paper
    Full reproducible rebuild of tables, figures, and manuscript PDFs.

python paper/paper_build.py --all
    Alias for --tables --figures --paper.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from paper_build_figures import (
    FIGURE_OUTPUTS,
    REPO_ROOT,
    build_figures,
    build_tables,
    ensure_figures,
    status as dependency_status,
)

MANUSCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = MANUSCRIPT_DIR / "ima-authoring-template"
TARGETS = ("main", "main_commented")
OUTPUT_STEM = "espino_2026_beyond_first_attendance"

REQUIRED_FILES = (
    MANUSCRIPT_DIR / "main.tex",
    MANUSCRIPT_DIR / "main_commented.tex",
    MANUSCRIPT_DIR / "manuscript.tex",
    MANUSCRIPT_DIR / "references.bib",
    TEMPLATE_DIR / "ima-authoring-template.cls",
)

PDF_OUTPUTS = (
    MANUSCRIPT_DIR / "main.pdf",
    MANUSCRIPT_DIR / "main_commented.pdf",
    MANUSCRIPT_DIR / f"{OUTPUT_STEM}.pdf",
    MANUSCRIPT_DIR / f"{OUTPUT_STEM}_commented.pdf",
)


def fail(message: str) -> None:
    print(f"Paper 2.1 build error: {message}", file=sys.stderr)
    raise SystemExit(1)


def build_env() -> dict[str, str]:
    env = os.environ.copy()
    current = env.get("TEXINPUTS", "")
    env["TEXINPUTS"] = f"{TEMPLATE_DIR}//{os.pathsep}{current}"
    return env


def run_latex(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(
        command,
        cwd=MANUSCRIPT_DIR,
        check=True,
        env=build_env(),
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
        run_latex(
            [
                latexmk,
                "-g",
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"{stem}.tex",
            ]
        )
        return

    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if not pdflatex or not bibtex:
        fail("install latexmk or both pdflatex and bibtex, then rerun")

    latex = [
        pdflatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"{stem}.tex",
    ]
    run_latex(latex)
    run_latex([bibtex, stem])
    run_latex(latex)
    run_latex(latex)


def build_paper(*, auto_dependencies: bool = True) -> None:
    missing_sources = [path for path in REQUIRED_FILES if not path.is_file()]
    if missing_sources:
        fail(
            "missing manuscript source files: "
            + ", ".join(str(path.relative_to(REPO_ROOT)) for path in missing_sources)
        )

    if auto_dependencies:
        ensure_figures()
    else:
        missing_figures = [
            path
            for path in FIGURE_OUTPUTS
            if not path.is_file() or path.stat().st_size == 0
        ]
        if missing_figures:
            fail(
                "missing manuscript figures: "
                + ", ".join(
                    str(path.relative_to(REPO_ROOT)) for path in missing_figures
                )
            )

    for stem in TARGETS:
        build_target(stem)

    copies = {
        "main": f"{OUTPUT_STEM}.pdf",
        "main_commented": f"{OUTPUT_STEM}_commented.pdf",
    }
    for stem, output_name in copies.items():
        shutil.copy2(MANUSCRIPT_DIR / f"{stem}.pdf", MANUSCRIPT_DIR / output_name)

    missing_pdf = [
        path for path in PDF_OUTPUTS if not path.is_file() or path.stat().st_size == 0
    ]
    if missing_pdf:
        fail(
            "expected compiled PDFs are missing or empty: "
            + ", ".join(str(path.relative_to(REPO_ROOT)) for path in missing_pdf)
        )

    print("Paper 2.1 PDFs: built successfully.")


def print_status() -> int:
    state = dependency_status()
    for key, missing in state.items():
        print(f"{key}: {'OK' if not missing else ', '.join(missing)}")

    missing_sources = [
        str(path.relative_to(REPO_ROOT))
        for path in REQUIRED_FILES
        if not path.is_file()
    ]
    missing_pdfs = [
        str(path.relative_to(REPO_ROOT))
        for path in PDF_OUTPUTS
        if not path.is_file() or path.stat().st_size == 0
    ]
    print(f"paper_sources: {'OK' if not missing_sources else ', '.join(missing_sources)}")
    print(f"pdfs: {'OK' if not missing_pdfs else ', '.join(missing_pdfs)}")
    return 0 if not missing_sources else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Paper 2.1 tables, figures, and manuscript PDFs."
    )
    parser.add_argument(
        "--tables",
        action="store_true",
        help="Force regeneration of canonical aggregate tables.",
    )
    parser.add_argument(
        "--figures",
        action="store_true",
        help="Force regeneration of vector figures; missing tables are automatic.",
    )
    parser.add_argument(
        "--paper",
        "--pdf",
        dest="paper",
        action="store_true",
        help="Compile clean and commented manuscript PDFs.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Force a complete tables + figures + paper rebuild.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report dependency/build status without changing files.",
    )
    parser.add_argument(
        "--no-auto",
        action="store_true",
        help="Do not create missing figure/table dependencies while compiling PDFs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.check:
        return print_status()

    if args.all:
        args.tables = True
        args.figures = True
        args.paper = True

    # No flags preserves the familiar build command: compile the manuscript,
    # while generating only missing upstream artifacts.
    if not any((args.tables, args.figures, args.paper)):
        args.paper = True

    if args.tables:
        build_tables(force=True)

    if args.figures:
        build_figures(force=True, auto_tables=not args.no_auto)

    if args.paper:
        build_paper(auto_dependencies=not args.no_auto)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
