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

## Current subfolders

- `general/` — general/foundational Paper 1 literature.
- future: `incentives/` — incentive/removal/behavioural-intervention literature.
- future: additional subfolders only when they represent a scientific function, never an upload batch.