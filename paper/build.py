from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


PAPER_DIR = Path(__file__).resolve().parent
MAIN = PAPER_DIR / "main.tex"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=PAPER_DIR, check=True)


def main() -> int:
    if not MAIN.exists():
        raise SystemExit(f"Missing manuscript: {MAIN}")

    if shutil.which("latexmk"):
        run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", MAIN.name])
    elif shutil.which("pdflatex") and shutil.which("bibtex"):
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", MAIN.name])
        run(["bibtex", MAIN.stem])
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", MAIN.name])
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", MAIN.name])
    else:
        raise SystemExit("Paper 3 requires latexmk or pdflatex + bibtex.")

    pdf = PAPER_DIR / "main.pdf"
    if not pdf.exists():
        raise SystemExit("LaTeX completed without producing main.pdf")
    print(f"Compiled: {pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
