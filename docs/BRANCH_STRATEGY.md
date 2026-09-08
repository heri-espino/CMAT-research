# Branch strategy

## Principle

This project uses **`main` as the canonical monorepo**. Branches are temporary workspaces for concrete changes, not permanent homes for Paper 1, Paper 2, analysis, privacy, literature, or reports.

Everything that is conceptually part of the project lives together on `main` in explicit subfolders with local READMEs.

## Why

The CMAT project is highly interdependent:

`controlled data -> canonical code -> canonical outputs -> report / Paper 1 / Paper 2`.

Long-lived thematic branches would force repeated merges and create multiple competing versions of the same scientific result. Short-lived feature branches reduce that risk.

## Normal workflow

1. Start from current `main`.
2. Create one short-lived branch for one concrete task.
3. Make the change and document it.
4. Run relevant tests/builds.
5. Open and review a Pull Request.
6. Merge into `main`.
7. Delete the branch.

Example:

`method/reconcile-v8-v5 -> PR -> main`

Then a later task starts from the updated `main`, for example:

`report/rebuild-statistical-report -> PR -> main`.

## Current active scientific branch

`method/reconcile-v8-v5` is the only branch that should be treated as active scientific development. It exists to reconcile the historical longitudinal v8 pipeline with the later methodology-v5 corrections without losing functionality.

## Deprecated thematic branches

The following branches were created before this policy was simplified. They should receive no new work:

- `analysis/all-discoveries`
- `report/technical-methodology`
- `paper1/ppa-persistence`
- `paper2/mu-performance`
- `literature/heavy-batch2`
- `privacy/release-controls`
- `integration/reproducible-pipeline`

Their subject matter now belongs in subfolders on `main`. They can be deleted later after confirming they contain no unique scientific changes.

## Scientific rule

There must be one canonical scientific chain. Papers and reports consume canonical aggregate outputs; they must not silently recalculate alternative versions of the study.

## Privacy rule

No branch may add administrative Excel files, row-level student/advising microdata, direct identifiers, HMAC keys, credentials, or unreviewed free-text fields.

## Commit style

Use descriptive prefixes such as:

- `method:` statistical-method changes
- `analysis:` result/output changes
- `report:` technical report changes
- `paper1:` / `paper2:` manuscript changes
- `literature:` bibliography/index changes
- `privacy:` release/governance changes
- `docs:` documentation
- `test:` tests
- `chore:` maintenance
