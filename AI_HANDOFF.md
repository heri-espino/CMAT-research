# AI handoff — CMAT research repository

This is the single canonical starting point for future AI sessions working in `heri-espino/CMAT-research`.

## 1. Repository model

- `main` is the canonical source of truth.
- Branches are short-lived task workspaces, not permanent scientific realities; delete them after merge.
- Scientific chain: `controlled institutional data -> code/ -> canonical aggregate outputs -> reports/ and papers/`.
- Literature chain: `literature/library/ -> general/paper-specific views -> manuscript bibliography`.
- ZIPs are backups/provenance packages, not version history.

Read `AGENTS.md` before repository changes and the subsystem README/AGENTS before editing that subsystem.

## 2. Publication portfolio

Canonical source: `docs/PUBLICATION_PORTFOLIO.md`.

Stable paper IDs:

1. `paper1_ppa_persistence` — *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*.
2. `paper2_mu_performance` — *Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics*.
3. `paper3_grading_heterogeneity` — *When the Same Grade Does Not Mean the Same Performance: Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment*.
4. `paper4_degree_help_seeking` — *Who Keeps Seeking Mathematics Help? Disciplinary Heterogeneity in University Mathematics Support Use*.
5. `paper5_longitudinal_trajectories` — *Longitudinal Trajectories of Mathematics Support Use Across the Undergraduate Degree*.

Do not rename these IDs casually. Change working titles/journal strategy in `docs/PUBLICATION_PORTFOLIO.md` first.

## 3. Administrative data interpretation

### Academic records

The academic table provides official degree programme and final course outcomes. CMAT visit records link to academic records through institutional student ID in the controlled data environment.

Official academic degree associated with the real academic attempt is the primary programme field. Forms-declared degree is not the main adjustment variable.

Academic rows are not automatically real attempts: degree changes/revalidations can replicate already-passed courses under another programme. Preserve real-attempt/revalidation logic.

### CMAT visits

Each Google Forms record is one recorded advisory visit; there is no duration measure. Multiple same-day records can be legitimate because professor/shift changes can produce separate visits. Do not label repeated same-day attendance as manipulation without evidence.

For the PPA analysis, the primary count is any CMAT registration during the MU period regardless of declared topic; course-tagged visits are a sensitivity.

## 4. PPA interpretation

PPA1 is a first-year institutional participation/incentive context. CMAT activities can contribute toward PPA1 credit/points, but **do not equate three CMAT records with three PPA points**.

Operational study threshold: **3 CMAT visit records during the MU term**.

Working assumption: students usually complete PPA1 in the first semester, so MU is treated as the incentive-linked context and later Calculus as a context where that same PPA1-linked CMAT incentive generally no longer applies. This is an assumption, not an observed individual completion date.

There is no exogenous PPA treatment variation. The research does **not** identify a causal effect of PPA.

## 5. Outcomes and classroom standardisation

Pass threshold: `7.5`.

- BV / RT / BA: adverse/non-passing states.
- EQV / REV / AC: administrative/non-comparable states.

Classroom is `professor × same course × same academic period`.

For numeric classroom-relative performance:

`Z_ic = (Y_ic - mean_classroom_c) / sd_classroom_c`.

A longitudinal `DELTA_Z = Z_CALC - Z_MU` is change in relative classroom position, not raw-grade change and not a causal treatment effect.

## 6. Cohorts that must not be conflated

### First-MU cohort

Current documented methodology snapshot: **N=6,627**.

This population answers contemporaneous questions such as `E[Z_MU | CMAT visit group]`.

### Later-Calculus progressor subset

Current documented snapshot: **N=4,211** students subsequently observed in Calculus with relevant coverage.

This is a future-conditioned selected population. It is useful for longitudinal/sensitivity questions but must not silently replace the full MU cohort.

### Refined strict longitudinal/PPA cohort

Historical refined snapshot: **N=3,241** primary next-regular-term paired cohort; **N=3,389** broader paired coverage/valid-Z cohort before the next-regular-term restriction.

This refined stage is later work and is not claimed to be covered by the methodology-v5 scientific-source fingerprint.

## 7. Historical methodology snapshot and restoration

An exact later-methodology historical snapshot is preserved at:

`code/snapshots/methodology_v5_2026-09-07/`

and its technical report v2 at:

`reports/technical_report_methodology_v2/`.

Restoration verification is documented at `docs/snapshots/methodology_v5_2026-09-07/README.md`.

Key verified properties:

- scientific-source fingerprint: `03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`;
- every source-manifest entry passed SHA-256 verification;
- methodology helper suite: **9/9 tests passed**;
- `PYTHON_FUNCTION_INDEX.md`: **320 symbols**;
- `informe_cmat.pdf`: **40 pages**, SHA-256 `1e52d36809924df4bc84db65f6cb6669fe33d1f402076e8930b3a173f550595f`;
- no original Excel/raw administrative microdata were included.

The restored snapshot includes the intended SciPy Gaussian KDE/Scott imputation logic, expanded `0/1/2/3/4+` comparisons, periodicity, degree-programme work and the N=4,211 sensitivity. Historical v8 and later methodology labels are different development lines, not a simple chronological ranking.

Do not assume restoration means the active canonical `code/` pipeline is fully reconciled. Inspect implementation/tests before making that claim.

## 8. Paper 1 longitudinal anchors

For the historical strict primary cohort (`N=3,241`), later Calculus CMAT use by MU visit group was documented as:

- 0 visits: `426/2470 = 17.25%`;
- 1–2 visits: `205/472 = 43.43%`;
- exactly 3: `56/103 = 54.37%`;
- 4+: `131/196 = 66.84%`.

Global 4×2 Pearson: `chi-square(3)=392.47`, `p≈9.47e-85`, Cramér `V=0.348`.

Exactly 3 vs 4+ documented contrast:

- risk difference ≈ `12.47` percentage points;
- Newcombe 95% CI ≈ `[0.92, 23.90]` pp;
- RR ≈ `1.229`;
- OR ≈ `1.691`.

Adjusted historical persistence models showed strong predictive associations relative to 0 MU visits (approximately OR `3.53` for 1–2, `4.84` for exactly 3, `9.82` for 4+), conditional on prior classroom-relative performance, official MU degree and MU period with classroom-clustered SEs.

Interpret as observational persistence patterns. Do not claim the incentive caused habit formation. The piecewise visit-count model is descriptive, **not RDD**.

## 9. Paper 2 empirical interpretation

The later methodology work expanded visit groups to `0 / 1 / 2 / 3 / 4+` and all ten pairwise comparisons using Games–Howell plus adjusted classroom/degree models with clustered SEs and Holm correction.

Interpretation to protect:

**the robust separation is primarily 0 visits versus positive use; differences among 1, 2, 3 and 4+ do not support a clean monotone dose-response.**

Exact-count tail analyses are descriptive. Sparse high-count groups should not drive a strong dose-response claim.

## 10. Temporal and degree-programme extensions

Later methodology work includes periodicity analyses for all CMAT activity and first-MU activity during each student's MU period. Use ACF/periodogram/peak results descriptively; do not call peaks exams without a validated calendar.

Degree-programme analyses use official academic programme. Programme-level correlations are ecological and must not be interpreted as individual mechanisms. Small programme cells may be omitted from specific summaries but are not deleted from the underlying data.

## 11. Literature subsystem

Read `literature/AI_HANDOFF.md` and `literature/AGENTS.md` for literature work.

The physical corpus is shared under `literature/library/` (`articles/`, `pdf/`, and `references/`). Scientific views exist for general literature and each of the five papers. Do not duplicate PDFs solely because a source supports multiple manuscripts and do not recreate upload-batch folders such as `Bib`, `Bib2`, `Bib3`, etc.

Paper 1 has a technical reading layer under `literature/papers/paper1_ppa_persistence/reading_notes/` with source-specific design, sample, methods, statistics, quotations and claim boundaries.

## 12. Privacy / release boundary

Never commit:

- administrative Excel workbooks;
- row-level student/advising microdata;
- direct identifiers;
- HMAC keys, salts or other secrets;
- credentials/tokens;
- unreviewed identifying free text.

Aggregated outputs can be committed after disclosure/privacy review. Literature PDFs/assets are retained only for internal research continuity in this private repository and are not automatically redistributable.

SHA-256 establishes integrity/provenance; it does not anonymise data.

## 13. Future data planned

The project plans to request:

- mathematics admission/diagnostic test results as a genuinely pre-treatment academic-preparation covariate;
- a survey on reasons for CMAT use, including PPA awareness, academic need, recommendation, familiarity and perceived usefulness.

These additions may strengthen adjustment/mechanism description but do not retroactively randomize CMAT use.

## 14. Reporting and language rules

Preserve validated null results and sensitivities in the canonical empirical record. If a number changes after methodological correction, trace it to canonical outputs and document the reason rather than manually editing isolated manuscript values.

Use: `association`, `predictive association`, `behavioural persistence`, `formal academic help-seeking`, `institutional participation incentive`, `pattern consistent with`.

Avoid unsupported claims such as: PPA caused use, CMAT caused grades, incentive created a habit, students were intrinsically motivated, or threshold analysis is an RDD.

## 15. Recommended session startup

1. read this file;
2. read `AGENTS.md`;
3. read `docs/PUBLICATION_PORTFOLIO.md` if manuscript strategy is relevant;
4. read `docs/MIGRATION_STATUS.md` and current methodology docs if code/results are relevant;
5. read `literature/AI_HANDOFF.md` if literature is relevant;
6. inspect `main` and any current PR before writing or modifying artifacts.
