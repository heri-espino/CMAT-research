from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VisitAnalysisSettings:
    project_root: Path
    repo_root: Path
    materias_path: Path
    asesorias_path: Path
    output_root: Path
    report_assets_dir: Path
    raw_report_figures_dir: Path
    professor_distributions_dir: Path
    logs_dir: Path


def _first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def get_settings(project_root: Path | None = None) -> VisitAnalysisSettings:
    root = project_root or Path(__file__).resolve().parents[1]
    repo_root = root
    output_root = root / "outputs"
    data_root = root / "data"
    raw_root = data_root / "raw"

    materias_path = _first_existing(
        raw_root / "Materias estudiantes-profesores 2019-2025 P y O.xlsx",
        raw_root / "Materias.xlsx",
        data_root / "Materias estudiantes-profesores 2019-2025 P y O.xlsx",
    )
    asesorias_path = _first_existing(
        raw_root / "Asesorias2024.xlsx",
        raw_root / "Asesorias.xlsx",
        data_root / "Asesorias2024.xlsx",
    )

    return VisitAnalysisSettings(
        project_root=root,
        repo_root=repo_root,
        materias_path=materias_path,
        asesorias_path=asesorias_path,
        output_root=output_root,
        report_assets_dir=output_root,
        raw_report_figures_dir=output_root / "figures",
        professor_distributions_dir=output_root / "professor_distributions",
        logs_dir=output_root / "logs",
    )
