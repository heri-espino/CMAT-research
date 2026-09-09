# Documentation

Cross-cutting project documentation. Keep active operating guidance separate from historical provenance.

## Canonical active documents

- `PUBLICATION_PORTFOLIO.md` — cross-paper plan, boundaries, priorities and journal routes.
- `GIT_WORKFLOW.md` — the single branch/Git workflow policy; Git itself is the authority for current branch state.
- `MIGRATION_STATUS.md` — current canonicalisation/scientific-migration status and unresolved reconciliation cautions.
- root `AI_HANDOFF.md` — compact global router for future AI sessions.
- root `REPRODUCING.md` — installation, tests and canonical execution entry points.

## Historical provenance

- `ARCHIVE_PROVENANCE.md` — archive hashes and high-level provenance for imported literature/methodology packages.
- `provenance/methodology_restoration_2026-09-07/README.md` — consolidated validation record for the historical methodology restoration previously identified as `methodology_v5`.

Historical version labels are allowed inside provenance records when they identify a specific imported state. They should not become active folder/report/code names.

## Ownership rule

Do not turn `docs/` into a second copy of subsystem documentation:

- study protocol / estimands / code architecture -> `code/`;
- paper-specific scope/status -> `papers/<paper_id>/README.md`;
- paper-specific literature -> `papers/<paper_id>/literature/`;
- shared literature retrieval rules -> `literature/`;
- report-specific build/provenance -> the relevant `reports/<report>/` directory.

When a working title, paper boundary, priority or journal strategy changes, update `PUBLICATION_PORTFOLIO.md` for the cross-paper view and the relevant paper README for detail. Do not duplicate the same detailed paper state across multiple handoffs.
