# Git workflow for this repository

This project uses a simple rule: **folders organize the project; branches organize temporary changes**.

## The normal pattern

Suppose `main` is stable and we want to reconcile the v8 and methodology-v5 code paths.

Create a short-lived branch:

```bash
git switch main
git pull
git switch -c method/reconcile-v8-v5
```

Work and commit there:

```bash
git add ...
git commit -m "method: reconcile KDE imputation with v8 pipeline"
```

Push and open a Pull Request:

```bash
git push -u origin method/reconcile-v8-v5
```

Review the diff, tests, numerical consequences, documentation changes, and privacy implications. When the change is accepted, merge the PR into `main` and delete the branch.

The next task starts again from the updated `main`.

## Why not permanent paper branches?

Paper 1, Paper 2, the report and the master analysis depend on the same scientific code and canonical outputs. Keeping permanent branches for each would create repeated merge work and could produce several incompatible versions of the same result.

Instead:

```text
main/
├── analysis/
├── reports/
├── papers/
│   ├── paper1_ppa_persistence/
│   └── paper2_mu_performance/
└── literature/
```

A paper update can still use a branch, but the branch describes the **change**, for example:

- `paper1/add-admission-covariate`
- `paper2/update-pairwise-results`
- `report/rebuild-after-methodology`
- `literature/add-buchele-2024`

After the PR is merged, the branch is deleted; the paper folder remains on `main`.

## What to inspect in a Pull Request

For scientific changes, check:

1. Which estimand or cohort changed?
2. Which functions changed?
3. Which outputs changed numerically?
4. Are tests passing?
5. Did the study protocol/changelog change?
6. Did the scientific source fingerprint change?
7. Does any result now require different interpretation?
8. Did the change introduce any privacy risk?

For LaTeX/report-only changes, check that numbers still match canonical outputs and that claims do not become stronger than the underlying analysis.

## Current example

`method/reconcile-v8-v5` is the current active feature branch. It exists only to perform one defined methodological reconciliation. Once merged, it should disappear.
