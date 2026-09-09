# Experiment runners

This directory is reserved for **stable, thin, reproducible runners** for specific scientific questions or manuscript analyses.

Reusable scientific logic does not belong here. Put reusable functions in `code/src/visitas_analysis/...`, test them there, and import them into a runner in this directory.

## Naming

Use stable scientific IDs rather than versions or dates. For the current publication portfolio, preferred runner names are:

- `paper1_ppa_persistence.py`
- `paper2_mu_performance.py`
- `paper3_grading_heterogeneity.py`
- `paper4_degree_help_seeking.py`
- `paper5_longitudinal_trajectories.py`

Do not create `*_v2.py`, `*_final.py`, `*_new.py`, or date-stamped variants. Git records historical versions.

## Runner responsibilities

A runner should be a short executable recipe that:

1. imports configuration;
2. imports canonical reusable functions;
3. constructs the required cohort using shared code;
4. calls the required analyses in a fixed order;
5. writes outputs to deterministic paths;
6. fails clearly when required inputs or invariants are missing.

It should **not** reimplement cleaning, cohort logic, statistics, models, confidence intervals, or plots that already exist in the package.

## Data updates

When a new data extract becomes available, rerun the same script. A new data vintage alone does not justify a new runner or new function. If the schema changes, adapt the shared ingestion/configuration layer and preserve the experiment's scientific specification whenever possible.

## Existing orchestration

The active repository currently has broader runners under `code/src/`:

- `run_study.py` — publication-oriented study pipeline;
- `run_analysis.py` — general/report pipeline.

Do not duplicate these pipelines here. Create a paper-specific runner only when an independently reproducible recipe is useful, and make it import the existing canonical functions rather than copying their logic.

See `code/.ai_handoff.md` for the complete reproducibility contract and `code/FUNCTION_INDEX.md` before creating any new function.
