# CMAT repository operating rules

## Start here

Before substantive work:

1. read `.ai_handoff.md`;
2. read the README/AGENTS file in the subsystem being changed;
3. inspect current canonical outputs/protocol before quoting numerical results;
4. use a short-lived branch for a concrete change unless the user explicitly requests otherwise.

## Canonical repository model

`main` is the source of truth. Organize the project by subfolder; use branches only as short-lived workspaces for concrete changes.

Read `docs/BRANCH_STRATEGY.md` and `docs/GIT_WORKFLOW.md` before creating or reusing a branch.

## Scientific dependency rule

Maintain one scientific chain:

`controlled data -> code/ -> analysis/ -> reports/ and papers/`.

Do not create manuscript-specific scientific pipelines. If Paper 1 or Paper 2 needs a methodological change, implement and validate it in canonical code first.

## Literature dependency rule

Maintain one literature chain:

`literature/library/ -> literature/general/ and literature/papers/ -> manuscript references.bib`.

- `literature/library/` is the only physical article store.
- Never duplicate an article because it belongs to multiple papers.
- Paper-specific literature folders contain roles/indexes only.
- Read `literature/AGENTS.md` before literature changes.

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
- Do not silently substitute the `N=4,211` future-Calculus progressor subset for the full first-MU cohort; they answer different questions.

## Documentation rule

Major folders should have a README explaining scope, inputs, outputs, canonical status and dependencies. Update `.ai_handoff.md` whenever methodology, estimands, cohort definitions, core results, literature architecture, or publication strategy materially change.
