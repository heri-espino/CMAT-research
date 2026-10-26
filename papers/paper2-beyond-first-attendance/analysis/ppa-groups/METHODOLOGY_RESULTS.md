# PPA visit-band analysis: methods, findings boundary, and reproduction

**Status: executable analysis staged; institutional regression results PENDING.** Boundary and synthetic tests are implemented; no new adjusted outcome estimates, clustered CIs, omnibus significance tests, or plots have been obtained from the validated student-level cohort in this environment. Do not write new statistical conclusions until the institutional runner succeeds. This component is **exploratory/post hoc**, not part of the original outcome-blind Paper 2.1 grouping decision.

## Question, cohort, and exposure
Question: How do observed same-period CMAT attendance associations differ around the optional three-visit PPA1 activity? Use exactly one **first eligible standard Matemáticas Universitarias attempt** per student, preserving the canonical N=6,627, 190 professor-period contexts and 1,234 CMAT users. Exclude nonstandard equivalencies/revalidations under the validated shared cohort pipeline, retain adverse BA/BV/RT results, and count **all** CMAT visits in the same academic term as the MU attempt.

PPA1 is a first-semester integration programme with an optional qualifying activity consisting of three CMAT visits; qualification for that activity occurs on visit 3, so continued recorded attendance starts on visit 4. **Individual motive, eligibility, participation, and actual PPA credit receipt are unobserved.** The categories are descriptive, not latent student types: 0 = no recorded CMAT attendance; 1–3 = visits within the potential activity threshold; 4+ = visits beyond that threshold, **not necessarily academic or intrinsically motivated**.

## Mutually exclusive specifications
| Model | Ordered groups | Pairs/outcome |
|---|---|---:|
| Primary exploratory PPA | `0 | 1–3 | 4+` | 3 |
| Secondary exploratory PPA | `0 | 1–3 | 4 | 5+` | 6 |
| Historical exact-count comparator | `0 | 1 | 2 | 3 | 4 | 5 | 6 | 7+` | 28 |

Each is an **independent categorical regression** with a separately estimated reference and covariance matrix. Neither the 1–3 versus 4+ primary coefficient nor its SE can be substituted with a contrast from the secondary regression or aggregated from exact-frequency coefficients. A 7+ bin means seven **or more** visits.

Historical counts, from `paper/paper2.1-visit-frequency:results/paper21/tables/10n_zero_inclusive_7plus_descriptives.csv`, were 0=5,393, 1=517, 2=245, 3=170, 4=96, 5=55, 6=50, 7+=101. Summing counts (not outcome means) gives **primary 0=5,393, 1–3=932, 4+=302**, and **secondary 0=5,393, 1–3=932, 4=96, 5+=206**. These are historical arithmetic reference counts, **not outputs from a new fit**.

## Outcomes, regression, confidence intervals
Primary `Z_GRADE_PRIMARY`: original numeric final grades plus the canonical within-professor-period below-7.5 imputation for adverse BV/RT/BA, subsequently standardized in professor-period contexts. Primary `PASS`: 1 if numeric grade >=7.5, else 0 for lower numeric grades and BV/RT/BA. No artificial PASS grades. Follow `main:cmat_analysis/src/cmat_analysis/measures/_grades.py` without changing the random seed or outcome rule.

For group specification `s`, independently fit for each outcome `q`:

```
Y_iq = alpha_professor_period(i) + gamma_degree(i)
       + sum_{g != 0} beta_{s,q,g} * 1{G_s(visits_i)=g} + epsilon_i
```

Delegate pairwise/Wald omnibus inference to `cmat_analysis.statistics.fixed_effect_group_comparisons`, with `CLASSROOM_ID` as both professor-period fixed effect and variance cluster, and `CLAVECARRERA` as a categorical degree control. For PASS the model is a **linear probability model**; multiply differences and nominal 95% CIs by 100 for **percentage points**, not odds ratios. Focal table reports **target minus baseline** (e.g. 4+ minus 1–3, 5+ minus 4, each positive group minus 0); shared estimator's original group1-minus-group2 sign is explicitly reversed. The overall F test evaluates equality of the adjusted group contrasts for that model; it does not establish a policy cutoff.

A model-standardization companion fits the identical FE formula and averages its group-specific fitted prediction over the empirical model sample's contexts/degree programmes, using delta-method cluster-robust covariance for each standardized mean. Its group differences are asserted to reproduce the shared estimator. Standardization can extrapolate into sparse/unobserved group-by-context combinations under the additive model; check and report pairwise context overlap. Observed group means/intervals from the existing `group_outcome_summary` helper are **conventional unclustered descriptives** and must not be mistaken for the cluster-robust adjusted intervals.

Numeric-result sensitivities fit `GRADE_NUMERIC` (original 0–10 grades) and `Z_GRADE_COMPLETE_CASE` separately, explicitly conditioning on having numeric final outcomes and hence changing the population. They cannot validate the full-cohort causal interpretation.

## Multiplicity, transparently fixed here
The **new exploratory PPA family contains 18 tests**: 3 primary plus 6 secondary pairwise comparisons, for **each** of Z and PASS. Apply Holm once to **all 18 original two-sided Wald p-values** at FWER alpha=0.05, regardless of overlap/dependence. This limits cherry-picking group definitions or the better outcome, but does not correct the broader researcher decision path, misspecification, endogenous attendance, or omitted student covariates. Nominal CIs are not simultaneous Holm intervals. Preserve the helper's within-model Holm as explicitly *auxiliary*, never as the primary 18-test PPA adjustment.

The 28-pair exact-frequency comparator retains its own existing correction and model meaning. Original Paper 2.1 users-only **15- and 21-pair** families are likewise distinct. No pooling or retroactive re-labeling is allowed. Numeric-only sensitivities are another selected-population analysis, not part of PPA-18; results need an explicit exploratory caveat.

## Comparison with previously completed models — not new PPA evidence
- **Piecewise:** `research/paper21-shapley-predictive-importance:notes/22_FOLLOWUP_QUESTIONS_RESULTS.md` gives first-use coefficient 0.3066 SD for Z and 0.1192 probability for PASS, with 0.0361 SD/extra visit and 0.0223 probability/extra visit under an **assumed** common capped additional-visit slope. This linear slope is not a PPA4 discontinuity test.
- **Nonlinear curves:** `research/paper21-shapley-predictive-importance:notes/24_ATTENDANCE_CURVE_RESULTS.md` compares linear/log/sqrt/saturating/unrestricted-category shapes. In the eight-category model, the adjusted Z 3→4 difference is -0.017 SD (nominal 95% CI [-0.191, 0.157]); PASS 3→4 is +0.052 probability units ([-0.045, 0.148]). Those adjacent contrasts do not resolve a boundary; topcoding, same-period timing and model-form selection matter.
- **Fused:** `paper/paper2.2.1-fused-frequency:notes/2026-10-07_fused_lasso_100_bootstrap_results.md` selects a stable Z `[0]|[1+]` split in 100/100 bootstrap refits but an all-fused PASS representation under its conservative one-SE heuristic. Discovery BIC ranks the all-fused PASS partition **128th of 128**, with `[0]|[1–3]|[4–7+]` preferred by BIC. This is a selection-method discrepancy, not an independently confirmed incentive mechanism or a significance test of the PPA group coefficients.

**Thesis:** the third visit supplies an institutionally meaningful descriptive boundary. **Antithesis:** self-selection, prior achievement, perceived difficulty, access and attendance accumulation can produce these group patterns without a causal PPA pathway. **Synthesis:** report each adjusted model and sample honestly, then compare their observational patterns with the historical methods without claiming equivalence, causal effects or independent replication.

## Reproduce
```bash
python -m pip install -e './cmat_analysis[dev]'
python -m pytest -q papers/paper2-beyond-first-attendance/analysis/ppa-groups/test_ppa_groups.py
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --check
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --materias /authorized/Materias.xlsx --asesorias /authorized/Asesorias.xlsx
```
The full runner **refuses** missing source files and invalid cohort N/contexts; it does not derive a regression from historical aggregates. Expected outputs, *only after full execution*: `results/tables/ppa-groups/{observed_groups,adjusted_means,pairwise_all_models,focus_target_minus_baseline,omnibus,model_info,pair_context_overlap,numeric_selected_sensitivity}.csv`, `results/figures/ppa-groups/ppa_{z_grade_primary,pass}.{pdf,png}`, and a source-hashed `results/provenance/ppa-groups/run_manifest.json`. No microdata are exported; review small-cell overlap tables for disclosure risk before public release.

## Provenance and limits
Sources: `main:docs/PAPER2_CONSOLIDATION_PLAN.md`; `paper/paper2.1-visit-frequency:paper/docs/analysis/{ANALYSIS_PLAN.md,VISIT_GROUPING_DECISION.md,OUTCOME_FRAMEWORK.md}`, `notes/04_METODOLOGIA_HOLM.md`, `code/run_paper21_outcomes.py`; `main:cmat_analysis/src/cmat_analysis/cohorts/attempts.py`, `main:cmat_analysis/src/cmat_analysis/measures/_grades.py`, and `main:cmat_analysis/src/cmat_analysis/statistics/attendance_frequency.py`.

Limitations: PPA credit/motive/eligibility unavailable; no individual prior math preparation; correlated same-term outcome and exposure; endogenous time at risk if students withdraw; sensitivity to administrative-grade imputation; numeric-only selection; sparse high-frequency categories; weak pairwise within-context overlap; possible modelling extrapolation; multiple exploratory researcher degrees of freedom. No causal dose-response is identified and a non-significant test never proves group equivalence.


## Integration-branch scope discrepancy (2026-10-26; requires administrator decision)

The originating PPA-agent task in this conversation explicitly requests both `0 | 1–3 | 4+` and the optional `0 | 1–3 | 4 | 5+` sensitivity. However, the updated `paper/paper2-beyond-first-attendance:docs/PAPER2_CONSOLIDATION_PLAN.md` and architecture handoff now state **only the three-group analysis is in the integrated-paper scope**. The agent preserves both models here for reproducibility of the original task, but the **four-group outputs are optional and should not be treated as agreed main-manuscript requirements** until the administrator resolves the conflicting contracts. The exploratory joint 18-test Holm adjustment applies **only if both groupings are formally retained as the evaluated family**; if only the three-group model is evaluated, Holm must be recomputed for the six Z/PASS pairwise tests rather than extracting adjusted p-values from the 18-test family. No empirical values have yet been obtained for either family.
