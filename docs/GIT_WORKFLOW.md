# Git workflow

## Principle

`main` is the canonical source of truth. Repository folders organize persistent project structure; Git branches organize temporary changes.

Do not maintain long-lived branches for individual papers, reports, literature themes, or alternate scientific realities. A branch should describe one concrete task and disappear after merge.

Git itself is the authority for current branch state. Do not maintain a manual `BRANCH_STATUS.md` or any documentation that names one feature branch as permanently "active".

## Normal workflow

1. Start from current `main`.
2. Create a short-lived branch when the change benefits from review/isolation.
3. Make one coherent change.
4. Run relevant tests/builds and inspect numerical consequences when scientific code changed.
5. Open/review a Pull Request when appropriate.
6. Merge into `main`.
7. Delete the branch.

Example branch names describe the task, not a permanent subsystem:

- `method/reconcile-longitudinal-pipeline`
- `paper1/add-admission-covariate`
- `paper2/update-pairwise-results`
- `report/rebuild-methodology-assets`
- `literature/add-buchele-2024`
- `docs/clarify-reproduction`

## Why not permanent paper/report branches?

The papers and reports share the same scientific code, data definitions and aggregate outputs. Permanent thematic branches would create repeated merges and competing versions of cohorts, estimands and results.

Persistent ownership therefore lives in folders on `main`:

```text
main/
├── code/
├── analysis/
├── reports/
├── papers/
├── literature/
└── docs/
```

A paper may use a temporary branch for a manuscript change, but after merge the branch disappears and `papers/<paper_id>/` remains the canonical home.

## Scientific review checklist

For scientific changes, verify:

1. Which cohort/estimand changed, if any?
2. Which functions changed?
3. Were existing functions searched/reused first via `code/FUNCTION_INDEX.md`?
4. Which outputs changed numerically?
5. Do tests pass?
6. Were protocol/changelog/function-index documents updated when required?
7. Does the scientific source fingerprint need to change?
8. Does interpretation need to change?
9. Is there any new privacy/disclosure risk?

For report/manuscript-only changes, verify that numbers still trace to canonical outputs and that claims do not become stronger than the analysis supports.

## Reproduction rule

A new data vintage normally means rerunning the same stable runner, not creating a new versioned branch/script/report copy. Git records history; stable runners record the scientific recipe.

See `../REPRODUCING.md` and `../code/.ai_handoff.md`.

## Privacy rule

No branch or commit may add administrative Excel files, row-level student/advising microdata, direct identifiers, HMAC keys/salts, credentials, or unreviewed identifying free text.

## Commit style

Use concise descriptive prefixes when useful:

- `method:` statistical/method changes
- `analysis:` retained result/output changes
- `report:` report changes
- `paper1:` / `paper2:` manuscript changes
- `literature:` bibliography/index changes
- `privacy:` release/governance changes
- `docs:` documentation
- `test:` tests
- `chore:` maintenance

The prefix is descriptive only; it does not imply a permanent branch or alternate source of truth.
