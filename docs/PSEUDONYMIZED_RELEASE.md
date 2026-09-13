# Pseudonymized release record

A controlled full-fields pseudonymized release has been generated from the current CMAT source workbooks. The repository is now private and access-controlled, so this release is eligible for repository storage under the conditions documented in `docs/DATA_PRIVACY.md`; the raw Excel workbooks and the HMAC secret remain outside Git.

Release ZIP SHA-256:

```text
f0fc1ffa979bee4aa66dde9915c4b3022d3398af145e47df058462e2ed478fa7
```

Source workbook SHA-256 values recorded for provenance:

```text
Materias estudiantes-profesores 2019-2025 P y O.xlsx
e2671767ed9a2daa14f5d08318113bfb0327539dde4cf12f4204584f28d367a1

Asesorias2024.xlsx
43a0fcd6f7f620b5b606a51efc9eac60761acdbb239d7ac839bf5c1e83bef295
```

The release contains 27,788 academic rows and 13,500 advisory rows. Student linkage between the academic and advisory sources was preserved after pseudonymization. Exact advisory timestamps and the substantive advisory research variables were retained because they are required for the planned temporal, longitudinal, and help-seeking analyses.

The release is pseudonymized rather than anonymous, so it remains controlled research data. Direct student identifiers are replaced by deterministic `stu_*` HMAC-SHA256 pseudonyms, academic professor identifiers by `prof_*` pseudonyms, and advisory professor names are currently represented separately as `advisor_*` because no verified professor-name-to-`CLAVEPROFESOR` crosswalk is available. The secret key is not stored in this repository.

Repository storage of the row-level release is conditional on the repository remaining private and access being limited to authorized collaborators. If the repository is ever made public, the row-level release must be purged from the complete Git/LFS history, releases, caches, and workflow artifacts before the visibility change. See `docs/DATA_PRIVACY.md` for the full storage and dissemination conditions.
