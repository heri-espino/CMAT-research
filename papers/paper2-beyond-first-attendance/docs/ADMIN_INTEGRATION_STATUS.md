# Paper 2 administrative integration status — 2026-10-26

**Current canonical branch:** `paper/paper2-beyond-first-attendance`.
**Decision:** development integration permitted; public professor-facing release **BLOCKED**.
**Do not merge whole historical branches to main, delete them, overwrite past PDF releases or promote draft documents to final.**

## Verified current branch/PR disposition

| Item | PR | Head branch | Decision / proof |
|---|---:|---|---|
| Architecture | — | `paper/paper2-beyond-first-attendance` | Namespace, provenance register, links and historical branch mapping present |
| Methods / evidence audit | [#97](https://github.com/heri-espino/CMAT-research/pull/97) | `paper/paper2-methods-audit-agent` | **MERGED** as documentation-only squash `191d0b53594683a1eb17eee20188867bd8dc40a1`; this is not research-release approval |
| Independent QA | [#96](https://github.com/heri-espino/CMAT-research/pull/96) | `paper/paper2-qa-agent` | **OPEN DRAFT**: independent final QA to be updated after manuscript/Marp/PPA changes and data-containment response |
| PPA group analysis | [#98](https://github.com/heri-espino/CMAT-research/pull/98) | `paper/paper2-ppa-groups-agent` | **OPEN DRAFT**: remove unrequested `0|1–3|4|5+`, correct declared family, confirm CI synthetic tests and obtain authorized institutional results |
| Integrated manuscript | [#99](https://github.com/heri-espino/CMAT-research/pull/99) | `paper/paper2-manuscript-agent` | **OPEN DRAFT**: build/validate real GitHub-viewable `manuscript/paper.pdf`, audit citations/numbers/ethical statements |
| Marp slides | [#100](https://github.com/heri-espino/CMAT-research/pull/100) | `paper/paper2-marp-agent` | **OPEN DRAFT**: align to only three PPA groups, render via Marp CLI and validate the actual final PDF |

Administrator review instructions were posted in each outstanding PR conversation on 2026-10-26.

## P0 — Controlled-data disclosure in PUBLIC repository

The public `main` branch currently contains `data/controlled/` pseudonymized, individual-level academic/CMAT/diagnostic source tables and normalized linked records. `docs/DATA_PRIVACY.md` and `data/controlled/PRIVACY_README.md` unequivocally restrict these files to a **private** authorized repository and state that even deterministic pseudonymization plus the retained timestamps/course metadata is **not anonymization**.

**Immediate necessary human action:** owner/admin must make the repository private or otherwise restrict access with the institutional data custodian **before** proceeding with public distribution, then assess historical clones/forks, branches, Git objects, Git LFS, releases, Actions artifacts, and access logs as available; determine approved incident-response, notification and public-history remediation. **Removing files only from the latest tree does not erase accessible historical versions.** This integration audit did not open or copy protected file contents. This issue is not solved by marking a PR private or by changing `.gitignore`.

GitHub connector access here does not expose a repository-visibility mutation. Consequently, do not claim containment, privacy incident closure, or public-release approval. Keep source data out of any new public PR or action artifacts.

## P1 — Scientific/source consistency blockers

1. The historical `results/paper21/tables/26c_zero_inclusive_7plus_pass_logit_pairwise.csv` contains 28 `reject_adjusted=True` flags with absent cluster uncertainty and p-values. These boolean flags are **invalid inference**. Retain historical provenance but exclude their significance claims; LPM/Holm results are a different, estimable model.
2. User-confirmed **only** requested PPA grouping is `0 | 1–3 | 4+` (N=5,393/932/302 from historical exact counts); no requested four-group sensitivity. All newly fitted comparisons are exploratory and **not yet performed** on an authorized institutional source in PR #98.
3. No integrated source-built manuscript PDF exists on the integration branch yet; PR #99 provisional local PDF is not a GitHub-file-backed reproducible output.
4. Marp PR #100 contains a real 30-page **offline fallback** PDF preview but not a verified Marp-CLI build; final visual/overflow QA and consistent figures pending.
5. Historical adjusted pairwise Holm arithmetic was independently checked in 148 linear-model records, but re-estimation from confidential inputs remains a separate pending validation step. Different analytical populations cannot be silently pooled.

## Historical branch retention

Preserve these refs without rebase, force push, deletion or blanket merge:

- `paper/paper2-mu-performance`: original MU performance study.
- `paper/paper2.1-visit-frequency`: historical Wald/Holm working manuscript and GitHub-viewable PDF.
- `paper/paper2.2.1-fused-frequency`: fused-lasso results and 100-bootstrap run.
- `paper/paper2.2.2-distributional-heterogeneity`: inherited EM/GMM, novel modality study unexecuted.
- `research/paper21-shapley-predictive-importance`: Shapley, piecewise visit model and curves.

Source snapshots, paths and frozen blob identities are documented in `docs/source-register.md`, `docs/source-register.tsv` and the merged `docs/claims-evidence-matrix.md`.

## Follow-on release sequence

1. Contain public controlled-data access and obtain institutional custodian directions. Do not imply deleting HEAD resolves the history exposure.
2. Correct #98 to the sole three-band design, use properly declared 3-contrast/outcome Holm scope, execute in an **authorized private** environment, and disclose-check only the aggregates.
3. Refresh #99 and #100 against merged methods evidence; exclude invalid logit inference; build actual repository PDFs with exact output hashes, citations and visual checks.
4. Independently re-audit integrated PDFs, data policy, PPA outputs, confidence intervals and all reference links through #96; resolve critical findings.
5. Only after sign-off should the administrator promote minimal mergeable content to main and update its homepage link. The current Paper 2.1 professor-facing PDF remains the official *working draft* until then.

**This record is a truthful integration status, not a representation that the integrated paper is final.**
