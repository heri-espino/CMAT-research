# Paper 2 administrator integration status — 2026-10-26 (updated)

**Canonical branch:** `paper/paper2-beyond-first-attendance`.
**Development integration: COMPLETE. Empirical new-cohort execution: NOT YET RUN. Final publication: NOT YET APPROVED.**

## Pull requests integrated into the same research branch

| PR | Evidence | Integration SHA | Release qualifications |
|---|---|---|---|
| [#97](https://github.com/heri-espino/CMAT-research/pull/97) | Methods, claims/evidence, discrepancies | `191d0b53594683a1eb17eee20188867bd8dc40a1` | Documentation audit, not validated cohort rerun |
| [#98](https://github.com/heri-espino/CMAT-research/pull/98) | PPA code and tests | `2072c5d67de2ea22d8772df9ebf826c09710bb89` | Corrected to **only** `0|1–3|4+`, Holm 3 pairs **per outcome**, updated cohort mode; no institutional fitted PPA estimates yet |
| [#99](https://github.com/heri-espino/CMAT-research/pull/99) | Integrated LaTeX draft and supplement | `7631ae2341159d56b9f55a247790d0984dd721ba` | Consolidated actual `manuscript/paper.pdf` not yet verified |
| [#100](https://github.com/heri-espino/CMAT-research/pull/100) | 22-slide Marp main deck + 8 appendix, SVG assets | `ffb6f213b3a274b62a9734cea2a569607fd595ae` | `deck.pdf` currently *offline fallback review preview*, not checked Marp CLI output |
| [#96](https://github.com/heri-espino/CMAT-research/pull/96) | Interim independent QA evidence | `4473d906087c00647de7eed1a631d1be8e9a2a8e` | Preintegration dated snapshot; final end-to-end QA remains pending |

The original source branches and historical paper PDF are **preserved**. No whole historical branch was blanket-merged into `main`, and the historical Holm result tables remain accessible by immutable source SHA.

## Unified reproduction infrastructure

Source-controlled runners from all original Paper 2 strands are now
under `analysis/runners/`, covering grouped support, original Wald/Holm,
numeric failure, EM/GMM/skew normal shape, controls, grouped Shapley,
piecewise regression, smooth/nonparametric attendance curves, and
fused-lasso 100-bootstrap regime stability. User-approved PPA grouping is
under `analysis/ppa-groups/`.

**One-command orchestration:**
`python papers/paper2-beyond-first-attendance/run_all.py --publish`.

The script tests, executes every stage, generates Holm aggregate figures,
validates key outputs, creates a source/output fingerprint manifest, copies
current aggregate tables/figures under this publication folder, and pushes
the audited aggregates only after an explicit user confirmation. It
**stops on failures instead of silently publishing incomplete results**.

[GitHub Actions smoke test](https://github.com/heri-espino/CMAT-research/actions/workflows/paper2-reproduction-smoke.yml)
performed successful Python 3.14 compilation, all supported no-private-data
runner checks, and 13/13 PPA synthetic tests after two initial defects were
identified and fixed. This does **not** certify the authorized institutional
experiment suite.

Updated input files can change student/cluster counts. The PPA runner supports
this explicitly and records the actual counts rather than forcing N=6,627;
the frozen-cohort lock is optional. Historical other scripts have intentionally
preserved their binning models; model adequacy must be reviewed when sparse
or novel attendance frequencies change.

## Public pseudonymized records — user position and unresolved governance

The user explicitly stated they are comfortable keeping pseudonymized data
public. We have respected that direction by **not changing repository visibility**
and by not deleting the earlier research histories. Nevertheless,
`docs/DATA_PRIVACY.md` describes those linked records as not anonymous
and requires restricted authorized access. The user's preference is not
evidence of institutional custodian authorization, nor does pseudonymization
remove quasi-identifier risk. Formal public release clearance and risk review
remain separate from the technical ability to run/publish the research.

This pipeline copies neither raw Excel files nor pseudonymized student-level
records into generated results or new commits. It includes direct-ID and
pseudonym-pattern checks but no automated filter can guarantee a public
aggregate meets all institutional disclosure rules. A custodian review is
required before describing the source-data release as approved.

## Remaining scientific/editorial gates

1. Execute the full institutional suite on the intended input version;
   reconcile all outcomes, current N/contexts, model convergence and
   distributional support. New PPA outcomes remain **pending**.
2. Review every updated numerical manuscript claim and every slide/chart
   against the newly generated committed CSVs. **Paper prose/Marp SVGs do
   not update automatically simply by rerunning regressions.**
3. Compile the integrated `manuscript/paper.pdf` from checked LaTeX sources,
   render `presentation/marp/deck.pdf` with official Marp CLI and inspect
   actual PDF pages, figures and links.
4. Re-audit invalid historical 26c PASS-logit Boolean inference flags; the
   newly ported runner now sets unestimable rejections to missing instead of
   `True`, without rewriting historical source exports.
5. Independent final QA after all empirical outputs and updated publications
   have been committed. No current university/custodian clearance, external
   causal identification or independent validation is implied.

**Current professor-facing link:** retain the prior historical Paper 2.1 PDF
until a newly integrated PDF is generated and signed off. The working Paper 2
integration is accessible via the namespaced README.
