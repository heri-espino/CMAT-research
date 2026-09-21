# Paper 2.1 — AI handoff

This file contains branch-specific rules for `paper/paper2.1-visit-frequency`.

Paper 2.1 was created from Paper 2 at commit `1956ef4bfe6073c9b28881a9da34d14cd22239a8`. The branch now contains a complete Paper 2.1 manuscript draft. Before changing it, read `paper/STATUS_AND_ROADMAP.md`, `paper/PROJECT_CONTEXT.md`, `paper/ANALYSIS_PLAN.md`, `paper/PRELIMINARY_RESULTS.md`, `paper/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`, and `paper/LITERATURE_ACCESS_NOTES.md`.

## What Paper 2.1 changes

Paper 2.1 is not simply Paper 2 with more categories. Its central estimand is the observational structure of outcomes across **positive CMAT attendance frequencies**.

The inherited Paper 2 rule `0 / 1 / 2 / 3 / 4+` is superseded here. The outcome-blind audit has frozen the primary positive-frequency grouping as **`1 / 2 / 3 / 4 / 5 / 6+`**. The decision must not be changed after inspecting outcome significance; see `paper/VISIT_GROUPING_DECISION.md`.

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

The main heatmaps focus on positive attendance-frequency groups. A zero-inclusive version may appear as a benchmark/supplement.

## Academic-management mechanism guardrail

Paper 2.1 may discuss the hypothesis that CMAT attendance marks broader academic engagement or institutional navigation, but only as a mechanism compatible with the observed outcome composition. Read `paper/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`.

Never infer from zero recorded visits that a student did not care about the course, university, GPA, or withdrawal options. Never write that CMAT users are definitively more engaged unless a direct engagement measure is obtained.

Before claiming a specific GPA or transcript consequence of BV/RT, verify the institutional rule and its historical applicability to the study years.

## Literature framing

Paper 2.1 now begins with a dense state of the art. The literature review must lead to the gap concerning the **shape and distinguishability of repeated mathematics-support attendance**, not merely repeat that support users often outperform non-users.

Use prior observational and identification-oriented evidence together, preserving the distinction between association and causal evidence.

Do not claim diminishing returns before the Paper 2.1 analyses support that shape.

`gokhool2026` is currently **abstract-only**. It may be cited for the two-dimensional engagement framing (0 vs 1+; visit count among users), the Coventry/12-discipline scope, listed demographic predictors, and the hurdle-model specification stated in the abstract. Do not attribute results, effect sizes, limitations, or conclusions not present in the supplied abstract. See `paper/LITERATURE_ACCESS_NOTES.md`.

## Manuscript status

`paper/sections/01.tex`--`04.tex` are now the canonical Paper 2.1 draft. They include the dense state of the art, frozen grouping rationale, benchmark and user-frequency results, academic-management/BV results, distributional sensitivity, limitations and conclusion. Do not revert them to the inherited Paper 2 wording.

The draft is **not submission-ready** until the TODOs in `paper/STATUS_AND_ROADMAP.md` are resolved, especially instructor-level clustering, entrance-exam sensitivity if available, institutional rule verification, and ethics/data-use wording.

## Shared-library provenance

The reusable methods developed during Paper 2.1 are upstreamed to `main`. The current reusable API version is **cmat-analysis 0.4.0**. Canonical shared functions now include:

- `add_academic_outcome_states` in `cmat_analysis.measures`;
- `add_topcoded_visit_group`;
- `visit_frequency_support_audit`;
- `visit_frequency_cut_frontier`;
- `visit_group_pair_overlap`;
- `fixed_effect_group_comparisons`;
- `group_outcome_summary`;
- `outcome_state_composition`;
- `distribution_profile`;
- `pairwise_effect_matrix` in `cmat_analysis.statistics`.

The Paper 2.1 runners now delegate those calculations to the library. Do not reintroduce local copies unless the shared API cannot represent a scientifically different estimand. Shared API documentation lives in the Sphinx guide `cmat_analysis/docs/user_guide/attendance_frequency.rst` and in `cmat_analysis/FUNCTION_INDEX.md`.

## Repository governance

Do not merge the whole paper branch into `main` or Paper 2. Shared scientific functions discovered here should go through the upstream library process first; Paper 2.1 is now a downstream consumer of the reviewed main-library capability.


## Combined ridgeline figure

Paper 2.1 no longer uses separate figures for mean standardised performance and final-outcome composition. The canonical descriptive figure is:

`results/paper21/figures/fig01_distribution_composition_ridgeline.pdf`

It combines the former Figure 1 and Figure 4. For each `0/1/2/3/4/5/6+` attendance group:

- the horizontal axis is the primary instructor-period-standardised outcome;
- the ridge is a real-data Gaussian KDE;
- PASS, numeric <7.5, BV, RT, and BA are stacked as weighted KDE components;
- all components within a group use one common bandwidth;
- each component is divided by the full group N, so its area equals the observed within-group share and the components sum to the total group KDE;
- the point and horizontal interval show the group mean and 95% CI;
- the plotted x-window shows the central 99% of each smoothed group distribution so extreme imputed lower-tail values do not compress the visual display; those observations remain in the underlying analysis.

For BV, RT, and BA, horizontal position uses the numerical value assigned by the canonical primary adverse-outcome imputation. This must be stated in the caption.

The reusable density calculation is `cmat_analysis.statistics.mixture_component_density`; the reusable plotter is `cmat_analysis.visualization.plot_stacked_ridgeline`. Do not recreate paper-local KDE logic.


## Observed numeric failure and Gaussian mixtures

Read `paper/MIXTURE_ANALYSIS_PLAN.md` before interpreting or modifying this analysis.

The evidence hierarchy is binding:

1. observed numeric-failure probability/odds;
2. GMM on `Z_GRADE_COMPLETE_CASE` as the primary multimodality analysis;
3. GMM on `Z_GRADE_PRIMARY` only as sensitivity to BV/RT/BA imputation.

The mixture runner is `code/run_paper21_mixture.py` and writes aggregate outputs 30--45. It compares K=1/2/3 with BIC/ICL and uses a parametric-bootstrap likelihood-ratio test for K=1 vs K=2. The proposed means (-1.1, 0.5) are only one additional EM initialization; default multistart EM and empirical-quantile starts are also used.

Never call the components "good students" and "students who tried but failed". Use `lower-performance component` and `higher-performance component`, because the model identifies distributional components rather than psychological or causal student types.

Posterior responsibilities are aggregated softly. No row-level component assignments are saved.

Do not claim that a low-performance component disappears after six visits unless the complete-case analysis supports this robustly; even then, high-frequency attendance is vulnerable to persistence/opportunity-time selection.

At the time this section was added, GitHub Actions jobs were failing before executing any steps across both `main` and the paper branch. Therefore the implementation is present but no controlled-data GMM result has yet been accepted into the manuscript.
