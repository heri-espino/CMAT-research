from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import pandas as pd

SRC_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SRC_ROOT.parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from cmat_analysis.privacy import canonical_identifier, hmac_pseudonym


MATERIAS_FILENAME = "Materias estudiantes-profesores 2019-2025 P y O.xlsx"
ASESORIAS_FILENAME = "Asesorias2024.xlsx"
RELEASE_MATERIAS_FILENAME = "Materias_pseudonymized.csv"
RELEASE_ASESORIAS_FILENAME = "Asesorias_pseudonymized.csv"


def _load_key(args: argparse.Namespace) -> bytes:
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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def _source_paths(repo_root: Path) -> tuple[Path, Path]:
    data = repo_root / "data"
    raw = data / "raw"
    materias = _first_existing(
        raw / MATERIAS_FILENAME,
        raw / "Materias.xlsx",
        data / MATERIAS_FILENAME,
    )
    asesorias = _first_existing(
        raw / ASESORIAS_FILENAME,
        raw / "Asesorias.xlsx",
        data / ASESORIAS_FILENAME,
    )
    return materias, asesorias


def _make_pseudonymized_data(
    repo_root: Path,
    destination: Path,
    key: bytes,
) -> dict[str, object]:
    raw_m, raw_a = _source_paths(repo_root)
    missing = [path for path in (raw_m, raw_a) if not path.is_file()]
    if missing:
        formatted = "\n".join(f"  - {path}" for path in missing)
        raise SystemExit(
            "Raw XLSX inputs were not found. Expected controlled local files under "
            f"data/raw/:\n{formatted}"
        )

    materias_raw = pd.read_excel(raw_m)
    asesorias_raw = pd.read_excel(raw_a)
    materias = materias_raw.copy()
    asesorias = asesorias_raw.drop_duplicates().reset_index(drop=True).copy()

    required_materias = {"CLAVEALUMNO", "CLAVEPROFESOR"}
    required_asesorias = {"fecha", "id", "profesor"}
    missing_m = required_materias - set(materias.columns)
    missing_a = required_asesorias - set(asesorias.columns)
    if missing_m or missing_a:
        raise SystemExit(
            "Unexpected source schema. "
            f"Missing Materias columns={sorted(missing_m)}; "
            f"missing Asesorias columns={sorted(missing_a)}"
        )

    materias["CLAVEALUMNO"] = materias["CLAVEALUMNO"].map(
        lambda value: hmac_pseudonym(value, key, "stu") if pd.notna(value) else None
    )
    materias["CLAVEPROFESOR"] = materias["CLAVEPROFESOR"].map(
        lambda value: hmac_pseudonym(value, key, "prof") if pd.notna(value) else None
    )

    original_visit_student = asesorias["id"].copy()
    original_visit_timestamp = asesorias["fecha"].copy()
    asesorias["id"] = asesorias["id"].map(
        lambda value: hmac_pseudonym(value, key, "stu") if pd.notna(value) else None
    )
    # The advisory source stores professor names, whereas Materias stores numeric
    # CLAVEPROFESOR values. Until a verified crosswalk exists, use a distinct
    # namespace so the release does not assert a false professor linkage.
    asesorias["profesor"] = asesorias["profesor"].map(
        lambda value: hmac_pseudonym(value, key, "advisor") if pd.notna(value) else None
    )
    asesorias["_VISIT_UID"] = [
        hmac_pseudonym(
            f"{position}|{timestamp}|{student}",
            key,
            "visit",
        )
        for position, (timestamp, student) in enumerate(
            zip(original_visit_timestamp, original_visit_student, strict=False)
        )
    ]

    # Retain the exact supplied timestamp, including clock time, because timing
    # is an explicit research variable. ISO-8601 gives a stable text encoding.
    visit_dt = pd.to_datetime(asesorias["fecha"], errors="coerce")
    asesorias["fecha"] = visit_dt.map(
        lambda value: value.isoformat() if pd.notna(value) else None
    )

    destination.mkdir(parents=True, exist_ok=True)
    materias_out = destination / RELEASE_MATERIAS_FILENAME
    asesorias_out = destination / RELEASE_ASESORIAS_FILENAME
    materias.to_csv(materias_out, index=False)
    asesorias.to_csv(asesorias_out, index=False)

    raw_students_m = {
        canonical_identifier(value) for value in materias_raw["CLAVEALUMNO"].dropna()
    }
    raw_students_a = {
        canonical_identifier(value) for value in asesorias_raw["id"].dropna()
    }
    pseudo_students_m = set(materias["CLAVEALUMNO"].dropna())
    pseudo_students_a = set(asesorias["id"].dropna())

    validation = {
        "academic_rows": int(len(materias)),
        "advisory_rows_raw": int(len(asesorias_raw)),
        "advisory_exact_duplicates_removed": int(asesorias_raw.duplicated().sum()),
        "advisory_rows_release": int(len(asesorias)),
        "student_overlap_raw": int(len(raw_students_m & raw_students_a)),
        "student_overlap_pseudonymized": int(
            len(pseudo_students_m & pseudo_students_a)
        ),
        "student_linkage_preserved": bool(
            len(raw_students_m & raw_students_a)
            == len(pseudo_students_m & pseudo_students_a)
        ),
        "advisor_names_pseudonymized": int(asesorias["profesor"].nunique(dropna=True)),
        "exact_timestamp_nonmissing": int(asesorias["fecha"].notna().sum()),
    }

    return {
        "release_created_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "method": "HMAC-SHA256 pseudonymization with research fields retained",
        "student_linkage": "Same stu_* pseudonym in Materias and Asesorias",
        "academic_professor_linkage": "CLAVEPROFESOR pseudonymized as prof_*",
        "advisory_professor_linkage": (
            "Asesorias.profesor contains professor names while Materias contains numeric "
            "CLAVEPROFESOR. It is pseudonymized as advisor_* and is not asserted to "
            "equal prof_* without a verified name-to-ID crosswalk."
        ),
        "fields_retained_in_asesorias": [*asesorias_raw.columns, "_VISIT_UID"],
        "timestamp_policy": (
            "Exact supplied timestamp retained in ISO-8601 form, including clock time."
        ),
        "fields_removed_from_asesorias": [],
        "secret_key_in_release": False,
        "source_sha256": {
            raw_m.name: _sha256(raw_m),
            raw_a.name: _sha256(raw_a),
        },
        "release_component_sha256": {
            materias_out.name: _sha256(materias_out),
            asesorias_out.name: _sha256(asesorias_out),
        },
        "validation": validation,
    }


def _privacy_text() -> str:
    return """# Privacy / pseudonymization

This controlled research release preserves the substantive advisory variables required for analysis, including exact timestamp, carrera, semestre, profesor, materia, tema, and periodo.

Original student identifiers are replaced by deterministic `stu_*` HMAC-SHA256 pseudonyms that are identical across Materias and Asesorias. Academic `CLAVEPROFESOR` values are replaced by deterministic `prof_*` pseudonyms. Advisory professor names are represented by deterministic `advisor_*` pseudonyms because no verified name-to-ID crosswalk is currently available.

No substantive advisory fields are removed, and the exact supplied timestamp is retained.

This is pseudonymization, not anonymization. Timestamp, career, semester, course, topic, grade, and longitudinal patterns can remain quasi-identifiers. The release may be stored in the CMAT repository only while the repository remains private and access is limited to authorized collaborators. The HMAC key and raw institutional workbooks must remain outside Git.
"""


def _write_release_files(
    release_dir: Path,
    manifest: dict[str, object],
) -> None:
    privacy = release_dir / "PRIVACY_README.md"
    manifest_path = release_dir / "PSEUDONYMIZATION_MANIFEST.json"
    privacy.write_text(_privacy_text(), encoding="utf-8")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    component_paths = [
        release_dir / RELEASE_MATERIAS_FILENAME,
        release_dir / RELEASE_ASESORIAS_FILENAME,
        manifest_path,
        privacy,
    ]
    checksums = release_dir / "SHA256SUMS.txt"
    checksums.write_text(
        "".join(f"{_sha256(path)}  {path.name}\n" for path in component_paths),
        encoding="utf-8",
    )


def create_release(
    repo_root: Path,
    output_zip: Path,
    key: bytes,
    *,
    install_controlled: bool = False,
) -> Path:
    with tempfile.TemporaryDirectory(prefix="cmat_release_") as tmp_name:
        release_dir = Path(tmp_name) / "CMAT_pseudonymized_release_full_fields"
        manifest = _make_pseudonymized_data(repo_root, release_dir, key)
        _write_release_files(release_dir, manifest)

        output_zip.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(release_dir.iterdir()):
                if path.is_file():
                    archive.write(path, arcname=path.name)

        if install_controlled:
            controlled = repo_root / "data" / "controlled"
            controlled.mkdir(parents=True, exist_ok=True)
            for path in release_dir.iterdir():
                if path.is_file():
                    shutil.copy2(path, controlled / path.name)

    return output_zip


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create the controlled full-fields pseudonymized CMAT release."
    )
    parser.add_argument(
        "--key-file",
        type=Path,
        help="Text file containing the secret pseudonymization key.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "CMAT_pseudonymized_release_full_fields.zip",
    )
    parser.add_argument(
        "--install-controlled",
        action="store_true",
        help=(
            "Also copy the pseudonymized CSVs and release metadata into "
            "data/controlled/ for private-repository analysis."
        ),
    )
    args = parser.parse_args()
    key = _load_key(args)
    output = create_release(
        REPO_ROOT,
        args.output.resolve(),
        key,
        install_controlled=args.install_controlled,
    )
    print(f"[OK] Pseudonymized release: {output}")
    print(f"SHA-256: {_sha256(output)}")
    if args.install_controlled:
        print(f"[OK] Installed controlled data: {REPO_ROOT / 'data' / 'controlled'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
