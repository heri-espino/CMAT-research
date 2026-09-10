from __future__ import annotations

import sys
import traceback
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

SRC_ROOT = Path(__file__).resolve().parent
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import pandas as pd

from cmat_analysis.analysis.report_compatible.main import run_raw_report_figures
from cmat_analysis.release_figures import report_figure_names
from cmat_analysis.reporting.run_log import write_run_log
from cmat_analysis.reporting.descriptive_pipeline import build_analytical_bundle
from cmat_analysis.reporting.metrics import (
    compute_classroom_unit_summary,
    compute_concentration_outputs,
    compute_student_summary,
    compute_student_visit_distribution,
    compute_year_summary,
)
from cmat_analysis.reporting.plots import generate_figures


VISITAS_FILE = "Asesorias2024.xlsx"
CATALOGO_FILE = "Materias estudiantes-profesores 2019-2025 P y O.xlsx"
VALID_EXCEL_EXTENSIONS = {".xlsx", ".xls"}

REQUIRED_VISITAS_COLUMNS = ("id", "fecha")
REQUIRED_CATALOGO_COLUMNS = (
    "CLAVEALUMNO",
    "CLAVEPROFESOR",
    "CLAVEVARIANTEMATERIA",
    "DESCRIBEMATERIA",
    "anio",
    "CLAVESESION",
    "CLAVECARRERA",
    "CALIFICACION",
)


class UserFacingError(Exception):
    pass


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def validate_excel_path(path: Path, relative_label: str) -> None:
    if not path.exists():
        raise UserFacingError(f"ERROR: No se encontro el archivo {relative_label}.")
    if path.suffix.lower() not in VALID_EXCEL_EXTENSIONS:
        allowed = ", ".join(sorted(VALID_EXCEL_EXTENSIONS))
        raise UserFacingError(
            f"ERROR: El archivo {relative_label} debe tener extension {allowed}."
        )


def validate_required_columns(df: pd.DataFrame, required: tuple[str, ...], file_name: str) -> None:
    for column in required:
        if column not in df.columns:
            found = ", ".join(str(col) for col in df.columns)
            raise UserFacingError(
                f"ERROR: El archivo {file_name} no contiene la columna requerida: {column}\n"
                f"Columnas encontradas: {found}"
            )


def validate_inputs(base_dir: Path) -> tuple[Path, Path, Path]:
    data_dir = base_dir / "data"
    visitas_path = data_dir / VISITAS_FILE
    catalogo_path = data_dir / CATALOGO_FILE
    figures_dir = base_dir / "outputs" / "figures"

    if not data_dir.exists():
        raise UserFacingError("ERROR: No existe la carpeta data.")

    validate_excel_path(visitas_path, f"data/{VISITAS_FILE}")
    validate_excel_path(catalogo_path, f"data/{CATALOGO_FILE}")
    figures_dir.mkdir(parents=True, exist_ok=True)

    try:
        visitas_df = pd.read_excel(visitas_path)
    except Exception as exc:
        raise UserFacingError(f"ERROR: No se pudo leer data/{VISITAS_FILE}: {exc}") from exc

    try:
        catalogo_df = pd.read_excel(catalogo_path)
    except Exception as exc:
        raise UserFacingError(f"ERROR: No se pudo leer data/{CATALOGO_FILE}: {exc}") from exc

    validate_required_columns(visitas_df, REQUIRED_VISITAS_COLUMNS, VISITAS_FILE)
    validate_required_columns(catalogo_df, REQUIRED_CATALOGO_COLUMNS, CATALOGO_FILE)
    return visitas_path, catalogo_path, figures_dir


def generate_descriptive_figures(base_dir: Path, catalogo_path: Path, visitas_path: Path, figures_dir: Path) -> list[Path]:
    bundle = build_analytical_bundle(
        project_root=base_dir,
        materias_path=catalogo_path,
        asesorias_path=visitas_path,
    )
    _, visit_tail, _, _ = compute_student_visit_distribution(bundle.student_visits)
    year_summary, _ = compute_year_summary(bundle)
    classroom_summary = compute_classroom_unit_summary(bundle)
    student_summary = compute_student_summary(bundle)
    _, lorenz_visits, _ = compute_concentration_outputs(
        bundle,
        student_summary,
        year_summary,
    )
    return generate_figures(
        student_visits=bundle.student_visits,
        visit_tail=visit_tail,
        student_year_visits=bundle.student_year_visits,
        classroom_summary=classroom_summary,
        lorenz=lorenz_visits,
        output_dir=figures_dir,
    )


def generate_all_figures(base_dir: Path, visitas_path: Path, catalogo_path: Path, figures_dir: Path) -> list[Path]:
    try:
        created = generate_descriptive_figures(base_dir, catalogo_path, visitas_path, figures_dir)
    except Exception as exc:
        raise UserFacingError(f"ERROR: No se pudieron generar las figuras descriptivas: {exc}") from exc

    try:
        run_raw_report_figures(
            materias_path=catalogo_path,
            asesorias_path=visitas_path,
            output_root=base_dir / "outputs",
            figures_dir=figures_dir,
        )
    except Exception as exc:
        raise UserFacingError(f"ERROR: No se pudieron generar las figuras del reporte: {exc}") from exc

    expected = report_figure_names()
    missing = [name for name in expected if not (figures_dir / name).exists()]
    if missing:
        missing_text = "\n".join(f"ERROR: No se pudo generar la figura {name}." for name in missing)
        raise UserFacingError(missing_text)

    created.extend(figures_dir / name for name in expected if (figures_dir / name).exists())
    generated = sorted(set(created), key=lambda path: path.name)
    write_run_log(
        logs_dir=base_dir / "outputs" / "logs",
        materias_path=catalogo_path,
        asesorias_path=visitas_path,
        mode="generador_figuras.exe",
        status="success",
        details={
            "figures_dir": str(figures_dir),
            "generated_file_count": len(generated),
            "generated_files": [path.name for path in generated],
        },
    )
    return generated


def main() -> int:
    base_dir = get_base_dir()

    try:
        visitas_path, catalogo_path, figures_dir = validate_inputs(base_dir)
        generated = generate_all_figures(base_dir, visitas_path, catalogo_path, figures_dir)
    except UserFacingError as exc:
        print(str(exc))
        return 1
    except Exception as exc:
        print(f"ERROR: Ocurrio un error inesperado: {exc}")
        traceback.print_exc()
        return 1

    print()
    print("Figuras generadas correctamente:")
    for name in report_figure_names():
        print(f"- {name}")
    print()
    print("Resumen:")
    print(f"- Ruta de {VISITAS_FILE}: {visitas_path}")
    print(f"- Ruta de {CATALOGO_FILE}: {catalogo_path}")
    print(f"- Carpeta de figuras: {figures_dir}")
    print(f"- Total de archivos creados o actualizados: {len(generated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
