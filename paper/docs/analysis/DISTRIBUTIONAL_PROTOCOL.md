# Paper 2.2.2 — Distributional research protocol (not executed)

## 1. Lock data hierarchy

Reproduce inherited cohort and outcome construction without raw exports. Primary within-group outcome: numeric complete-case instructor-period Z; imputed `Z_GRADE_PRIMARY` is a distinct sensitivity. Record cohort count, number of instructor-period clusters, grade support/min/max, fraction of ties and rounded values, truncation, censoring, top/bottom heaping, and how BA/BV/RT are represented; observe sample changes across specifications.

Primary grouping to audit: `0/1/2/3/4/5/6/7+` as the Paper 2.1 display grid. Preserve original support-motivated pooled `6+` robustness and note that the exact 6 vs 7+ contrast has sparse overlap. Predefine whether the multiple mode tests are across all eight groups or a smaller supported primary family **before** examining new p-values.

## 2. Reproduce baseline (Paper 2.1 methods, not novel evidence)

Within each supported group run numerical comparisons of Gaussian K=1,2,3 (log likelihood, AIC, BIC, ICL), K1-vs-K2 parametric bootstrap LRT, one skew-normal vs GMM2 BIC bootstrap, held-out log predictive density under repeated folds, Ashman D, means/SD/weights, entropy and soft responsibilities. Existing code: `code/run_paper21_mixture.py`, reusable `cmat_analysis/src/cmat_analysis/statistics/mixtures.py`. Store replication separately as `results/paper222/`.

An observed two-Gaussian advantage is a model-approximation finding. It **does not test number of modes**. K1 vs K2 chi-square reference is nonregular; retain bootstrap calibration. Report Monte Carlo uncertainty, seeds, convergence, degeneracy and multiple starts.

## 3. Direct modality question (new, subject to validity audit)

Evaluate whether the **underlying density**, at scientifically meaningful resolution, is unimodal versus at least bimodal. Candidate tools include Hartigan's dip statistic, Silverman-style critical bandwidth and bootstrap confidence bands for smoothed density/mode count. However, grade ties, finite scores, heaping, support boundaries, and instructor-period dependence can invalidate textbook continuous-iid reference distributions. The next agent must perform a method feasibility and null-calibration review **before** attaching p-values to these tests.

Possible calibrated approaches: simulate from fitted single-mode rounded/bounded/heaped nulls with the same grade measurement mechanism; use cluster-aware resampling for *stability*; if testing requires within-cluster dependence, propose and justify a null simulation that preserves it, or refrain from formal modality p-values. Differentiate null-model misspecification from evidence for two modes. Do not introduce arbitrary jitter as a fix without documented sensitivity/measurement meaning.

## 4. Challenging one-mode alternatives

At minimum single Gaussian, single skew-normal and flexible unimodal candidates (e.g. unimodal constrained smooth density or bounded/graded and rounded distribution where scientifically justified) versus K2 Gaussian mixture. Use identical observations for each within-specification comparison. Report support limitations of Gaussian/skew-normal on bounded outcomes. Compare in-sample AIC/BIC and **genuinely held-out log density** using nested tuning when needed; avoid treating repeated CV folds as independent observations for p-values.

Investigate whether the chosen regularisation/bandwidth, extreme outliers or low-frequency groups create false peaks. For imputed scores, separately analyse discrete administrative mass and numeric-grade component; a lower mass induced by coding rules is not evidence of a distinct underlying normal student population.

## 5. Distinguish component separation from modality

For K2, report ordered component means, SD, weights, Ashman D, posterior entropy/maximum responsibility, fitted total-mixture **number and locations of modes**, and uncertainty or bootstrap stability of the modes. A large Ashman D is a separation diagnostic, not a guaranteed modality test, and a tiny fitted weight can describe an outlier-fitting component. Never automatically assign hard student labels; use posterior soft responsibilities. Compare mode evidence to held-out score and alternative one-mode fits.

## 6. Planned tests and multiplicity

- **Existing bootstrap LRT:** null one Gaussian versus two Gaussian components; p-value is conditional on the Gaussian null and i.i.d. simulation model.
- **Existing bootstrap of BIC difference:** null one skew-normal versus two-Gaussian fit advantage; not a direct unimodality test.
- **Candidate direct modality test:** null of unimodality; valid p-value only after support/heaping/cluster calibration passes audit.
- Correct multiplicity for a predeclared family of primary group-wise modality tests (e.g. Holm across eight); label imputed and sensitivity checks separately and do not combine them opportunistically.
- BIC/ICL, CV scores, Ashman D, entropy and observed density mode counts are **diagnostics/model selection, not independent hypothesis-test p-values**.

## 7. Deliverables and null outcomes

A comparative evidence table for each outcome/group, support diagnostics, plots of actual grades/heaping, fitted continuous densities with visible mode locations and uncertainty, robustness across bandwidths/initialisations/groups, and a conclusion that may be **unimodal / multimodal-supported / inconclusive**. Never force two modes, declare exactly two student populations or infer engagement types.