# AGENTS.md — literature subsystem

This file defines how humans and automated agents should operate inside `literature/`.

## 1. Scientific organization is primary

Do not organize literature by upload batch. The user-facing structure is:

- `library/` — canonical source material and master catalogue;
- `general/` — cross-project conceptual literature;
- `papers/paper1_ppa_persistence/` — incentive-context persistence;
- `papers/paper2_mu_performance/` — CMAT use and MU performance;
- `papers/paper3_grading_heterogeneity/` — grading/assessment comparability;
- `papers/paper4_degree_help_seeking/` — disciplinary heterogeneity in support use;
- `papers/paper5_longitudinal_trajectories/` — full-degree support trajectories.

Historical source imports may remain nested under `library/source_material/` for provenance, but their storage boundaries must not dictate scientific interpretation.

The canonical five-paper title/priority/journal plan is `../docs/PUBLICATION_PORTFOLIO.md`.

## 2. One physical source, many views

A paper can support several research questions. Do not copy the same PDF/Markdown into general + multiple paper folders. Instead, add references to the canonical source from multiple indices/cards.

## 3. Retrieval protocol

For a literature question:

1. identify whether the question is general, paper-specific, or cross-paper;
2. open the corresponding `INDEX.md` first;
3. if a paper-specific `READING_GUIDE.md` exists, use it for rapid technical orientation;
4. use `library/CATALOG.md` and source-material indices to locate the canonical record;
5. read only the relevant extracted Markdown sections;
6. inspect `references/` only for citation chaining or bibliography verification;
7. inspect the PDF for exact tables, figures, coefficients, confidence intervals, sample sizes, page-level wording, or extraction ambiguity;
8. use Docling assets only where they actually exist and materially help.

Do not load the entire corpus into context when a targeted search is sufficient.

## 4. Source reliability

- Source PDFs are the final verification layer.
- Extracted Markdown is the primary efficient reading layer.
- Separated references are secondary metadata.
- Docling assets are optional visual fallbacks.
- Never infer a material numerical value from visibly corrupted extraction.

## 5. Duplicate/version handling

When apparent duplicates are found:

- compare title, authors, year, DOI and scholarly version;
- collapse exact duplicate copies in the scientific catalogue;
- retain genuinely different versions (e.g. working paper vs published article) when analytically relevant;
- record the preferred canonical source and provenance rather than silently deleting useful history.

## 6. Paper-specific role tagging

Paper views should annotate each source with a role such as:

- `core` — directly supports theory/design/contribution;
- `supporting` — useful framing or interpretation;
- `methods` — supports statistical or measurement choices;
- `context` — institutional/domain background;
- `contrast` — competing explanation or alternative interpretation.

Where useful, also note `used_in` and `do_not_claim` boundaries.

## 7. Technical reading notes

For active manuscript literature, technical reading notes are the evidence layer between the source and manuscript drafting. Paper 1 uses `papers/paper1_ppa_persistence/READING_GUIDE.md` and `reading_notes/`.

A substantive reading note should capture, when the source actually reports them:

- design and sample (`N`, group sizes, study/sample count `k`);
- exposure/predictor and outcome definitions;
- statistical/qualitative method;
- individual important results rather than only an overall conclusion;
- coefficients/correlations, SE, CI, p-values, test statistics, `R²`, effect sizes, heterogeneity and reliability where applicable;
- short quotation anchors;
- what the paper supports for CMAT and what it does not support;
- exact local Markdown/PDF and page/table/figure anchors.

Do **not** fabricate quantitative statistics for conceptual, narrative-review or qualitative papers. State `inferential statistics: not applicable` and document their actual methodology.

Preserve null results. Do not selectively record only significant results.

If a statistic is calculated by us rather than printed in the source, label it explicitly as a derived calculation and record the source quantities used.

## 8. Five-paper routing rules

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

## 9. Maintenance rule

When adding or materially changing literature:

- update `library/CATALOG.md`;
- update every relevant scientific view among general + Papers 1–5;
- update the relevant `MISSING_LITERATURE.md` when a gap is filled or newly identified;
- add/update a technical reading note when the source is substantive for an active manuscript;
- update `AI_HANDOFF.md` if architecture, retrieval rules, portfolio status or major literature gaps changed;
- update `../docs/PUBLICATION_PORTFOLIO.md` only when title/priority/journal strategy actually changes;
- do not rename stable paper IDs casually;
- keep manuscript `.bib` files with manuscripts, not inside this research-library folder.

## 10. Portfolio consistency

The manuscript folders under root `papers/` and the literature views under `literature/papers/` must use the same stable IDs:

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Do not create alternate IDs for the same paper.

## 11. Privacy/copyright boundary

This is a private research repository. Literature PDFs and extraction artifacts are internal research materials and are not automatically redistributable in a public release. Administrative student data must never be added here.