# Paper 2.1 — status and roadmap

**Branch:** `paper/paper2.1-visit-frequency`  
**Created from Paper 2:** 2026-09-20  
**Stage:** controlled analysis complete + manuscript integrated; external pre-submission inputs remain

## Current scientific idea

Paper 2.1 starts from a dense state-of-the-art review and places the zero-attendance benchmark and repeated CMAT use in a common `0 / 1 / 2 / 3 / 4 / 5 / 6 / 7+` reporting grid. Its substantive focus is where outcome differences appear across that full attendance distribution, while distinguishing the broad zero-versus-positive margin from contrasts among CMAT users.

Two principal outcome families will be analysed in parallel:

1. PASS versus non-PASS, with non-PASS = numeric <7.5 or BA/BV/RT;
2. continuous imputed final grade standardised within instructor-period group.

The current `4+` top-code is not binding on this branch.

## Milestones

### M0 — Branch and scientific contract — COMPLETE

- [x] create `paper/paper2.1-visit-frequency` from current Paper 2;
- [x] separate Paper 2.1 scope from Paper 2;
- [x] define dual principal outcomes;
- [x] document outcome-blind upper-frequency grouping principle;
- [x] document pairwise, heatmap, and equivalence strategy.

### M1 — State of the art — DRAFTED

- [x] review the selected mathematics-support literature specifically for visit-frequency grouping and repeated attendance;
- [x] extract how prior studies define 0, 1, repeated, and high-frequency attendance;
- [x] identify evidence about non-engagement, self-selection, and repeated use;
- [ ] identify whether any study formally tests equivalence or saturation/plateau patterns;
- [x] draft a dense state-of-the-art section ending in the Paper 2.1 research gap;
- [ ] perform a final literature audit before submission and add only sources that materially inform frequency grouping, repeated attendance, outcome composition, or interpretation;
- [x] cite Gokhool & Lawson (2026) only for abstract-supported claims and record the access limitation in `literature_selected/ACCESS_NOTES.md`.

### M2 — Support audit and final visit grouping — COMPLETE

- [x] generate exact positive-visit counts with instructor-period support;
- [x] quantify within-instructor-period overlap among positive groups;
- [x] compare candidate top-codes using the pair-overlap frontier;
- [x] freeze the final grouping before inspecting Paper 2.1 outcomes;
- [x] record the decision in `paper/docs/analysis/VISIT_GROUPING_DECISION.md` and `paper/visit_grouping_spec.json`.

**Current manuscript reporting grid:** `0 / 1 / 2 / 3 / 4 / 5 / 6 / 7+`.

**Historical support-based robustness grouping:** positive-attendance `1 / 2 / 3 / 4 / 5 / 6+`; retain it to document the outcome-blind tail-support decision and for pooled-tail sensitivities.

### M3 — Dual-outcome and distributional inference

- [x] document the three-layer outcome framework in `paper/docs/analysis/OUTCOME_FRAMEWORK.md`;
- [x] document the administrative-withdrawal attendance context and manuscript guardrail in `paper/docs/interpretation/ADMINISTRATIVE_OUTCOME_NOTE.md`;
- [x] implement the reproducible Paper 2.1 outcome runner;
- [x] verify the current controlled-data run in CI;
- [x] reproduce 0 vs 1+ benchmark for PASS and continuous Z;
- [x] run user-only omnibus model for continuous Z;
- [x] run user-only omnibus model for PASS probability;
- [x] estimate all positive-group pairwise contrasts;
- [x] apply Holm adjustment separately by outcome family;
- [x] flag adjacent contrasts explicitly in the pairwise outputs;
- [x] implement instructor-level clustering sensitivity through the shared cmat_analysis API;
- [x] review the canonical instructor-level clustering outputs and report them in the manuscript as a sensitivity;
- [x] retain numeric-only continuous complete-case sensitivity;
- [x] implement PASS / numeric grade <7.5 / BV-RT / BA composition by frequency;
- [x] implement exact BV / RT / BA composition tables;
- [x] implement non-PASS administrative-vs-numeric benchmark and frequency models;
- [x] implement narrower non-PASS BV/RT-vs-numeric models;
- [x] implement imputed and complete-case Z-score quantile profiles;
- [x] verify and interpret the academic-management outputs from controlled-data CI, including BV-specific and RT-specific contrasts.

### M3A — Observed failure and Gaussian mixtures — COMPLETE

- [x] freeze the analysis hierarchy in `paper/docs/analysis/MIXTURE_ANALYSIS_PLAN.md`;
- [x] implement observed numeric-failure descriptives by `0/1/2/3/4/5/6+`;
- [x] implement model-standardized numeric-failure probabilities plus clustered fixed-effect logistic comparisons and Holm-adjusted odds ratios;
- [x] implement complete-case univariate GMM comparison for K=1/2/3;
- [x] include multiple EM starts, with (-1.1, 0.5) only as one additional two-component initialization;
- [x] implement BIC, ICL, posterior entropy, responsibilities, Ashman's D, and parametric-bootstrap 1-vs-2 component test;
- [x] implement soft component composition rather than hard class assignment;
- [x] repeat the GMM on the imputed primary Z only as a sensitivity;
- [x] obtain a successful controlled-data CI run and inspect outputs 30--46 (GitHub Actions run `35657154301`, head `50876b0e66f4893b4a447018be33f35bba4054e1`);
- [x] decide that the complete-case mixture evidence belongs in the manuscript only as exploratory distributional sensitivity, not as latent-class evidence;
- [x] implement the complete-case ridgeline with weighted lower/higher Gaussian overlays;
- [x] implement the compact lower-component weight figure, with the imputed specification shown as sensitivity;
- [x] add a conservative manuscript interpretation after inspecting the controlled-data estimates;
- [x] implement a one-component skew-normal specification check against one Gaussian and a two-Gaussian mixture;
- [x] validate tables 47--48 in the fast controlled workflow (run `36678572075`, commit `dc12a547acd726a6d8289115641813c0e5723c5a`);
- [x] document the refined result: imputed GMM K=2 beats a single skew-normal in every group, while the complete-case result is mixed;
- [x] quantify soft component composition among users, showing strong enrichment of BV/RT/BA in the imputed lower component;
- [x] promote the skew-normal and generic shape-comparison functions to `main/cmat_analysis`.
- [x] validate the fully integrated Paper 2.1 recipe after upstream synchronization (run `36685329947`, head `93b16efb40efd7ed6803ab50568bc5fb075a10b9`), verifying tables 01--48 and figures 01--05 in artifact `paper21-analysis-93b16efb40efd7ed6803ab50568bc5fb075a10b9`.

### M4 — Equivalence and visual synthesis

- [x] decide that no defensible equivalence margin has been specified independently of the observed data, so no formal equivalence claim will be made;
- [x] do not run post-hoc equivalence tests; non-significant contrasts are not interpreted as equivalence;
- [x] replace the separate mean-Z and outcome-composition figures with one combined real-data ridgeline whose stacked component areas reproduce PASS / numeric <7.5 / BV / RT / BA shares;
- [x] produce continuous-Z pairwise heatmap;
- [x] produce pass-probability pairwise heatmap;
- [ ] optionally produce zero-inclusive supplementary heatmaps;
- [ ] fit an exploratory smooth/spline among users without using it to choose the categorical cut;
- [x] write a synthesis: strong zero-versus-positive separation, irregular positive-frequency structure, and no multiplicity-supported adjacent staircase; instructor-level clustering leaves open a broader low-versus-high separation.

### M5 — Entrance-exam extension — WAITING ON DATA

- [ ] inherit and complete the entrance-exam intake audit from Paper 2;
- [ ] assess coverage among the Paper 2.1 positive-frequency groups;
- [ ] rerun the principal models with observed baseline preparation if the score is usable;
- [ ] compare the frequency structure before and after baseline adjustment.

### M6 — Paper 2.1 manuscript — FULL DRAFT COMPLETE

- [x] replace the inherited Paper 2 manuscript with a Paper 2.1-specific manuscript;
- [x] begin with the dense state-of-the-art section;
- [x] keep 0 vs 1+ as a short benchmark rather than the main result;
- [x] make the pairwise frequency structure, performance margin, and academic-management margin the central Results section;
- [x] integrate the two heatmaps;
- [x] write a compact conclusion about what can and cannot be distinguished among attendance frequencies;
- [x] preserve observational/non-causal language.

## Shared-library status

Paper 2.1 reusable methods are upstream on `main`; the current mixture/logit, standardized-probability, skew-normal and shape-comparison extension is **cmat-analysis 0.4.2** and documented through Sphinx and the generated function index. The paper runners are downstream consumers; future methodological improvements should be made in `main/cmat_analysis` first whenever they are reusable across education studies.

## Immediate next task

The controlled Paper 2.1 analysis is now complete through the observed-failure, instructor-clustering and Gaussian-mixture extensions, and the corresponding interpretation is integrated into `paper/sections/01.tex`--`04.tex`. The full GMM validation is GitHub Actions run `35657154301` at `50876b0e66f4893b4a447018be33f35bba4054e1`, with tables 01--46 and figures 01--05. The subsequent skew-normal shape check is run `36678572075` at `dc12a547acd726a6d8289115641813c0e5723c5a`, which verified tables 47--48. `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md` is the canonical record of the combined distributional analysis.

Remaining pre-submission work depends partly on inputs not contained in the repository: (1) add the university entrance-exam sensitivity if the requested data are usable; (2) verify historical institutional rules for BV/RT/BA before making any GPA/transcript claim; (3) insert the exact ethics/IRB/data-use authorization statement; and (4) run a final referee-style literature, numerical-consistency and typesetting audit. The frozen `1/2/3/4/5/6+` grouping must not be changed in response to outcome significance.
