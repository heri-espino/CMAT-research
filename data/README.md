# Data policy

Raw administrative data are intentionally **not stored in GitHub**.

## Canonical local layout

Controlled source files should be placed under `data/raw/`, which is ignored by Git except for its documentation file. The current canonical filenames are:

```text
data/raw/
├── Materias estudiantes-profesores 2019-2025 P y O.xlsx
├── Asesorias2024.xlsx
└── pre_treatment_covariates.xlsx   # optional, if approved/available
```

The shared CMAT configuration searches this directory automatically, so paper and study runners normally do not require explicit `--materias` or `--asesorias` arguments once the files are present. The shorter local aliases `Materias.xlsx` and `Asesorias.xlsx` are also accepted. Explicit CLI paths remain available when a different controlled location is required.

A temporary backward-compatible fallback still recognizes the historical raw-file locations directly under `data/`, as well as privacy-reviewed anonymized CSV inputs where supported. New local setups should use `data/raw/`.

The analysis expects controlled local inputs such as:

- official academic records with course attempts/final grades;
- CMAT visit records linked internally through institutional student ID;
- future approved pre-treatment measures such as mathematics-admission/diagnostic scores;
- future survey responses about reasons for CMAT use, if collected and approved.

These files may contain direct or indirect identifiers and must remain in the institutionally controlled environment.

## What may be committed

- schemas/dictionaries with no identifying values;
- synthetic examples;
- source-file SHA-256 hashes for provenance;
- privacy-reviewed aggregated statistics;
- code that reads local data through configurable paths.

## What must not be committed

- student IDs;
- names/emails;
- row-level academic histories;
- raw CMAT Forms exports;
- identifiable free text;
- HMAC keys or salts;
- access credentials;
- privately licensed source files unless explicitly approved.

A SHA-256 checksum proves integrity/version identity only. It does not anonymise a dataset.
