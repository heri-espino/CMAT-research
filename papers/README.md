# Papers

Publication-specific manuscript projects for the five-paper CMAT research programme.

## Production role

`papers/` is the **publication-selection layer**. The broad scientific reasoning, sensitivities and exploratory/methodological record should first exist in `reports/`; papers then select the validated subset needed for a journal argument.

```text
root/code
    reusable scientific computation
        ↓
reports/
    broad analysis + brainstorming + methodological record
        ↓
papers/
    final publication-specific selection and narrative
```

A paper is therefore downstream of the reports, not a parallel analysis project.

## Core rule: one paper, one home

Each paper has a single canonical directory under `papers/<paper_id>/`. Everything editorially specific to that manuscript belongs there: scope/RQs, literature interpretation, manuscript source, reviewed final paper-specific assets and submission material.

Do **not** mirror paper-specific folders elsewhere. In particular, there is no separate `literature/papers/` hierarchy.

The physical literature corpus remains shared under `literature/library/`; paper folders contain only paper-specific interpretation/annotation, not duplicate source PDFs.

## Scientific boundary

Papers do **not** maintain independent versions of cohorts, estimands, models, statistical tests or numerical results.

If manuscript work reveals that a new calculation is needed:

1. identify the source report/scientific question;
2. search `../code/FUNCTION_INDEX.md`;
3. implement/reuse the calculation in root `../code/src/visitas_analysis/`;
4. test it and regenerate the relevant report outputs;
5. only then select the validated result into the paper.

The canonical cross-paper portfolio is `../docs/PUBLICATION_PORTFOLIO.md`; detailed paper status belongs in each paper README.

## Canonical per-paper layout

```text
papers/<paper_id>/
├── README.md        # scope, RQs, contribution, targets, status, source reports
├── literature/      # paper-specific evidence map/notes; no duplicate PDFs
├── manuscript/      # LaTeX/manuscript source
├── results/         # selected final aggregate tables/figures for the paper
├── code/            # optional thin packaging/build runner only
└── submission/      # journal-specific submission material
```

Create folders only when they contain real files; do not add empty scaffolding solely for symmetry.

## Optional paper-local code

A future `papers/<paper_id>/code/` folder is allowed only for **thin product orchestration or packaging**. It may import root-code functions or consume reviewed report outputs, but it must not contain a second implementation of scientific logic.

For example, a paper build script may select/copy approved figures from a report and compile the manuscript; it should not independently calculate the regression that produced the figure.

## Report provenance

When a paper copies a final table/figure into `results/` for submission portability, document which report/output it came from. The report remains the broader empirical workspace; the paper-local copy is the final selected publication asset.

Do not silently edit a copied number or figure inside the paper. Changes must originate in root code/report production and then propagate downstream.

## Planned manuscripts

1. `paper1_ppa_persistence/` — persistence of formal mathematics-support use after the first-year incentive-linked context.
2. `paper2_mu_performance/` — contemporaneous CMAT use and classroom-relative MU performance.
3. `paper3_grading_heterogeneity/` — instructor-by-term grading heterogeneity and assessment comparability.
4. `paper4_degree_help_seeking/` — disciplinary/degree-programme heterogeneity in support use and persistence.
5. `paper5_longitudinal_trajectories/` — full-degree longitudinal trajectories of mathematics-support use.

## Literature boundary

- `../literature/library/` = canonical physical/shared source corpus;
- `../literature/general/` = cross-project/thematic literature maps;
- `<paper_id>/literature/` = paper-specific source priorities, reading notes, annotations, gaps and claim boundaries.

A source used by multiple papers still has one physical record in `literature/library/`.
