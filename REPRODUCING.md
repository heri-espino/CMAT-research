# Reproducing CMAT analyses

This document is the repository-level entry point for reproducing computational outputs. Scientific definitions belong in `code/STUDY_PROTOCOL.md`; code architecture belongs in `code/.ai_handoff.md`; this file only documents the execution path.

## 1. Requirements

The active Python project is under `code/` and currently requires Python `>=3.14,<3.15`. Direct analysis dependencies are version-pinned in both `code/pyproject.toml` and `code/requirements.txt`; `code/environment.yml` records the fuller Conda environment used for the current setup.

Raw/row-level institutional data are intentionally not stored in GitHub.

## 2. Create the Python environment

### Option A — pip / virtual environment

From the repository root:

```bash
python -m venv .venv
```

Activate it using the command appropriate for your operating system, then:

```bash
python -m pip install --upgrade pip
cd code
python -m pip install -e ".[dev]"
cd ..
```

### Option B — Conda

```bash
conda env create -f code/environment.yml
conda activate cmat314
```

If an existing `cmat314` environment is already available, update/verify it rather than creating a second version-named environment.

## 3. Verify the codebase

Run tests:

```bash
cd code
python -m pytest
cd ..
```

Verify the report runner structure without loading controlled data:

```bash
python code/experiments/methodology_report.py --check
```

The searchable function inventory is:

`code/FUNCTION_INDEX.md`

Regenerate it after Python changes with:

```bash
python code/scripts/generate_function_index.py
```

Normally the repository workflow also refreshes this file after Python changes.

## 4. Controlled inputs

The two principal controlled inputs are:

- academic/course records (`materias`);
- CMAT advisory/visit records (`asesorias`).

They must remain outside GitHub. Do not copy raw administrative workbooks into the repository merely to make a run easier.

The methodology runner can receive paths explicitly:

```bash
python code/experiments/methodology_report.py \
  --materias /path/to/Materias.xlsx \
  --asesorias /path/to/Asesorias.xlsx
```

On Windows PowerShell, the same command can be written on one line:

```powershell
python code/experiments/methodology_report.py --materias "C:\path\Materias.xlsx" --asesorias "C:\path\Asesorias.xlsx"
```

Use `--extra-covariates` only when an approved covariate file is part of the intended scientific specification.

## 5. Reproduce the methodology report outputs

Canonical runner:

```bash
python code/experiments/methodology_report.py --materias <academic-file> --asesorias <visits-file>
```

The runner is the stable recipe. It imports reusable functions from the package, executes the methodology analyses in their fixed order, writes deterministic aggregate outputs, and stages the report assets expected by `reports/methodology_report/`.

Local generated outputs are written under:

`code/outputs/methodology_report/`

This path is ignored by Git.

The report directory receives the reviewed/staged aggregate tables/figures required by the LaTeX report. The runner also writes build/provenance metadata so the input files and generated state can be identified.

### Generate without staging into the report

```bash
python code/experiments/methodology_report.py \
  --materias <academic-file> \
  --asesorias <visits-file> \
  --no-stage
```

### Compile the LaTeX report

If a compatible LaTeX installation is available:

```bash
python code/experiments/methodology_report.py \
  --materias <academic-file> \
  --asesorias <visits-file> \
  --compile
```

Compilation is presentation/build work; the scientific calculations are performed upstream by the imported Python functions.

## 6. Data updates

When a new institutional data extract arrives:

1. do not create a new `*_v2.py` runner;
2. verify that the input schema remains compatible;
3. run the tests;
4. rerun the same stable experiment/report runner with the new controlled input paths;
5. compare cohort counts, diagnostics and aggregate outputs with the previous retained state;
6. investigate unexpected differences before replacing retained/report outputs;
7. update manuscript/report prose only after the regenerated outputs are accepted.

A new data vintage is not, by itself, a methodological change.

## 7. Scientific changes

If cohort membership, an estimand, outcome construction, imputation, statistical test/model, standard errors, threshold logic or another result-generating rule changes:

1. modify the reusable implementation in `code/src/visitas_analysis/`;
2. update/add tests;
3. update `code/STUDY_PROTOCOL.md` or relevant methodology documentation;
4. regenerate `code/FUNCTION_INDEX.md`;
5. rerun every affected stable runner;
6. compare old/new aggregate outputs;
7. only then update reports/papers.

Do not implement the changed estimand only inside a paper or report runner.

## 8. Retaining outputs

Generated local files under `code/outputs/` are disposable/reproducible build artifacts.

After scientific and privacy review:

- project-wide or multi-paper retained aggregates belong under `analysis/shared/`;
- an aggregate artifact with one clear manuscript owner may belong under `papers/<paper_id>/results/`;
- do not retain duplicate copies in both places without a documented reason.

Current pre-reconciliation aggregate history is stored under `analysis/shared/historical_outputs/` for provenance/comparison.

## 9. Paper-specific reproduction

Paper-specific runners should live in `code/experiments/` using stable paper IDs and should import canonical functions. Do not create a paper runner until the paper has a defined reproducible analytical recipe; do not create placeholder runners merely to complete the directory structure.

At present, `methodology_report.py` is the canonical fully named report-specific runner. Future paper runners should follow the same thin-runner pattern documented in `code/experiments/README.md`.

## 10. Troubleshooting / provenance

Start with:

- `code/.ai_handoff.md` — code/reproducibility rules;
- `code/FUNCTION_INDEX.md` — locate existing functions;
- `code/STUDY_PROTOCOL.md` — scientific specification;
- `docs/MIGRATION_STATUS.md` — active/historical methodology status;
- `reports/methodology_report/README.md` — report-specific build/provenance notes.

If an older implementation is needed, retrieve it from Git history rather than restoring a permanent snapshot directory into the active tree.
