from __future__ import annotations

import argparse
import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import pandas as pd

SRC_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_ROOT.parent
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from visitas_analysis.privacy import hmac_pseudonym


def _load_key(args) -> bytes:
    if args.key_file:
        text = Path(args.key_file).read_text(encoding="utf-8").strip()
    else:
        text = os.environ.get("CMAT_PSEUDONYM_KEY", "").strip()
    if not text:
        raise SystemExit(
            "No pseudonym key supplied. Set CMAT_PSEUDONYM_KEY or use --key-file. "
            "Generate a key with: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    if len(text) < 32:
        raise SystemExit("Pseudonym key is too short; use at least 32 characters.")
    return text.encode("utf-8")


def _term_anchor(year: int, period: str) -> str:
    p = str(period).strip().upper()
    month = {"P": 1, "PRIMAVERA": 1, "V": 5, "VERANO": 5, "O": 9, "OTOÑO": 9, "OTONO": 9}.get(p, 1)
    return f"{int(year):04d}-{month:02d}-01"


def _make_anonymized_data(project: Path, destination: Path, key: bytes) -> dict:
    raw_a = project / "data" / "Asesorias2024.xlsx"
    raw_m = project / "data" / "Materias estudiantes-profesores 2019-2025 P y O.xlsx"
    if not raw_a.exists() or not raw_m.exists():
        raise SystemExit("Raw XLSX inputs were not found in data/. Run this from the internal project.")

    materias = pd.read_excel(raw_m).copy()
    asesorias = pd.read_excel(raw_a).copy()

    # Exact duplicate advisory rows are removed before coarsening dates so that
    # genuine distinct visits remain distinct but duplicated source rows do not.
    asesorias = asesorias.drop_duplicates().reset_index(drop=True)

    materias["CLAVEALUMNO"] = materias["CLAVEALUMNO"].map(
        lambda x: hmac_pseudonym(x, key, "stu") if pd.notna(x) else None
    )
    materias["CLAVEPROFESOR"] = materias["CLAVEPROFESOR"].map(
        lambda x: hmac_pseudonym(x, key, "prof") if pd.notna(x) else None
    )

    # Keep only fields needed by the redesigned study. This is data minimization,
    # not merely identifier hashing.
    academic_cols = [
        "CLAVEALUMNO", "CLAVECARRERA", "anio", "CLAVESESION", "NUMORDEN",
        "CLAVEVARIANTEMATERIA", "DESCRIBEMATERIA", "CALIFICACION", "CLAVEPROFESOR",
    ]
    materias = materias[academic_cols]

    visit_dt = pd.to_datetime(asesorias["fecha"], errors="coerce")
    asesorias["id"] = asesorias["id"].map(
        lambda x: hmac_pseudonym(x, key, "stu") if pd.notna(x) else None
    )
    # Preserve calendar DAY because the redesigned study now examines same-day
    # PPA completion and recurring temporal peaks. Exact clock time is removed
    # from the shareable release; a keyed visit-event pseudonym keeps multiple
    # legitimate visits on the same day distinct.
    asesorias["_VISIT_UID"] = [
        hmac_pseudonym(f"{i}|{row.get('fecha')}|{row.get('id')}", key, "visit")
        for i, (_, row) in enumerate(asesorias.iterrows())
    ]
    asesorias["fecha"] = visit_dt.dt.normalize().dt.strftime("%Y-%m-%d")
    advisory_cols = ["fecha", "id", "materia", "periodo", "_VISIT_UID"]
    asesorias = asesorias[advisory_cols]

    destination.mkdir(parents=True, exist_ok=True)
    materias.to_csv(destination / "Materias_anonymized.csv", index=False)
    asesorias.to_csv(destination / "Asesorias_anonymized.csv", index=False)

    return {
        "academic_rows": int(len(materias)),
        "advisory_rows_after_exact_deduplication": int(len(asesorias)),
        "student_identifier": "HMAC-SHA256 keyed pseudonym (namespace stu)",
        "academic_professor_identifier": "HMAC-SHA256 keyed pseudonym (namespace prof)",
        "visit_event_identifier": "HMAC-SHA256 keyed pseudonym (namespace visit)",
        "advisory_timestamp": "coarsened to calendar day (YYYY-MM-DD); exact clock time removed",
        "dropped_advisory_fields": ["carrera", "semestre", "profesor", "tema"],
        "secret_key_in_release": False,
    }


def _copy_public_code(project: Path, release_root: Path) -> None:
    excluded = {
        "data", "reporte", "legacy", "outputs", "release_anonymized",
        "manual", "scripts", "__pycache__", ".pytest_cache", ".git",
    }
    for item in project.iterdir():
        if item.name in excluded:
            continue
        target = release_root / item.name
        if item.is_dir():
            shutil.copytree(item, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(item, target)


def create_release(project: Path, output_zip: Path, key: bytes) -> Path:
    with tempfile.TemporaryDirectory(prefix="cmat_release_") as tmp:
        tmp = Path(tmp)
        release_root = tmp / "CMAT_publication_study_anonymized"
        release_root.mkdir()
        _copy_public_code(project, release_root)
        manifest = _make_anonymized_data(project, release_root / "data", key)
        privacy_text = (
            "# Privacy / pseudonymization\n\n"
            "This release contains no original student IDs or professor IDs. Direct identifiers are replaced with deterministic keyed HMAC-SHA256 pseudonyms, and the secret key is deliberately not included. Advisory timestamps are coarsened to calendar day (the day is retained for the temporal analyses), while clock time and unused free-text/person fields are removed.\n\n"
            "Important: this is **pseudonymization**, not a guarantee of full anonymity. Course, period, career, grade and rare attendance patterns can still act as quasi-identifiers. Any public data release should therefore receive institutional privacy/ethics review, apply cell-size/disclosure controls if required, and never include the HMAC key or the original data.\n"
        )
        (release_root / "PRIVACY_README.md").write_text(privacy_text, encoding="utf-8")
        (release_root / "PSEUDONYMIZATION_MANIFEST.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        # Verify that the public project runs from the anonymized CSVs and
        # regenerate aggregate outputs from those pseudonymized inputs.
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{release_root / 'src'}:{release_root}"
        subprocess.run(
            [sys.executable, str(release_root / "src" / "run_study.py")],
            cwd=release_root, env=env, check=True,
        )

        output_zip.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in release_root.rglob("*"):
                if path.is_file():
                    zf.write(path, path.relative_to(release_root.parent))
    return output_zip


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a pseudonymized CMAT release ZIP.")
    ap.add_argument("--key-file", type=Path, help="Text file containing a secret pseudonymization key.")
    ap.add_argument("--output", type=Path, default=PROJECT_ROOT.parent / "CMAT_publication_study_anonymized.zip")
    args = ap.parse_args()
    key = _load_key(args)
    out = create_release(PROJECT_ROOT, args.output, key)
    print(f"[OK] Anonymized/pseudonymized release: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
