# Data policy

Raw administrative data are intentionally **not stored in GitHub**, even while this repository is private. The project distinguishes raw institutional source files from the controlled pseudonymized research release, non-sensitive institutional catalogs, and the normalized relational layer used for new analyses.

## Canonical local raw-data layout

Controlled source files should be placed under `data/raw/`, which is ignored by Git except for its documentation file. The current canonical filenames are:

```text
data/raw/
├── Materias estudiantes-profesores 2019-2025 P y O.xlsx
├── Asesorias2024.xlsx
└── pre_treatment_covariates.xlsx   # optional, if approved/available
```

The shared CMAT configuration searches this directory automatically, so paper and study runners normally do not require explicit `--materias` or `--asesorias` arguments once the files are present. The shorter local aliases `Materias.xlsx` and `Asesorias.xlsx` are also accepted. Explicit CLI paths remain available when a different controlled location is required.

A temporary backward-compatible fallback still recognizes the historical raw-file locations directly under `data/`, as well as approved pseudonymized CSV inputs where supported. New raw-data setups should use `data/raw/`.

## Institutional catalog layer

Non-student catalogs recovered from the historical `dev.xlsx` and `prod.xlsx` workbooks live under `data/catalogs/`:

```text
data/catalogs/
├── schools.csv
├── careers.csv
├── course_catalog.csv
├── CATALOG_PROVENANCE.json
└── README.md
```

The school-to-career assignments follow the institutional Licenciaturas catalog supplied by the project owner on 2026-09-13. Catalog conflicts are preserved rather than silently collapsed, because several different course codes share the same subject name and four historical course codes are associated with more than one catalog name.

## Controlled pseudonymized flat layer

A row-level pseudonymized research release may be stored under `data/controlled/` only while the repository is private and access is restricted to authorized collaborators. The flat compatibility files remain in place because historical analyses were written against their original wide structure:

```text
data/controlled/
├── Materias_pseudonymized.csv
├── Asesorias_pseudonymized.csv
└── Diagnostico_pseudonymized.csv   # optional legacy diagnostic source
```

The current release uses deterministic keyed HMAC-SHA256 pseudonyms for student identifiers and academic professor identifiers, which preserves analytical linkage without storing the original institutional IDs. The advisory professor-name field is currently pseudonymized independently because no verified professor-name-to-`CLAVEPROFESOR` crosswalk is available. The HMAC secret is never stored in Git, releases, manifests, workflow artifacts, or repository documentation.

## Normalized relational layer

New analyses should prefer the additive relational representation under `data/controlled/normalized/`, which removes repeated descriptive strings from the fact tables while preserving the same pseudonymized identities and exact CMAT timestamps. It is generated from the flat controlled inputs and the institutional catalogs with:

```bash
python cmat_analysis/scripts/build_normalized_controlled_data.py
```

The normalized model separates dimensions such as schools, careers, subjects, topics, terms, students, instructors and advisors from fact tables such as course attempts, advisory visits and diagnostics. Career is represented as a term- and source-specific observation rather than a permanent student attribute, because program changes, multiple programs and administrative inconsistencies are possible.

`advisory_visits.timestamp` retains the exact date and clock time. The advisory fact table references career, subject and topic lookup IDs rather than repeating the original text on every row. Academic `CLAVECARRERA` values are mapped to current careers only when the mapping is directly supported or when same-student/same-term diagnostic evidence is sufficiently strong; unresolved historical codes remain explicit instead of being guessed.

The flat and normalized layers intentionally coexist: **legacy analyses may continue to consume the flat files, while new analyses should prefer the normalized model.**

See `docs/DATA_PRIVACY.md`, `docs/PSEUDONYMIZED_RELEASE.md`, `data/catalogs/README.md`, and `data/controlled/normalized/README.md` before adding, replacing, distributing, or publishing row-level pseudonymized files.

## What may be committed while the repository is private

- schemas/dictionaries with no identifying values;
- institutional catalogs that contain no student-level data;
- synthetic examples;
- source-file SHA-256 hashes for provenance;
- privacy-reviewed aggregated statistics;
- code that reads local or controlled data through configurable paths;
- the specifically documented pseudonymized flat and normalized research layers under `data/controlled/`, provided that the HMAC secret and raw institutional identifiers are absent.

## What must never be committed

- original student IDs;
- student names or emails;
- raw institutional Excel workbooks;
- raw CMAT Forms exports containing direct identifiers;
- the HMAC key or any equivalent pseudonymization secret;
- access credentials;
- privately licensed source files unless explicitly approved.

A SHA-256 checksum proves integrity/version identity only. It does not anonymize a dataset, and pseudonymization does not eliminate reidentification risk.

If repository visibility may change to public, the controlled row-level flat and normalized releases must be removed from the complete Git/LFS history, releases, caches, and workflow artifacts before that change; deleting only the current working-tree copy is insufficient.
