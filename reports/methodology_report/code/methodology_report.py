"""Atomic entry point for the methodology report.

All reusable scientific and report-build functions live in the repository-level
``code/`` package. This file only locates that package and invokes the stable
methodology-report recipe.
"""

from __future__ import annotations

from pathlib import Path
import sys


REPORT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
CODE_ROOT = REPO_ROOT / "code"
SRC_ROOT = CODE_ROOT / "src"

for path in (SRC_ROOT, CODE_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from visitas_analysis.reporting.methodology_build import methodology_report_cli


if __name__ == "__main__":
    raise SystemExit(methodology_report_cli(REPO_ROOT, REPORT_DIR))
