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
- legacy notebooks and aggregated study outputs preserved for reproducibility;
- literature reorganized by scientific use rather than upload batch.

The original automated heavy literature/v8 import commit is:

`d7e8db74253ef1cc1227b2a0bb4373ad94bed66a` — `migration: import heavy bibliography and v8 research snapshot`.

## Literature architecture

The former top-level `Bib/` and `Bib2/` names are no longer the scientific interface.

Current organization:

- `literature/library/` — source layer and master catalogue;
- `literature/general/` — cross-project literature map;
- `literature/papers/paper1_ppa_persistence/` — Paper 1 literature view;
- `literature/papers/paper2_mu_performance/` — Paper 2 literature view;
- `literature/AI_HANDOFF.md` and `literature/AGENTS.md` — future-AI/human operating rules.

Historical source imports are preserved under:

- `literature/library/source_material/visual_corpus/` — 20 source PDFs, 20 extracted Markdown records, separated references and 136 visual assets;
- `literature/library/source_material/pdf_markdown_corpus/` — 30 extracted Markdown records, 29 source PDFs, 24 separated reference files and no visual assets by design.

These source-material folders preserve provenance only; general/Paper 1/Paper 2 indices determine scientific relevance.

The `kahu_2018_student-engagement-educational-interface` record remains a documented exception with a Markdown source copy rather than a PDF in the PDF/Markdown source corpus.

## Current methodology status

The later methodology snapshot (`CMAT_publication_study_v5_methodology_sanitized`) contains corrections made after the historical v8 snapshot, including classroom-level KDE imputation, complete 0/1/2/3/4+ pairwise contrasts, the 4,211-progressor sensitivity, population-specific periodicity, and expanded degree-programme analyses.

Recorded scientific-source fingerprint for that methodology snapshot:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

These methodological changes still need to be reconciled with the v8 longitudinal/PPA code before `code/` can be treated as one fully unified canonical executable pipeline. A merged branch-status/PR by itself does not change the scientific code.

## Privacy boundary

Never migrate:

- administrative Excel files;
- row-level student/advising microdata;
- direct identifiers;
- HMAC keys or credentials;
- unreviewed identifying free text.

Literature PDFs are retained only because this repository is private and the owner explicitly requested internal research continuity. They are not automatically suitable for redistribution in a public release.

## Working rule

Future substantive changes should be committed through short-lived feature branches and merged into `main`. ZIPs are optional offline backups, not the project history.
Future substantive changes happen in this repository. ZIPs are optional offline backups. Literature should be added once to `literature/library/`; manuscripts reference it through paper-specific indexes rather than maintaining duplicated literature folders.
