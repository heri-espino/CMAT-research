# Protocol — grouped Shapley and prediction (Paper 2.1, exploratory)

**Status (21 October 2026):** implementation committed on a separate research branch. Institutional-data Shapley values and out-of-context scores **have not been computed or validated** in this session. This does not modify the manuscript's inferential specification.

## Question and notation

How much *explained variance* does each existing predictor group account for in the CMAT models, and do the predictors generalize to students in professor-period contexts not used in fitting?

Three **indivisible** feature groups (players): attendance frequency (8 categories, `VISIT_GROUP`), degree programme (`CLAVECARRERA`), professor-period (`CLASSROOM_ID`). A categorical factor is **one** player, regardless of its number of dummy columns. Degree and professor-period are potentially correlated with attendance.

The project currently has three outcomes/models: (1) continuous `Z_GRADE_PRIMARY`, analyzed with OLS; (2) binary `PASS`, analyzed with LPM; and (3) binary `PASS`, analyzed with a logistic GLM. Full adjustment is D; A/B/C are subset models.

For every model, refit its baseline and all predictor-block coalitions, then average their marginal fit gains using Shapley weights. The fit functions differ:
- **Z OLS**: ordinary in-sample R², interpreted as the fraction of empirical Z variance explained by the model.
- **PASS LPM**: ordinary in-sample R² for the binary 0/1 outcome, *not* a probability change.
- **PASS logit**: McFadden's likelihood-based pseudo-R², `1 - logLik(S)/logLik(intercept)`. It **must not** be compared numerically to ordinary R². Fits are descriptive and do **not** address the earlier invalid clustered standard errors in logit D.

For the full three-block specification the exact allocation obeys `phi(attendance) + phi(degree) + phi(professor_period) = v(full)`. No Shapley estimate is a causal effect. Shared information between correlated blocks is distributed by the Shapley convention.

## Predictive validation (deliberately separate from the in-sample decomposition)

The in-sample Shapley ranking answers how the historical fitted models explain the sample. It is *not* a trustworthy ranking of prospective predictive usefulness: classroom dummies are high-dimensional and have no defined value for novel professor-periods.

A second, group-held-out five-fold experiment therefore trains on some **professor-period clusters** and predicts the others with only two available transferable predictor groups: attendance and degree. It refits one-hot-encoded OLS for Z and L2 logistic regression for PASS within each fold, handling unseen career levels without revealing identifiers.

Its coalition value is held-out skill relative to the fold's **training-sample mean**. For Z this is out-of-context squared-error skill; for PASS it is the Brier skill score. The baseline coalition has skill zero by construction; other values and contributions may be negative. Use the two-variable exact Shapley allocation to describe out-of-context predictive skill, never as causal importance.

This validation is **retrospective end-of-term prediction**: attendance counts include the entire semester, so they are not available at semester start. Also, Z is constructed within professor-period from final outcomes, including an imputation procedure for BV/RT/BA. It is not an immediately observable, deployable early-warning target.

## Data, audit, execution and outputs

Inputs: same institutionally authorized first eligible MU cohort as Paper 2.1, N=6,627 and 190 professor-period contexts; the two outcome samples are required to coincide. Same eight attendance bins used in the preceding sensitivity models. The script refuses to report values if its fully adjusted Z OLS R² does not reproduce the previously validated 0.0582281949 within numerical tolerance.

```bash
git switch research/paper21-shapley-predictive-importance
python -m pip install -e './cmat_analysis[dev]'
python -m pytest -q cmat_analysis/tests/test_paper21_shapley_importance.py
python code/run_paper21_shapley_importance.py --check
python code/run_paper21_shapley_importance.py
```

An authorized local environment must have both input files discoverable by `get_study_config()`. The runner stops if either input is missing. Optional flags `--materias PATH` and `--asesorias PATH` select approved local inputs.

Aggregate-only output directory: `results/paper21/tables/shapley_importance/`, with four CSVs for in-sample block importance, in-sample coalitions, held-out skill importance, and held-out coalitions. A generated report appears at `notes/19_SHAPLEY_PREDICTIVE_IMPORTANCE.md`. No student-level predictions or personally identifying information are saved.

## Limits and next research steps

- **Not yet the most important variable overall:** available factors are only CMAT attendance, degree and professor-period. We need appropriately timed prior-achievement, entrance diagnostic, earlier GPA, and academic engagement measures before making substantive rankings of broader determinants. The optional `pre_treatment_covariates.xlsx` is not assumed present or usable without verification.
- **Do not equate explanatory importance with intervention effect.** Attendance can be weak in prediction despite an actual effect, or predictive because students choose to seek help when struggling.
- **Avoid using classroom-standardized Z as an operational early-warning score.** Future research should use pre-specified targets (numeric final grades for those with grades; separately treat administrative outcomes) and time-specific inputs.
- **Feature importance uncertainty** needs clustered resampling or repeated held-out folds in any confirmatory report; current exploratory point estimates have no confidence intervals.
- **No manuscript overwrite:** report as an exploratory supplement unless the study question, target, measurement timing and validation strategy are formally revised.
