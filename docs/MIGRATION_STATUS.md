# Migration status

## Canonical repository

`heri-espino/CMAT-research` is the canonical GitHub repository for the CMAT research/publication project.

## Completed

- private repository verified;
- root README and canonical structure documented;
- privacy-first `.gitignore` added;
- repository operating rules added in `AGENTS.md`;
- raw-data exclusion policy added in `data/README.md`;
- heavy private literature policy enabled;
- Git LFS configuration documented for literature/report/paper binaries;
- heavy snapshot inventory and source checksums recorded in `docs/HEAVY_SNAPSHOT.md`;
- **heavy literature Batch 1 imported into `literature/Bib/`**, including PDFs, Docling Markdown, separated references and 136 PNG/table/figure assets;
- **historical v8 scientific snapshot imported into `code/`**, excluding administrative raw data;
- **historical v8 LaTeX report imported into `reports/technical_report_v8/`**;
- legacy notebooks and existing aggregated study outputs from that snapshot preserved for reproducibility.

The automated heavy import commit is:

`d7e8db74253ef1cc1227b2a0bb4373ad94bed66a` — `migration: import heavy bibliography and v8 research snapshot`.

## Current methodology snapshot still to reconcile

The most recent sanitised methodology work available locally was labelled `CMAT_publication_study_v5_methodology_sanitized`, together with the methodology-focused LaTeX report. It contains methodological changes made after the historical v8 snapshot was created, including the corrected classroom-level KDE imputation logic, the 0/1/2/3/4+ all-pairs analysis, the 4,211-progressor sensitivity, periodicity by population and the three-population degree-programme analyses.

Scientific-source fingerprint recorded for that methodology snapshot:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

The refined longitudinal PPA cohort/results were developed in another analytical stage and must remain provenance-labelled separately until the latest methodological and longitudinal code paths are reconciled into one canonical pipeline and assigned a new source fingerprint.

## Heavy literature snapshot requested by repository owner

The repository owner explicitly requested preservation of the heavy private bibliography snapshot, including source PDFs and Docling PNG assets.

### Batch 1 — COMPLETE

Source: `Bib.zip`

Target: `literature/Bib/`

- 20 PDFs;
- 20 article Markdown extractions;
- 136 Docling visual assets;
- separated reference files and technical index files.

This batch is now physically present in GitHub.

### Batch 2 — PENDING BINARY TRANSFER

Source archive: `339dc703-470e-407c-bb54-97ab069e4ce7.zip`

Target archival path: `literature/Bib2/`

- 29 PDFs;
- 29 article Markdown extractions;
- 322 Docling visual assets;
- separated reference files and technical index files.

SHA-256 and local inventory are recorded in `docs/HEAVY_SNAPSHOT.md`. This second archive was supplied directly in the research session and was never committed to `CMAT2`, so the GitHub Action that cloned `CMAT2` could not import it. The current connector cannot stream a 78 MB local binary archive or hundreds of PNG/PDF files by local path. A one-time Git/LFS upload from a local Git client is therefore still required for Batch 2.

## Migration policy

Migrate and preserve:

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
- in this private repository only: literature PDFs and Docling visual assets.

Never migrate:

- administrative Excel files;
- row-level student/advising data;
- direct identifiers;
- HMAC keys or other secrets/credentials.

## Working rule

Future substantive changes should be committed directly to this repository. ZIPs are optional offline backups, not the project history. The next repository-level task is to reconcile the current methodology overlay with the imported v8 code before treating `code/` as a single canonical executable pipeline.
