# 23 — Registered exploratory attendance-curve comparison

**Created 2026-10-22. Code committed but institutional data not run.** This is a new exploratory sensitivity prompted by inspection of prior grade ridgelines, first-vs-additional attendance contrasts and sparse exact-six visits. It is **not** a prespecified confirmatory analysis and does not revise Paper 2.1's original Wald/Holm families.

## Motivation

The observed adjusted difference between zero and one CMAT visit is comparatively large. Within attendees, a simple constant-per-additional-visit slope was positive in an exploratory two-part model, but the eight-category estimates have considerable uncertainty, especially at exactly six visits. We want to ask whether a *working curve with diminishing increments* describes the data better than a straight additional-visit line, while retaining a fully flexible nonmonotone reference.

**Research hypothesis, not an accepted finding:** outcomes may exhibit a first-visit discontinuity in their association with recorded attendance, followed by smaller incremental associations as further visits accumulate.

## Outcomes and populations

The four separate analyses deliberately distinguish:
1. `Z_GRADE_PRIMARY` (N=6,627): imputed adverse administrative outcomes and then standardized within professor-period. Directly comparable with historical Paper 2.1 Z regression.
2. `PASS` (N=6,627): binary 0/1 LPM, with all BA/BV/RT coded non-PASS.
3. `Z_GRADE_COMPLETE_CASE`: standardized observed numeric grade only (no imputed states), among students with computable numeric-only Z.
4. `GRADE_NUMERIC`: unstandardized observed numerical grade (0–10 scale), among students with a numeric final grade.

The last two outcomes are conditioned on obtaining numeric grades; their sample is not equivalent to the complete cohort. Differences can reflect adverse administrative-outcome selection rather than improved math learning. All visit categories use `0/1/2/3/4/5/6/7+`; the 7+ category is top-coded.

## Model families

All models fit **OLS** to their continuous outcomes and **LPM/OLS** to PASS, including professor-period fixed effects and degree-programme controls, and estimate SEs robustly clustered by professor-period.

Let `k = min(recorded visits, 7)` and `I(k>0)` indicate any attendance. Compare five *fixed* shape specifications:

- **Linear additional-visit slope:** `Y = controls + a*I(k>0) + b*max(k-1,0) + e`.
- **Logarithmic diminishing-increment:** `Y = controls + a*I(k>0) + b*log(max(k,1)) + e`.
- **Square-root diminishing-increment:** `Y = controls + a*I(k>0) + b*(sqrt(max(k,1))-1) + e`.
- **Saturating exponential:** `Y = controls + a*I(k>0) + b*(1-exp(-0.5*max(k-1,0))) + e`. The decay constant 0.5 is pre-fixed, not optimized on observed grades.
- **Unrestricted categorical reference:** `Y = controls + C(visit_group; ref=0) + e` with seven independent contrasts; can show 5 > 6 without violating an assumed curve.

These parameterizations **do not force positive coefficients**; a positive value of `b` is necessary for the proposed increasing-with-diminishing-increments pattern. Even if a curve fits better, the empirical question is *shape of association*, not what another visit would causally do to a student.

## Outputs, uncertainty, diagnostic validity

Per outcome:
- Observed raw means by category, counts of eligible students and contexts, and **cluster-robust** mean confidence intervals.
- Adjusted 0-to-each-positive-category contrasts and **nominal** cluster-robust 95% confidence intervals for each of five shape candidates.
- Seven adjusted adjacent contrasts (0→1 through 6→7+) with cluster-robust intervals from the *unrestricted* categorical reference; Holm over these seven adjacent comparisons **within each outcome**, separately from all previous 15/21/28 families. Highlight 5→6 and its uncertainty without assuming a plateau.
- In-sample R²/AIC/BIC for the full fixed-effect fits on **the same observations within each outcome**.
- Five-fold professor-period-held-out squared prediction error (PASS: clipped-LPM Brier; continuous: MSE) and skill relative to training-fold mean baseline. These predictive fits intentionally **exclude professor-period FE** because they cannot be extrapolated into held-out contexts; they preserve degree and the functional attendance terms. This CV comparison answers a different question from the fixed-effect in-sample analysis. It remains retrospective because attendance is only fully known at term end.
- Four PNG figures, each with two panels: observed mean with 95% clustered CI, and the fitted 0-reference adjusted curves with category-model CI and log-model band. **They are statistical plots of actual results, not visual predictions or images generated without data.**

Avoid ranking shapes solely by the best in-sample R²: unrestricted dummy models have many more parameters and mechanical fit advantages. Compare AIC/BIC and held-out errors, and keep the actual unrestricted coefficients visible. Do not treat a difference of CV skill as significant without repeated or clustered uncertainty analysis. If log/sqrt/saturating performs favorably, that is compatibility with concavity, **not proof of a naturally occurring causal plateau**.

### Known limits

- **Top-coding** lumps visits >=7; the x-axis label 7+ cannot be interpreted as exactly 7.
- **Sparse upper frequencies** yield imprecise local differences: an observed 5→6 reversal can be sampling noise or selection.
- **Grade ceiling** at 10 and differential administrative outcomes make raw numeric means and complete-case Z sensitive to population composition.
- **Professor-period standardized Z** is constructed with reference to final grades within every context; its held-out predictive skill is retrospective and may not represent a deployable target.
- **No timing** of visits relative to first course difficulties: stronger students may attend, weaker students may seek help, and persisting students have more opportunity to accumulate visits.
- The functional families were proposed after seeing aggregate outcomes; no multiple-model specification search is a confirmation procedure.

## Reproducible execution: Windows 11 Conda PowerShell

```powershell
cd C:\Users\175199\CMAT-research
conda activate cmat-research
git pull --ff-only origin research/paper21-shapley-predictive-importance
python -m pytest -q cmat_analysis/tests/test_paper21_attendance_curves.py
python code/run_paper21_attendance_curves.py --check
python code/run_paper21_attendance_curves.py
Get-Content .\notes\24_ATTENDANCE_CURVE_RESULTS.md -Encoding UTF8
```

Institutional workbooks stay under private local `data/raw/` as in previous experiments. Existing controls and grade definitions are imported, not duplicated. No CSV or PNG is written by the `--check` option.

**Generated after a successful authorized run:**
- `notes/24_ATTENDANCE_CURVE_RESULTS.md`
- `results/paper21/tables/attendance_curves/unadjusted_means_cluster_ci.csv`
- `results/paper21/tables/attendance_curves/model_comparison_in_sample.csv`
- `results/paper21/tables/attendance_curves/adjusted_curves_cluster_ci.csv`
- `results/paper21/tables/attendance_curves/adjacent_differences_holm.csv`
- `results/paper21/tables/attendance_curves/group_heldout_shape_cv.csv`
- `results/paper21/figures/attendance_curves/{imputed_z,pass_lpm,numeric_only_z,observed_numeric_grade}_attendance_curve.png`

Before pushing, audit all aggregate tables, plot ticks, group counts and sample changes; never commit records, student/teacher IDs, secrets or raw workbooks. Once validated, update `notes/20_RESEARCH_TRACKER.md` with *observed* empirical values and code SHA. Do not add new exploratory tests directly into the frozen paper manuscript.
