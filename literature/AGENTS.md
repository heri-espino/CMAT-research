# AGENTS.md — literature subsystem

This file defines how humans and automated agents should operate inside `literature/` and how shared literature is routed into paper-local literature workspaces.

## 1. Scientific organization is primary

Do not organize literature by upload batch. The physical/shared literature subsystem is:

- `library/` — canonical source layer and master catalogue;
- `general/` — cross-project conceptual literature.

Paper-specific literature is **not mirrored inside `literature/`**. It is co-located with the corresponding manuscript:

- `../papers/paper1_ppa_persistence/literature/` — incentive-context persistence;
- `../papers/paper2_mu_performance/literature/` — CMAT use and MU performance;
- `../papers/paper3_grading_heterogeneity/literature/` — grading/assessment comparability;
- `../papers/paper4_degree_help_seeking/literature/` — disciplinary heterogeneity in support use;
- `../papers/paper5_longitudinal_trajectories/literature/` — full-degree support trajectories.

Canonical title/priority/journal plan: `../docs/PUBLICATION_PORTFOLIO.md`. Detailed paper-specific scope lives in `../papers/<paper_id>/README.md`.

## 2. One physical source, many views

A work can support several research questions. Do not copy the same PDF/Markdown into general + multiple paper folders. Instead, register/refer to the canonical source from multiple scientific indices or reading notes.

## 3. Retrieval protocol

For a literature question:

1. identify whether it is general, paper-specific, or cross-paper;
2. open `general/INDEX.md` or the corresponding `../papers/<paper_id>/literature/INDEX.md` first;
3. if a paper-specific `READING_GUIDE.md` exists, use it for rapid technical orientation;
4. use `library/CATALOG.md` to locate the canonical record;
5. read only relevant extracted Markdown sections;
6. inspect `library/references/` only for citation chaining/bibliography verification;
7. inspect the source PDF for exact tables, figures, coefficients, confidence intervals, sample sizes, page-level wording, or extraction ambiguity;
8. use the source PDF for exact visual verification; extracted Docling assets are not retained in the active library.

Do not load the whole corpus when targeted retrieval is sufficient.

## 4. Source reliability

- Source PDFs are the final verification layer.
- Extracted Markdown is the primary efficient reading layer.
- Separated references are secondary metadata.
- The source PDF is the visual verification layer.
- Never infer a material numerical value from visibly corrupted extraction.

## 5. Adding a new work

1. choose a stable ID such as `author_year_short-topic`;
2. add the canonical Markdown record to `library/articles/`;
3. add the source PDF to `library/pdf/` when available and appropriate for this private repository;
4. add separated references to `library/references/` when useful;
5. update `library/CATALOG.md`;
6. update every relevant scientific view among `general/` and `../papers/<paper_id>/literature/`;
7. update a relevant `MISSING_LITERATURE.md` when a gap is filled or newly identified;
8. create/update a technical reading note when the source is substantive for an active manuscript;
9. update `AI_HANDOFF.md` if architecture, retrieval rules, portfolio status or major gaps changed.

Do not recreate upload-batch folders (`Bib`, `Bib2`, `Bib3`, etc.), `source_material/`, extracted asset trees, a `literature/papers/` mirror, or paper-specific physical source copies.

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

For active manuscript literature, technical reading notes are the evidence layer between source and manuscript drafting. Paper 1 currently uses `../papers/paper1_ppa_persistence/literature/READING_GUIDE.md` and `../papers/paper1_ppa_persistence/literature/reading_notes/`.

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

### Reading-note subfolders

Reading-note subfolders are scientific retrieval categories, not mini-libraries and not provenance folders. Keep one canonical technical note per source; when a source serves several scientific functions, cross-reference it rather than duplicating the note.

For Paper 1:

- `reading_notes/general/` is the home for foundational and cross-cutting engagement, help-seeking, mathematics-support, first-year-transition and persistence literature.
- `reading_notes/incentives/` is now active and contains sources whose central scientific contribution concerns incentives, incentive removal/expiration, participation contingencies, thresholds, or behavioural interventions that help interpret the PPA change in incentive context.
- incentive-specific notes should record intervention type, target behaviour, assignment/exposure, magnitude/threshold when applicable, timing and removal, follow-up horizon, compliance/take-up, identification strategy, post-incentive behaviour, mechanism evidence, and transportability to CMAT when reported.
- mentioning motivation, tutoring, attendance or engagement is not enough to route a source to `incentives/`; the incentive/behavioural mechanism must be substantive.

Current Paper 1 incentive-note anchors include Gneezy et al. (2011), Angrist et al. (2009), Leuven et al. (2010), Agnew et al. (2021), Oreopoulos & Petronijevic (2019), Blondeel et al. (2023), and Damgaard & Nielsen (2018).

Create any additional reading-note subfolder only when it has a distinct scientific purpose, a recurring set of substantive sources or committed review stream, a stable inclusion/exclusion rule, and clear manuscript-retrieval value. Do not create folders by upload batch, provider, extraction method, file type, processing status or arbitrary chronology.

The detailed Paper 1 routing policy lives in `../papers/paper1_ppa_persistence/literature/reading_notes/README.md`. Update that file when a new scientific-function subfolder is introduced.

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

## 10. Portfolio consistency and ownership

Stable paper IDs are:

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Each paper has one canonical home at `../papers/<paper_id>/`. Its literature view is `../papers/<paper_id>/literature/`. Do not mirror these directories under `literature/`.

Paper-specific `.bib` files belong with manuscript source under the relevant paper directory, not in this research-library subsystem.

## 11. Privacy/copyright boundary

This is a private research repository. Literature PDFs and extraction artifacts are internal research materials and are not automatically redistributable in a public release. Administrative student data must never be added here.
