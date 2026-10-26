# 24 — Attendance curve comparison (exploratory; generated)

Four outcomes: imputed professor-period Z, PASS LPM, numeric-only Z
and observed numeric final grade (last two condition on numeric results).
No CMAT causal effects are estimated. All confidence intervals use
professor-period clustered sandwich covariance.

## Model comparison

All in-sample shapes use degree and professor-period fixed effects.
Five-fold grouped CV **excludes** professor-period fixed effects because
test contexts were not observed in training; it includes degree, and
compares shape generalization using squared error or binary Brier.
In-sample AIC/BIC and out-of-context CV score are not the same estimand.

| Outcome | Shape | R² in sample | AIC | Held-out skill | CV error |
|---|---|---:|---:|---:|---:|
| Z_GRADE_PRIMARY | linear | 0.0581 | 18753.4 | 0.0169 | 0.9549 |
| Z_GRADE_PRIMARY | log | 0.0580 | 18754.0 | 0.0168 | 0.9550 |
| Z_GRADE_PRIMARY | sqrt | 0.0580 | 18753.6 | 0.0168 | 0.9550 |
| Z_GRADE_PRIMARY | saturating | 0.0579 | 18754.4 | 0.0167 | 0.9551 |
| Z_GRADE_PRIMARY | categories | 0.0582 | 18762.3 | 0.0163 | 0.9555 |
| PASS | linear | 0.1717 | 7166.6 | 0.0037 | 0.1916 |
| PASS | log | 0.1715 | 7168.3 | 0.0037 | 0.1916 |
| PASS | sqrt | 0.1716 | 7167.2 | 0.0037 | 0.1916 |
| PASS | saturating | 0.1714 | 7169.2 | 0.0036 | 0.1916 |
| PASS | categories | 0.1718 | 7175.7 | 0.0027 | 0.1918 |
| Z_GRADE_COMPLETE_CASE | linear | 0.0535 | 15694.9 | 0.0028 | 0.9631 |
| Z_GRADE_COMPLETE_CASE | log | 0.0535 | 15694.9 | 0.0027 | 0.9631 |
| Z_GRADE_COMPLETE_CASE | sqrt | 0.0535 | 15694.9 | 0.0028 | 0.9631 |
| Z_GRADE_COMPLETE_CASE | saturating | 0.0535 | 15694.9 | 0.0027 | 0.9631 |
| Z_GRADE_COMPLETE_CASE | categories | 0.0539 | 15702.5 | 0.0028 | 0.9631 |
| GRADE_NUMERIC | linear | 0.1534 | 23517.2 | 0.0119 | 4.3941 |
| GRADE_NUMERIC | log | 0.1535 | 23517.1 | 0.0119 | 4.3943 |
| GRADE_NUMERIC | sqrt | 0.1535 | 23517.1 | 0.0119 | 4.3942 |
| GRADE_NUMERIC | saturating | 0.1535 | 23517.0 | 0.0119 | 4.3943 |
| GRADE_NUMERIC | categories | 0.1537 | 23525.7 | 0.0116 | 4.3956 |

## Raw attendance-frequency means (unadjusted)

| Outcome | Visits | N | Clusters | Mean | 95% clustered CI |
|---|---|---:|---:|---:|---|
| Z_GRADE_PRIMARY | 0 | 5393 | 190 | -0.061 | [-0.072, -0.050] |
| Z_GRADE_PRIMARY | 1 | 517 | 152 | 0.219 | [0.145, 0.293] |
| Z_GRADE_PRIMARY | 2 | 245 | 114 | 0.247 | [0.155, 0.339] |
| Z_GRADE_PRIMARY | 3 | 170 | 84 | 0.278 | [0.154, 0.402] |
| Z_GRADE_PRIMARY | 4 | 96 | 69 | 0.267 | [0.105, 0.429] |
| Z_GRADE_PRIMARY | 5 | 55 | 40 | 0.382 | [0.226, 0.538] |
| Z_GRADE_PRIMARY | 6 | 50 | 36 | 0.288 | [0.021, 0.554] |
| Z_GRADE_PRIMARY | 7+ | 101 | 57 | 0.457 | [0.317, 0.598] |
| PASS | 0 | 5393 | 190 | 0.721 | [0.695, 0.748] |
| PASS | 1 | 517 | 152 | 0.810 | [0.769, 0.851] |
| PASS | 2 | 245 | 114 | 0.808 | [0.753, 0.863] |
| PASS | 3 | 170 | 84 | 0.818 | [0.746, 0.889] |
| PASS | 4 | 96 | 69 | 0.865 | [0.784, 0.945] |
| PASS | 5 | 55 | 40 | 0.855 | [0.770, 0.939] |
| PASS | 6 | 50 | 36 | 0.820 | [0.684, 0.956] |
| PASS | 7+ | 101 | 57 | 0.891 | [0.828, 0.955] |
| Z_GRADE_COMPLETE_CASE | 0 | 4467 | 189 | -0.056 | [-0.068, -0.045] |
| Z_GRADE_COMPLETE_CASE | 1 | 433 | 147 | 0.256 | [0.192, 0.321] |
| Z_GRADE_COMPLETE_CASE | 2 | 209 | 105 | 0.193 | [0.109, 0.277] |
| Z_GRADE_COMPLETE_CASE | 3 | 144 | 80 | 0.326 | [0.257, 0.395] |
| Z_GRADE_COMPLETE_CASE | 4 | 84 | 63 | 0.145 | [-0.002, 0.292] |
| Z_GRADE_COMPLETE_CASE | 5 | 49 | 36 | 0.232 | [0.130, 0.335] |
| Z_GRADE_COMPLETE_CASE | 6 | 43 | 31 | 0.192 | [0.005, 0.379] |
| Z_GRADE_COMPLETE_CASE | 7+ | 93 | 55 | 0.238 | [0.116, 0.359] |
| GRADE_NUMERIC | 0 | 4470 | 190 | 8.293 | [8.174, 8.413] |
| GRADE_NUMERIC | 1 | 434 | 148 | 8.887 | [8.746, 9.028] |
| GRADE_NUMERIC | 2 | 209 | 105 | 8.783 | [8.613, 8.952] |
| GRADE_NUMERIC | 3 | 144 | 80 | 9.092 | [8.916, 9.268] |
| GRADE_NUMERIC | 4 | 84 | 63 | 8.867 | [8.661, 9.072] |
| GRADE_NUMERIC | 5 | 49 | 36 | 8.808 | [8.565, 9.051] |
| GRADE_NUMERIC | 6 | 43 | 31 | 8.856 | [8.557, 9.155] |
| GRADE_NUMERIC | 7+ | 93 | 55 | 8.823 | [8.567, 9.078] |

## Adjusted category contrasts and their uncertainty

The unrestricted eight-category model does NOT assume a monotone trend.
Its 5→6 interval is the relevant check for the observed late dip.
Intervals are nominal unless explicitly labeled Holm.

| Outcome | Visits versus zero | Difference | 95% clustered CI |
|---|---|---:|---|
| Z_GRADE_PRIMARY | 1 | 0.305 | [0.222, 0.389] |
| Z_GRADE_PRIMARY | 2 | 0.360 | [0.262, 0.457] |
| Z_GRADE_PRIMARY | 3 | 0.373 | [0.248, 0.499] |
| Z_GRADE_PRIMARY | 4 | 0.356 | [0.187, 0.525] |
| Z_GRADE_PRIMARY | 5 | 0.530 | [0.346, 0.715] |
| Z_GRADE_PRIMARY | 6 | 0.413 | [0.152, 0.674] |
| Z_GRADE_PRIMARY | 7+ | 0.549 | [0.398, 0.701] |
| PASS | 1 | 0.121 | [0.084, 0.159] |
| PASS | 2 | 0.146 | [0.095, 0.198] |
| PASS | 3 | 0.142 | [0.079, 0.206] |
| PASS | 4 | 0.194 | [0.114, 0.274] |
| PASS | 5 | 0.218 | [0.119, 0.317] |
| PASS | 6 | 0.205 | [0.079, 0.330] |
| PASS | 7+ | 0.266 | [0.191, 0.341] |
| Z_GRADE_COMPLETE_CASE | 1 | 0.341 | [0.266, 0.417] |
| Z_GRADE_COMPLETE_CASE | 2 | 0.299 | [0.200, 0.398] |
| Z_GRADE_COMPLETE_CASE | 3 | 0.419 | [0.342, 0.497] |
| Z_GRADE_COMPLETE_CASE | 4 | 0.236 | [0.073, 0.399] |
| Z_GRADE_COMPLETE_CASE | 5 | 0.388 | [0.239, 0.537] |
| Z_GRADE_COMPLETE_CASE | 6 | 0.288 | [0.090, 0.486] |
| Z_GRADE_COMPLETE_CASE | 7+ | 0.311 | [0.171, 0.452] |
| GRADE_NUMERIC | 1 | 0.678 | [0.529, 0.827] |
| GRADE_NUMERIC | 2 | 0.672 | [0.481, 0.862] |
| GRADE_NUMERIC | 3 | 0.886 | [0.707, 1.065] |
| GRADE_NUMERIC | 4 | 0.652 | [0.409, 0.895] |
| GRADE_NUMERIC | 5 | 0.827 | [0.529, 1.125] |
| GRADE_NUMERIC | 6 | 0.879 | [0.508, 1.251] |
| GRADE_NUMERIC | 7+ | 0.722 | [0.404, 1.039] |

## Unrestricted adjacent contrasts: 7-comparison Holm family / outcome

| Outcome | Pair | Estimate | Nominal CI95 | Holm p |
|---|---|---:|---|---:|
| Z_GRADE_PRIMARY | 0->1 | 0.305 | [0.222, 0.389] | 0.0000 |
| Z_GRADE_PRIMARY | 1->2 | 0.055 | [-0.070, 0.179] | 1.0000 |
| Z_GRADE_PRIMARY | 2->3 | 0.013 | [-0.118, 0.145] | 1.0000 |
| Z_GRADE_PRIMARY | 3->4 | -0.017 | [-0.191, 0.157] | 1.0000 |
| Z_GRADE_PRIMARY | 4->5 | 0.174 | [-0.047, 0.395] | 0.7347 |
| Z_GRADE_PRIMARY | 5->6 | -0.117 | [-0.433, 0.199] | 1.0000 |
| Z_GRADE_PRIMARY | 6->7+ | 0.136 | [-0.158, 0.430] | 1.0000 |
| PASS | 0->1 | 0.121 | [0.084, 0.159] | 0.0000 |
| PASS | 1->2 | 0.025 | [-0.032, 0.082] | 1.0000 |
| PASS | 2->3 | -0.004 | [-0.074, 0.066] | 1.0000 |
| PASS | 3->4 | 0.052 | [-0.045, 0.148] | 1.0000 |
| PASS | 4->5 | 0.024 | [-0.088, 0.136] | 1.0000 |
| PASS | 5->6 | -0.013 | [-0.166, 0.140] | 1.0000 |
| PASS | 6->7+ | 0.062 | [-0.083, 0.207] | 1.0000 |
| Z_GRADE_COMPLETE_CASE | 0->1 | 0.341 | [0.266, 0.417] | 0.0000 |
| Z_GRADE_COMPLETE_CASE | 1->2 | -0.043 | [-0.156, 0.071] | 1.0000 |
| Z_GRADE_COMPLETE_CASE | 2->3 | 0.121 | [0.013, 0.228] | 0.1407 |
| Z_GRADE_COMPLETE_CASE | 3->4 | -0.183 | [-0.342, -0.025] | 0.1407 |
| Z_GRADE_COMPLETE_CASE | 4->5 | 0.152 | [-0.036, 0.340] | 0.4500 |
| Z_GRADE_COMPLETE_CASE | 5->6 | -0.100 | [-0.309, 0.109] | 1.0000 |
| Z_GRADE_COMPLETE_CASE | 6->7+ | 0.023 | [-0.204, 0.250] | 1.0000 |
| GRADE_NUMERIC | 0->1 | 0.678 | [0.529, 0.827] | 0.0000 |
| GRADE_NUMERIC | 1->2 | -0.006 | [-0.216, 0.203] | 1.0000 |
| GRADE_NUMERIC | 2->3 | 0.214 | [-0.000, 0.428] | 0.3005 |
| GRADE_NUMERIC | 3->4 | -0.234 | [-0.474, 0.006] | 0.3005 |
| GRADE_NUMERIC | 4->5 | 0.176 | [-0.163, 0.514] | 1.0000 |
| GRADE_NUMERIC | 5->6 | 0.052 | [-0.369, 0.473] | 1.0000 |
| GRADE_NUMERIC | 6->7+ | -0.158 | [-0.595, 0.280] | 1.0000 |

## Interpretive boundaries

- Log and square-root fits *impose* declining additional-visit increments.
  A favorable CV score does not prove the underlying causal response is concave.
- The saturating exponential uses lambda=0.5 fixed in advance; its
  horizontal limit is a chosen functional form, not a discovered plateau.
- The log coefficient begins at visit 1: it cannot by itself identify
  a treatment effect of an exogenously assigned first CMAT visit.
- Group 7+ combines seven and more visits, not exact seven.
- Original numeric final grades have an upper bound of 10 and
  numeric-only subsets exclude BA/BV/RT, whereas primary Z imputes them.
- Group-count and professor-period overlap are highly unequal; the
  5→6 contrast may have much greater uncertainty than 0→1.
- This exploratory family (seven adjacent contrasts per outcome)
  does not replace earlier 15/21/28-comparison Holm inferences.
- Recorded visits accumulate over the same term as outcomes; motivation,
  prior preparation, persistence and administrative outcomes may confound
  the association. No early-warning interpretation is justified.

Figures are at results/paper21/figures/attendance_curves/*.png.
