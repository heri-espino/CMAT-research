# Migration and canonicalisation status

## Canonical repository

`heri-espino/CMAT-research` is the canonical private repository for the CMAT research/publication project.

## Completed repository migration

- private repository and privacy-first `.gitignore`;
- root operating rules (`AGENTS.md`) and AI continuity handoff (`.ai_handoff.md`);
- historical v8 scientific snapshot under `code/`, excluding administrative raw data;
- historical v8 LaTeX report under `reports/technical_report_v8/`;
- legacy notebooks and aggregate historical outputs preserved for provenance;
- two historical literature ingestion batches imported into Git history;
- literature corpus **canonicalised into `literature/library/`**, with one physical copy per work/version and semantic indices under `literature/general/` and `literature/papers/`.

## Literature canonicalisation

Historical import names `literature/Bib/`, `literature/Bib2/` and accidental `literature/Bib2-2/` are no longer active paths. They remain recoverable from Git history.

Current active library representation:

- 50 Markdown article/version records;
- 49 source PDFs;
- separated references where available;
- 136 historical Docling PNG/table/figure assets associated with the original archived subset;
- no regenerated assets for the later literature expansion, intentionally, because those images were considered redundant with the retained source PDFs.

See `literature/library/PROVENANCE.md` and `docs/HEAVY_SNAPSHOT.md`.

## Scientific methodology still to reconcile

The imported historical v8 code contains the refined longitudinal/PPA pipeline. A later sanitised methodology snapshot introduced corrections/extensions after that snapshot, including intended SciPy classroom-level KDE imputation, `0/1/2/3/4+` all-pair analyses, the `N=4,211` progressor sensitivity, population-specific periodicity, and expanded degree-programme analyses.

Recorded source fingerprint for the later methodology snapshot:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

The refined longitudinal results and the later methodology must remain provenance-labelled until one canonical executable pipeline integrates both and receives a new source fingerprint.

## Data/privacy migration policy

Preserve in repository:

- source/config/tests/documentation;
- technical-report/manuscript sources;
- privacy-reviewed aggregate outputs;
- literature metadata, Markdown, references and internal source PDFs/assets in this private repository.

Never migrate:

- administrative Excel files;
- row-level student/advising data;
- direct identifiers;
- HMAC keys or credentials;
- unreviewed identifying free text.

## Working rule

Future substantive changes happen in this repository. ZIPs are optional offline backups. Literature should be added once to `literature/library/`; manuscripts reference it through paper-specific indexes rather than maintaining duplicated literature folders.
