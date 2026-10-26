# Architecture-stage migration decision log

| ID | Decision | Rationale / unresolved requirement |
|---|---|---|
| A-001 | Freeze five source heads and `main` SHA in the register; create integration branch only from `main` | Avoid wholesale 600+ divergent publication commits; immutable evidence traceability |
| A-002 | Inventory file-level differences against `main`, including transient QA and upstream changes | Record full scope without inflating the canonical manuscript tree; common identical upstream assets stay in `main` |
| A-003 | Reference most historical code/results/manuscripts; do not copy whole source trees | Prevent duplicated/stale outputs and conflicting scientific claims |
| A-004 | Copy the 441-byte Paper 2.1 attendance-group JSON as a frozen historical artifact with the **same Git blob SHA** | Gives analysis agents a concrete, lightweight grouping artifact without treating it as the new protocol |
| A-005 | Establish all six requested namespaces and six scientific analysis subareas with README marker files | Git does not track empty directories; no results implied |
| A-006 | Do not move source `cmat_analysis/`, tests or CI config; enumerate upstream-review candidates in source register | Shared API requires a separate minimal, reviewed and tested upstream change |
| A-007 | Keep old Paper 2.1 PDF at its original branch and refuse a premature new PDF link | Preserve functioning publication-facing entry point; destination has no approved PDF |
| A-008 | Record contradictory dated status notes rather than choose one silently | Fused initial status is outdated for 100-bootstrap execution; Paper 2.2.2 novel modality work is still unexecuted; Shapley ledger has dated supersession |
| A-009 | Prohibit inferred equivalence, multimodality, experimental effects, and post hoc PPA claims | Historical evidence is observational and method-specific |
| A-010 | No PR to `main`, no branch deletion, history rewrite, force push or historical result replacement in architecture phase | Repo governance and user constraint |
| A-011 | Integrate the subsequent one-commit `main` charter update (`d6b1670553e9a838339c4c0bebb397667ba3a392`) into this branch through a non-destructive merge, preserving the original creation-time baseline and SHA-pinned source inventory | User clarified that only `0 | 1–3 | 4+` is requested; old four-group suggestion is explicitly **not** a requirement. No scientific output changed. |

## Open decisions requiring scientific or administrator authority

- Whether Paper 2.1's full cohort, PASS and imputed Z are confirmed on compatible source hashes across all historical runs; exact input hashes and reference grades must be reconciled.
- Whether the new PPA coarse grouping is a central exploratory result or a supplement. Individual students' PPA1 eligibility, incentive credit, and motivation are **not** observed.
- How to reconcile the fused PASS one-SE-selected all-fused partition versus the exhaustive BIC-preferred multi-block partition; further synthetic calibration/repeated-CV is not yet complete.
- Whether the GMM/skew-normal evidence warrants new calibrated unimodality/heaping tests or should remain supplementary; no latent student subgroup claims.
- Whether to interpret first-visit curves, Shapley fit allocation and held-out predictive skill in the central argument without overpromoting their retrospective associations.
- Data-use/ethics wording, requested entrance-exam baseline, figure disclosure audits, integrated TeX build and original old-PDF human review remain outside architecture ownership.

**Status:** register complete relative to frozen heads; **scientific publication integration not yet performed**.
