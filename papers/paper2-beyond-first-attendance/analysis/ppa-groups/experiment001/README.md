# experiment001 — PPA-threshold attendance groupings

## Why
Test whether observed mathematics-center attendance patterns around the optional PPA1 three-visit activity are associated with final MU grade Z and PASS, without assigning behavioral motives or causal status. The integration contract specifies three groups; a conflicting original agent task also requested an optional four-group sensitivity. Both are explicit modes, never overlapping levels within one model.

## How
- **Cohort:** the canonical first-eligible MU sample, exactly N=6,627, 190 professor-period clusters, 1,234 CMAT users, and historical exact-frequency support verified before fit.
- **Primary:** `0 | 1–3 | 4+` as one categorical FE model; historical exact `0/1/2/3/4/5/6/7+` kept separate.
- **Optional:** `--include-secondary` also fits `0 | 1–3 | 4 | 5+`, another separate categorical FE model, never combining `4` with `4+` as distinct levels in one model.
- **Outcomes:** `Z_GRADE_PRIMARY` and `PASS` built using the shared `cmat_analysis.measures` functions. Numeric-grade and selected complete-case sensitivities explicitly separated.
- **Uncertainty:** cluster at `CLASSROOM_ID`; include professor-period FE and degree-programme categorical covariates.
- **Multiplicity:** Holm over six primary pairwise Z/PASS tests by default, or all 18 PPA tests jointly if optional secondary is enabled. Exact-frequency comparison remains a distinct 28-pair family per outcome.
- **Observed and adjusted measures:** group N, descriptive means, adjusted standardization with delta-method cluster CIs, Wald pairwise contrasts and F omnibus; confidence intervals remain nominal unless otherwise marked.
- **Output:** only aggregate CSV/figures after authorized run, with source/code hashes and a manifest.

## Reproduce from a full authorized repository checkout
```bash
python -m pip install -e './cmat_analysis[dev]'
python -m pytest -q papers/paper2-beyond-first-attendance/analysis/ppa-groups/test_ppa_groups.py papers/paper2-beyond-first-attendance/analysis/ppa-groups/test_synthetic_models.py
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --check
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --materias /authorized/Materias.xlsx --asesorias /authorized/Asesorias.xlsx
# Only with approved expansion to the four-group sensitivity:
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --materias /authorized/Materias.xlsx --asesorias /authorized/Asesorias.xlsx --include-secondary
```

## Findings at this checkpoint
The staged local grouping tests passed (11 unit tests; `--check` passed); the committed end-to-end shared-estimator integration tests have **not** run in this environment. Historical visit counts imply primary 5,393/932/302 and optional secondary 5,393/932/96/206. These are validated arithmetic aggregates from historical exact counts, **not newly adjusted model estimates**. There is no empirical evidence from this new fitted model yet to accept/reject a 3-to-4-visit breakpoint hypothesis.

## Next
Run synthetic integration tests using the actual installed shared `cmat_analysis` package, then execute the institutional data workflow with authorized explicit paths and exact sample validation. Independently review adjusted means/contrasts, CIs, tables, plots, disclosure limits and sensitivity population selection. Reconcile the integration plan's three-group-only scope with the originating task's optional four-group request **before** manuscript integration. Administrator controls PR merge and all cross-cutting publication changes.

## Source register
- `main:docs/PAPER2_CONSOLIDATION_PLAN.md` and `paper/paper2-beyond-first-attendance:docs/PAPER2_CONSOLIDATION_PLAN.md` (later clarification).
- `paper/paper2.1-visit-frequency:paper/docs/analysis/{ANALYSIS_PLAN.md,VISIT_GROUPING_DECISION.md,OUTCOME_FRAMEWORK.md}`.
- `paper/paper2.1-visit-frequency:results/paper21/tables/10n_zero_inclusive_7plus_descriptives.csv`.
- `main:cmat_analysis/src/cmat_analysis/statistics/attendance_frequency.py`.
- `main:cmat_analysis/src/cmat_analysis/measures/_grades.py`.
