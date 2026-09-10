# CMAT repository operating rules

## Start here

Before substantive work:

1. read `AI_HANDOFF.md`;
2. read `docs/RESEARCH_WORKFLOW.md` when the task concerns research architecture, report development, or movement of evidence into papers;
3. read the README/AI handoff for the subsystem being changed;
4. **for any Python/scientific-code task, read `code/.ai_handoff.md` and search `code/FUNCTION_INDEX.md` before proposing or writing a reusable function**;
5. inspect the owning report/paper and current canonical outputs/protocol before quoting numerical results;
6. use a short-lived branch for a concrete change when useful unless the user explicitly requests otherwise.

## Canonical repository model

`main` is the source of truth. Git is the history/provenance layer.

The primary production chain is:

```text
controlled data
    ↓
root code
    ↓
atomic reports
    ↓
publication papers
```

More precisely:

`controlled data -> code/src/visitas_analysis/ -> reports/<report_id>/ -> papers/<paper_id>/`.

The working analogy is: **root `code/` is the internal scientific library; reports are reproducible research workspaces that use that library; papers are curated publication products built from validated report evidence.**

`analysis/shared/` is auxiliary storage for cross-report aggregates/provenance, not a required production stage.

## Root-code authority

Reusable scientific/computational logic belongs in `code/src/visitas_analysis/`.

Before implementing functionality:

1. read `code/.ai_handoff.md`;
2. search `code/FUNCTION_INDEX.md`;
3. inspect the referenced implementation;
4. reuse or extend an existing scientifically equivalent function;
5. if a new reusable symbol is truly needed, place it in the appropriate root-code module and add a concise docstring/tests;
6. regenerate the function index in the same scientific change.

Do **not** place reusable cohort logic, estimators, transformations, statistical tests, model definitions, confidence intervals, imputation rules or plotting functions inside a report or paper folder.

## Atomic report rule

`reports/` is the scientific-development/brainstorming layer. Read `reports/AI_HANDOFF.md` before substantive report work.

Each report is an atomic product that may contain:

- `README.md`;
- `code/` with a **thin local entry point**;
- `tables/`;
- `figures/`;
- `notes/`;
- `provenance/`;
- LaTeX source and compiled artifact.

A report-local runner may resolve paths, parse product-specific CLI arguments, select configuration and call root-code functions in a fixed order. It must **not** become an independent scientific codebase.

Canonical example:

```bash
python reports/methodology_report/code/methodology_report.py --check
```

The implementation it calls remains under root `code/`.

There is intentionally no active `code/experiments/` directory; product recipes are co-located with their products.

## New research idea rule

When a new analytical idea appears, do not start by coding it in a paper or report-local helper. Use this sequence:

1. give the question an existing/new report home;
2. record the question, rationale, assumptions and uncertainties in that report;
3. search the root-code function index;
4. implement any missing reusable capability only in root `code/`, with tests/documentation;
5. call it from the report-local runner;
6. preserve diagnostics, nulls, sensitivities and interpretation in the report;
7. after review, select only the necessary validated evidence into a paper.

If manuscript work later exposes a missing analysis, return upstream to root code + the appropriate report before changing paper numbers.

The full version of this workflow is `docs/RESEARCH_WORKFLOW.md` and the report-specific operational checklist is `reports/AI_HANDOFF.md`.

## Reports → papers rule

`reports/` should preserve the broad empirical record, including nulls, sensitivities, alternative specifications, methodological discussion and exploratory results.

`papers/` is the publication-selection layer. Papers select validated evidence from reports and root code; they may not redefine cohorts, estimands or scientific functions independently.

If a manuscript exposes a methodological problem, fix it first in root `code/`, test it, regenerate the affected report outputs, verify changed numbers, and only then update the paper.

## Stable paper IDs and single-home rule

Use these IDs consistently:

- `paper1_ppa_persistence`
- `paper2_mu_performance`
- `paper3_grading_heterogeneity`
- `paper4_degree_help_seeking`
- `paper5_longitudinal_trajectories`

Each paper has exactly one canonical home: `papers/<paper_id>/`. Paper-specific literature belongs under that paper; do not recreate `literature/papers/`.

If a paper eventually needs local build code, use `papers/<paper_id>/code/` only for thin orchestration/packaging that imports root code or consumes reviewed report outputs.

## Reproducibility / data updates

A new data vintage normally means rerunning the same stable report/paper runner, not writing a new script.

Do not create `v2`, `final`, `new`, dated or alternate report/paper/code copies solely for version control.

Scientific-code changes require tests and corresponding protocol/methodology updates. Paper-specific selections happen after report outputs are stable.

## Preservation / provenance

Git history is the canonical storage for historical source states. Dated/version-labelled identifiers may remain in provenance records when they identify a specific historical state, but they must not become active parallel trees.

Historical `Bib/Bib2` names are provenance only and must not be recreated.

## Data/privacy boundary

Never commit:

- administrative Excel workbooks;
- row-level student/advising microdata;
- direct student or professor identifiers;
- HMAC/secret keys;
- credentials/tokens;
- unreviewed identifying free text.

Aggregated outputs may be committed after privacy review. Heavy literature PDFs/assets are internal research material in this private repository, not automatically redistributable content.

## Scientific interpretation rules

- Preserve validated discoveries, null results and sensitivity analyses in the broad report/empirical record.
- Keep causal language conservative for student-selected CMAT use.
- Do not infer motivation, habit formation or psychological states from administrative visits.
- Classroom is `instructor × course × academic period` unless a reviewed methodological change replaces it.
- Reported results should be reproducible from root code plus a stable product-local runner; notebooks or hand-edited outputs are not the canonical computational source.

## Literature rules

The physical literature corpus is shared under `literature/library/`. Cross-project literature maps live under `literature/general/`. Paper-specific literature indices, reading notes and gap trackers live with their paper under `papers/<paper_id>/literature/`.

Do not recreate upload-batch folders such as `Bib3`, `Bib4`, etc.

## Documentation / handoff

Major product folders should have a README explaining scope, inputs, outputs, canonical status and dependencies.

Future AI sessions should start with:

1. `AI_HANDOFF.md`;
2. `docs/RESEARCH_WORKFLOW.md` for the code → reports → papers production model;
3. `REPRODUCING.md` when execution matters;
4. `code/.ai_handoff.md` + `code/FUNCTION_INDEX.md` before code work;
5. `reports/AI_HANDOFF.md` + the relevant report README for report work;
6. `docs/PUBLICATION_PORTFOLIO.md` + relevant paper README for manuscript work;
7. literature handoffs when literature changes;
8. current methodology/protocol before scientific-code changes.

Update the owning document whenever code, estimands, portfolio boundaries or major architecture changes. Keep root handoffs compact rather than duplicating subsystem detail. **When a durable workflow rule emerges in conversation, record it in the repository documentation instead of relying on chat memory.**