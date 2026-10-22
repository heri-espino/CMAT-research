# 19 — Shapley predictive importance (exploratory)

Exact grouped Shapley attribution; no student microdata exported.
Attributions represent **model fit or predictive skill**, not causal effects.
The player blocks are attendance frequency, degree, and professor-period.
The R² and McFadden pseudo-R² columns have different denominators and
must not be compared as if they were the same quantity.

## In-sample decompositions for all 12 historical specifications

| Outcome | Method | Model | Block | Contribution | Total fit | Share | Status |
|---|---|---|---|---:|---:|---:|---|
| Z_GRADE_PRIMARY | Z_OLS | A | attendance | 0.01753 | 0.01753 | 1.00000 | valid |
| Z_GRADE_PRIMARY | Z_OLS | B | attendance | 0.01671 | 0.05099 | 0.32776 | valid |
| Z_GRADE_PRIMARY | Z_OLS | B | degree | 0.03428 | 0.05099 | 0.67224 | valid |
| Z_GRADE_PRIMARY | Z_OLS | C | attendance | 0.01888 | 0.02022 | 0.93344 | valid |
| Z_GRADE_PRIMARY | Z_OLS | C | professor_period | 0.00135 | 0.02022 | 0.06656 | valid |
| Z_GRADE_PRIMARY | Z_OLS | D | attendance | 0.01803 | 0.05823 | 0.30964 | valid |
| Z_GRADE_PRIMARY | Z_OLS | D | degree | 0.03656 | 0.05823 | 0.62794 | valid |
| Z_GRADE_PRIMARY | Z_OLS | D | professor_period | 0.00363 | 0.05823 | 0.06242 | valid |
| PASS | PASS_LPM | A | attendance | 0.00902 | 0.00902 | 1.00000 | valid |
| PASS | PASS_LPM | B | attendance | 0.00846 | 0.04682 | 0.18076 | valid |
| PASS | PASS_LPM | B | degree | 0.03836 | 0.04682 | 0.81924 | valid |
| PASS | PASS_LPM | C | attendance | 0.01389 | 0.13764 | 0.10090 | valid |
| PASS | PASS_LPM | C | professor_period | 0.12375 | 0.13764 | 0.89910 | valid |
| PASS | PASS_LPM | D | attendance | 0.01331 | 0.17182 | 0.07747 | valid |
| PASS | PASS_LPM | D | degree | 0.03656 | 0.17182 | 0.21277 | valid |
| PASS | PASS_LPM | D | professor_period | 0.12195 | 0.17182 | 0.70976 | valid |
| PASS | PASS_LOGIT | A | attendance | 0.00861 | 0.00861 | 1.00000 | valid |
| PASS | PASS_LOGIT | B | attendance | 0.00823 | 0.03981 | 0.20682 | valid |
| PASS | PASS_LOGIT | B | degree | 0.03157 | 0.03981 | 0.79318 | valid |
| PASS | PASS_LOGIT | C | attendance | 0.01363 | 0.12741 | 0.10699 | valid |
| PASS | PASS_LOGIT | C | professor_period | 0.11378 | 0.12741 | 0.89301 | valid |
| PASS | PASS_LOGIT | D | attendance | 0.01330 | 0.16004 | 0.08307 | valid |
| PASS | PASS_LOGIT | D | degree | 0.03227 | 0.16004 | 0.20163 | valid |
| PASS | PASS_LOGIT | D | professor_period | 0.11448 | 0.16004 | 0.71530 | valid |

## Out-of-professor-period prediction (five-fold GroupKFold)

Held-out groups never appear in training. Only attendance and degree can
enter these predictions; an unseen professor-period fixed effect cannot
be estimated. Baseline is the training-fold average in each fold.

| Outcome | Block | Contribution to held-out skill | Full held-out skill |
|---|---|---:|---:|
| Z_GRADE_PRIMARY | attendance | 0.01509 | 0.01848 |
| Z_GRADE_PRIMARY | degree | 0.00339 | 0.01848 |
| PASS | attendance | 0.00536 | 0.01761 |
| PASS | degree | 0.01225 | 0.01761 |

For PASS, the held-out metric is Brier skill (larger is better),
not an odds ratio, p-value, or classical OLS R².
Held-out scores and Shapley values may be negative when predictions
are worse than the training-fold baseline.

## Essential restrictions

- Z is standardized within professor-period and imputes adverse states;
  the dependent variable itself is not a directly available early grade.
- Full-semester visits are measured contemporaneously with final grades;
  this is **retrospective prediction**, not a semester-start forecast.
- Prior mathematical achievement, diagnostic tests, motivation, and
  socioeconomic resources are not included: this experiment cannot
  identify the most important determinant of grades in general.
- Correlated predictors share credit by convention, not causally.
- The full logistic model previously lacked valid clustered inference;
  descriptive pseudo-R² here cannot repair that problem.
- Do not replace the Paper 2.1 Wald/Holm hypothesis tests with these
  exploratory importance rankings.
