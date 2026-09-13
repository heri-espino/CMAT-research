from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = REPO_ROOT / "data" / "catalogs"


def test_institutional_catalog_dimensions_are_consistent() -> None:
    schools = pd.read_csv(CATALOG_ROOT / "schools.csv")
    careers = pd.read_csv(CATALOG_ROOT / "careers.csv")
    courses = pd.read_csv(CATALOG_ROOT / "course_catalog.csv")

    assert len(schools) == 5
    assert schools["school_id"].is_unique
    assert len(careers) == 52
    assert careers["career_id"].is_unique
    assert set(careers["school_id"]) <= set(schools["school_id"])

    assert len(courses) == 369
    assert not courses.duplicated(["course_code", "catalog_name"]).any()
    ambiguous_codes = courses.groupby("course_code")["catalog_name"].nunique()
    assert int((ambiguous_codes > 1).sum()) == 4
