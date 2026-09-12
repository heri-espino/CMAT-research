# Contributing to CMAT Research

This repository is a research compendium rather than a single software package, so contributions must preserve both scientific reproducibility and the branch governance described in `docs/REPO_GOVERNANCE.md`.

## Where changes belong

Reusable scientific logic belongs in `cmat_analysis/` and should be integrated into `main` before it is consumed by publication branches. Broad diagnostics, sensitivity analyses, null results, and exploratory work belong in the canonical `brainstorm/` layer. Publication-specific writing, selected literature, runners, figures, and submission material belong only on the corresponding `paper/*` branch. Historical `brainstorm/*` branches are provenance workspaces and must not be merged wholesale into `main`.

## Development setup

Use either the pip or Conda setup documented in `REPRODUCING.md`. Before opening a pull request, run the relevant test suite and any branch-specific checks; for shared library changes, at minimum run:

```bash
python -m pip install -e './cmat_analysis[dev,docs]'
(cd cmat_analysis && pytest -q)
```

## Research and privacy requirements

Never commit administrative workbooks, row-level student/advising microdata, direct identifiers, credentials, secrets, HMAC keys or salts, or unreviewed identifying free text. Aggregate outputs must receive privacy review before being committed. Withdrawals, cohort definitions, outcome construction, and other scientific conventions must be documented rather than silently changed.

## Pull requests

Keep pull requests narrow enough to review scientifically. Describe the research or infrastructure purpose, files changed, validation performed, and any effect on public APIs, cohorts, retained outputs, or manuscripts. Reusable changes discovered on a paper branch should be promoted to `main` first and then streamed back to long-lived branches.

## Citation and third-party materials

Do not add third-party articles, figures, tables, or other copyrighted materials unless their storage and use are appropriate for the repository. Repository citation metadata lives in `CITATION.cff`, `CITATION.bib`, and `codemeta.json`; paper-specific author lists and citations remain branch-specific and must not be inferred from repository ownership.
