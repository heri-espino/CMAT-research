"""Thin entry point for the methodology brainstorm."""
from pathlib import Path
from cmat_analysis.reporting.methodology_build import methodology_report_cli

REPORT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]

if __name__ == "__main__":
    raise SystemExit(methodology_report_cli(REPO_ROOT, REPORT_DIR))
