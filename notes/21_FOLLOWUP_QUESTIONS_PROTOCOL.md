# 21 — Exploratory follow-up protocol: programme overlap, CMAT participation, numeric grades

**Created 2026-10-22. Status: implementation committed; controlled-data results not yet generated or interpreted.** The synthesis and historical provenance are in [20_RESEARCH_TRACKER.md](20_RESEARCH_TRACKER.md). This research is **not** an update to Paper 2.1's prespecified Wald/Holm analysis.

## Design and sample

- First eligible MU attempt, same cohort/period-wide attendance and numerical grade/pass definitions as Paper 2.1.
- Require N=6,627 students and 190 professor-period contexts; do not automatically generalize beyond the matched period and subject.
- Controlled inputs via `cmat_analysis.config.study_config.get_study_config`. `--materias` and `--asesorias` explicitly select approved input paths.
- No identifiers, classroom-by-degree microcells, student-level scores, raw grade densities, or student-level rows are written.

## Q1 — Programme assignment and degree-mixing opportunities

Measure professor-period groups containing **more than one degree programme** and fraction of students in them. Record aggregate counts and the median number of programmes per group.

Within these *mixed contexts* only, fit:
1. `Z_GRADE_PRIMARY ~ C(VISIT_GROUP) + C(CLASSROOM_ID)`;
2. `Z_GRADE_PRIMARY ~ C(VISIT_GROUP) + C(CLASSROOM_ID) + C(CLAVECARRERA)`.

Report the difference in **in-sample R²** as a descriptive partial-fit diagnostic, not a significant or causal effect. Why mixed-only? When programme and classroom align perfectly, the programme effect is not separately identifiable from fixed classroom effects. The mixed-only subset is selected; do not compare its R² directly to the entire cohort's Shapley allocations as if the estimands were equal. Disentangling selection into a degree from earlier mathematical preparation requires pre-enrolment grades/exam information.

## Q2 — First visit versus additional visits

Fit two outcomes separately with OLS for continuous imputed Z and LPM for binary PASS:

`Y ~ ANY_VISIT + EXTRA_VISITS_CAPPED_7 + C(CLASSROOM_ID) + C(CLAVECARRERA)`.

The constructed columns are:

- `ANY_VISIT = 1(visits >= 1)`;
- `EXTRA_VISITS_CAPPED_7 = max(min(visits,7) - 1, 0)`.

Under the **piecewise linear model assumption**, the first term is the 0→1 adjusted difference and the second is the *constant assumed per-additional-visit slope* for 1→2 through 6→7+. The model-implied 1→7+ contrast equals 6 × the extra-visit slope. In reality 7+ is top-coded, so this is **not** the effect of exactly seven visits.

Estimate SE clustered by professor-period and nominal two-sided confidence intervals; apply Holm adjustment **only to these two exploratory attendance terms within each outcome**. This is a new, deliberately constrained working model: any p-value belongs to this two-term family and must **not** be transplanted into the previous 15/21/28 pairwise families. Check sensitivity later to nonlinear extra-visits and positivity/overlap. No causal first-visit, dose-response, treatment or plateau inference follows.

## Q3 — What happens to the observed numeric grade distribution near 7.5?

Only observed numeric final grades are included in the grade distribution; imputed adverse final states are explicitly excluded. Split into non-overlapping visit groups `0`, `1`, `2–6`, `7+` to avoid disclosing sparse exact-tail cells.

For each, output: numeric N, numeric mean, p10/p25/median/p75/p90, observed numeric PASS proportion, proportion of numeric grades in [7.0,8.0] inclusive (within half a point of the PASS threshold). Separately output totals, administrative-state fraction and full-cohort PASS fraction by the same visit groups. Minimum cohort support 30 per group; abort rather than releasing unsupported tiny groups.

These are **descriptive marginal summaries** of different outcomes/populations. They are not adjusted quantile regressions; grade quantiles conditional on retaining a numeric grade cannot resolve whether participating students differ in administrative withdrawals. If a quantile-regression follow-up is pursued, prespecify its target, FE/cluster uncertainty method, support checks and administrative-outcome selection handling.

## Running on Windows 11 / Conda

```powershell
git switch research/paper21-shapley-predictive-importance
git pull --ff-only origin research/paper21-shapley-predictive-importance
conda activate cmat-research
python -m pytest -q cmat_analysis/tests/test_paper21_followup_questions.py
python code/run_paper21_followup_questions.py --check
python code/run_paper21_followup_questions.py
Get-Content .\notes\22_FOLLOWUP_QUESTIONS_RESULTS.md -Encoding UTF8
```

Requires the same two **authorized private** academic/CMAT source workbooks as the Shapley runner; never upload or commit them.

**Expected outputs, after a successful controlled run:**
- `results/paper21/tables/followup_questions/degree_professor_period_overlap.csv`
- `results/paper21/tables/followup_questions/two_part_attendance_z_pass.csv`
- `results/paper21/tables/followup_questions/observed_numeric_grade_quantiles.csv`
- `results/paper21/tables/followup_questions/numeric_vs_administrative_composition.csv`
- `notes/22_FOLLOWUP_QUESTIONS_RESULTS.md`

The CLI refuses to overwrite the canonical Paper 2.1 results. Use an aggregate-disclosure review before pushing the new files. Record the code SHA, sample and outcome definitions with any later empirical report.
