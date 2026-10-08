# 2026-10-07 — Full Paper 2.2.1 run: 100 cluster bootstrap replicates

**Status: completed computationally; substantive interpretation remains observational and conditional on the specified selection heuristic.** This note supersedes the **failure diagnosis** of the initial run; it does not erase that record.

## Provenance and exact protocol

- Commit recorded in the executable run manifest: `c9faa397bd0a6c7c8c67025ab94f8314e0996018`.
- Run UTC: 2026-10-08 02:50:36 (evening of 2026-10-07 at project local UTC-6).
- Data provenance: see two SHA-256 **input hashes** in `results/paper221/run_manifest.json`. Do not reproduce row-level data in this note.
- Cohort: **N=6,627**, **190 instructor-period classroom clusters**; discovery: **4,675**, 133 clusters; reserved validation: **1,952**, 57 clusters.
- Settings: split seed 221; discovery fraction 0.70; 4 grouped CV folds with 1 repeat; 12 lambdas; 1-SE-style parsimony heuristic; **100 classroom-resampled bootstrap fits with full lambda retuning**; 7+ primary grid and pooled 6+ sensitivity; two separately estimated outcomes (`Z_GRADE_PRIMARY`, `PASS`).
- Execution status: `completed_no_causal_claim`; **all four specifications have 100/100 successful bootstrap replications, 0 failures and no manifest warnings**.
- Output locations: `results/paper221/run_manifest.json`, `results/paper221/tables/*_{blocks,cv,boundary_stability,holdout_wald,exhaustive_partitions}.csv`, `results/paper221/figures/*.pdf`.

## Observed selected partitions

| Frequency representation | Z_GRADE_PRIMARY | PASS |
| --- | --- | --- |
| 0, 1, 2, 3, 4, 5, 6, 7+ (primary) | `[0] | [1,2,3,4,5,6,7+]` (2 blocks) | `[0,1,2,3,4,5,6,7+]` (one all-fused block) |
| 0, 1, 2, 3, 4, 5, 6+ (support sensitivity) | `[0] | [1,2,3,4,5,6+]` (2 blocks) | `[0,1,2,3,4,5,6+]` (one all-fused block) |

**Important:** algorithmic fusion is a parsimonious model representation, **not proof of equality within a fused block**. Likewise, the PASS all-fused model is not evidence that every frequency has equal population pass probability. The selected lambda is 0.0280911649 for Z and 0.0240823298 for PASS in the 7+ representation.

## Boundary selection stability (all 100 successful)

| Cut | Z, 7+ | PASS, 7+ | Z, 6+ sensitivity | PASS, 6+ sensitivity |
| --- | ---: | ---: | ---: | ---: |
| 0|1 | **100%** | 37% | **100%** | 37% |
| 1|2 | 10% | 2% | 9% | 2% |
| 2|3 | 0% | 0% | 1% | 0% |
| 3|4 | 1% | 1% | 1% | 1% |
| 4|5 | 0% | 0% | 0% | 0% |
| 5|6 (or 5|6+) | 0% | 0% | 0% | 0% |
| 6|7+ | 0% | 0% | not applicable | not applicable |

These are **selection frequencies**, not significance levels, calibrated confidence statements or probabilities that a population boundary is true. The stable Z 0|1 split holds even when the sparse high-frequency tail is pooled.

## Unpenalised reserved-cluster comparison

With the **two Z blocks selected in discovery**, the validation-only model estimates:

- **1+ minus 0:** +0.2636168771 instructor-period-standardised grade SD.
- Classroom-cluster-robust SE: 0.0579751954.
- Nominal 95% CI: [0.1499854942, 0.3772482600].
- Two-sided Wald/Holm p: 0.00000543997 (only one discovered adjacent contrast in this outcome).
- Validation: N=1,952; B0=1,585; B1=367; 57 clusters overall; 52 classrooms containing both blocks.

For PASS, the selected model has **one block**, so **no selected-boundary Wald comparison is defined or reported**. Never interpret a missing `*_pass_holdout_wald.csv` as a p-value of 1 or as equivalence.

The holdout was kept out of the new **algorithm's** discovery and bootstrap, but the wider Paper 2.1 programme had previously explored this institutional cohort and related outcomes. Therefore, the Wald check is an *internal, algorithmically held-out validation*, **not a prospectively untouched or external replication**; previous research-wide exploration can weaken the interpretation of nominal post-selection significance.

## Divergence in PASS and sensitivity of the one-SE heuristic

The 7+ PASS grid finds minimum within-held-out-classroom CV loss at lambda **0.000360465**, MSE **0.168914521**, whereas the most regularised candidate admitted by the heuristic has lambda **0.024082330**, MSE **0.173192158** and one all-fused block. The minimum-loss fold-score heuristic SE is about **0.00475009**, so the more highly penalised alternative is within that permissive tolerance. Four folds and one repetition do **not** justify treating this as a formal SE or a hypothesis test.

Furthermore, the exhaustive 128-partition **discovery-sample** BIC ranks the all-fused PASS model **128th out of 128**, while its best partition is `[0]|[1-3]|[4-7+]` (cuts 0|1 and 3|4), followed closely by the `[0]|[1+]` model (BIC difference about 1.53). BIC compares in-sample fit under a Gaussian working likelihood for the LPM; it neither validates the extra boundary nor licenses choosing the best partition post hoc for testing on already inspected data.

For Z, the selected `[0]|[1+]` partition is **rank 1 of 128** by the same relative discovery BIC, consistent with its 100% bootstrap selection rate.

**Planned methodological sensitivity:** evaluate selection using minimum CV loss as a *labelled, post hoc sensitivity*, with repeated grouped-fold splits and outcome-specific score diagnostics; avoid silently changing the primary one-SE rule after seeing PASS. Assess predictive improvement and false fusion rates on synthetic binary outcomes. Any new contrasts chosen by this sensitivity require their own inferential qualification.

## Interpretation and publication implications

**Supported under this pipeline:** a parsimonious adjusted **initial-use separation in Z**, stable under 100 cluster resamples and the original tail-pooling sensitivity, with a positive reserved-cluster adjusted difference.

**Not established:** a reliably located additional positive-frequency boundary, equivalence of 1–7+ visits, a PASS null effect, a causal return to visiting CMAT, or a policy changepoint at the three-visit PPA incentive. The PASS outcome suggests that the one-SE-style selection rule may be too conservative for this binary LPM, even though an association with initial use is present in earlier analyses.

**Next:** update the LaTeX manuscript with these numerical findings while retaining all caveats, discuss the one-SE/BIC disagreement, develop a pre-labelled minimum-CV/repeated-fold robustness exercise, and seek an external or future cohort if truly independent confirmatory evidence is needed.
