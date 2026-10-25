# 22 — Follow-up questions: exploratory results

Institutionally authorized Paper 2.1 first-eligible MU cohort.
All outputs are aggregated. These analyses are observational, not causal.

## 1. Degree mixing within professor-period contexts

- Mixed contexts: 190/190 (100.0%).
- Students in mixed contexts: 6627 (100.0%).
- Incremental descriptive in-sample Z R² for degree within mixed contexts: 0.0380.

Classroom overlap and within-mixed-class fit alone cannot establish
self-selection into mathematics-intensive degrees or causal programme effects.

## 2. First visit versus additional visits (piecewise working model)

Z uses OLS units of SD; PASS uses LPM coefficients in probability units
(multiply by 100 for percentage points). Both have clustered uncertainty
at professor-period and programme/classroom covariates.
Holm correction here covers **two predeclared terms per outcome**, not
the original 15/21/28 attendance-pair families.

| Outcome | Term | Coefficient | Nominal CI95 | Holm p |
|---|---|---:|---|---:|
| Z_GRADE_PRIMARY | ANY_VISIT | 0.3066 | [0.2335, 0.3796] | 0.0000 |
| Z_GRADE_PRIMARY | EXTRA_VISITS_CAPPED_7 | 0.0361 | [0.0081, 0.0640] | 0.0114 |
| PASS | ANY_VISIT | 0.1192 | [0.0846, 0.1539] | 0.0000 |
| PASS | EXTRA_VISITS_CAPPED_7 | 0.0223 | [0.0089, 0.0356] | 0.0010 |

ANY_VISIT is the fitted 0→1 contrast. EXTRA_VISITS_CAPPED_7
models a **single linear per-visit slope** for the increase 1→2→...→7+,
so the model-implied 1→7+ difference is six times that slope.
7+ is top-coded, so this is a model assumption rather than a measured
equal-increment response. The historical Holm contrasts remain primary.

## 3. Observed numeric final grades and passing boundary

| Visits | Numeric N | P10 | Median | P90 | Numeric PASS rate | Near 7.5 (±0.5) |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 4470 | 6.29 | 9.00 | 10.00 | 87.0% | 14.0% |
| 1 | 434 | 7.70 | 9.20 | 10.00 | 96.5% | 15.7% |
| 2-6 | 529 | 7.60 | 9.10 | 10.00 | 96.0% | 17.6% |
| 7+ | 93 | 7.70 | 8.90 | 10.00 | 96.8% | 18.3% |

| Visits | Total N | Numeric N | Administrative share | Full-cohort PASS |
|---|---:|---:|---:|---:|
| 0 | 5393 | 4470 | 17.1% | 72.1% |
| 1 | 517 | 434 | 16.1% | 81.0% |
| 2-6 | 616 | 529 | 14.1% | 82.5% |
| 7+ | 101 | 93 | 7.9% | 89.1% |

These grade quantiles **exclude BA, BV and RT**, whereas primary Z
imputes adverse states and PASS treats them as nonpassing.
Group comparisons above are unadjusted descriptive summaries; they
cannot isolate CMAT effects from self-selection or differences in enrolment.

## Research interpretation / non-inferences

- Degree allocation and mathematical preparation remain unmeasured hypotheses.
- One fitted visit coefficient does not identify a causal first-visit effect.
- A weak extra-visit coefficient does not establish equivalence or saturation.
- Descriptive quantiles are not fixed-effect-adjusted quantile regression.
- No claim that a professor grades more easily is identified here.
- Neither this experiment nor Shapley is a true start-of-term forecast.
