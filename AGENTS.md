# CMAT repository operating rules

## Start here

Before substantive work:

1. read `AI_HANDOFF.md`;
2. read the README/AGENTS file in the subsystem being changed;
3. **for any Python/code task, read `code/.ai_handoff.md` and search `code/FUNCTION_INDEX.md` before proposing or writing a new function**;
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

## Code reuse / token-efficiency / reproducibility rule

`code/.ai_handoff.md` is the architectural contract for Python work. `code/FUNCTION_INDEX.md` is the canonical searchable inventory of the active Python tree. It is generated from the AST and includes reusable/source symbols plus a separate test-symbol section.

Before implementing functionality:

1. read `code/.ai_handoff.md`;
2. search the index by concept, likely function name, and tags;
3. inspect the referenced implementation;
4. reuse or extend an existing function whenever scientifically equivalent;
5. do not create a parallel estimator, cleaner, cohort builder, plotting helper, or transformation only because its location was not immediately obvious;
6. if a new reusable symbol is truly needed, place it in the appropriate importable module, add a concise docstring/tests, and do **not** hide the scientific logic inside an experiment runner;
7. import the reusable function into the stable runner that reproduces the relevant scientific question;
8. regenerate the index in the same code change (`python code/scripts/generate_function_index.py`).

Paper/question-specific runners belong under `code/experiments/` and must have stable descriptive names rather than `v2`, `final`, `new`, or date suffixes. A new data vintage normally means rerunning the same stable runner, not writing a new script. Git is the provenance/history layer.

GitHub automatically refreshes the index after Python changes under `code/`, but code authors should still verify that the generated description is useful.

## Stable paper IDs and single-home rule

Use these IDs consistently across `papers/`, documentation, runners and issue/PR descriptions:

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Each paper has exactly one canonical home: `papers/<paper_id>/`. Paper-specific literature belongs in `papers/<paper_id>/literature/`; do not recreate a parallel `literature/papers/` hierarchy or alternate folder names for the same manuscript.

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
- Reported results should be reproducible from stable runners; do not make notebooks or hand-edited output files the canonical computational source.

## Literature rules

The physical literature corpus is shared under `literature/library/`. Cross-project literature maps live under `literature/general/`. Paper-specific literature indices, reading notes and gap trackers live with their paper under `papers/<paper_id>/literature/`. Read `literature/AGENTS.md` before reorganizing or adding literature.

Do not recreate upload-batch folders such as `Bib3`, `Bib4`, etc. New sources belong in the shared library and are then indexed into every relevant general or paper-local view.

## Documentation / handoff

Major folders should have a README explaining scope, inputs, outputs, canonical status and dependencies.

Future AI sessions should start with:

1. `AI_HANDOFF.md` — global project state;
2. `code/.ai_handoff.md` — code architecture/reproducibility contract before any code work;
3. `code/FUNCTION_INDEX.md` — locate existing capabilities before writing code;
4. `docs/PUBLICATION_PORTFOLIO.md` — five-paper plan;
5. `literature/AI_HANDOFF.md` — literature-specific state when relevant;
6. the relevant `papers/<paper_id>/README.md` and `papers/<paper_id>/literature/` when working on a manuscript;
7. current methodological protocol/changelog before changing scientific code.

Update the project handoff/changelog whenever code, estimands, portfolio boundaries or major architecture changes.
