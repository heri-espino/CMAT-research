# Migration and canonicalisation status

## Canonical repository

`heri-espino/CMAT-research` is the canonical private repository for the CMAT research/publication project.

## Completed repository migration

- private repository verified;
- monorepo structure and operating rules documented;
- privacy-first `.gitignore` and raw-data exclusion policy added;
- historical literature source material imported and preserved;
- historical v8 scientific snapshot imported into `code/` without administrative raw data;
- historical v8 LaTeX report preserved in `reports/technical_report_v8/`;
- later methodology-v5 snapshot and technical report v2 restored exactly for provenance;
- legacy notebooks and aggregated study outputs preserved for reproducibility;
- literature reorganized by scientific use rather than upload batch;
- five-paper publication portfolio established under `docs/PUBLICATION_PORTFOLIO.md` and mirrored under root `papers/` and `literature/papers/`.

The original automated heavy literature/v8 import commit is:

`d7e8db74253ef1cc1227b2a0bb4373ad94bed66a` — `migration: import heavy bibliography and v8 research snapshot`.

## Literature architecture

The former top-level `Bib/` and `Bib2/` names are no longer the scientific interface.

Current organization:

- `literature/library/` — source layer and master catalogue;
- `literature/general/` — cross-project literature map;
- `literature/papers/paper1_ppa_persistence/` — Paper 1 literature view;
- `literature/papers/paper2_mu_performance/` — Paper 2 literature view;
- `literature/papers/paper3_grading_heterogeneity/` — Paper 3 literature view;
- `literature/papers/paper4_degree_help_seeking/` — Paper 4 literature view;
- `literature/papers/paper5_longitudinal_trajectories/` — Paper 5 literature view;
- `literature/AI_HANDOFF.md` and `literature/AGENTS.md` — future-AI/human operating rules.

Historical source imports are preserved under:

- `literature/library/` (consolidated) — 20 source PDFs, 20 extracted Markdown records, separated references and 136 visual assets;
- `literature/library/` (consolidated) — 30 extracted Markdown records, 29 source PDFs, 24 separated reference files and no visual assets by design.

These source-material folders preserve provenance/storage. Scientific relevance is defined by the general and five paper-specific views.

The `kahu_2018_student-engagement-educational-interface` record remains a documented exception with a Markdown source copy rather than a PDF in the PDF/Markdown source corpus.

## Current methodology status

The exact later methodology snapshot is preserved at:

`code/snapshots/methodology_v5_2026-09-07/`

with technical report v2 at:

`reports/technical_report_methodology_v2/`.

Recorded scientific-source fingerprint:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

Restoration verification is documented in `docs/snapshots/methodology_v5_2026-09-07/README.md`: all file-level manifests passed, 9/9 methodology helper tests passed, the Python function index contains 320 symbols, and the restored report PDF is 40 pages with its exact SHA-256 recorded.

That later snapshot contains corrections/extensions made after the historical v8 line, including SciPy KDE/Scott imputation, complete 0/1/2/3/4+ pairwise contrasts, the 4,211-progressor sensitivity, population-specific periodicity and expanded degree-programme analyses.

The refined longitudinal/PPA N=3,241 stage is later work and is not claimed to be covered by the methodology-v5 fingerprint.

The historical v8 longitudinal/PPA logic and the later methodology corrections still need to be reconciled into one fully validated active canonical executable pipeline. A restored snapshot or merged PR does not by itself prove that the active `code/` implementation has absorbed every correction.

## Privacy boundary

Never migrate or commit:

- administrative Excel files;
- row-level student/advising microdata;
- direct identifiers;
- HMAC keys, credentials or tokens;
- unreviewed identifying free text.

Literature PDFs are retained only because this repository is private and the owner explicitly requested internal research continuity. They are not automatically suitable for redistribution in a public release.

## Working rule

Future substantive changes happen in this repository. `main` is the source of truth; temporary branches, when used, should be short-lived and deleted after merge. ZIPs are optional offline backups, not project history. Literature should be added once to the shared library source layer and referenced through general/paper-specific indexes rather than duplicated across manuscripts.


## Literature consolidation update — 2026-09-08

The active literature tree was simplified after verification that all historical Markdown/PDF/reference filenames were represented byte-for-byte in the flat canonical library. The historical `source_material/` hierarchy, duplicate Docling `assets/` tree, and the redundant former secondary inventory were removed. The single master inventory is now `literature/library/CATALOG.md`; original batch checksums and former layout remain documented in provenance and Git history.
