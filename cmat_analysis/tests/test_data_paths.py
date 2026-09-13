from pathlib import Path

from cmat_analysis.config.settings import get_settings
from cmat_analysis.config.study_config import get_study_config


MATERIAS_NAME = "Materias estudiantes-profesores 2019-2025 P y O.xlsx"
ASESORIAS_NAME = "Asesorias2024.xlsx"


def test_study_config_prefers_data_raw(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)
    materias = raw / MATERIAS_NAME
    asesorias = raw / ASESORIAS_NAME
    materias.touch()
    asesorias.touch()

    config = get_study_config(tmp_path)

    assert config.materias_path == materias
    assert config.asesorias_path == asesorias


def test_study_config_accepts_short_local_aliases(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)
    materias = raw / "Materias.xlsx"
    asesorias = raw / "Asesorias.xlsx"
    materias.touch()
    asesorias.touch()

    config = get_study_config(tmp_path)

    assert config.materias_path == materias
    assert config.asesorias_path == asesorias


def test_study_config_keeps_legacy_data_fallback(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir(parents=True)
    materias = data / MATERIAS_NAME
    asesorias = data / ASESORIAS_NAME
    materias.touch()
    asesorias.touch()

    config = get_study_config(tmp_path)

    assert config.materias_path == materias
    assert config.asesorias_path == asesorias


def test_visit_settings_prefers_data_raw(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)
    materias = raw / MATERIAS_NAME
    asesorias = raw / ASESORIAS_NAME
    materias.touch()
    asesorias.touch()

    settings = get_settings(tmp_path)

    assert settings.materias_path == materias
    assert settings.asesorias_path == asesorias
