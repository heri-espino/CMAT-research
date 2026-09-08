from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PROJECT_ROOT

DATA_ROOT = PROJECT_ROOT / "data"
DEFAULT_MATERIAS_PATH = DATA_ROOT / "Materias estudiantes-profesores 2019-2025 P y O.xlsx"
DEFAULT_ASESORIAS_PATH = DATA_ROOT / "Asesorias2024.xlsx"

OUTPUT_ROOT = PROJECT_ROOT / "outputs"
REPORT_ASSETS_DIR = OUTPUT_ROOT
RAW_REPORT_FIGURES_DIR = OUTPUT_ROOT / "figures"
PROFESSOR_DISTRIBUTIONS_DIR = OUTPUT_ROOT / "professor_distributions"
LEGACY_FIGURES_DIR = OUTPUT_ROOT / "legacy_figures"
LOGS_DIR = OUTPUT_ROOT / "logs"
