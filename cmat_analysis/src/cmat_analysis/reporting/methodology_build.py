from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

from cmat_analysis.config.study_config import get_study_config
from cmat_analysis.reporting.methodology_report import write_methodology_table_snippets
from cmat_analysis.study.methodology_pipeline import run_methodology_pipeline


METHODOLOGY_SOURCE_FINGERPRINT = "03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f"

EXTERNAL_REFINED_SNAPSHOT_RELATIVE = (
    Path("tables/90_refined_longitudinal_persistence_summary_snapshot.csv"),
    Path("tables/latex_longitudinal_refined_3241.tex"),
    Path("figures/refined_longitudinal_persistence_3241.png"),
)


def _sha256(path: Path) -> str:
    """Return the SHA-256 digest of a controlled input file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _stage_generated_assets(
    output_dir: Path,
    report_dir: Path,
    repo_root: Path,
) -> dict[str, list[str]]:
    """Stage generated aggregate assets into the atomic report directory."""
    generated_tables = output_dir / "tables"
    generated_figures = output_dir / "figures"
    report_tables = report_dir / "tables"
    report_figures = report_dir / "figures"
    report_tables.mkdir(parents=True, exist_ok=True)
    report_figures.mkdir(parents=True, exist_ok=True)

    staged_tables: list[str] = []
    staged_figures: list[str] = []
    for src in sorted(generated_tables.glob("*.csv")):
        dst = report_tables / src.name
        shutil.copy2(src, dst)
        staged_tables.append(str(dst.relative_to(repo_root)))
    for src in sorted(generated_figures.glob("*.png")):
        dst = report_figures / src.name
        shutil.copy2(src, dst)
        staged_figures.append(str(dst.relative_to(repo_root)))

    snippets = write_methodology_table_snippets(generated_tables, report_tables)
    staged_tables.extend(str(p.relative_to(repo_root)) for p in snippets)
    return {"tables": staged_tables, "figures": staged_figures}


def _compile_report(report_dir: Path) -> Path:
    """Compile the methodology report after scientific outputs have been staged."""
    tex = report_dir / "methodology_report.tex"
    latexmk = shutil.which("latexmk")
    if latexmk:
        subprocess.run(
            [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name],
            cwd=report_dir,
            check=True,
        )
    else:
        pdflatex = shutil.which("pdflatex")
        biber = shutil.which("biber")
        if not pdflatex or not biber:
            raise RuntimeError("Compilation requires latexmk, or both pdflatex and biber.")
        subprocess.run(
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", tex.name],
            cwd=report_dir,
            check=True,
        )
        subprocess.run([biber, tex.stem], cwd=report_dir, check=True)
        subprocess.run(
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", tex.name],
            cwd=report_dir,
            check=True,
        )
        subprocess.run(
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", tex.name],
            cwd=report_dir,
            check=True,
        )

    pdf = report_dir / "methodology_report.pdf"
    if not pdf.exists():
        raise RuntimeError("LaTeX completed without creating methodology_report.pdf")
    return pdf


def _check_structure(code_root: Path, report_dir: Path) -> list[str]:
    """Validate the root-code/report boundary without loading controlled data."""
    src_root = code_root / "src"
    required = [
        code_root / "FUNCTION_INDEX.md",
        src_root / "cmat_analysis/study/methodology_pipeline.py",
        src_root / "cmat_analysis/study/extended_methodology.py",
        src_root / "cmat_analysis/study/methodology_plots.py",
        report_dir / "methodology_report.tex",
        report_dir / "referencias.bib",
    ]
    issues = [f"missing required path: {path}" for path in required if not path.exists()]
    for relpath in EXTERNAL_REFINED_SNAPSHOT_RELATIVE:
        path = report_dir / relpath
        if not path.exists():
            issues.append(f"missing external refined snapshot: {path}")
    return issues


def _parse_args(default_output_dir: Path, argv: list[str] | None) -> argparse.Namespace:
    """Parse the stable methodology-report runner interface."""
    parser = argparse.ArgumentParser(
        description="Reproduce the atomic brainstorm/methodology_report product from controlled CMAT inputs."
    )
    parser.add_argument("--materias", type=Path, help="Override academic-record input path.")
    parser.add_argument("--asesorias", type=Path, help="Override CMAT advisory-record input path.")
    parser.add_argument("--extra-covariates", type=Path, help="Optional pre-treatment covariate file.")
    parser.add_argument("--output-dir", type=Path, default=default_output_dir)
    parser.add_argument(
        "--no-stage",
        action="store_true",
        help="Generate inside the report build directory without replacing retained tables/figures.",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile methodology_report.tex after staging regenerated assets.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate report/root-code structure without loading controlled data.",
    )
    return parser.parse_args(argv)


def methodology_report_cli(
    repo_root: Path,
    report_dir: Path,
    argv: list[str] | None = None,
) -> int:
    """Run the methodology-report recipe while keeping scientific functions in root/code.

    The product-local script under ``brainstorm/methodology_report/code/`` should do
    nothing beyond locating the repository and calling this function. Scientific
    cohort, outcome, model, test, and plot definitions remain in the canonical
    ``cmat_analysis/src/cmat_analysis`` package.
    """
    repo_root = Path(repo_root).resolve()
    report_dir = Path(report_dir).resolve()
    code_root = repo_root / "cmat_analysis"
    default_output_dir = report_dir / "build"
    args = _parse_args(default_output_dir, argv)

    issues = _check_structure(code_root, report_dir)
    if issues:
        for issue in issues:
            print(f"[ERROR] {issue}", file=sys.stderr)
        return 2
    if args.check:
        print("[OK] methodology_report atomic runner structure is complete.")
        print("[OK] reusable scientific/build functions resolve from root/code.")
        print("[NOTE] Refined N=3,241 material remains an explicitly external later-stage snapshot.")
        return 0

    output_dir = args.output_dir.resolve()
    config = get_study_config(code_root)
    config = replace(config, output_dir=output_dir)
    if args.materias:
        config = replace(config, materias_path=args.materias.resolve())
    if args.asesorias:
        config = replace(config, asesorias_path=args.asesorias.resolve())
    if args.extra_covariates:
        config = replace(config, extra_covariates_path=args.extra_covariates.resolve())

    for label, path in (
        ("materias", Path(config.materias_path)),
        ("asesorias", Path(config.asesorias_path)),
    ):
        if not path.exists():
            print(f"[ERROR] controlled input {label} not found: {path}", file=sys.stderr)
            return 2

    result = run_methodology_pipeline(config)
    staged: dict[str, list[str]] = {"tables": [], "figures": []}
    if not args.no_stage:
        staged = _stage_generated_assets(Path(result["output_dir"]), report_dir, repo_root)

    manifest = {
        "runner": str((report_dir / "code/methodology_report.py").relative_to(repo_root)),
        "root_code_package": "cmat_analysis/src/cmat_analysis",
        "methodology_source_provenance_fingerprint": METHODOLOGY_SOURCE_FINGERPRINT,
        "inputs": {
            "materias": {
                "path": str(config.materias_path),
                "sha256": _sha256(Path(config.materias_path)),
            },
            "asesorias": {
                "path": str(config.asesorias_path),
                "sha256": _sha256(Path(config.asesorias_path)),
            },
            "extra_covariates": (
                {
                    "path": str(config.extra_covariates_path),
                    "sha256": _sha256(Path(config.extra_covariates_path)),
                }
                if config.extra_covariates_path is not None
                and Path(config.extra_covariates_path).exists()
                else None
            ),
        },
        "generated_output_dir": str(result["output_dir"]),
        "primary_mu_n": int(result["primary_n"]),
        "longitudinal_4211_risk_set_n": int(result["longitudinal_n"]),
        "staged": staged,
        "external_later_stage_snapshot_not_generated_here": [
            str((report_dir / relpath).relative_to(repo_root))
            for relpath in EXTERNAL_REFINED_SNAPSHOT_RELATIVE
        ],
        "report_prose_policy": (
            "CSV tables, figures and LaTeX table snippets are regenerated. "
            "Review embedded numeric prose in methodology_report.tex whenever "
            "a new data extract changes results."
        ),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "methodology_report_build_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if args.compile:
        if args.no_stage:
            print("[ERROR] --compile cannot be combined with --no-stage.", file=sys.stderr)
            return 2
        print(f"[OK] compiled: {_compile_report(report_dir)}")

    print("[OK] methodology_report scientific pipeline completed.")
    print(f"Generated working outputs: {result['output_dir']}")
    print(f"Primary MU cohort: {result['primary_n']}")
    print(f"Longitudinal 4,211-style risk set: {result['longitudinal_n']}")
    if not args.no_stage:
        print(f"Staged retained report assets: {report_dir}")
    print(f"Build manifest: {manifest_path}")
    print("[NOTE] Refined N=3,241 PPA material remains external by design.")
    return 0
