# Papers

Publication-specific manuscript projects for the five-paper CMAT research programme.

## Core rule: one paper, one home

Each paper has a single canonical directory under `papers/<paper_id>/`. Everything that is specific to that paper belongs under that directory: scope/RQs, literature interpretation, manuscript source, reviewed paper-specific results, and submission material.

Do **not** mirror paper-specific folders elsewhere in the repository. In particular, there is no separate `literature/papers/` hierarchy.

The physical literature corpus remains shared under `literature/library/`; paper folders contain only the paper-specific interpretation/indexing of those sources, not duplicate PDFs.

## Scientific boundary

Papers consume the canonical scientific pipeline and aggregate outputs; they do **not** maintain independent versions of cohorts, estimands, models, or numerical results.

The canonical cross-paper portfolio is `../docs/PUBLICATION_PORTFOLIO.md`. It summarizes priorities and boundaries. The detailed source of truth for a particular manuscript is that paper's own `README.md`.

## Planned manuscripts

1. `paper1_ppa_persistence/` — persistence of formal mathematics-support use after the first-year incentive-linked context.
2. `paper2_mu_performance/` — contemporaneous CMAT use and classroom-relative MU performance.
3. `paper3_grading_heterogeneity/` — instructor-by-term grading heterogeneity and assessment comparability.
4. `paper4_degree_help_seeking/` — disciplinary/degree-programme heterogeneity in support use and persistence.
5. `paper5_longitudinal_trajectories/` — full-degree longitudinal trajectories of mathematics-support use.

## Canonical per-paper layout

```text
papers/<paper_id>/
├── README.md        # canonical paper scope, RQs, contribution, targets, status
├── literature/      # paper-specific literature index/notes; no duplicate source PDFs
├── manuscript/      # LaTeX/manuscript source when drafting begins
├── results/         # reviewed paper-specific aggregate tables/figures when retained
└── submission/      # journal-specific cover letters/checklists/supplementary files
```

Only `README.md` and `literature/` are required before drafting. Create `manuscript/`, `results/`, and `submission/` only when they contain real files; do not add empty scaffolding solely for symmetry.

## Literature boundary

- `../literature/library/` = canonical physical/shared source corpus (`articles/`, `pdf/`, `references/`, catalog/provenance).
- `../literature/general/` = cross-project/thematic literature maps.
- `<paper_id>/literature/` = interpretation of shared sources for one paper: priority, role, reading notes, gaps, and claim boundaries.

A source used by three papers still has one physical record in `literature/library/` and three possible paper-specific annotations.

## Code and results boundary

Reusable scientific logic stays in `../code/src/visitas_analysis/`. Stable experiment runners stay in `../code/experiments/`. A paper-specific runner should reproduce that paper's outputs without copying scientific functions into the paper directory.

If a manuscript exposes a methodological problem, fix it first in `code/`, test it, regenerate canonical outputs, verify changed numbers, and only then update the manuscript.
