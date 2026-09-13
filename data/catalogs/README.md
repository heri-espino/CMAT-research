# Institutional catalogs

These non-student catalogs were recovered from the historical `dev.xlsx` and `prod.xlsx` workbooks. Their `Escuelas`, `Carreras`, and `Materias` sheets are identical in the supplied files.

`schools.csv` contains the five institutional schools. `careers.csv` contains the 52 current licenciaturas and their school assignment, using the institutional Licenciaturas catalog supplied by the project owner on 2026-09-13. `course_catalog.csv` contains unique `(course_code, catalog_name)` pairs from the historical Materias catalog after removing exact duplicate rows.

The course catalog is intentionally not collapsed to one row per code because four historical course codes have more than one catalog name and several different codes share the same subject name. The normalized data model therefore keeps conceptual subjects separate from institutional course variants instead of inventing a one-to-one relation.

`CATALOG_PROVENANCE.json` records source hashes and extraction diagnostics. Student-level sheets from `dev.xlsx`/`prod.xlsx` are not part of this catalog layer.
