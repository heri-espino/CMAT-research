# Methodological synthesis — Paper 2 beyond first attendance

**Version:** audit of committed branch heads as of 2026-10-26. **Purpose:** reconcile distinct scientific questions without rewriting an existing manuscript, modifying analyses, or equating algorithm selection with hypothesis testing. This document should be reviewed alongside [the claims matrix](claims-evidence-matrix.md) and [discrepancy report](discrepancy-report.md).

## 1. Scope, notation and identification

Let `i` index a first-eligible Matemáticas Universitarias attempt, `c(i)` the professor × academic-period grading context, `d(i)` the degree programme, and `K_i` the number of **recorded same-semester** CMAT visits. `Y_i^Z` is the canonically imputed and context-standardized continuous final outcome; `Y_i^P=1` when the numeric final mark is at least 7.5 and zero for numeric failure, BA, BV or RT. `Y_i^{Z,cc}` and `Y_i^{num}` are defined *only* for students with usable observed numeric marks (different numerical sample counts).

**Baseline support:** N=6,627 observations, 190 contexts, 5,393 recorded `K=0`, 1,234 `K>=1`. The distinction is exposure **recording**, not verified take-up of every mathematics-learning channel. Motivation, prior preparation, financial resources, actual PPA1 eligibility/credit and service use outside the center are not measured in these outcome models.

A working adjusted model is

```text
E[Y_i | K_i,d(i),c(i)] = alpha_{c(i)} + gamma_{d(i)} + f(K_i)
```

with OLS for Z or a linear probability model for PASS and cluster-robust covariance at the professor-period level. Here `f` describes *conditional differences in observed final outcomes*. Because `K` is self-selected and accumulates during the same academic term, `f(k)-f(0)` does **not** identify `E[Y_i(k)-Y_i(0)]` without strong, unverified causal assumptions. Context standardisation and fixed effects reduce some observed grading-context confounding, not student-level selection or simultaneity.

## 2. The main inferential anchor: Wald contrasts and Holm

The originally chosen positive-attendance frequency partition `1/2/3/4/5/6+` defines six groups and `6 choose 2 = 15` pairwise hypotheses **per outcome** among N=1,234 attendees in 176 contexts. For pair `a,b`,

```text
Delta_ab = L_ab' beta_hat,
SE(Delta_ab) = sqrt(L_ab' V_cluster(beta_hat) L_ab),
W_ab = Delta_ab / SE(Delta_ab).
```

The omnibus Wald test jointly tests the contrasts against zero; it does not supply a confidence interval for each pair and does not prove equality when nonsignificant. Holm's step-down correction sorts the 15 pairwise p-values and controls the familywise Type-I error rate **within that declared family** under correctly calibrated constituent tests. The original omnibus p-values are 0.316551 (Z) and 0.152215 (PASS); no individual positive-frequency pair survives Holm.

Three designs must not be silently pooled:
1. The historical `1/2/3/4/5/6+` **15-pair** family, among users.
2. The later `1/2/3/4/5/6/7+` **21-pair** user-only sensitivity (Z omnibus 0.21257, PASS 0.10198).
3. The `0/1/2/3/4/5/6/7+` **28-pair** all-student profile (N=6,627), including zero-vs-user comparisons. Its PASS 7+ vs 1 adjusted +14.49 pp survives Holm, whereas its analogous Z +0.244 SD does not. The broader 0-vs-1+ benchmark is an additional single-comparison question.

The full-cohort benchmark yields +0.3612 Z SD and +15.29 PASS pp for recorded attendance versus none after context/degree adjustment. This is a statistically precise association; it cannot isolate the causal effect of making a first visit. Clustering by professor rather than context reduces independent clusters from 176 to 51 in the user-only comparison and changes the p-values (e.g. Z omnibus 0.0477). Neither clustering approach can correct uncontrolled selection, and switching clustering because it changes significance is not appropriate.

**PASS LPM vs logit:** LPM coefficients are absolute probability differences, whereas logit parameters are log-odds differences and exponentiated odds ratios. Logistic model D (both context FE and degree controls) converged numerically but lacks estimable valid clustered uncertainty; the point estimates cannot carry confidence/p-value claims. Models A/B/C are sensitivity evidence with different adjustment sets. No model should be awarded confirmatory status by counting more significant pairwise contrasts.

## 3. Administrative endpoints versus observed numeric grades

The original continuous Z uses institutional imputation for BA/BV/RT before within-context standardisation, while PASS treats these nonnumeric states as failures without imputation. Removing those statuses changes both the construct and population. For example, `GRADE_NUMERIC` has 5,526 students and `Z_GRADE_COMPLETE_CASE` has 5,522, rather than the 6,627 in primary full-cohort outcomes. Numeric-only analyses are conditional on receiving a numerical grade and therefore subject to outcome selection.

Among recorded nonpass cases, the administrative status share is 923/1,504 for nonusers versus 178/217 for users; the **conditional** adjusted difference is +0.1323 (95% CI 0.0680–0.1965). This is a compositional contrast within nonpassing students, not evidence that CMAT induces withdrawals or that a particular code measures an academic-support mechanism. The numeric-failure analysis estimates 13.253% adjusted numeric failure at zero versus 3.334% at one visit (numeric-only logistic model); the users-only omnibus p=0.4802 shows it cannot resolve fine-frequency differences on that outcome.

## 4. EM/Gaussian mixtures and distributional adequacy

A Gaussian-mixture fit `p(y|K=k)=sum_{j=1}^J pi_{jk} Normal(y;mu_{jk},sigma^2_{jk})` can approximate skewed, bounded, heaped or truly multimodal density. Selecting `J=2` or rejecting a single Gaussian tests *fit against that reference family*, not the number of modes or the number of real student populations. Distinguish three questions:

- **Density complexity:** can K=1 Gaussian be rejected using a parametric-bootstrap likelihood-ratio reference? The historical complete-case results suggest yes, but the smallest reported bootstrap p is bounded by 1/(B+1).
- **Competing skew shape:** can a **single skew-normal** explain the same observations? For numeric complete cases, several moderate-to-high attendance groups favour skew-normal under BIC; on imputed Z, GMM2 tends to be favoured. Cross-validated log predictive density adds a non-nested out-of-sample check, not a proof of modality.
- **Actual modality and latent groups:** do deheaped/bounded distribution models, formal mode-count tests and stable, independently validated structure support more than one mode or student type? **No new Paper 2.2.2 validation of this question exists.**

For 7+ complete cases (N=93), an approximately 1.08% lower component with its SD at a 0.001 numerical floor is particularly consistent with an extreme-observation fitting pathology. Imputed lower-component responsibility is enriched in administrative endpoints; it should not be converted into a binary label or a behaviour type. Include short results/adequacy cautions in the supplement; exclude bimodal-student or two-class assertions from the publication.

## 5. Ordered fused lasso: parsimony versus equality

For ordered frequency groups, the working fusion estimator solves a penalized goodness-of-fit problem of the form

```text
min_{alpha,gamma,theta} (1/2n) * sum_i (Y_i-alpha_c-gamma_d-theta_{K_i})^2
   + lambda * sum_{k=1}^{G-1} |theta_{k+1}-theta_k|.
```

Zero differences at the fitted penalty are **algorithmic regularization**, not accepted equality hypotheses. The completed 2026-10-08 experiment separated 70% of professor-period contexts for discovery from 30% for internal reserved-cluster evaluation (4,675/1,952 students, 133/57 contexts), tuned within four grouped CV folds, and retuned 100 cluster bootstrap fits in each of four Z/PASS × 7+/pooled-6+ specifications. The Z selected partition `[0]|[1+]` appeared at boundary 0|1 in 100% of bootstrap refits and had an internal holdout adjusted +0.2636 SD (95% CI 0.1500–0.3772). This is evidence of **within-procedure selection stability** under the given tuning rule.

The same 1-SE-style heuristic fused all PASS categories (0|1 selected in just 37% of bootstrap refits), but the all-fused partition ranked **last (128/128)** in exhaustive discovery-sample BIC for the 7+ representation. No PASS selected-boundary Wald test was defined; its corresponding CSV is empty. This conflict signals sensitivity to the penalty-selection rule and outcome-specific loss, not a substantive PASS null or confirmed equivalence. Furthermore, the institutional outcomes had been explored by the broader Paper 2.1 programme before the algorithmic split, so the holdout is internally isolated from the fused-lasso search, not a genuinely untouched external sample.

## 6. Grouped Shapley: fit allocation versus predictive skill

The grouped Shapley value of attendance block `A`, given value function `v(S)` for included block coalition `S`, averages `v(S ∪ {A})-v(S)` across coalition orders with Shapley weights. This is a *credit-allocation convention* under correlated predictors, not a manipulable causal effect or a rank ordering of all determinants of learning.

In fully adjusted model D, attendance receives ~30.96% of model Z R² 0.05823 and ~7.75% of model PASS-LPM R² 0.17182. These percentages are **shares of small/moderate explained fit, not percentages of grade causation**. McFadden pseudo-R² from logit has a different denominator and must not be combined numerically with OLS R².

Five-fold out-of-professor-period retrospective prediction omits FE for held-out contexts; its Z skill relative to a fold-mean baseline is 0.01848, and PASS Brier skill is 0.01761. Visits have been accumulated throughout the term and are not available in advance: the analysis says little about a deployable beginning-of-semester warning model. Absence of prior skills, motivation and external support limits any claim of comprehensive variable importance.

## 7. First visit, extra visits and rival curve shapes

The exploratory piecewise model `f(k)=a I(k>=1)+b max(min(k,7)-1,0)` separates a fitted zero→one discontinuity from a constant extra-visit slope. Both estimated terms are positive for Z and PASS under the chosen full-cohort FE-adjusted working model; the extra-visit terms are +0.03609 SD and +2.225 pp respectively, with separate **two-term** Holm correction. This is not a proof that an individual gains those quantities by visiting again.

The October 26-published curve analysis compares five shapes—linear extra visits, `log(k)`, `sqrt(k)-1`, saturating exponential with fixed decay 0.5, and an unrestricted categorical specification—on four distinct outcomes. In-sample all-shape fits include professor-period FE and degree controls; five-fold context-held-out CV intentionally *excludes* professor-period FE. Model fit and predictive performance answer different questions. The linear shape narrowly outperforms several alternatives on Z/PASS held-out scores, but the differences are small and have no separate uncertainty test. The unrestricted categorical model permits dips: the Z 5→6 estimate is −0.117 (95% CI −0.433 to +0.199; Holm p=1) and is consistent with sampling uncertainty, sparse support, confounding, or nonmonotone association.

Log, square-root and exponential forms may impose diminishing increments, rather than discover a natural plateau. The only adjacent differences surviving a *seven-adjacent* Holm family for the main Z/PASS outcomes are 0→1. This does not overrule the user-only historical family or establish that all extra-visit slopes are truly zero. The unrestricted numeric-grade and numeric-only-Z analyses have different denominators and administrative-selection vulnerability.

## 8. PPA threshold grouping — a planned explanatory check

PPA1's optional first-semester activity uses three visits as a **possible participation incentive**. Individual eligibility, motive and credit receipt are not observed; hence attendance 1–3 cannot be identified as “PPA-only,” attendance 4+ cannot be assumed incentive-free, and a comparison at visit 3→4 is not a regression discontinuity. The proposed mutually exclusive partitions are `0|1–3|4+` (primary) and `0|1–3|4|5+` (secondary). Neither is a finalized result at this audit date, and the common three-visit criterion does not make the results preregistered. The PPA agent must report adjusted Z/PASS group coefficients, counts and context overlap, professor-period clustered uncertainty, explicit **new** within-outcome Holm families, and numeric-only/admin sensitivity before claims are admitted.

## 9. Joint thesis, antithesis and synthesis

**Thesis:** stable adjusted 0 versus positive-visit differences in Wald contrasts, categorical curves and the Z fused model suggest that initial contact marks a salient behavioral division in the observed cohort.

**Antithesis:** within-users tests are imprecise after multiplicity correction; model-specific slopes and the full-cohort PASS 7+ contrast provide partial competing signals, while administrative imputation, covariate selection, sparse tails and binary-model penalty choices complicate claims of thresholds or saturation. No causal assignment or independent out-of-time validation was performed.

**Synthesis:** make the article primarily about the *shape and evidentiary limits of same-semester attendance associations*. State that the strongest repeatable contrast separates recorded nonattendance from some attendance, while frequency gradients *among attendees* are not resolved consistently by the pre-outcome Holm family. Present penalized fusion, curve shape, mixture adequacy and Shapley as complementary diagnostics, not independent causal replications.

## 10. Editorial deployment and validation sequence

**Main text:** cohort/outcomes, adjusted benchmark, original positive-frequency Wald omnibus and Holm contrasts, and the PPA-group analysis only after signed provenance and post-hoc labeling. Provide one concise figure for unadjusted group support and a transparent paragraph contrasting observed numeric and administrative outcomes.

**Supplement:** 7+ tail/full-cohort contrast and alternative cluster choices; the A/B/C/D adjustment sensitivity (mark D-logit inference missing); all seven-adjacent curve contrasts and competing shapes; complete-case/imputed GMM and skew-normal diagnostics; fused selection metrics, bootstrap stability and PASS penalty conflict; Shapley fit shares versus retrospective cross-validation; observed numeric-grade/admin composition.

**Exclude pending validation:** causal effects of visit 1/3/4 or each extra visit; official PPA1 completion/type labels; student latent classes/bimodality; equivalence or saturation statements; actionable early-warning predictions; any p-value from nonestimable logit D; new Paper 2.2.2 claims.

Validation sequence: (1) pin source branch SHA, run manifest and CSV/plot bytes; (2) verify cohort and each model's analysis denominator and context count; (3) check parameter orientation, outcome unit, zero/positive population and fixed-effects/cluster definition; (4) independently reconstruct all Wald contrasts and Holm corrections if controlled data access is authorized; (5) reconcile PPA source once committed; (6) perform privacy screening and scientific review before elevating any exploratory text to primary inference. Existing CSVs are not edited in this audit.
