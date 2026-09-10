# Migration and canonicalisation status

## Canonical repository

`heri-espino/CMAT-research` is the canonical private repository for the CMAT research/publication project.

## Completed repository canonicalisation

- private monorepo and privacy-first raw-data exclusion policy established;
- historical literature source material imported and consolidated under `literature/library/`;
- historical scientific code/report states imported and verified;
- cumulative research record preserved in `brainstorm/research_compendium/`;
- methodology/statistical report preserved in `brainstorm/methodology_report/`;
- five-paper portfolio established under `docs/PUBLICATION_PORTFOLIO.md`;
- each paper made a single canonical home under `papers/<paper_id>/`, including its paper-specific literature view;
- former parallel `literature/papers/` hierarchy removed;
- active `code/` cleaned to executable pipeline + immediate technical documentation;
- duplicate code snapshots, legacy notebooks, old manuals/reports, stale branch-status file and obsolete root migration scripts removed from the active tree;
- previously committed pipeline outputs classified as shared historical aggregates under `brainstorm/shared/historical_outputs/`;
- branch policy consolidated into `docs/GIT_WORKFLOW.md`;
- historical methodology-restoration documentation consolidated under `docs/provenance/methodology_restoration_2026-09-07/`.

Important historical commits remain available through Git, including:

- `d7e8db74253ef1cc1227b2a0bb4373ad94bed66a` — original automated heavy literature/scientific import;
- `20a993d92e8cc197a9060180d8cb6a6caf2607a7` — complete tree immediately before the active-code cleanup;
- `0508f847faff280c4013bfc4173ee7ddce1cfc18` — paper/literature co-location refactor.

## Current literature architecture

- `literature/library/` — physical/shared source layer and catalogue;
- `literature/general/` — cross-project literature map;
- `papers/<paper_id>/literature/` — paper-specific interpretation, reading notes and gap tracking.

Old upload-batch names and the former `literature/papers/` mirror are provenance only.

## Historical methodology state

A later methodology code state was restored and verified during migration with historical scientific-source fingerprint:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`

Detailed validation/archive identity is now consolidated at:

`docs/provenance/methodology_restoration_2026-09-07/README.md`

That state covers the `N=6,627` first-MU analysis and `N=4,211` future-progressor sensitivity, including SciPy KDE/Scott imputation, complete `0/1/2/3/4+` comparisons, periodicity extensions and expanded degree-programme analyses.

The refined longitudinal/PPA `N=3,241` stage is later work and is not claimed to be covered by that fingerprint.

## Current unresolved scientific maintenance

The later methodology corrections and the refined longitudinal/PPA logic documented in the cumulative research record still require deliberate reconciliation into one fully validated canonical executable study pipeline.

Repository cleanup does **not** resolve that scientific question. Removing duplicate snapshots only changes storage/architecture.

If historical implementation details are needed, retrieve the relevant state from Git history rather than recreating `code/snapshots/` or another version-numbered source tree.

## Analysis/output architecture

`code/` is source code. Generated local outputs under `code/outputs/` are ignored by Git.

Shared privacy-reviewed retained aggregates belong under `brainstorm/shared/`. Existing historical aggregate outputs are retained at:

`brainstorm/shared/historical_outputs/`

They remain useful for provenance/comparison. A new canonical aggregate output set should be frozen only after the relevant active pipeline is validated.

A reviewed output with a clear single-paper owner may be retained under `papers/<paper_id>/results/`, but it must originate from canonical code/runners and should not be duplicated elsewhere without reason.

## Privacy boundary

Never migrate or commit administrative Excel files, row-level student/advising microdata, direct identifiers, HMAC keys/salts, credentials/tokens, or unreviewed identifying free text.

Literature PDFs are retained for internal research continuity in this private repository and are not automatically suitable for redistribution.

## Working rule

`main` is the source of truth. Git is project history. Active paths are named by scientific purpose rather than versions; historical labels such as `v8`, `v5`, or `v2` remain only where needed to identify provenance objects, archive hashes, fingerprints or historical records.
