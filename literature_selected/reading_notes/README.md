# Paper 1 reading-note protocol

Technical reading notes are the human-readable evidence layer between the source PDFs/Markdown and manuscript drafting.

## Required sections for every substantive source

1. **Citation** — final bibliographic identity/DOI when known.
2. **60-second summary** — what the paper actually studies and finds.
3. **Role in Paper 1** — theory, context, empirical comparator, methods, contrast, etc.
4. **Design and sample** — design type, setting, N/k, groups and timing.
5. **Variables / constructs** — exposure, outcome and key operational definitions where relevant.
6. **Methodology** — regression, t-test, ANOVA, MANOVA, chi-square, meta-analysis, qualitative coding, conceptual review, etc.
7. **Key results** — one row per important result, including the reported estimate and uncertainty where available.
8. **Short quotations** — at most a few brief quotations that are genuinely useful for manuscript reasoning; always retain page/table anchors.
9. **What this paper lets us say**.
10. **What it does not let us say**.
11. **Local verification** — canonical Markdown/PDF path and relevant page/table/figure.

## Quantitative reporting fields

When reported by the source, capture as applicable:

- sample size `N` and group sizes;
- number of studies/samples `k` for meta-analysis;
- means and SDs;
- correlations `r`;
- regression coefficients `β` / `B` and SE;
- odds ratios / risk ratios / marginal effects;
- `t`, `F`, `χ²`, ANOVA/MANOVA statistics;
- `p` values;
- 95% CI and, for meta-analysis, prediction intervals;
- `R²` / adjusted `R²`;
- effect sizes such as Cohen's `d`, partial `η²`;
- heterogeneity such as `Q`, `I²`, `τ²`;
- scale reliability such as Cronbach's `α`;
- model/design features that materially affect interpretation.

Never infer a missing statistic from another statistic unless the note explicitly labels the calculation as **our derived calculation** and preserves the source values used.

## Non-quantitative papers

A conceptual review, qualitative interview study, or narrative review should **not** be made to look weaker by inventing a fake quantitative section. State `inferential statistics: not applicable` and document its actual evidentiary contribution: framework, coding procedure, sample construction, themes, triangulation, review process, etc.

## Result-level rule

Do not write only “the study found a positive effect.” Record each result separately when it matters for Paper 1. Example:

| Outcome | Estimate / test | Uncertainty | Interpretation |
|---|---|---|---|
| first-course grade | `F=15.03`, effect size `=.28` | `p=.001` | intervention group higher |
| first-year retention | `χ²=2.94` | `p=.086` | not statistically significant |

Null results are retained. They are often scientifically important.

## Verification rule

Statistics and quotations should be verified against the local source PDF/Markdown and table/page location. If extraction is corrupted or ambiguous, inspect the PDF before recording the value.

## Reading-note subfolder policy

Subfolders under `reading_notes/` are **scientific retrieval views**, not storage batches. Each substantive source should normally have one canonical technical note. If a source serves several functions, keep the note in its best-fitting scientific home and cross-reference it from the relevant guide/index rather than creating duplicate note files.

### `general/` — foundational and cross-cutting literature

Use `general/` for foundational or cross-cutting Paper 1 literature that is not primarily about a specific intervention mechanism. Typical functions include:

- student engagement and first-year transition frameworks;
- academic help-seeking theory and meta-analysis;
- mathematics/statistics support evaluation literature;
- social support, belonging, persistence and retention context;
- papers that provide broad conceptual framing used across several sections of Paper 1.

A paper should remain in `general/` when its main contribution is broad framing even if it contains a secondary discussion of incentives.

### `incentives/` — incentive/removal/behavioural-intervention evidence

This is now an active Paper 1 reading-note stream. Its scientific function is to isolate evidence that helps interpret the CMAT/PPA setting as a **change in incentive context**, not merely as generic help-seeking.

Current notes cover Gneezy et al. (2011), Angrist et al. (2009), Leuven et al. (2010), Agnew et al. (2021), Oreopoulos & Petronijevic (2019), Blondeel et al. (2023), and Damgaard & Nielsen (2018).

Include sources whose central design or argument involves one or more of the following:

- financial or non-financial incentives tied to educational participation, effort, attendance, study behaviour or achievement;
- participation requirements, thresholds, rewards, penalties or other explicit behavioural contingencies;
- introduction, withdrawal, expiration or removal of an incentive;
- persistence, decay, crowd-out, habit formation or behaviour after the incentive is no longer present, when those mechanisms are actually studied or theorized by the source;
- behavioural interventions or nudges that are useful comparators for incentive-linked participation, while preserving the distinction between a nudge and a material incentive;
- experiments, quasi-experiments, observational studies, reviews or theory papers that directly inform how incentive-linked behaviour should be interpreted.

Do **not** place a source here merely because it mentions motivation, engagement, tutoring or attendance. The incentive or behavioural-intervention mechanism must be scientifically substantive to the paper.

For incentive-specific notes, capture these fields whenever the source reports them:

- intervention/incentive type and whether it is financial, material, administrative, informational or social;
- target behaviour and unit of assignment/exposure;
- incentive magnitude, threshold or eligibility rule when applicable;
- timing: introduction, duration, removal/expiration and follow-up horizon;
- whether post-incentive behaviour is directly observed;
- compliance/take-up and whether treatment assignment differs from actual participation;
- primary and secondary outcomes;
- identification strategy and what causal claim, if any, the design supports;
- evidence for persistence, decay, substitution, crowd-out or other proposed mechanisms;
- population/setting differences that matter for transportability to CMAT/PPA;
- a short **CMAT relevance** statement explaining whether the source is a direct comparator, theoretical mechanism, or contrast case.

Important Paper 1 boundary: the CMAT data do not contain exogenous PPA treatment variation. Incentive literature can motivate competing explanations and interpretation, but it does not convert the observational CMAT design into a causal estimate of PPA.

### future: additional scientific-function subfolders

Create another subfolder only when it represents a recurring scientific function that materially improves retrieval and synthesis. A new folder should satisfy all of the following:

1. **Distinct scientific purpose** — it corresponds to a construct, mechanism, design family, measurement problem, or evidentiary function used in the manuscript.
2. **More than a one-off source** — normally several substantive notes, or a clearly committed review stream, should belong there.
3. **Stable routing rule** — another reader should be able to decide why a paper belongs there from the folder description.
4. **Manuscript relevance** — the grouping should make drafting, comparison or claim verification easier.
5. **No duplication requirement** — sources that span functions are cross-referenced rather than copied into several folders.

Never create subfolders for:

- upload batches (`Bib`, `Bib2`, `batch3`, etc.);
- source provider or download session;
- extraction tool or processing status;
- file type (`pdf`, `markdown`, `assets`);
- arbitrary chronology such as `new/`, `old/`, or `September_upload/`;
- a single paper that does not yet form a scientific literature family.

When a new scientific-function folder is created, update this README with its inclusion/exclusion rule and update `READING_GUIDE.md`, `literature/AGENTS.md`, and `literature/AI_HANDOFF.md` when the new routing rule is important for future work.