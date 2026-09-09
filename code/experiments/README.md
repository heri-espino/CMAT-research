# Experiment runners

This directory contains **stable, thin, reproducible runners** for specific scientific questions and report builds.

Reusable scientific logic does not belong here. Put reusable functions in `code/src/visitas_analysis/...`, test them there, and import them into a runner in this directory.

## Active runner: `methodology_report.py`

The first report-specific runner reproduces the scientific assets for `reports/methodology_report/`:

```bash
python code/experiments/methodology_report.py
```

It:

1. loads the shared CMAT configuration and controlled inputs;
2. runs the shared publication-study pipeline for the base analysis;
3. adds the methodology-review functions restored from the validated methodology snapshot (`0/1/2/3/4+`, Games–Howell, FE+Holm, exact 0–12, career populations, and the N=4,211 progressor sensitivity);
4. regenerates aggregate CSV tables and PNG figures under `code/outputs/methodology_report/`;
5. regenerates the `latex_*.tex` table snippets consumed by `methodology_report.tex`;
6. stages those generated aggregates into `reports/methodology_report/`;
7. writes a build manifest with input SHA-256 values and output/provenance metadata;
8. optionally compiles the LaTeX report with `--compile`.

Useful commands:

```bash
python code/experiments/methodology_report.py --check
python code/experiments/methodology_report.py --no-stage
python code/experiments/methodology_report.py --compile
python code/experiments/methodology_report.py --materias /path/Materias.xlsx --asesorias /path/Asesorias.xlsx
```

The later refined N=3,241 PPA result included in the methodology report is explicitly external to this methodology runner and is preserved as a later-stage snapshot rather than silently relabelled as methodology output.

## Naming

Use stable scientific IDs rather than versions or dates. Future paper runners should use:

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

For `methodology_report.py`, the new extract can be passed explicitly with `--materias` and `--asesorias`; the build manifest records the SHA-256 of those files. After a changed extract, compare generated results with the previous retained aggregates and review any numeric prose in the LaTeX document before calling the PDF updated.

## Existing broad orchestration

The repository also has broader runners under `code/src/`:

- `run_study.py` — publication-oriented study pipeline;
- `run_analysis.py` — general/report pipeline.

Report/paper runners should import or wrap these shared pipelines rather than copy their scientific logic.

See `code/.ai_handoff.md` for the complete reproducibility contract and `code/FUNCTION_INDEX.md` before creating any new function.
