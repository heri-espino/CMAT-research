"""Synthetic-only checks for local source discovery and complete-output contract."""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_all_results import (
    ALL_FILES, CURVE_FILES, FOLLOWUP_FILES, discover_pair, find_inputs,
)


def test_complete_output_contract_has_15_distinct_aggregate_paths():
    assert len(ALL_FILES) == 15
    assert len(FOLLOWUP_FILES) == 5
    assert len(CURVE_FILES) == 10
    assert len(set(ALL_FILES)) == 15
    assert all(p.endswith((".csv", ".png", ".md")) for p in ALL_FILES)
    assert not any("controlled" in p or "data/raw" in p for p in ALL_FILES)


def test_discovers_pair_from_original_config_layout(tmp_path):
    old = tmp_path / "CMAT-research"
    raw = old / "data" / "raw"
    raw.mkdir(parents=True)
    academic = raw / "Materias.xlsx"
    advisory = raw / "Asesorias.xlsx"
    academic.write_bytes(b"synthetic test input")
    advisory.write_bytes(b"synthetic test input")
    assert discover_pair(old, None) == (academic.resolve(), advisory.resolve())


def test_finds_canonical_names_in_nearby_local_folder(tmp_path):
    old = tmp_path / "CMAT-research"
    old.mkdir()
    other = tmp_path / "working-copy" / "data" / "raw"
    other.mkdir(parents=True)
    a = other / "Materias estudiantes-profesores 2019-2025 P y O.xlsx"
    b = other / "Asesorias2024.xlsx"
    a.write_bytes(b"test")
    b.write_bytes(b"test")
    assert discover_pair(old, None) == (a.resolve(), b.resolve())
    result = find_inputs([tmp_path])
    assert a.resolve() in result["materias"]
    assert b.resolve() in result["asesorias"]


def test_missing_private_inputs_stops_without_guessing(tmp_path):
    old = tmp_path / "CMAT-research"
    old.mkdir()
    with pytest.raises(SystemExit, match="Cannot generate new institutional"):
        discover_pair(old, None)
