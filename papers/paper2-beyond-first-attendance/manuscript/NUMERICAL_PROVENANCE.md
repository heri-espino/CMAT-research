# Quantitative claims and immutable result provenance

This register accompanies the manuscript source in draft PR #99. Values are observational and reproduced from committed aggregate output rather than re-estimated. References to files on historical branches are source records, **not** claims that the files were migrated to this branch. Numbers appearing in cited external literature retain their paper-level bibliography citations. The methods agent's full claims-to-evidence matrix remains the authoritative review document; this register is an author-side mapping, subject to administrator audit.

## Frozen source heads

- **H — original Paper 2.1 Holm/Wald:** `1546c594bfb6867ad52064594469061ec7fd7fc6` on `paper/paper2.1-visit-frequency`.
- **F — ordered fused frequency:** `29810a86aef4c13a0327760955fae674ac349981` on `paper/paper2.2.1-fused-frequency`.
- **M — inherited mixture diagnostics:** `b1cace126fd73b74e8353c8a6170dc40af2243c2` on `paper/paper2.2.2-distributional-heterogeneity`.
- **R — supplementary fit and predictive research:** `5915976ff5a7e3c4eededd0c1e39290b8b4d402c` on `research/paper21-shapley-predictive-importance`.

Use `https://github.com/heri-espino/CMAT-research/blob/<FULL_HEAD_SHA>/<SOURCE_PATH>` to open the exact immutable source; e.g. [historical benchmark](https://github.com/heri-espino/CMAT-research/blob/1546c594bfb6867ad52064594469061ec7fd7fc6/results/paper21/tables/10_benchmark_0_vs_1plus.csv).

| Main manuscript numerical claim | Source and path | Model/population / inferential qualification |
|---|---|---|
| Cohort N=6,627; zero N=5,393; any N=1,234; 190 professor–period contexts | H: `results/paper21/tables/10_benchmark_0_vs_1plus.csv`, `11_primary_group_descriptives.csv` | First eligible MU attempt; no causal allocation |
| Exact category sizes: 0=5,393; 1=517; 2=245; 3=170; 4=96; 5=55; 6=50; 7+=101 | H: `results/paper21/tables/10n_zero_inclusive_7plus_descriptives.csv` | Raw subgroup counts, descriptive |
| Z any versus none +0.3612 SD, 95% CI [0.3017,0.4207]; PASS +15.29 pp, CI [12.44,18.15] pp | H: `results/paper21/tables/10_benchmark_0_vs_1plus.csv` | Full-cohort OLS and LPM with degree/instructor-period FE; clusters=190; **association** |
| Positive-user (1/2/3/4/5/6+) omnibus Z p=.31655 and PASS p=.15222; N=1,234 and 176 contexts | H: `results/paper21/tables/12_primary_omnibus.csv` | Omnibus across six positive frequencies; non-rejection not equality |
| 15-pair user-only Holm results; raw 1 vs 6+ Z p=.02188, PASS p=.01141; Holm .32814 and .17108 | H: `results/paper21/tables/13_primary_pairwise_continuous.csv`, `14_primary_pairwise_pass.csv` | 15 within-outcome pairs, distinct from seven-level and full-grid sensitivities |
| Positive-only seven-level omnibus Z p≈.21257 and PASS p≈.10198; 21-pair Holm no pair survives | H: `results/paper21/tables/21_sensitivity_7plus_omnibus.csv`, `22_sensitivity_7plus_pairwise_continuous.csv`, `23_sensitivity_7plus_pairwise_pass.csv` | Later exploration and changed upper-tail support |
| Zero-inclusive eight-level Z/PASS all seven zero-vs-positive contrasts Holm-positive; PASS 7+ minus 1 = +14.49 pp (95% CI [+5.91,+23.07], Holm p=.02056) | H: `results/paper21/tables/26a_zero_inclusive_7plus_pairwise_continuous.csv`, `26k_zero_inclusive_7plus_pairwise_pass_lpm.csv`, `26i_zero_inclusive_7plus_omnibus.csv` | 28 Holm pairs **per outcome**; do not equate to positive-only analysis |
| Instructor-cluster sensitivity: nonadjacent PASS 6+ minus 1 = +12.01 pp; CI [+4.26,+19.76]; Holm p=.03579 | H: `results/paper21/tables/27_instructor_cluster_pairwise_pass.csv`, `28_instructor_cluster_omnibus.csv` | 51 professors, alternative covariance; not replication or an adjacent step |
| Piecewise Z ANY +.30656 SD and EXTRA +.03609 SD; PASS ANY +11.923 pp and EXTRA +2.225 pp | R: `results/paper21/tables/followup_questions/two_part_attendance_z_pass.csv` | 2-term Holm per outcome, top-coded 7+; slope imposes linear increments |
| Linear vs categorical held-out skill: Z .016917 vs .016303; PASS .003715 vs .002710 | R: `results/paper21/tables/attendance_curves/group_heldout_shape_cv.csv` | 5 professor–period GroupKFold; no unseen FE or temporal forecasting |
| Fused Z split 0 | 1+ stable in 100/100 refits; held-out Z +.26362 CI [.14999,.37725]; PASS 0|1 in 37/100 refits, all-fused selected despite discovery BIC rank 128/128 | F: `results/paper221/run_manifest.json`; `tables/7plus_z_grade_primary_boundary_stability.csv`, `tables/7plus_z_grade_primary_holdout_wald.csv`, `tables/7plus_pass_boundary_stability.csv`, `tables/7plus_pass_exhaustive_partitions.csv` | Internal algorithmic holdout, not population boundary probabilities; selection-rule sensitivity |
| Grouped Shapley in-sample Z attendance contribution .01803 of total R² .05823; PASS attendance .01331 of total R² .17182 | R: `results/paper21/tables/shapley_importance/in_sample_shapley_12_models.csv` | Fit allocation, no causal interpretation |
| Out-of-context heldout Z attendance .01509 vs degree .00339; PASS Brier attendance .00536 vs degree .01225 | R: `results/paper21/tables/shapley_importance/out_of_context_shapley.csv` | Same-term **retrospective** skill |
| Historic complete-case/imputed GMM and skew-normal comparisons | M: `results/paper21/tables/37_complete_case_gmm_selection.csv`, `47_complete_case_skewnormal_vs_gmm.csv`, `48_imputed_skewnormal_vs_gmm.csv` | Model adequacy only; new 2.2.2 modality tests still pending |

## Unavailable estimates and verification gates

**No numerical PPA-group adjusted results are yet asserted.** The administrator now requires only `0 | 1–3 | 4+`; the PPA analysis branch inspected had source/test files but no result run manifest or empirical tables. Actual individual PPA eligibility, credit and motivations are not observed.

The main LaTeX retains historic Paper 2.1 numerical prose. Until the designated scientific auditor signs off, do not mistake this author-side ledger for a new replication of protected microdata, a claim of empirical PPA validation, formal registration of exploratory groupings, or a fully reviewed simultaneous confidence-interval procedure. The committed source still needs **its own PDF build and GitHub blob verification** before release. The prior Paper 2.1 PDF remains unchanged.