from __future__ import annotations

import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REPORT_SOURCE_DIR = PROJECT_ROOT / "reporte"
FONTS_SOURCE_DIR = PROJECT_ROOT / "fonts"
OUTPUTS_SOURCE_DIR = PROJECT_ROOT / "outputs"

LATEX_BUILD_EXTENSIONS = {
    ".aux",
    ".log",
    ".out",
    ".synctex.gz",
    ".toc",
}


def should_copy_latex_file(path: Path) -> bool:
    name = path.name.lower()
    return not any(name.endswith(ext) for ext in LATEX_BUILD_EXTENSIONS)


def copy_tree_filtered(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            copy_tree_filtered(item, target)
        elif should_copy_latex_file(item):
            shutil.copy2(item, target)


def prepare_release_latex(release_dir: Path) -> None:
    report_dir = release_dir / "reporte"
    fonts_dir = release_dir / "fonts"
    outputs_dir = release_dir / "outputs"

    if not (REPORT_SOURCE_DIR / "main.tex").exists():
        raise FileNotFoundError(f"No se encontro {REPORT_SOURCE_DIR / 'main.tex'}")
    if not FONTS_SOURCE_DIR.exists():
        raise FileNotFoundError(f"No se encontro {FONTS_SOURCE_DIR}")

    copy_tree_filtered(REPORT_SOURCE_DIR, report_dir)
    copy_tree_filtered(FONTS_SOURCE_DIR, fonts_dir)
    if OUTPUTS_SOURCE_DIR.exists():
        copy_tree_filtered(OUTPUTS_SOURCE_DIR, outputs_dir)
    else:
        outputs_dir.mkdir(parents=True, exist_ok=True)

    if not (fonts_dir / "static" / "EBGaramond-Regular.ttf").exists():
        raise FileNotFoundError("No se pudo copiar fonts/static/EBGaramond-Regular.ttf.")
    if not (outputs_dir / "figures").exists():
        raise FileNotFoundError("No se pudo crear outputs/figures.")
    if not (outputs_dir / "tex").exists():
        raise FileNotFoundError("No se pudo crear outputs/tex.")
    if not (report_dir / "main.tex").exists():
        raise FileNotFoundError("No se pudo crear reporte/main.tex.")


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python src/prepare_release_latex.py dist_release/visitas_cmat")
        return 1
    prepare_release_latex(Path(sys.argv[1]).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
