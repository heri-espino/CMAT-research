# Paper 2.1 — scientific context

CMAT is UDLAP's mathematics support centre. Its visit records can be matched to the academic period of students' first eligible Matemáticas Universitarias attempt; they do not measure learning gains or the duration or reasons for attending.

**Question:** do adjusted final performance and the probability of passing differ by recorded attendance frequency after explicit family-wise multiplicity adjustment? Separate first use (0 vs any) from the distribution of counts among users.

**Population:** 6,627 students, 190 instructor-period grading groups, 1,234 positive-frequency attendees. Outcome-blind grouping: `1/2/3/4/5/6+`, with finer tail `6/7+` as a subsequently reported sensitivity. The historical PPA participation option involving three visits is contextual, not a causal treatment threshold.

**Outcomes:** instructor-period standardised final Z with documented adverse-outcome coding, and binary PASS (numeric ≥7.5). A numeric-only grade sensitivity has a different conditioning population.

**Methods:** fixed effects instructor–period and degree, cluster-robust Wald omnibus and pairwise contrasts, Holm within prespecified outcome/specification families. Contrast families: positive 6+ (15), finer positive 7+ (21), full including 0 (28). An instructor-level clustering sensitivity is reported.

**Interpretation:** no causal assignment, no equivalence inferred from nonrejection, no claim of a regular improvement with every additional visit.

**Sources:** `paper/docs/analysis/ANALYSIS_PLAN.md`, `VISIT_GROUPING_DECISION.md`, `results/paper21/tables/`, `notes/`, `paper/sections/`.