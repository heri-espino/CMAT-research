# AGENTS.md — literature subsystem

This file defines how humans and automated agents should operate inside `literature/`.

## 1. Scientific organization is primary

Do not organize literature by upload batch. The user-facing structure is:

- `library/` — canonical source layer and master catalogue;
- `general/` — cross-project conceptual literature;
- `papers/paper1_ppa_persistence/` — incentive-context persistence;
- `papers/paper2_mu_performance/` — CMAT use and MU performance;
- `papers/paper3_grading_heterogeneity/` — grading/assessment comparability;
- `papers/paper4_degree_help_seeking/` — disciplinary heterogeneity in support use;
- `papers/paper5_longitudinal_trajectories/` — full-degree support trajectories.

Historical source imports remain nested under `library/source_material/` for provenance. Their storage boundaries must not dictate scientific interpretation.

Canonical title/priority/journal plan: `../docs/PUBLICATION_PORTFOLIO.md`.

## 2. One physical source, many views

A work can support several research questions. Do not copy the same PDF/Markdown into general + multiple paper folders. Instead, register/refer to the canonical source from multiple scientific indices or reading notes.

## 3. Retrieval protocol

For a literature question:

1. identify whether it is general, paper-specific, or cross-paper;
2. open the corresponding `INDEX.md` first;
3. if a paper-specific `READING_GUIDE.md` exists, use it for rapid technical orientation;
4. use `library/CATALOG.md` and the source-material indices to locate the canonical record;
5. read only relevant extracted Markdown sections;
6. inspect `references/` only for citation chaining/bibliography verification;
7. inspect the source PDF for exact tables, figures, coefficients, confidence intervals, sample sizes, page-level wording, or extraction ambiguity;
8. use Docling assets only where they actually exist and materially help.

Do not load the whole corpus when targeted retrieval is sufficient.

## 4. Source reliability

- Source PDFs are the final verification layer.
- Extracted Markdown is the primary efficient reading layer.
- Separated references are secondary metadata.
- Docling assets are optional visual fallbacks.
- Never infer a material numerical value from visibly corrupted extraction.

## 5. Adding a new work

1. choose a stable ID such as `author_year_short-topic`;
2. place/register the work in the appropriate canonical source-material layer under `library/source_material/`;
3. retain the source PDF when available and appropriate for this private repository;
4. retain separated references when useful;
5. add visual assets only when they already exist or are genuinely needed—do not regenerate hundreds of images for archival completeness;
6. update `library/CATALOG.md`;
7. update every relevant scientific view among `general/` and Papers 1–5;
8. update a relevant `MISSING_LITERATURE.md` when a gap is filled or newly identified;
9. create/update a technical reading note when the source is substantive for an active manuscript;
10. update `AI_HANDOFF.md` if architecture, retrieval rules, portfolio status or major gaps changed.

Do not create `library/articles/`, `Bib3`, `Bib4`, or paper-specific physical source copies unless the architecture is intentionally changed and documented first.

## 6. Duplicate/version handling

When apparent duplicates are found:

- compare title, authors, year, DOI and scholarly version;
- collapse exact duplicate copies in the scientific catalogue;
- retain genuinely different versions (for example working paper vs published article) when analytically relevant;
- prefer the published version for manuscript citation unless there is a reason not to;
- preserve provenance rather than silently destroying useful history.

## 7. Paper-specific role tagging

Paper views should annotate each source with roles such as:

- `core` — directly supports theory/design/contribution;
- `supporting` — useful framing or interpretation;
- `methods` — supports statistical or measurement choices;
- `context` — institutional/domain background;
- `contrast` — competing explanation or alternative interpretation.

Where useful, also record `used_in` and `do_not_claim` boundaries.

## 8. Technical reading notes

For active manuscript literature, technical reading notes are the evidence layer between source and manuscript drafting. Paper 1 currently uses `papers/paper1_ppa_persistence/READING_GUIDE.md` and `reading_notes/`.

A substantive note should capture, when actually reported:

- design and sample (`N`, group sizes, study/sample count `k`);
- exposure/predictor and outcome definitions;
- statistical or qualitative method;
- individual important results, including null findings;
- coefficients/correlations, SE, CI, p-values, test statistics, `R²`, effect sizes, heterogeneity and reliability where applicable;
- short quotation anchors;
- what the paper supports for CMAT and what it does not support;
- exact local Markdown/PDF and page/table/figure anchors.

Do **not** fabricate quantitative statistics for conceptual, narrative-review or qualitative papers. State `inferential statistics: not applicable` and document the actual method.

If a statistic is calculated by us rather than printed in the source, label it explicitly as derived and record the source quantities used.

## 9. Five-paper routing rules

### Paper 1 — incentive-linked persistence
Relevant families: incentives, incentive removal, persistence, engagement, academic help-seeking, first-year transitions and mathematics-support context.

Do not describe PPA as an exogenous treatment and do not identify a causal PPA effect from observational CMAT data.

### Paper 2 — MU performance
Relevant families: mathematics/statistics support, tutoring/help-seeking, selection into support, usage intensity, academic performance, classroom adjustment and observational robustness.

Do not convert association into a causal tutoring effect without an identified design.

### Paper 3 — grading heterogeneity
Relevant families: higher-education assessment, grading severity/leniency, instructor/section comparability, multilevel variation, measurement, standardization and mathematics-assessment context.

Do not treat classroom-relative `Z` as latent mathematical proficiency; it is contextual relative position.

### Paper 4 — disciplinary help-seeking heterogeneity
Relevant families: academic help-seeking, engagement, disciplinary/major differences, support access, mathematics-support non-engagement, programme context and ecological inference.

Do not infer individual mechanisms from programme-level averages or scatterplots.

### Paper 5 — longitudinal trajectories
Relevant families: longitudinal help-seeking, repeated support use, educational transitions, sequence/state models, learning analytics, STEM progression, longitudinal missingness and data ethics.

Do not label trajectory classes as motivation/habit/need solely from visit patterns.

## 10. Portfolio consistency

The manuscript folders under root `papers/` and literature views under `literature/papers/` must use the same stable IDs:

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Paper-specific `.bib` files belong with manuscript source under root `papers/`, not in this research-library subsystem.

## 11. Privacy/copyright boundary

This is a private research repository. Literature PDFs and extraction artifacts are internal research materials and are not automatically redistributable in a public release. Administrative student data must never be added here.
