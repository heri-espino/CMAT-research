# Paper 2 scientific methodology audit — remote artifact provenance

**Audit date:** 2026-10-26; second remote review on the same date after the administrator changed the PPA requirement and new agent branches/QA became available. **NOT RELEASE-APPROVED — critical public controlled-data disclosure.** **Authoring branch:** `paper/paper2-methods-audit-agent`, forked explicitly from `paper/paper2-beyond-first-attendance`, which existed at `d61739ff89eca96be5113a1cb47ea8be496891dd` at branch creation. No original analysis source, historical branch or institutional data was changed.

## Verified source snapshots

| Source | Branch head at audit | Representative verified paths and Git blob SHA |
|---|---|---|
| Historical Holm anchor | `paper/paper2.1-visit-frequency @ 1546c594bfb6867ad52064594469061ec7fd7fc6` | `results/paper21/tables/10_benchmark_0_vs_1plus.csv` `7d46b93747280e465804bb5f87e44919d133b552`; `12_primary_omnibus.csv` `ce43f64fa89e499b31ba69329e93cc1e6790079d`; `13_primary_pairwise_continuous.csv` `98b4aa1d7b958fa2bdc352db1b64f767ea0c43c1`; `14_primary_pairwise_pass.csv` `0930761c16c308ea1006291075d05c1d545f085a`; `26k_zero_inclusive_7plus_pairwise_pass_lpm.csv` `729ab741a2595d7e735d51d8a06632dcd9e96f20` |
| Additional Holm model diagnostics | Same H branch head | `results/paper21/tables/28_instructor_cluster_omnibus.csv` `d22a488ef4fe418b081a409d062d8538a9958c75`; `29_instructor_cluster_benchmark_0_vs_1plus.csv` `bd1a0e3274a3699efd0f6846bddf8fb535df8b7e`; `adjustment_experiment/pass_model_diagnostics_4x2.csv` `fae8836cabf01601338e45374f3d7bb2c095c58e` |
| Numeric and administrative endpoints | Same H branch head | `results/paper21/tables/30_numeric_failure_descriptives.csv` `7c3e021ba1333f19647cd7e78cc6886470de43f5`; `31a_numeric_failure_adjusted_probabilities_zero_inclusive.csv` `86b4fe29fb4868cc14a41582e964a05086e9cf40`; `10e_nonpass_management_benchmark_0_vs_1plus.csv` `39f14f1999e8153d93cac5846d91765f475b5e` |
| Historical mixture / skew fit | `paper/paper2.2.2-distributional-heterogeneity @ b1cace126fd73b74e8353c8a6170dc40af2243c2` | `results/paper21/tables/37_complete_case_gmm_selection.csv` `b8cce7f8dfa495701309a33b31c7812a85678f9a`; `39_complete_case_gmm_bootstrap_1_vs_2.csv` `502d46916214ac0f944e57c53be42cd53fd9f51a`; `47_complete_case_skewnormal_vs_gmm.csv` `82e21eac4565f4f31695f70024e814f31dc38612`; `48_imputed_skewnormal_vs_gmm.csv` `926cbca1f7549dd75dc490dfe32bb42f35154d36`; `49_complete_case_skewnormal_bootstrap_vs_gmm.csv` `2c31b18bd37f5cd358a3d5f06ecf927c132cb2a0`; `50_complete_case_skewnormal_vs_gmm_cross_validation.csv` `ff08b5b096e7700a559c9570276617282d8e46fb` |
| Fused-lasso completed run | `paper/paper2.2.1-fused-frequency @ 29810a86aef4c13a0327760955fae674ac349981` | `results/paper221/run_manifest.json` `f1463463d91a5d4af6144af33210283599f2cd54`; `tables/7plus_z_grade_primary_boundary_stability.csv` `02afd71889dfea45604eff423ada18c72fb4a229`; `tables/7plus_pass_boundary_stability.csv` `d0bf374539ae657a7ec6851bf729a6aafb9a67c3`; `tables/7plus_z_grade_primary_holdout_wald.csv` `3a5151fd5b9739e3bca20c404fe1cce1c5375099`; `tables/7plus_pass_holdout_wald.csv` `8b137891791fe96927ad78e64b0aad7bded08bdc` (empty) |
| Grouped Shapley and holdout | `research/paper21-shapley-predictive-importance @ 5915976ff5a7e3c4eededd0c1e39290b8b4d402c` | `results/paper21/tables/shapley_importance/in_sample_shapley_12_models.csv` `c68bad74e49af2501c3b74a09de523cf063fa1bc`; `out_of_context_shapley.csv` `2ce4a79da2842835b21958674443ba2903a42599` |
| First-versus-additional visits | Same R branch head | `results/paper21/tables/followup_questions/two_part_attendance_z_pass.csv` `39f3b781ad162c5c9ec146e437b8e70239ff0d42`; `numeric_vs_administrative_composition.csv` `d3924bd6bde792be4572278f66e06d9315f8548c` |
| Attendance curves (published after older ledger) | Same R branch head | `results/paper21/tables/attendance_curves/model_comparison_in_sample.csv` `e3c711a2bd74e2f7df29153c56f5b5e6747e59f2`; `adjacent_differences_holm.csv` `bda72c6950c7afd28524dd72a8849a39f82791f9`; `group_heldout_shape_cv.csv` `e8b7497284513f61709661d4874ad842c25465d4`; `unadjusted_means_cluster_ci.csv` `0102b05daed2a19df0cf0b15be39110535601f2b`. Four corresponding committed `results/paper21/figures/attendance_curves/*.png` were inventoried; figures were not re-rendered. |

## Historical parent versus executable run SHA

- The fused manifest records execution commit `c9faa397bd0a6c7c8c67025ab94f8314e0996018`, UTC `2026-10-08T02:50:36.054293+00:00`, four specifications with `100/100` successful bootstrap retunes and **no warnings**, on a head now at `29810a86...`. The actual underlying input-file SHA-256 fingerprints are retained **only in the original manifest** and deliberately not reprinted here.
- Mixture and skew-fit records in branch M are inherited Paper 2.1 historical analyses. The prospective Paper 2.2.2 modality extension was marked *research design only* in `PAPER_BRANCH.md`; this audit has not fabricated a Paper 2.2.2 experiment.
- The research branch's `notes/25_PUBLICATION_LEDGER.md` now contains a 2026-10-26 supersession paragraph correcting its archived October 25 missing-results text.
- The *later* PPA agent branch `324fd86d23e2ccbf1f430497b0abb08853f6c7f0` contains PPA code/tests, historical aggregate counts and a provenance `STATUS.md` declaring empirical PPA regression results **pending**. It retains the withdrawn four-group model and an exploratory 18-contrast Holm correction spanning both outcomes and two grouped models. The **latest** administrator charter on `main` `d6b1670553e9a838339c4c0bebb397667ba3a392` requires *only* `0|1–3|4+`, so new results must not be approved until specification/family alignment. No PPA effect estimate was entered into the claims matrix.

## Verification scope and limitations

The GitHub connector was used to fetch the *actual repository branch listing, individual committed UTF-8 source notes, JSON manifest and CSV contents* rather than relying exclusively on branch descriptions. A recursive Git tree confirmed the source file inventories. For quoted results, model outcome, row/group, coefficient direction, standard error/CI/p, sample N, cluster count and correction-family context were cross-read where the CSV exposed them.

**Independently checked in second pass:** Holm p-value step-down and nominal normal-approximation CI arithmetic for 148 committed aggregate Wald contrast rows (original 10-pair, user-only 15-pair, user-only 21-pair, zero-inclusive 28-pair, two outcomes each). No adjusted-p mismatches, maximum CI arithmetic absolute deviation 6.91e-6. Read public GitHub repository metadata and targeted **directory listings/policy text only**, without fetching protected row-level file bodies. Independently inspected historical invalid PASS-logit CSV's 28 inconsistent boolean flags. **Not performed:** controlled-data microdata access; full software/model rerun; regeneration of fitted covariance/uncertainty from rows; screenshot-based independent rendering of binary PDF/PNG figures; full confidential history/artifact scan; statistical disclosure review of any new aggregated PPA result; Git LFS filesystem verification. This work is documentation-only and contains no student-level data or identifiers.


## Second-pass external dependency snapshots (2026-10-26)

| Dependency | Verified branch / current artifact | Implication |
|---|---|---|
| Canonical charter | `main @ d6b1670553e9a838339c4c0bebb397667ba3a392`; `docs/PAPER2_CONSOLIDATION_PLAN.md` | Explicitly **only three PPA groups** `0|1–3|4+`; four-group is *not requested* |
| Integration home | `paper/paper2-beyond-first-attendance @ 8f687416522f40a016373e341cf0df697e64bf37` | Architecture source register and publication skeleton present; downstream PRs remain separate |
| PPA candidate | `paper/paper2-ppa-groups-agent @ 324fd86d23e2ccbf1f430497b0abb08853f6c7f0`, PR #98 | Empirical regressions **not run/published**; four-group and 18-test family remain coded against current requested scope |
| Original manuscript candidate | `paper/paper2-manuscript-agent @ f3d06e4fc26790a1d27dc48e36122417a6632745`, PR #99 | Editable manuscript and integrated-evidence section; `BUILD_STATUS.md` lacks byte-verified integrated GitHub PDF |
| Marp candidate | `paper/paper2-marp-agent @ 676690623e3531afee3b22d6017ba74df82bfd78`, PR #100 | Markdown and eleven `figures/*.svg` resources present, but PPA slide still refers to four-group, and final PDF not verified |
| Independent release QA | `paper/paper2-qa-agent @ b33f7a508172e85bfc11527a86b2cdb7dce09617`, PR #96 | Flags P0 public restricted student data and 28 invalid PASS-logit rejection flags. Its *earlier* four-group requirement interpretation is superseded by main's subsequently amended administrator charter. |

**Independently verified privacy policy conflict:** `heri-espino/CMAT-research` is **public** and current `main/data/controlled/` contains pseudonymized academic/advisory/diagnostic files and linkable normalized person-level records. `data/controlled/PRIVACY_README.md` states the information is **not anonymized**, retains potentially identifying quasi-identifiers, and may reside in the repository only while **private**. This audit contains no student records. The administrator/institutional data custodian must handle current exposure and historical distribution as a security incident before release; a paper-agent methods PR cannot remediate it.

**Second-pass numerical verification details:**

| Source family | Z records; Holm rejections | PASS records; Holm rejections | Max Holm absolute error |
|---|---:|---:|---:|
| Original `0/1/2/3/4+` | 10; 4 | 10; 5 | 0 |
| Positive users `1/2/3/4/5/6+` | 15; 0 | 15; 0 | 0 |
| Positive users `1/2/3/4/5/6/7+` | 21; 0 | 21; 0 | 0 |
| All `0/1/2/3/4/5/6/7+` | 28; 7 | 28; 8 | 0 |

The Holm algorithm was independently recomputed by ascending raw p-value, step-down multiplier `(m-j+1)` and monotone cumulative maximum, capped at 1. The source nominal CI calculations agree with `estimate ±1.96×cluster_SE` within 7e-6. This is an exported-result consistency check, **not** independent validation of institutional clustering or sampling design.

## Editorial controls

The [claims matrix](../../docs/claims-evidence-matrix.md), [methodological synthesis](../../docs/methodological-synthesis.md) and [discrepancy report](../../docs/discrepancy-report.md) are **recommendations** to the administrator and do not automatically certify a final article or alter approved historical research. The integration branch remains the PR base; its owner decides when scientific gates are satisfied.
