# CMAT repository operating rules

## Start here

Before substantive work:

1. read `AI_HANDOFF.md`;
2. read the README/AGENTS file in the subsystem being changed;
3. **for any Python/code task, search `code/FUNCTION_INDEX.md` before proposing or writing a new function**;
4. inspect current canonical outputs/protocol before quoting numerical results;
5. use a short-lived branch for a concrete change unless the user explicitly requests otherwise.

## Canonical repository model

`main` is the source of truth. Organize the project by subfolder; use branches only as short-lived workspaces for concrete changes and delete them after merge.

Read `docs/BRANCH_STRATEGY.md` and `docs/GIT_WORKFLOW.md` before creating or reusing a branch.

## Scientific dependency rule

Maintain one scientific chain:

`controlled data -> code/ -> analysis/ -> reports/ and papers/`.

Do not create manuscript-specific scientific pipelines. If any of the five planned papers needs a methodological change, implement and validate it in canonical code first, regenerate aggregate outputs, and only then update the manuscript.

The canonical five-paper publication plan is `docs/PUBLICATION_PORTFOLIO.md`.

## Code reuse / token-efficiency rule

`code/FUNCTION_INDEX.md` is the canonical searchable inventory of the active Python tree. It is generated from the AST and includes reusable/source symbols plus a separate test-symbol section.

Before implementing functionality:

1. search the index by concept, likely function name, and tags;
2. inspect the referenced implementation;
3. reuse or extend an existing function whenever scientifically equivalent;
4. do not create a parallel estimator, cleaner, cohort builder, plotting helper, or transformation only because its location was not immediately obvious;
5. if a new reusable symbol is truly needed, add a concise docstring so the generated index explains it;
6. regenerate the index in the same code change (`python code/scripts/generate_function_index.py`).

GitHub automatically refreshes the index after Python changes under `code/`, but code authors should still verify that the generated description is useful.

## Stable paper IDs

Use these IDs consistently across `papers/`, `literature/papers/`, documentation and issue/PR descriptions:

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Do not create alternate folder names for the same manuscript.

## Preservation rule

Historical snapshots may be retained for provenance, but must be clearly labeled historical and must not silently overwrite canonical paths. Historical `Bib/Bib2` names are preserved in Git history only and must not be recreated.

## Data/privacy boundary

Never commit:

- administrative Excel workbooks;
- row-level student/advising microdata;
- direct student or professor identifiers;
- HMAC/secret keys;
- credentials/tokens;
- unreviewed identifying free text.

Aggregated outputs may be committed after privacy review. Heavy literature PDFs/assets are internal research material in this private repository, not automatically redistributable content.

## Analysis/reporting rules

- Preserve all validated discoveries in the master analysis and technical report, including null results and sensitivity analyses.
- Keep causal language conservative for student-selected CMAT use.
- Do not infer motivation, habit formation, or psychological states from administrative visits.
- Classroom is `instructor × course × academic period` unless a later reviewed methodological change explicitly replaces it.
- Scientific-code changes require tests, protocol/changelog/function-index updates, and a new source fingerprint.
- Paper-specific selections happen after canonical outputs are stable.
- Paper folders may select results; they may not redefine them independently.

## Literature rules

The physical literature corpus is shared under `literature/library/`. General and paper-specific folders are scientific views over that library. Read `literature/AGENTS.md` before reorganizing or adding literature.

Do not recreate upload-batch folders such as `Bib3`, `Bib4`, etc. New sources belong in the shared library and are then indexed into every relevant paper view.

## Documentation / handoff

Major folders should have a README explaining scope, inputs, outputs, canonical status and dependencies.

Future AI sessions should start with:

1. `AI_HANDOFF.md` — global project state;
2. `code/FUNCTION_INDEX.md` — before any code work;
3. `docs/PUBLICATION_PORTFOLIO.md` — five-paper plan;
4. `literature/AI_HANDOFF.md` — literature-specific state when relevant;
5. current methodological protocol/changelog before changing scientific code.

Update the project handoff/changelog whenever code, estimands, portfolio boundaries or major architecture changes.
