---
marp: true
paginate: true
size: 16:9
html: true
style: |
  section { background: #fbfdfe; color: #17364d; font-family: 'DejaVu Sans', Arial, sans-serif; padding: 42px 65px; }
  h1 { color: #153e5c; font-size: 38px; }
  p { font-size: 22px; line-height: 1.32; }
  strong { color: #087e8b; }
  img { max-width: 96%; max-height: 430px; display: block; margin: auto; }
  footer { font-size: 11px; color: #617e8b; }
  section.lead { background:#153e5c; color:white; }
  section.lead h1, section.lead strong { color:white; }
  section.appendix { background:#f1f6f8; }
---
<!-- _class: lead -->
# Beyond the First Visit

CMAT attendance and mathematics outcomes. **Paper 2 — provisional scientific synthesis**, 26 October 2026. For research faculty and CMAT administration.

<!-- _footer: Source: Consolidation plan -->
<!-- Speaker notes: Integrated validation pending. -->

---
# Principal message

The strongest evidence distinguishes **zero recorded visits from initial use**. Adjusted outcome differences are sizeable, while positive-frequency increments are less precise and model-dependent. No causal benefits are identified.

<!-- _footer: Source: Paper 2.1 Wald/Holm and 10_benchmark -->
<!-- Speaker notes: Estimation, model selection and prediction are different layers. -->

---
# Why mathematics support matters

Learning centres supplement instruction amid different levels of preparation. Use is self-selected; non-engagement may reflect access barriers. Experiments and observational studies provide different types of evidence.

<!-- _footer: Source: Lawson et al. 2020; Mullen et al. 2024; Pugatch & Wilson 2018 -->
<!-- Speaker notes: Do not transport a randomized estimate from another institution. -->

---
# CMAT and the optional PPA1 activity

PPA1 provides **one optional three-CMAT-visit integration activity**. The study does not observe individual intentions, PPA eligibility or credit use. Three visits motivate an exploratory grouping, not a discontinuity design.

<!-- _footer: Source: Consolidation plan, 2026-10-26 -->
<!-- Speaker notes: Never identify PPA-induced or uninterested students from visit counts. -->

---
# Cohort and empirical design

First eligible MU attempt with CMAT coverage, context fixed effects, degree adjustment and professor-period clustered uncertainty. Primary outcomes: `Z_GRADE_PRIMARY`, `PASS`; numeric-only and administrative sensitivities differ in sample and target.

<!-- _footer: Source: Paper 2.1 specifications; consolidation plan -->
<!-- Speaker notes: All attendance and grades are recorded in the same term. -->

---
# Visit distribution and precision

![Aggregate figure](figures/attendance.svg)

N=6,627; 190 professor-period contexts; 5,393 with zero visits and 1,234 with positive recorded visits. Sparse high-frequency support constrains fine-grained contrasts.

<!-- _footer: Source: 01_cohort_flow.csv; 10n_zero_inclusive_7plus_descriptives.csv -->
<!-- Speaker notes: The original all-period first eligible pool was 7,777. -->

---
# Raw grades and passing rates

![Aggregate figure](figures/raw.svg)

These are **unadjusted between-student means**, not longitudinal growth or experimental effects. The exact-frequency series is not strictly monotone.

<!-- _footer: Source: 10n_zero_inclusive_7plus_descriptives.csv -->
<!-- Speaker notes: The groups have strongly unequal denominators. -->

---
# Any attendance vs zero

Adjusted 1+ minus 0: **+0.361 grade SD**, CI [0.302,0.421], and **+15.29 PASS percentage points**, CI [12.44,18.15]. The 1+ pool is not exactly one visit.

<!-- _footer: Source: 10_benchmark_0_vs_1plus.csv -->
<!-- Speaker notes: 190 professor-period clusters; observational contrast. -->

---
# Wald and Holm inference

**Original primary Paper 2.1 users-only analysis:** 1/2/3/4/5/6+ with **15 Holm-adjusted pairs per outcome**; none survives. The omnibus tests do not reject.
**Complementary full-cohort analysis:** 0/1/2/3/4+ with **10** pairs per outcome; zero-versus-positive differences are clearer.
**Separate sensitivity families:** users-only seven groups (**21** pairs), zero-inclusive eight groups (**28** pairs), and exploratory adjacent comparisons (**7** pairs).
SEs are clustered by professor-period; nominal 95% CIs are not Holm simultaneous CIs.

<!-- _footer: Source: Paper 2.1 tables 12–14, 21–23, 33/41, 26a/26k; methods PR #97; QA PR #96 -->
<!-- Speaker notes: The 15-pair user-only family is the original Paper 2.1 primary analysis, not the 10-pair full-cohort model. Methods PR #97 and QA PR #96 confirm the separate families and 148 valid linear-model arithmetic checks. -->
---
# Adjusted standardized-grade contrasts

![Adjusted 95% clustered intervals](figures/adj-z.svg)

This figure is the **complementary ten-pair zero-inclusive model**. Every group differs from zero after Holm; no positive-versus-positive grade contrast survives here or in the original users-only 15-pair family.

<!-- _footer: Source: 33_exact_visit_groups_fe_pairwise.csv, Paper 2.1 -->
<!-- Speaker notes: The plotted confidence intervals are nominal and clustered; Holm refers to p-values in the complementary ten-pair family. Do not treat this as the original users-only design. -->
---
# Adjusted PASS contrasts

![Adjusted PASS contrasts](figures/adj-pass.svg)

In the **complementary ten-pair model**, zero differs from each positive group. **1 versus 4+** also survives Holm (p≈0.011). The original users-only 15-pair family has no surviving pairwise contrast.

<!-- _footer: Source: 41_exact_visit_groups_pass_fe_pairwise.csv, Paper 2.1 -->
<!-- Speaker notes: These PASS coefficients are linear-probability differences in percentage points. Invalid historical PASS-logit inferential flags were deliberately not used. -->
---
# PPA grouping: not yet validated

![Aggregate figure](figures/ppa.svg)

Only user-approved grouping: `0 | 1–3 | 4+`. **Pending validated adjusted estimates**. The figure is a grouping diagram, not a plotted result.

<!-- _footer: Source: PAPER2_CONSOLIDATION_PLAN.md -->
<!-- Speaker notes: Do not infer group effects from historical exact group coefficients. -->

---
# Two-part first/additional visits

Adjusted working model: Z first-visit **+0.307 SD**, additional-visit slope **+0.036 SD**; PASS first **+11.92 pp**, extra **+2.23 pp**. The common post-first slope is imposed and top-coded at 7+.

<!-- _footer: Source: two_part_attendance_z_pass.csv -->
<!-- Speaker notes: Two-term Holm correction is separate from pairwise families. -->

---
# Five fitted curve families

![Aggregate figure](figures/curves.svg)

Linear, log, square-root and saturating fits impose different increment shapes; categorical effects do not. Slightly better in-sample AIC or grouped validation does not prove causal diminishing returns.

<!-- _footer: Source: attendance_curves/adjusted_curves_cluster_ci.csv -->
<!-- Speaker notes: Saturating parameter lambda was fixed in protocol. -->

---
# Five-to-six dip: broad uncertainty

![Aggregate figure](figures/five-six.svg)

Sixth minus fifth adjusted contrast: grade **−0.117 SD**, CI [−0.433,+0.199]; PASS **−1.33 pp**, CI [−16.62,+13.96]. Neither survives seven-adjacent Holm. N5=55, N6=50.

<!-- _footer: Source: attendance_curves/adjacent_differences_holm.csv -->
<!-- Speaker notes: A negative point is not evidence that a sixth visit harms students. -->

---
# Fused-lasso boundary stability

![Aggregate figure](figures/fused.svg)

Grade discovery selects `[0] | [1–7+]`; 0|1 boundary appears in **100/100** cluster bootstrap refits. PASS one-SE-style selection fuses all counts, although its 0|1 boundary appears 37/100 times.

<!-- _footer: Source: fused 7plus blocks and boundary_stability CSVs -->
<!-- Speaker notes: Stability is algorithmic selection frequency, not truth probability. -->

---
# Internally held-out grade comparison

Reserved n=1,952 in 57 contexts: discovered Z group 1+ minus zero **+0.264 SD**, CI [0.150,0.377]. PASS has no selected boundary, so no comparable selected Wald contrast. Not an external or prospectively untouched replication.

<!-- _footer: Source: 7plus_z_grade_primary_holdout_wald.csv -->
<!-- Speaker notes: Research-wide outcome exploration preceded this particular split. -->

---
# Mixtures and skew-normal alternatives

Historical EM Gaussian mixtures and skew-normal fits test distributional adequacy under different outcome encodings. A better K=2 likelihood does **not** identify two student types or even two visible modes. Prospective modality test remains pending.

<!-- _footer: Source: Distributional branch results/paper21/tables/37–52 -->
<!-- Speaker notes: Administrative imputation can introduce mass points. -->

---
# Observed outcomes and administration

![Aggregate figure](figures/states.svg)

PASS, numeric fail, BV, RT and BA are different observed states. Numeric-only grades exclude administrative outcomes; primary Z applies defined imputation. Combining these populations changes the estimand.

<!-- _footer: Source: 10d_zero_inclusive_exact_administrative_composition.csv -->
<!-- Speaker notes: These shares are descriptive; all five states are exclusive. -->

---
# In-sample Shapley fit attribution

![Aggregate figure](figures/shapley.svg)

Model D: attendance accounts for approximately **31% of grade R²** and **8% of PASS R²**. Degree dominates grade fit; professor-period dominates PASS fit. These are not causal contributions.

<!-- _footer: Source: shapley_importance/in_sample_shapley_12_models.csv -->
<!-- Speaker notes: Model R² is only .058 for grade and .172 for PASS. -->

---
# Out-of-context predictive skill

![Aggregate figure](figures/prediction.svg)

Five-fold professor-period-held-out analysis: grade R² skill **1.85%**, PASS Brier skill **1.76%**. Test-context FE indicators are unavailable. These are retrospective predictions, not actionable start-of-term warnings.

<!-- _footer: Source: shapley_importance/out_of_context_shapley.csv -->
<!-- Speaker notes: The two percentages use different loss functions. -->

---
# Synthesis and next study

**Supported:** large adjusted zero/positive separation, uncertain consecutive increments, model-dependent selected boundaries and differing administrative outcome composition.

**Unresolved:** self-selection, PPA1 participation, preparation, functional form and prospective generalization.

**Next:** validate the sole three-band PPA specification; harmonize denominators; collect baseline readiness and visit timing; evaluate ethical prospective encouragement.

**Release gate — DO NOT RELEASE:** independent QA PR #96 reports a critical public controlled-data exposure and invalid PASS-logit significance flags. Institutional response and renewed review are prerequisites.

<!-- _footer: Source: Methods PR #97, QA PR #96 and committed aggregates, 2026-10-26 -->
<!-- Speaker notes: The critical privacy finding should be handled by the repository administrator and institution's data custodian; do not disclose individual data in presentation materials. No observed difference here identifies a causal tutoring effect. -->
---
<!-- _class: appendix -->
# Appendix A — evidence hierarchy

**Inferential anchors:** original user-only 15-pair Wald/Holm contrasts and complementary zero-inclusive ten-pair contrasts.

**Sensitivity analyses:** positive-only tail 21-pair and zero-inclusive 28-pair families; first/additional visit and fitted curve shapes.

**Model diagnostics:** fused-lasso grouping; Gaussian mixtures versus skewness; Shapley in-sample attribution; retrospective held-out prediction.

**PPA:** mutually exclusive 0 | 1–3 | 4+ remains exploratory and **not estimated on authorized institutional microdata**.

<!-- _footer: Source: Methods claims-to-evidence matrix (PR #97); PPA PR #98 -->
<!-- Speaker notes: These methods measure different features of the same cohort and do not constitute independent experimental replications. -->
---
<!-- _class: appendix -->
# Appendix B — cohort numbers

Eligible first MU attempts across all historical periods: **7,777**; covered analysis: **6,627**. Exact n: 0=5393, 1=517, 2=245, 3=170, 4=96, 5=55, 6=50, 7+=101. 190 professor-period contexts.

<!-- _footer: Source: 01_cohort_flow.csv; 10n_zero_inclusive_7plus_descriptives.csv -->
<!-- Speaker notes: The terminal category is top-coded. -->

---
<!-- _class: appendix -->
# Appendix C — multiplicity

For a pair i,j, test H0: adjusted mu(i) = mu(j) with professor-period cluster-robust Wald uncertainty. Holm step-down adjustment is applied within a declared comparison family.

**Paper 2.1 families, per outcome:** primary users-only **15**; users-only 7-level sensitivity **21**; zero-inclusive five-group **10**; zero-inclusive eight-group **28**.

**Other analyses:** seven adjacent steps, two piecewise terms; proposed PPA-18 = (3+6) x 2 outcomes in one jointly Holm-adjusted family.

Nominal cluster-robust intervals are **not** simultaneous Holm intervals.

<!-- _footer: Source: Paper 2.1 tables 12–14, 21–23, 33/41, 26a/26k; QA PR #96; PPA PR #98 -->
<!-- Speaker notes: QA checked 148 previously published linear contrasts for arithmetic consistency with zero mismatches. This does not authenticate institutional inputs or the defective PASS-logit inference flags. -->
---
<!-- _class: appendix -->
# Appendix D — piecewise formula

`Y=alpha_context + gamma_degree + beta_0 ANY_VISIT + beta_plus EXTRA + error`. `ANY_VISIT=1(K>=1)`; `EXTRA=max(min(K,7)-1,0)`. Z betas 0.30656/0.03609; PASS betas 0.11923/0.02225.

<!-- _footer: Source: two_part_attendance_z_pass.csv -->
<!-- Speaker notes: Do not interpret beta_plus as a separate estimate for each visit. -->

---
<!-- _class: appendix -->
# Appendix E — shape-selection sensitivity

| Grade-Z shape | In-sample AIC | Grouped held-out R2 skill |
|---|---:|---:|
| Linear | 18753.43 | 0.01692 |
| Logarithmic | 18753.99 | 0.01676 |
| Square-root | 18753.62 | 0.01685 |
| Saturating | 18754.40 | 0.01672 |
| Categorical | 18762.27 | 0.01630 |

The five fitted shapes differ little in held-out skill; professor-period fixed effects were unavailable for unseen validation contexts.

<!-- _footer: Source: attendance_curves/model_comparison_in_sample.csv and group_heldout_shape_cv.csv -->
<!-- Speaker notes: These are model-fit and held-out-loss comparisons, not a formal test of diminishing causal response. -->
---
<!-- _class: appendix -->
# Appendix F — fused protocol

Discovery n=4,675 / 133 contexts, reserve n=1,952 / 57 contexts; 100/100 bootstrap retunings successful. Z selected 0|1 in 100%. PASS all-fused under one-SE-style heuristic but **128/128** by exhaustive discovery BIC.

<!-- _footer: Source: 2026-10-07_fused_lasso_100_bootstrap_results.md -->
<!-- Speaker notes: Selection depends strongly on PASS heuristic. -->

---
<!-- _class: appendix -->
# Appendix G — distributions

Numeric complete-case BIC prefers GMM K=2 vs single skew-normal in groups 0,1,2; skew-normal K=1 in 3,4,5,6+. Held-out log predictive density also varies. Do not infer underlying social subgroups.

<!-- _footer: Source: 47_complete_case_skewnormal_vs_gmm.csv; 50_complete_case_skewnormal_vs_gmm_cross_validation.csv -->
<!-- Speaker notes: Sparse frequencies and grade ceilings affect fits. -->

---
<!-- _class: appendix -->
# Appendix H — provenance and readiness

Historical source SHAs: Paper 2.1 **1546c594…**; fused **29810a86…**; mixture **b1cace12…**; Shapley **5915976f…**.

Scientific review drafts: methods/claims matrix **PR #97**, integrated manuscript **PR #99**; PPA **PR #98** has code but no validated institutional fit.

**DO NOT RELEASE:** QA **PR #96** reports controlled student records in the public repository and invalid historical PASS-logit inference; privacy remediation and re-audit required.

The deck PDF is an **offline fallback preview**, not an official Marp CLI-validated release.

<!-- _footer: Source: Source branch tips; PRs #96–#99; 2026-10-26 -->
<!-- Speaker notes: Existing PRs are unmerged review material. The controlled-data release block applies to all publication actions; verify Git history, forks and artifacts under authorized data-custodian oversight. -->