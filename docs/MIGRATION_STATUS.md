# Migration status

## Canonical repository

`heri-espino/CMAT-research` is the canonical GitHub repository for the CMAT research/publication project.

## Completed

- private repository verified;
- monorepo structure and operating rules documented;
- privacy-first `.gitignore` and raw-data exclusion policy added;
- Batch 1 literature imported into `literature/Bib/`;
- historical v8 scientific snapshot imported into `code/` without administrative raw data;
- historical v8 LaTeX report preserved in `reports/technical_report_v8/`;
- legacy notebooks and aggregated study outputs preserved for reproducibility;
- **Batch 2 literature curated into `literature/Bib2/`** with text/PDF fallback and no visual assets.

The original automated heavy Batch 1 import commit is:

`d7e8db74253ef1cc1227b2a0bb4373ad94bed66a` — `migration: import heavy bibliography and v8 research snapshot`.

## Current methodology status

The later methodology snapshot (`CMAT_publication_study_v5_methodology_sanitized`) contains corrections made after the historical v8 snapshot, including classroom-level KDE imputation, complete 0/1/2/3/4+ pairwise contrasts, the 4,211-progressor sensitivity, population-specific periodicity, and expanded degree-programme analyses.

Recorded scientific-source fingerprint for that methodology snapshot:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

These methodological changes still need to be reconciled with the v8 longitudinal/PPA code before `code/` can be treated as one fully unified canonical executable pipeline. A merged branch-status/PR by itself does not change the scientific code.

## Literature batches

### Batch 1 — complete

Target: `literature/Bib/`

- 20 source PDFs;
- 20 article Markdown extractions;
- 136 retained Docling visual assets;
- separated reference files and index metadata.

### Batch 2 — complete, curated asset-free representation

Canonical target: `literature/Bib2/`

Current GitHub inventory:

- 30 extracted Markdown records;
- 29 source PDFs;
- 24 separated reference files;
- 0 Docling visual assets by design.

The original Batch 2 archive contained visual assets, but they were intentionally omitted from the GitHub representation because the PDFs are retained as the visual/source-of-truth fallback and the assets were large/redundant.

`kahu_2018_student-engagement-educational-interface` is the documented exception: the local source copy is Markdown rather than PDF.

The accidental upload path `literature/Bib2-2/` is removed in the curation branch; `literature/Bib2/` is the only canonical path.

## Privacy boundary

Never migrate:

- administrative Excel files;
- row-level student/advising microdata;
- direct identifiers;
- HMAC keys or other secrets/credentials.

Literature PDFs are retained only because this repository is private and the owner explicitly requested internal research continuity. They are not automatically suitable for redistribution in a public release.

## Working rule

Future substantive changes should be committed through short-lived feature branches and merged into `main`. ZIPs are optional offline backups, not the project history.
