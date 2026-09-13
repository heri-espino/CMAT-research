# Data policy

Raw administrative data are intentionally **not stored in GitHub**, even while this repository is private. The project distinguishes raw institutional source files from the controlled pseudonymized research release.

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

## Controlled pseudonymized release

A row-level pseudonymized research release may be stored under `data/controlled/` only while the repository is private and access is restricted to authorized collaborators. This release is not anonymous: exact timestamps, career, semester, course, topic, period, grades, and longitudinal patterns can remain quasi-identifiers.

The current release uses deterministic keyed HMAC-SHA256 pseudonyms for student identifiers and academic professor identifiers, which preserves analytical linkage without storing the original institutional IDs. The advisory professor-name field is currently pseudonymized independently because no verified professor-name-to-`CLAVEPROFESOR` crosswalk is available. The HMAC secret is never stored in Git, releases, manifests, workflow artifacts, or repository documentation.

See `docs/DATA_PRIVACY.md` and `docs/PSEUDONYMIZED_RELEASE.md` before adding, replacing, distributing, or publishing any row-level pseudonymized file.

## What may be committed while the repository is private

- schemas/dictionaries with no identifying values;
- synthetic examples;
- source-file SHA-256 hashes for provenance;
- privacy-reviewed aggregated statistics;
- code that reads local or controlled data through configurable paths;
- the specifically documented pseudonymized research release under `data/controlled/`, provided that the HMAC secret and raw institutional identifiers are absent.

## What must never be committed

- original student IDs;
- student names or emails;
- raw institutional Excel workbooks;
- raw CMAT Forms exports containing direct identifiers;
- the HMAC key or any equivalent pseudonymization secret;
- access credentials;
- privately licensed source files unless explicitly approved.

A SHA-256 checksum proves integrity/version identity only. It does not anonymize a dataset, and pseudonymization does not eliminate reidentification risk.

If repository visibility may change to public, the controlled row-level release must be removed from the complete Git/LFS history, releases, caches, and workflow artifacts before that change; deleting only the current working-tree copy is insufficient.
