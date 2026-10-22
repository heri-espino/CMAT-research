# CMAT research tracker — completed evidence and next experiments

Updated 2026-10-22. This is a **cross-study navigation index**, not a newly fitted model or a replacement for Paper 2.1's prespecified inferential plan. It intentionally distinguishes the old Paper 2.1 GMM study from the unexecuted Paper 2.2.2 modality extension.

## 1 — Attendance frequency, PASS and Z: Wald tests and Holm adjustment — COMPLETED

**Purpose:** Estimate adjusted differences in final grade Z (OLS, in SD units) and binary PASS (LPM, probability points; logistic sensitivity) across attendance categories; account for professor-period and degree.

**Main evidence:** [Paper 2.1 frequency results](05_RESULTADOS_Y_PROCEDENCIA.md), [controlled adjustment sensitivity synthesis](18_SINTESIS_MODELOS_CONTROLES_PASS_Z.md); [Z 4×OLS detail](17_RESULTADOS_OLS_ZSCORE_CONTROLES.md), [PASS 4×LPM/logit detail](15_RESULTADOS_COMPARACION_LPM_LOGIT_CONTROLES.md), [study protocol](../paper/docs/analysis/ANALYSIS_PLAN.md).

**Verified observations:**
- 6,627 eligible first MU attempts, 190 professor-period contexts; 1,234 participants in CMAT.
- Adjusted **any attendance vs no attendance** benchmark: **+0.361 Z SD**, **+15.29 PASS percentage points** (observational).
- **Primary positive-only family** `1/2/3/4/5/6+`: 15 Holm-adjusted pairs per outcome; no significant pair. The distinct positive-only fine-tail 21-pair sensitivity also rejected no pairs.
- **Exploratory zero-inclusive 8-group 28-pair full-sample model** D: 0→1 **+0.305 Z**, Holm p<0.0001, and **+12.13 PASS pp**, Holm p<0.0001; 1→7+ **+0.244 Z**, Holm p=0.1623, and **+14.49 PASS pp**, Holm p=0.0206.
- 1→7+ PASS is **specification-sensitive**: no Holm rejection for LPM A/B or logit C; logit D cluster-robust inference is unavailable. Not confirmatory evidence of dose response. No 3→4 significance after Holm.
- Keep the 15-, 21-, and 28-pair correction families distinct; no absence-of-effect/equivalence or causal claims.

## 2 — Expectation–maximization (EM) / Gaussian mixtures for **two Z definitions** — COMPLETED HISTORICALLY, MODALITY UNRESOLVED

**Location:** The historical Paper 2.1 files are retained as inherited research material on [`paper/paper2.2.2-distributional-heterogeneity`](https://github.com/heri-espino/CMAT-research/tree/paper/paper2.2.2-distributional-heterogeneity), specifically [MIXTURE_ANALYSIS_RESULTS.md](https://github.com/heri-espino/CMAT-research/blob/paper/paper2.2.2-distributional-heterogeneity/paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md), [mixture plan](https://github.com/heri-espino/CMAT-research/blob/paper/paper2.2.2-distributional-heterogeneity/paper/docs/analysis/MIXTURE_ANALYSIS_PLAN.md), and [historical runner](https://github.com/heri-espino/CMAT-research/blob/paper/paper2.2.2-distributional-heterogeneity/code/run_paper21_mixture.py). This research branch does **not** contain or rerun the historical EM runner.

**Different outcomes (do not conflate):**
- `Z_GRADE_COMPLETE_CASE`: observed **numeric** final grades only, standardized within professor-period; **primary for shape/model-adequacy investigation**.
- `Z_GRADE_PRIMARY`: imputed adverse administrative states BA/BV/RT, then standardized within professor-period; **sensitivity** for grade imputation.

**Verified historical observations:**
- EM fits univariate GMM K=1/2/3 by visit category; BIC/ICL, bootstrap K1–K2, skew-normal alternative, repeated held-out log predictive density, component weights and posterior administrative-state composition.
- One Gaussian frequently underfits; **K=2 does not prove two density modes or two latent student types**.
- Against a one-component *skew-normal* on numeric-only Z, the two-Gaussian fit is supported most consistently for **0, 1 and 2 visits**; for 3/4/6+ skewness is often adequate, and 5 is inconclusive.
- For imputed Z, K=2 is preferred across the historical pooled-tail frequency groups; the lower mixture component is substantially enriched in administrative outcomes, especially BV. This can be induced or sharpened by outcome construction.
- Exact 6 / 7+ tail re-estimation is exploratory and sparse: a 7+ numeric-only fitted component near 1% weight with near-zero SD is a tail/degeneracy warning, not proof of a student subpopulation.
- Historical manuscript/results report completed institutional runs and provenance; **Paper 2.2.2 itself is still design-stage and has not validated additional unimodality tests**. See [2.2.2 status](https://github.com/heri-espino/CMAT-research/blob/paper/paper2.2.2-distributional-heterogeneity/paper/docs/results/RESULTS_STATUS_222.md).

## 3 — Grouped Shapley / R² and held-out predictive skill — COMPLETED

**Files:** [full study report](19_SHAPLEY_PREDICTIVE_IMPORTANCE.md), [12-model contributions](../results/paper21/tables/shapley_importance/in_sample_shapley_12_models.csv), [held-out contributions](../results/paper21/tables/shapley_importance/out_of_context_shapley.csv), [runner](../code/run_paper21_shapley_importance.py), [tests](../cmat_analysis/tests/test_paper21_shapley_importance.py), [protocol](19_SHAPLEY_PROTOCOL.md).

**User-run verification, 2026-10-22:** Windows 11 Conda Python 3.14.8; **7 synthetic tests passed** and institutional-data runner completed, writing the four aggregate CSVs and report, which were verified on the remote branch. Same N=6,627; 190 clusters.

**Full model D grouped contributions**, as a **share of model fit**, NOT total variance and NOT causal effects:

| Outcome and metric | Total model fit | Attendance share | Degree share | Professor-period share |
|---|---:|---:|---:|---:|
| Z OLS, in-sample R² | 0.05823 | 30.96% | 62.79% | 6.24% |
| PASS LPM, in-sample R² | 0.17182 | 7.75% | 21.28% | 70.98% |
| PASS logit, McFadden pseudo-R² | 0.16004 | 8.31% | 20.16% | 71.53% |

**Group-held-out five-fold prediction**, training without the held-out professor-periods and **using only attendance and degree**:
- Z squared-error skill vs training-fold-mean baseline: **0.01848**; Shapley attendance 0.01509, degree 0.00339.
- PASS Brier skill vs baseline: **0.01761**; Shapley attendance 0.00536, degree 0.01225.
- These skill metrics are distinct, small, and use **end-of-semester attendance**, so they are *retrospective* rather than start-of-semester forecasts.
- Z is standardized **within professor-period**: the near-zero classroom-only explanatory power is mechanical. Professor–degree allocation and degree-based selection remain hypotheses, not identified mechanisms.

## 4 — Next hypotheses and code — IMPLEMENTED, INSTITUTIONAL RESULTS PENDING

**Runner:** [`code/run_paper21_followup_questions.py`](../code/run_paper21_followup_questions.py); **design and caveats:** [`notes/21_FOLLOWUP_QUESTIONS_PROTOCOL.md`](21_FOLLOWUP_QUESTIONS_PROTOCOL.md); **synthetic tests:** [`cmat_analysis/tests/test_paper21_followup_questions.py`](../cmat_analysis/tests/test_paper21_followup_questions.py).

1. **Degree–classroom overlap:** How often do professor-period contexts mix degree programmes? Within mixed contexts, how much extra *descriptive in-sample* Z R² does programme add beyond attendance and classroom FE?
2. **Any attendance versus additional visits:** Fit a predeclared two-part piecewise linear model for PASS and imputed Z: `ANY_VISIT` (0→1) and `EXTRA_VISITS_CAPPED_7` (linear 1→7+), controlling for professor-period FE and degree with cluster-robust SE. Correct the two attendance-term p-values by Holm per outcome; these are observational *working-model contrasts*, not a causal dose-response or a substitute for the historical 15/21/28-pair analyses.
3. **Numeric grade distribution and passing boundary:** Describe observed-numeric final-grade quantiles, numeric passing rates and concentration around 7.5 by non-overlapping coarse visit groups, and report administrative-state shares separately. This is intentionally **descriptive and selected on having a numeric final grade**, not a fitted conditional-quantile treatment effect.

**Status:** code and synthetic tests can be run locally; **no new institutional-data estimates or empirical findings from these follow-ups are claimed in this document**. Keep resulting data under `results/paper21/tables/followup_questions/` and written report `notes/22_FOLLOWUP_QUESTIONS_RESULTS.md`. Do not copy or overwrite the scientific manuscript or any historical primary-result tables.

## Guardrails shared across all studies

- Grade/pass outcomes are observational and CMAT attendance is voluntary/contemporaneous; adjusting for programme and professor-period does not resolve unmeasured preparation or motivation.
- PASS uses numeric grade ≥7.5, treats BA/BV/RT as non-PASS and never imputes grades; imputed Z does impute those states; numeric grade summaries restrict to observed numerical records.
- No row-level data, professor IDs, student IDs, salts, assignment lists or sensitive small-group tables in GitHub.
- Preserve dates, code paths, branch, population and model specification with each analysis. New results require a completed authorized run and explicit validation.
