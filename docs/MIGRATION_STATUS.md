# Migration and canonicalisation status

## Canonical repository

`heri-espino/CMAT-research` is the canonical private repository for the CMAT research/publication project.

## Completed repository migration

- private repository verified;
- monorepo structure and operating rules documented;
- privacy-first `.gitignore` and raw-data exclusion policy added;
- historical literature source material imported and consolidated;
- historical scientific code/report states imported and verified;
- cumulative LaTeX research record preserved in `reports/research_compendium/`;
- methodology/statistical report preserved in `reports/methodology_report/`;
- literature reorganized by scientific use rather than upload batch;
- five-paper publication portfolio established under `docs/PUBLICATION_PORTFOLIO.md`;
- paper-specific literature views consolidated into each canonical `papers/<paper_id>/literature/` home; the former parallel `literature/papers/` hierarchy was removed;
- active `code/` cleaned so it contains only the executable pipeline and immediate technical documentation;
- duplicate code snapshots, legacy notebooks, old manuals/reports, and the obsolete migration workflow removed from the working tree;
- previously committed pipeline outputs moved out of `code/outputs/` and classified as shared historical aggregates under `analysis/shared/historical_outputs/`.

The original automated heavy literature/scientific import commit is:

`d7e8db74253ef1cc1227b2a0bb4373ad94bed66a` — `migration: import heavy bibliography and v8 research snapshot`.

The complete tree immediately before the code cleanup remains available through Git at:

`20a993d92e8cc197a9060180d8cb6a6caf2607a7`.

The code-cleanup commit is:

`d4647083e9e45fec9113bee2b9ad798c1df87658`.

The paper/literature co-location refactor is:

`0508f847faff280c4013bfc4173ee7ddce1cfc18` — `refactor: co-locate paper-specific literature with papers`.

## Literature architecture

Current organization:

- `literature/library/` — physical/shared source layer and master catalogue;
- `literature/general/` — cross-project literature map;
- `papers/paper1_ppa_persistence/literature/` — Paper 1 literature view;
- `papers/paper2_mu_performance/literature/` — Paper 2 literature view;
- `papers/paper3_grading_heterogeneity/literature/` — Paper 3 literature view;
- `papers/paper4_degree_help_seeking/literature/` — Paper 4 literature view;
- `papers/paper5_longitudinal_trajectories/literature/` — Paper 5 literature view;
- `literature/AI_HANDOFF.md` and `literature/AGENTS.md` — shared-library/retrieval operating rules.

The old upload-batch names and the former `literature/papers/` mirror are provenance only and are not the scientific interface.

## Current methodology status

A later methodology code state was restored and verified during migration, with historical scientific-source fingerprint:

`03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`.

Its restoration verification remains documented in `docs/snapshots/methodology_v5_2026-09-07/README.md`. The duplicate source tree that had been retained under `code/snapshots/` was later removed from the active working tree because Git already preserves it.

That historical methodology state includes corrections/extensions such as SciPy KDE/Scott imputation, complete `0/1/2/3/4+` pairwise contrasts, the 4,211-progressor sensitivity, population-specific periodicity and expanded degree-programme analyses.

The refined longitudinal/PPA N=3,241 stage is later work and is not claimed to be covered by that fingerprint.

The historical longitudinal/PPA logic documented in `reports/research_compendium/` and the later methodology corrections still need to be reconciled into one fully validated active executable pipeline. Removing the duplicate snapshot folder does not change that scientific requirement.

If historical implementation details are needed during reconciliation, retrieve the relevant state from Git history rather than recreating a permanent `code/snapshots/` hierarchy.

## Analysis/output architecture

`code/` is source code. Generated local outputs under `code/outputs/` are ignored by Git.

Shared/privacy-reviewed retained aggregates belong under `analysis/shared/`. The aggregate outputs already present in repository history are currently retained at:

`analysis/shared/historical_outputs/`.

They remain useful for provenance and comparison, but a new canonical aggregate output set should be frozen only after the active scientific pipeline is reconciled and validated.

When a reviewed output has a clear single-paper owner, it may instead be retained under `papers/<paper_id>/results/`; it must still originate from canonical code/runners and should not be duplicated in both locations without a documented reason.

## Privacy boundary

Never migrate or commit:

- administrative Excel files;
- row-level student/advising microdata;
- direct identifiers;
- HMAC keys, credentials or tokens;
- unreviewed identifying free text.

Literature PDFs are retained only because this repository is private and the owner explicitly requested internal research continuity. They are not automatically suitable for redistribution in a public release.

## Working rule

Future substantive changes happen in this repository. `main` is the source of truth; temporary branches, when used, should be short-lived and deleted after merge. Git is project history. Do not create permanent version-numbered code folders or ZIP-derived snapshots inside the active tree unless there is a specific scientific reason that cannot be served by Git provenance.

## Naming rule for reports

Active report paths describe purpose rather than version. Historical labels such as `v8`, `v5`, or `v2` remain only when needed to identify imported states, fingerprints, archive hashes, or dated provenance records.
