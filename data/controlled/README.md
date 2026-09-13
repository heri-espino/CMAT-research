# Controlled pseudonymized CMAT data

This directory is reserved for the project’s row-level pseudonymized research release. It may be versioned only while the repository remains private and access is restricted to authorized collaborators.

Expected files:

```text
data/controlled/
├── Materias_pseudonymized.csv
├── Asesorias_pseudonymized.csv
├── PSEUDONYMIZATION_MANIFEST.json
├── SHA256SUMS.txt
└── PRIVACY_README.md
```

The current release ZIP has SHA-256:

```text
f0fc1ffa979bee4aa66dde9915c4b3022d3398af145e47df058462e2ed478fa7
```

The shared `cmat_analysis` configuration prefers raw local Excel files under `data/raw/` when they are available; otherwise it automatically falls back to the two controlled pseudonymized CSV files in this directory.

## Why this storage model reduces privacy risk

The committed research release contains no original student identifier and no original academic professor identifier. Student identities are represented by deterministic keyed HMAC-SHA256 `stu_*` pseudonyms and academic professors by `prof_*` pseudonyms, while the secret key is stored separately and never committed. This preserves the linkage required for longitudinal analysis without storing the institutional IDs needed to regenerate that linkage.

The release remains pseudonymized rather than anonymous because exact timestamps, career, semester, course, topic, grades, and longitudinal patterns may function as quasi-identifiers. Repository privacy and access control are therefore part of the protection model rather than optional conveniences. Raw Excel workbooks remain outside Git regardless of repository visibility.

The advisory `profesor` field is currently represented by `advisor_*` pseudonyms rather than the academic `prof_*` namespace because the supplied advisory source contains professor names while the academic source contains numeric `CLAVEPROFESOR`, and no verified crosswalk is available. The project deliberately avoids inventing that linkage.

The HMAC key must never be placed in this directory, Git history, releases, workflow artifacts, or documentation. If this repository is ever made public, the row-level controlled release must be removed from the complete Git/LFS history and all releases/artifacts before the visibility change.

See `docs/DATA_PRIVACY.md` and `docs/PSEUDONYMIZED_RELEASE.md` for the governing project documentation.
