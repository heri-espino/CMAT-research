# Data privacy for CMAT research

CMAT row-level administrative records are treated as controlled research data. The project distinguishes raw data from pseudonymized research data and from privacy-reviewed aggregate outputs.

The full-fields research release is pseudonymized, not anonymous. Original student identifiers are replaced with deterministic `stu_*` HMAC-SHA256 pseudonyms and academic professor identifiers with `prof_*` pseudonyms. The advisory `profesor` field is currently pseudonymized independently as `advisor_*` because the supplied academic file contains only numeric `CLAVEPROFESOR` and no verified name-to-ID crosswalk is available. The project does not invent that linkage.

The secret HMAC key is stored separately from the repository and is never included in data files, manifests, Git history, releases, or workflow artifacts. Raw Excel workbooks also remain outside Git under the local `data/raw/` convention. SHA-256 checksums are retained only for provenance and integrity verification.

The advisory release intentionally retains exact timestamp, `carrera`, `semestre`, `materia`, `tema`, and `periodo` because these fields are needed for analyses of timing, academic trajectory, help-seeking topic, course context, and longitudinal use. Because these variables can still act as quasi-identifiers, the full-fields row-level release must be stored only in a private repository with access limited to authorized collaborators.

This design reduces privacy risk because direct institutional identifiers and the pseudonymization secret are absent from the repository while analytical linkage is preserved. It does not make the data anonymous, so access control remains part of the protection model.

If the repository is later made public, row-level pseudonymized files must first be removed from the complete Git history and from any LFS objects, releases, caches, or workflow artifacts. Deleting only the current copy is not sufficient. Public dissemination should be limited to code, documentation, privacy-reviewed aggregates, or a separately reviewed and more strongly minimized derivative dataset.

This document records the project's technical privacy safeguards and storage conditions; it is not a substitute for institutional, legal, ethics, or data-governance approval.
