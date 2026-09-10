from __future__ import annotations

from pathlib import Path
from typing import Any

from cmat_analysis.reporting.report_assets import generate_report_assets
from cmat_analysis.reporting.run_log import write_run_log


def run_visitas_pipeline(
    settings: Any,
    *,
    include_report_assets: bool = True,
    include_raw_figures: bool = True,
) -> dict[str, object]:
    """Regenerate project outputs from the canonical raw Excel inputs."""
    artifacts: dict[str, object] = {}

    Path(settings.output_root).mkdir(parents=True, exist_ok=True)
    Path(settings.logs_dir).mkdir(parents=True, exist_ok=True)

    if include_report_assets:
        artifacts["report_assets"] = generate_report_assets(
            project_root=Path(settings.project_root),
            materias_path=Path(settings.materias_path),
            asesorias_path=Path(settings.asesorias_path),
            output_dir=Path(settings.report_assets_dir),
        )

    if include_raw_figures:
        from cmat_analysis.analysis.report_compatible.main import run_raw_report_figures

        artifacts["raw_figures"] = run_raw_report_figures(
            materias_path=Path(settings.materias_path),
            asesorias_path=Path(settings.asesorias_path),
            output_root=Path(settings.output_root),
        )

    artifacts["run_log"] = write_run_log(
        logs_dir=Path(settings.logs_dir),
        materias_path=Path(settings.materias_path),
        asesorias_path=Path(settings.asesorias_path),
        mode="run_analysis",
        status="success",
        details={
            "include_report_assets": include_report_assets,
            "include_raw_figures": include_raw_figures,
        },
    )
    return artifacts
