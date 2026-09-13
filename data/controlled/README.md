# Controlled pseudonymized CMAT data

This directory contains the project’s row-level pseudonymized research data. It may be versioned only while the repository remains private and access is restricted to authorized collaborators.

The data layer now deliberately has two representations:

```text
data/controlled/
├── Materias_pseudonymized.csv          # flat compatibility input
├── Asesorias_pseudonymized.csv         # flat compatibility input
├── Diagnostico_pseudonymized.csv       # optional legacy DMU input
├── normalized/                         # relational representation for new analyses
├── PSEUDONYMIZATION_MANIFEST.json
├── SHA256SUMS.txt
└── PRIVACY_README.md
```

Historical analyses may continue to consume the two original flat files. New analyses should prefer `data/controlled/normalized/`, which keeps the same pseudonymized student identities while reducing repeated descriptive data and separating dimensions from fact tables.

The shared `cmat_analysis` configuration still prefers raw local Excel files under `data/raw/` when they are available; otherwise legacy runners automatically fall back to the controlled flat pseudonymized CSV files. The normalized layer is generated independently with:

```bash
python cmat_analysis/scripts/build_normalized_controlled_data.py
```

## Why this storage model reduces privacy risk

The committed research release contains no original student identifier and no original academic professor identifier. Student identities are represented by deterministic keyed HMAC-SHA256 `stu_*` pseudonyms and academic professors by `prof_*` pseudonyms, while the secret key is stored separately and never committed. This preserves the linkage required for longitudinal analysis without storing the institutional IDs needed to regenerate that linkage.

The release remains pseudonymized rather than anonymous because exact timestamps, career, semester, course, topic, grades, diagnostics, and longitudinal patterns may function as quasi-identifiers. Repository privacy and access control are therefore part of the protection model rather than optional conveniences. Raw Excel workbooks remain outside Git regardless of repository visibility.

The advisory `profesor` field is represented by `advisor_*` pseudonyms rather than the academic `prof_*` namespace because the supplied advisory source contains professor names while the academic source contains numeric `CLAVEPROFESOR`, and no verified crosswalk is available. The project deliberately avoids inventing that linkage.

The normalized representation preserves exact advisory clock time and stores repeated career, subject and topic labels once in lookup tables. Career is represented as a source- and term-specific observation, so program changes or conflicting administrative records are not overwritten by a single permanent student attribute.

The HMAC key must never be placed in this directory, Git history, releases, workflow artifacts, or documentation. If this repository is ever made public, all row-level controlled flat and normalized files must be removed from the complete Git/LFS history and all releases/artifacts before the visibility change.

See `docs/DATA_PRIVACY.md`, `docs/PSEUDONYMIZED_RELEASE.md`, `data/README.md`, and `normalized/README.md` for the governing project documentation.
