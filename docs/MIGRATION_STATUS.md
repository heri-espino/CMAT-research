# Migration status

## Canonical repository

`heri-espino/CMAT-research` is now the canonical GitHub repository for the CMAT research/publication project.

## Completed

- private repository verified;
- root README and canonical structure documented;
- privacy-first `.gitignore` added;
- repository operating rules added in `AGENTS.md`;
- raw-data exclusion policy added in `data/README.md`.

## Source snapshot to migrate

The latest sanitised methodology snapshot available at migration time is the local project previously labelled `CMAT_publication_study_v5_methodology_sanitized`, together with the methodology-focused LaTeX report.

Scientific-source fingerprint recorded for that methodology snapshot:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

The refined longitudinal PPA cohort/results were developed in a later analytical stage and must remain provenance-labelled separately until their logic is reintegrated into one canonical pipeline and assigned a new source fingerprint.

## Migration policy

Migrate:

- Python source and configuration;
- tests;
- study protocol;
- Python function index;
- methodology changelog;
- AI handoff;
- technical-report LaTeX source;
- manuscript LaTeX sources;
- privacy-reviewed aggregated output tables/figures;
- literature metadata, cards, indices and citation notes.

Do not migrate:

- administrative Excel files;
- student-level linked data;
- direct identifiers;
- HMAC keys/secrets;
- copyrighted literature PDFs by default;
- historical ZIP snapshots as the source of truth.

## Working rule

Future substantive changes should be committed directly to this repository. ZIPs should be treated only as optional offline backups, not as the project history.
