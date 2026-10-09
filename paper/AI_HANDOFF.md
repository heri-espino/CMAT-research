# Paper 2.1 — AI handoff

This file contains branch-specific rules for `paper/paper2.1-visit-frequency`.

**New editor/research agent, 2026-10-09:** Start with root `notes/README.md` and its dated Holm-first scientific/editorial synthesis before rewriting `paper/sections/01.tex`–`04.tex`. The principal strategy is the historical fixed-effects Wald contrasts with separate Holm families; do not transfer fused-lasso partitions from the separate `paper/paper2.2.1-fused-frequency` branch. Distinguish the support-frozen pooled 6+ design from the later 7+ reporting grid, and distinguish full zero-inclusive pairwise p-values from user-only inference. Do not silently remove GMM without an explicit editorial decision. This is a documentation stage, not a newly executed study.

Paper 2.1 was created from Paper 2 at commit `1956ef4bfe6073c9b28881a9da34d14cd22239a8`. The branch now contains a complete Paper 2.1 manuscript draft. Before changing it, read `paper/docs/project/STATUS_AND_ROADMAP.md`, `paper/docs/project/PROJECT_CONTEXT.md`, `paper/docs/analysis/ANALYSIS_PLAN.md`, `paper/docs/results/PRELIMINARY_RESULTS.md`, `paper/docs/interpretation/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`, `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`, and `literature_selected/ACCESS_NOTES.md`.

## What Paper 2.1 changes

Paper 2.1 is not simply Paper 2 with more categories. Its central estimand is the observational structure of outcomes across **positive CMAT attendance frequencies**.

The inherited Paper 2 rule `0 / 1 / 2 / 3 / 4+` is superseded here. The current manuscript reporting grid is **`0 / 1 / 2 / 3 / 4 / 5 / 6 / 7+`**. The earlier outcome-blind audit selected `1 / 2 / 3 / 4 / 5 / 6+` as the better-supported positive-frequency inferential grouping; preserve that historical decision as a pooled-tail robustness check rather than rewriting it as if `7+` had been pre-specified.

## What remains inherited from Paper 2

- first eligible MU attempt with CMAT coverage;
- period-wide CMAT attendance irrespective of visit subject label;
- instructor × academic-period grading context;
- pass mark = 7.5;
- BA/BV/RT are adverse/non-passing;
- no causal claims;
- DMU diagnostic is not an acceptable uniform baseline;
- entrance exam, if received and usable, is only an observed-preparation sensitivity;
- exact institutional ethics/data-use wording remains required before submission.

## Principal outcomes and academic-result states

### Binary performance
PASS = numeric grade >=7.5.

non-PASS = numeric grade <7.5, BA, BV, or RT.

### Continuous performance
Use the canonical Paper 2 adverse-outcome imputation and standardise final performance within instructor-period group. Keep the numeric complete-case standardised outcome as a sensitivity.

### Academic-result composition
Primary descriptive states are PASS / numeric <7.5 / BV-RT / BA. Also preserve BV, RT and BA separately in an exact administrative-token table.

Among non-PASS cases, analyse administrative outcome versus numeric failure, BV/RT versus numeric failure, and **BV versus numeric failure**. Current controlled-data evidence is specifically concentrated in BV; RT does not show the same adjusted 0-versus-1+ pattern. Do not generalise the BV result to all administrative codes, and do not merge BA with BV/RT when discussing a student-initiated academic-management mechanism.

In manuscript prose, any timing caveat should normally be limited to one sentence noting that administrative outcomes may occur before the end of the academic period and can therefore provide less opportunity to accumulate visits.

## Inference hierarchy

For continuous Z, primary inference should come from the fixed-effect model with cluster-robust uncertainty; Welch/Games–Howell is secondary.

For PASS, report adjusted probability/risk differences in percentage points using the same basic fixed-effect and clustering logic. Do not present an ANOVA on a binary outcome as the main analysis.

All positive-group pairwise comparisons require a predeclared multiplicity family and adjustment.

## Equivalence

A non-significant pairwise test does not establish that two attendance groups are the same. Use the word **equivalent** only if a formal equivalence design with a pre-specified practical margin is implemented.

Otherwise classify unsupported pairwise comparisons as inconclusive.

## Heatmaps

Heatmap colour represents effect magnitude/direction:

- difference in Z for the continuous outcome;
- difference in pass probability for the binary outcome.

Do not colour by p-value. Statistical/equivalence status may be indicated separately.

The main pairwise dashboards now use the full `0 / 1 / 2 / 3 / 4 / 5 / 6 / 7+` grouping. The effect dashboard combines adjusted standardised-grade differences with PASS odds-ratio point estimates; the p-value dashboards show raw and Holm-adjusted inference, with PASS significance taken from the stable fixed-effect linear-probability model.

## Academic-management mechanism guardrail

Paper 2.1 may discuss the hypothesis that CMAT attendance marks broader academic engagement or institutional navigation, but only as a mechanism compatible with the observed outcome composition. Read `paper/docs/interpretation/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`.

Never infer from zero recorded visits that a student did not care about the course, university, GPA, or withdrawal options. Never write that CMAT users are definitively more engaged unless a direct engagement measure is obtained.

Before claiming a specific GPA or transcript consequence of BV/RT, verify the institutional rule and its historical applicability to the study years.

## Literature framing

Paper 2.1 now begins with a dense state of the art. The literature review must lead to the gap concerning the **shape and distinguishability of repeated mathematics-support attendance**, not merely repeat that support users often outperform non-users.

Use prior observational and identification-oriented evidence together, preserving the distinction between association and causal evidence.

Do not claim diminishing returns before the Paper 2.1 analyses support that shape.

`gokhool2026` is currently **abstract-only**. It may be cited for the two-dimensional engagement framing (0 vs 1+; visit count among users), the Coventry/12-discipline scope, listed demographic predictors, and the hurdle-model specification stated in the abstract. Do not attribute results, effect sizes, limitations, or conclusions not present in the supplied abstract. See `literature_selected/ACCESS_NOTES.md`.

## Manuscript status

`paper/sections/01.tex`--`04.tex` are now the canonical Paper 2.1 draft. They include the dense state of the art, frozen grouping rationale, benchmark and user-frequency results, academic-management/BV results, distributional sensitivity, limitations and conclusion. Do not revert them to the inherited Paper 2 wording.

The draft is **not submission-ready** until the TODOs in `paper/docs/project/STATUS_AND_ROADMAP.md` are resolved, especially instructor-level clustering, entrance-exam sensitivity if available, institutional rule verification, and ethics/data-use wording.

## Shared-library provenance

The reusable methods developed during Paper 2.1 are upstreamed to `main`. The current reusable API version is **cmat-analysis 0.4.3**. Canonical shared functions now include:

- `add_academic_outcome_states` in `cmat_analysis.measures`;
- `add_topcoded_visit_group`;
- `visit_frequency_support_audit`;
- `visit_frequency_cut_frontier`;
- `visit_group_pair_overlap`;
- `fixed_effect_group_comparisons`;
- `group_outcome_summary`;
- `outcome_state_composition`;
- `distribution_profile`;
- `pairwise_effect_matrix`;
- `fit_univariate_gaussian_mixture`;
- `gaussian_mixture_model_selection`;
- `gaussian_mixture_component_summary`;
- `gaussian_mixture_responsibilities`;
- `soft_component_composition`;
- `parametric_bootstrap_gmm_lrt`;
- `skew_normal_fit_summary`;
- `compare_univariate_shape_models`;
- `parametric_bootstrap_skew_normal_vs_gmm`;
- `cross_validated_skew_normal_vs_gmm` in `cmat_analysis.statistics`.

The Paper 2.1 runners now delegate those calculations to the library. Do not reintroduce local copies unless the shared API cannot represent a scientifically different estimand. Shared API documentation lives in the Sphinx guide `cmat_analysis/docs/user_guide/attendance_frequency.rst` and in `cmat_analysis/FUNCTION_INDEX.md`.

## Repository governance

Do not merge the whole paper branch into `main` or Paper 2. Shared scientific functions discovered here should go through the upstream library process first; Paper 2.1 is now a downstream consumer of the reviewed main-library capability.


## Current manuscript story

The current manuscript's main substantive story is:

- strong zero-versus-positive separation;
- no discontinuity at the three-visit PPA threshold, so visits 1--3 must be interpreted cautiously as potentially incentive-influenced;
- descriptive shifts beyond that range, especially four-to-five and exact-six-to-7+, with the 7+ PASS profile remaining significantly above one visit after Holm adjustment;
- a high-performance and lower-performance outcome structure that is much clearer in the imputed completed outcome than in observed numeric grades alone.

Do not turn the 4-to-5 or 6-to-7+ descriptive changes into causal thresholds: neither adjacent contrast is statistically resolved. The 7+ group is distinctive mainly because of its overall profile and its Holm-significant PASS contrast with one visit, not because 6 versus 7+ is significant.

## Combined ridgeline figure

Paper 2.1 no longer uses separate figures for mean standardised performance and final-outcome composition. The canonical descriptive figure is:

`results/paper21/figures/fig01_distribution_composition_ridgeline.pdf`

It combines the former Figure 1 and Figure 4. For each `0/1/2/3/4/5/6/7+` attendance group:

- the horizontal axis is the primary instructor-period-standardised outcome;
- the ridge is a real-data Gaussian KDE;
- PASS, numeric <7.5, BV, RT, and BA are stacked as weighted KDE components;
- all components within a group use one common bandwidth;
- each component is divided by the full group N, so its area equals the observed within-group share and the components sum to the total group KDE;
- the point and horizontal interval show the group mean and 95% CI;
- the plotted x-window is fixed at $Z\in[-2,2]$ so the descriptive ridgeline and complete-case mixture ridgeline use the same central scale; observations outside that display window remain in the underlying analysis.

For BV, RT, and BA, horizontal position uses the numerical value assigned by the canonical primary adverse-outcome imputation. This must be stated in the caption.

The reusable density calculation is `cmat_analysis.statistics.mixture_component_density`; the reusable plotter is `cmat_analysis.visualization.plot_stacked_ridgeline`. Do not recreate paper-local KDE logic.


## Observed numeric failure and Gaussian mixtures

Read `paper/docs/analysis/MIXTURE_ANALYSIS_PLAN.md` before interpreting or modifying this analysis.

The evidence hierarchy is binding:

1. observed numeric-failure probability/odds;
2. GMM on `Z_GRADE_COMPLETE_CASE` as the primary multimodality analysis;
3. GMM on `Z_GRADE_PRIMARY` only as sensitivity to BV/RT/BA imputation.

The mixture runner is `code/run_paper21_mixture.py`. It compares K=1/2/3 with BIC/ICL and uses a parametric-bootstrap likelihood-ratio test for K=1 vs K=2. It also compares one skew-normal with GMM K=2 using three complementary diagnostics: AIC/BIC on the observed sample, a parametric bootstrap generated under the fitted skew-normal null, and repeated held-out log predictive density. Groups 0--5 come from the historical zero-inclusive fit; exact 6 and 7+ are re-estimated separately in outputs 53--68 and are combined into the current main figures. The proposed means (-1.1, 0.5) are only one additional EM initialization; default multistart EM and empirical-quantile starts are also used.

Never call the components "good students" and "students who tried but failed". Use `lower-performance component` and `higher-performance component`, because the model identifies distributional components rather than psychological or causal student types.

Posterior responsibilities are aggregated softly. No row-level component assignments are saved.

Do not claim that a low-performance component disappears after six visits unless the complete-case analysis supports this robustly; even then, high-frequency attendance is vulnerable to persistence/opportunity-time selection.

Controlled validation now has two layers. The historical 199-replicate GMM run is `35657154301`, and the earlier integrated recipe was revalidated successfully in run `36685329947` at branch head `93b16efb40efd7ed6803ab50568bc5fb075a10b9`, with tables 01--48 and figures 01--05 verified. The direct skew-normal-null bootstrap and predictive comparison was then validated in focused run `36826363767` at branch head `50f6e568aa38f3b9ec99be4b08124c72a1e989b8`, which verified tables 47--52 and uploaded artifact `paper21-shape-validation-50f6e568aa38f3b9ec99be4b08124c72a1e989b8` (artifact ID `11145891079`). The full Paper 2.1 CI is configured to verify tables 01--52 and publication figures with the more intensive settings, while the focused shape workflow is the rapid reproducibility check for the specification question.

The canonical combined interpretation is in `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`. For numeric complete cases, zero, one and two visits show concordant evidence for the two-Gaussian representation; three and four are adequately skew-normal, five is inconclusive, exact six is adequately skew-normal, and the apparent 7+ GMM is an unstable tail fit whose lower component is essentially one failed observation. For the imputed outcome, groups 0--5 and 7+ favour the mixture, while exact six is mixed across diagnostics. Among users the imputed higher-component mean stays near 0.54--0.65 SD, while lower-component weight changes sharply, including 35.7% to 9.1% from four to five visits and 25.2% to 14.3% from exact six to 7+. The imputed lower component is strongly enriched in administrative outcomes, especially BV. Preserve the distinction between descriptive mixture structure and literal latent student types.
