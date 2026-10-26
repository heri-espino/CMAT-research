# Paper 2 consolidation — administrator coordination contract

**Established:** 2026-10-26. **Coordinator:** repository integrator/admin.
**Status:** migration and integrated-manuscript proposal; not a claim that analyses form a completed validated single paper.

## Mission

Consolidate the related mathematics-support attendance analyses into one coherent,
auditable and professor-facing article, with a Marp presentation for faculty and
CMAT administration. Preserve earlier evidence and branches. Keep substantive
scientific disagreements visible. No agent may invent estimates or treat a
retrospective association as an intervention effect.

## Branch/source register (verified on GitHub)

| Branch | Legitimate contribution | Restrictions |
|---|---|---|
| `paper/paper2-mu-performance` | Original MU attendance/performance paper; its own PDF and 0/1/2/3/4+ framing | Distinct historical article; inspect scope before importing claims |
| `paper/paper2.1-visit-frequency` | Holm/Wald primary inference, 1/2/3/4/5/6+ and 0/1/2/3/4/5/6/7+ sensitivity; directly viewable `paper/paper.pdf` | Preserve original p-value families and published working draft |
| `paper/paper2.2.1-fused-frequency` | Exploratory ordered fused-lasso selection; October 7/8 results with 100 bootstrap refits | Its older `PAPER_BRANCH.md` says results pending, but `notes/2026-10-07_fused_lasso_100_bootstrap_results.md` documents completed experiment. Update status, do not presume equivalence |
| `paper/paper2.2.2-distributional-heterogeneity` | **Inherited historical** EM/GMM & skew-normal diagnostics; prospective new 2.2.2 modality tests **not completed** | K=2 GMM is neither proof of bimodality nor identification of student populations |
| `research/paper21-shapley-predictive-importance` | Grouped Shapley/predictive skill, first-vs-additional-visit model, numeric-grade outcomes, five curve families, four plot PNGs; currently committed full-precision CSVs | Existing `notes/25_PUBLICATION_LEDGER.md` was written before data publication and may be stale |

**Baseline analytical cohort:** 6,627 first eligible MU attempts in 190
professor-period contexts, 1,234 CMAT users. Original results must be
recomputed/reconciled on compatible source definitions before any pooled
comparison across papers. Keep admin outcomes BV/RT/BA distinct from
numeric-only grades.

## Scientific organizing question

How should same-term mathematics-centre attendance counts be interpreted in
relation to final mathematics outcomes, when the first visit, repeated visits,
institutional PPA1 incentive and distributional heterogeneity may contribute
different observational patterns?

Proposed evidence hierarchy for the **integrated** paper:
1. **Main inferential anchor:** Paper 2.1 fixed-effect-adjusted Z/PASS group
   contrasts and specified Wald/Holm multiplicity families.
2. **Substantive new test:** PPA-threshold-based three-group contrasts,
   explicitly **exploratory/post hoc** unless separately justified in a dated
   protocol; student motivation and PPA1 credit are **not observed**.
3. **Within-paper observational sensitivity:** piecewise first-vs-extra visit
   regression, log/sqrt/saturating vs free categorical curve fits (fit rather
   than causal effect), model-checking and sparse-tail uncertainty.
4. **Model-dependent exploratory corroboration:** ordered fused lasso, Shapley
   fit attribution and held-out retrospective performance, mixture model
   adequacy and administrative outcome composition. These answer DIFFERENT
   questions; they do not replicate the Holm hypothesis test.
5. Move extensive tables, model searches, code and technical diagnostics to
   online supplements/reproducibility records. The main text should make a
   focused scientific argument rather than present every number uncritically.

## PPA-threshold grouping: **three mutually exclusive groups**

**User clarification, 2026-10-26:** The only requested grouped specification
is **`0 | 1–3 | 4+`**. The prior four-group `0 | 1–3 | 4 | 5+`
sensitivity was an assistant suggestion, **not a user requirement** and must
not be included as a required analytical or presentation result.

- `0`: **5,393** students, 81.4% of cohort — no recorded CMAT attendance.
- `1–3`: **932** students, 14.1% — recorded attendance up to the optional
  three-visit PPA1 activity threshold.
- `4+`: **302** students, 4.6% — recorded attendance exceeds three visits.

These counts are sums of published exact-frequency group counts for the
6,627-student eligible MU cohort, **not** freshly adjusted model results.
The three groups are exhaustive and disjoint; no category distinguishes
exactly four visits in the requested PPA analysis.

- Preserve the original exact-visit `0/1/2/3/4/5/6/7+` comparisons and
  historical `1/2/3/4/5/6+` analyses as **separate existing evidence**,
  without treating them as an additional PPA grouping.
- Three CMAT visits are **one optional** qualifying PPA1 activity for some
  eligible first-semester students. Individual eligibility, intent and credit
  receipt are unobserved. Label `1–3` as `within the three-visit threshold`,
  **not** confirmed PPA users; label `4+` as `beyond the threshold`,
  **not** definitely academically motivated. Likewise, `0` means no
  **recorded** visits, not student disinterest.
- Apply explicitly defined Holm families to the new three-group contrasts,
  preserving distinctions from the historical 15-, 21- and 28-pair families.
- Prefer full-cohort PASS and imputed Z plus numeric-only sensitivities,
  clustered professor-period uncertainty, group N/overlap checks and
  programme heterogeneity. Recorded visits are contemporaneous with final
  outcomes, not a randomized instructional dose.

## Canonical destination: namespaced and mergeable

- **Integration branch:** `paper/paper2-beyond-first-attendance`, created from
  current `main` (not wholesale merging 600+ divergent commits from older
  publication branches).
- **Publication home:** `papers/paper2-beyond-first-attendance/`.
- Suggested subdirectories:
  - `manuscript/` (English LaTeX, bib, sections, compiled `paper.pdf`)
  - `analysis/holm/`, `analysis/ppa-groups/`,
    `analysis/first-visit-curves/`, `analysis/fused/`,
    `analysis/mixture/`, `analysis/shapley/`
  - `results/tables/`, `results/figures/`, `results/provenance/`
  - `presentation/marp/` (English main deck, figures, generated PDF)
  - `supplement/` and `docs/` (claims-to-evidence audit, choices, status)
- A small top-level `README.md` in this new folder must point to the latest
  actual PDF, editable manuscript, Marp deck, and transparent current status.
- **Retain all historical branches and PDFs.** Never delete/rebase/force-push
  the original paper, research, mixture or fused branches.
- Keep reusable estimators, model validation and fixtures in
  `cmat_analysis/`; promote upstream in separate, minimal `main` PRs
  with synthetic tests. Avoid forked duplicate scientific libraries.
- The old historical `paper/paper2.1-visit-frequency/paper/paper.pdf` and
  `main` README link remain active until the new canonical PDF has been built,
  published, and link-verified on GitHub.

## Multi-agent branch and merge protocol

Agent 1 (architecture) first creates the canonical integration branch/folder
from current main and a line-by-line historical inventory. Do not copy all
branch root trees. Each subsequent agent branches **from this integration
branch** using an allowed `paper/*` name and opens a PR *back to the
integration branch*, never to `main` directly.

Proposed agent work branches: `paper/paper2-ppa-groups-agent`,
`paper/paper2-methods-audit-agent`, `paper/paper2-manuscript-agent`,
`paper/paper2-marp-agent`. Administrator alone merges, updates
cross-cutting README/workflows, resolves conflicts, and later submits
small, targeted upstream promotions to `main`.

**Ownership boundaries:**
- Architecture: destination skeleton, mapping and provenance index.
- PPA groups: `analysis/ppa-groups/`, group tables/plots; synthetic tests.
- Methods audit: `docs/claims-evidence-matrix.md`, scientific synthesis,
  run manifests/status and provenance.
- Manuscript: `manuscript/`, `supplement/` only after approved evidence.
- Marp: `presentation/marp/` only after validated model tables/figures.
- Shared root `README.md`, `.github/workflows/`, `.gitignore`,
  `.gitattributes`, `cmat_analysis/` and official branch retirement
  decisions belong to admin/upstream integrator.

**Each agent must report**: source branches+commits, files changed, tests/build
logs with exact status, disclosure checks, formulas and comparison families,
missing dependencies, PR URL and scope. No silent success claims; no invisible
background work. A prompt in one separate chat does not communicate to other
agents: rely on committed docs and PRs.

## Acceptance gates

- Identical cohort/outcome definitions or explicit stratified exceptions;
  coherent adjusted/observed/complete-case labels and confidence intervals.
- Every reported number maps to an actual committed aggregate CSV/manifest.
- Any unexecuted study is labeled as pending; old progress notes reconciled.
- Markdown/LaTeX render, all references/figures resolve, CI synthetic tests
  pass, Marp deck exports cleanly, actual PDF bytes (not Git LFS pointer) are
  viewable on GitHub. Exclude personal, proprietary or row-level source data.
- Professor-facing main README links to the integrated paper **only after**
  the new PDF exists and passes a human scientific review. Otherwise preserve
  the current Paper 2.1 link.
- Administrator reviews PRs and records final scientific decisions; agents
  may propose, not unilaterally certify that exploratory analyses constitute
  confirmatory evidence or a ready-to-submit single paper.
