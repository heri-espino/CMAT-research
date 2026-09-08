# Migration status

## Canonical repository

`heri-espino/CMAT-research` is now the canonical GitHub repository for the CMAT research/publication project.

## Completed

- private repository verified;
- root README and canonical structure documented;
- privacy-first `.gitignore` added;
- repository operating rules added in `AGENTS.md`;
- raw-data exclusion policy added in `data/README.md`;
- heavy private literature policy enabled;
- Git LFS configured for literature/report/paper PDFs and PNGs;
- heavy snapshot inventory and source checksums recorded in `docs/HEAVY_SNAPSHOT.md`.

## Source snapshot to migrate

The latest sanitised methodology snapshot available at migration time is the local project previously labelled `CMAT_publication_study_v5_methodology_sanitized`, together with the methodology-focused LaTeX report.

Scientific-source fingerprint recorded for that methodology snapshot:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

The refined longitudinal PPA cohort/results were developed in a later analytical stage and must remain provenance-labelled separately until their logic is reintegrated into one canonical pipeline and assigned a new source fingerprint.

## Heavy literature snapshot requested by repository owner

The repository owner explicitly requested preservation of the heavy private bibliography snapshot, including source PDFs and Docling PNG assets. These files are allowed in this **private** repository and should be tracked with Git LFS.

Raw archival batches:

- `Bib.zip` -> `literature/Bib/`: 20 PDFs, 20 article Markdown files, 136 Docling visual assets;
- second literature archive -> `literature/Bib2/`: 29 PDFs, 29 article Markdown files, 322 Docling visual assets.

See `docs/HEAVY_SNAPSHOT.md` for SHA-256 checksums.

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
- literature metadata, cards, indices and citation notes;
- in this private repository only: literature PDFs and Docling visual assets, via Git LFS.

Never migrate:

- administrative Excel files;
- row-level student/advising data;
- direct identifiers;
- HMAC keys or other secrets/credentials.

## Connector limitation for initial heavy binary transfer

The connected GitHub interface can write repository files and Git objects but does not expose a local-directory `git push`/Git-LFS streaming operation. The initial ~140 MB PDF/PNG transfer therefore has to be performed by a Git/LFS client that can stream the local files. The repository is already configured for that transfer; after the initial binary objects exist in GitHub, normal code/document maintenance can continue through the connected GitHub workflow.

## Working rule

Future substantive changes should be committed directly to this repository. ZIPs are optional offline backups, not the project history.
