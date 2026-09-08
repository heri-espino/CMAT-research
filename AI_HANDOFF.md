# AI handoff — CMAT research repository

This is the global starting point for future AI sessions working in `heri-espino/CMAT-research`.

## 1. Repository model

- `main` is the canonical source of truth.
- Use short-lived branches for concrete changes, then merge back to `main`.
- The project is a monorepo: code, analysis, reports, papers, literature and documentation are complementary folders, not long-lived branch-specific realities.
- Read `AGENTS.md` and `docs/BRANCH_STRATEGY.md` before changing repository architecture.

## 2. Scientific dependency chain

Maintain one chain:

`controlled institutional data -> code/ -> canonical aggregate outputs -> reports/ and papers/`

Manuscripts do not maintain independent scientific pipelines. If a paper needs a methodological change, change and validate canonical code first.

## 3. Publication portfolio

Canonical source: `docs/PUBLICATION_PORTFOLIO.md`.

Stable paper IDs:

1. `paper1_ppa_persistence` — *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*.
2. `paper2_mu_performance` — *Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics*.
3. `paper3_grading_heterogeneity` — *When the Same Grade Does Not Mean the Same Performance: Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment*.
4. `paper4_degree_help_seeking` — *Who Keeps Seeking Mathematics Help? Disciplinary Heterogeneity in University Mathematics Support Use*.
5. `paper5_longitudinal_trajectories` — *Longitudinal Trajectories of Mathematics Support Use Across the Undergraduate Degree*.

Do not rename these IDs casually. Titles and journal targets may evolve, but update `docs/PUBLICATION_PORTFOLIO.md` first when they do.

## 4. Current scientific anchors

Important current definitions/interpretation rules:

- CMAT visit records are student-selected support use; do not treat attendance as randomized treatment.
- PPA1 is an institutional first-year participation context. The current data do not provide exogenous PPA treatment variation; do not identify a causal PPA effect.
- Primary first-MU performance cohort in the current methodological snapshot is `N=6,627`.
- Broad linked MU→later Calculus cohort is `N=4,211`.
- A stricter next-regular-term longitudinal/PPA snapshot has `N=3,241`; verify that its logic is fully represented in current canonical executable code before relying on it as reproducible from `main`.
- Classroom is `professor/instructor × subject/course × academic period`.
- Classroom-relative `Z` describes relative position in an observed classroom distribution; it is not absolute mathematical proficiency.
- Official academic degree programme (`CLAVECARRERA`) is the primary programme variable.
- Programme-level summaries are ecological and must not be interpreted as individual mechanisms.

## 5. Methodology/version caution

The repository historically contains a refined longitudinal/PPA line (often called `v8`) and a later methodological correction line (often called `v5_methodology`) with improved KDE imputation, complete visit-group comparisons, periodicity and degree-programme analyses.

Version numbers are historical package labels, not chronological truth. Never assume `v8` is automatically newer/better than every `v5` component.

Before changing scientific code:

1. read `docs/MIGRATION_STATUS.md`;
2. inspect the current `code/` implementation and tests;
3. inspect the study protocol/changelog available in `code/`/docs;
4. verify whether the intended methodological correction is already in canonical code;
5. update tests, documentation and the scientific-source fingerprint when code changes.

A merged branch/PR name alone is not evidence that scientific reconciliation is complete; inspect the actual code and outputs.

## 6. Literature subsystem

Read `literature/AI_HANDOFF.md` and `literature/AGENTS.md` for literature work.

The physical corpus is shared under `literature/library/`. Scientific views exist for general literature and each of the five papers. Do not duplicate PDFs solely because a source supports multiple manuscripts. Do not recreate upload-batch folders such as `Bib3`/`Bib4`.

## 7. Privacy / release boundary

Never commit:

- administrative Excel workbooks;
- row-level student/advising microdata;
- direct identifiers;
- HMAC keys or other secrets;
- credentials/tokens;
- unreviewed identifying free text.

Aggregated outputs can be committed after disclosure/privacy review. Literature PDFs/assets are retained only for internal research continuity in this private repository and are not automatically redistributable.

SHA-256 hashes establish integrity/provenance; they do not anonymize data.

## 8. Reporting rules

- Preserve validated null results and sensitivities in the master analysis/technical report.
- Do not let a target journal determine which empirical findings are kept in the canonical record.
- Papers select defensible subsets only after the empirical record is stable.
- If a number changes after a methodological correction, trace the change to canonical outputs and document it rather than manually editing manuscript numbers.

## 9. Recommended session startup

For a new AI session:

1. read this file;
2. read `AGENTS.md`;
3. read `docs/PUBLICATION_PORTFOLIO.md` if manuscript strategy is relevant;
4. read `docs/MIGRATION_STATUS.md` and current methodology docs if code/results are relevant;
5. read `literature/AI_HANDOFF.md` if literature is relevant;
6. inspect the current branch/PR before writing;
7. work through a short-lived branch for substantial changes.

## 10. User preferences relevant to repository work

- rigorous statistical reasoning and explicit assumptions;
- clean, conventional LaTeX without decorative colored boxes;
- preserve historical work unless a replacement is intentional and documented;
- prefer GitHub commits/PRs over repeated ZIP handoffs;
- keep raw/private institutional data outside GitHub;
- report methodological discoveries and limitations rather than hiding inconvenient results.