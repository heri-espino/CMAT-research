# PPA-grouping execution status — 2026-10-26

**STAGED; INSTITUTIONAL ESTIMATES PENDING.** The agent branch implements the canonical `0 | 1–3 | 4+` model and preserves the original conversation's `0 | 1–3 | 4 | 5+` sensitivity as an explicit, separately enabled option. Group boundaries and Holm-family definitions have synthetic tests; no institutionally fitted PPA outcomes, effect estimates, clustered confidence intervals, Holm-adjusted empirical p-values, publication plots or figure QA have been produced.

## Reproducibility evidence

- Local staged source unit checks: `python -m pytest -q test_ppa_groups.py` — **11 passed**, using the local staged boundary/test code (2026-10-26). This is **not** a claim that GitHub executed the current PR HEAD.
- Local `python -m compileall -q .` — passed for locally staged files.
- Local data-free `python run_ppa_groups.py --check` — passed on the staged local runner.
- `test_synthetic_models.py` is committed but awaits a full checkout and installed `cmat_analysis`; it now **fails rather than silently skips** when the shared estimator is missing. End-to-end synthetic shared-estimator test status: **not run**.
- GitHub workflow **Branch architecture policy** (run 40319279277) succeeded on the then-current PR commit; no Python scientific-test workflow or authorized institutional job success has been established.
- Repository branch HEAD may advance; see PR #98 and its commits for definitive source SHAs.

## Authorized institutional execution

A full run requires both `--materias` and `--asesorias` explicit, authorized paths. The runner verifies N=6,627, 190 instructor-period contexts, 1,234 recorded users, and the historical exact visit-count support before publishing aggregate results. The **default** active exploratory multiplicity family is six tests across Z and PASS; `--include-secondary` expands the family to 18 tests. Raw source files are never copied into publication directories.

`historical_counts_only_REFERENCE.csv` is a historical count reconstruction with provenance; it is **not** a new fitted result. No regression parameters should be inferred from it.

## Integration and ethics holds

The integration branch was ahead of this work branch by three architecture commits when reviewed. Its updated scope permits only the primary three-group specification; the older PPA-agent task in this conversation additionally requested four-group sensitivity. The CLI makes the latter opt-in, and the administrator must decide whether to publish it. The integration scaffold README remains under administrator ownership; detailed methods are in `analysis/ppa-groups/METHODOLOGY_RESULTS.md`.

The repository is currently public while its controlled-data documentation states that versioned row-level pseudonymized records require restricted access. No controlled student-level source was read or republished in this task. Administrator/institutional disclosure remediation is required outside this agent's scope.
