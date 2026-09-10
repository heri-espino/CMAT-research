# Reproducing CMAT analyses

This document is the repository-level execution entry point. Scientific definitions belong in `code/STUDY_PROTOCOL.md`; reusable-code architecture belongs in `code/.ai_handoff.md`; product-specific build details belong in the owning report/paper README.

## 1. Production model

```text
controlled data
    ↓
root/code reusable functions
    ↓
product-local thin runner
    ↓
report
    ↓
paper selection
```

For the methodology report, the product-local runner is inside the report itself:

`reports/methodology_report/code/methodology_report.py`.

## 2. Requirements

The active Python project is under `code/` and currently requires Python `>=3.14,<3.15`. Direct dependencies are version-pinned in `code/pyproject.toml` and `code/requirements.txt`; `code/environment.yml` records the fuller Conda environment.

Raw/row-level institutional data are intentionally not stored in GitHub.

### Git LFS for PDFs and heavy binaries

This repository intentionally uses **Git LFS** for heavy research binaries, including PDFs under `literature/`, `reports/`, and `papers/`, as well as selected PNG/JPG assets and archive ZIPs. Git stores small pointer files in normal history while Git LFS materializes the corresponding binaries in the working tree.

Install Git LFS once on each computer before cloning:

```bash
git lfs install
git clone <repository-url>
```

A normal clone performed after `git lfs install` should materialize LFS files automatically. If the repository was already cloned and a PDF opens as a small text file containing `version https://git-lfs.github.com/spec/v1`, run:

```bash
git lfs install
git lfs pull
```

Useful diagnostics:

```bash
git lfs ls-files
git lfs status
```

Do not migrate repository-wide PDFs back into normal Git merely to make them visible locally; install/materialize LFS instead. The LFS policy is defined in `.gitattributes` and exists to keep normal Git history smaller as the literature and report corpus grows.

## 3. Create the Python environment

### pip / virtual environment

From the repository root:

```bash
python -m venv .venv
```

Activate it, then:

```bash
python -m pip install --upgrade pip
cd code
python -m pip install -e ".[dev]"
cd ..
```

### Conda

```bash
conda env create -f code/environment.yml
conda activate cmat314
```

If an existing environment already matches the recorded specification, verify/update it rather than creating a version-suffixed duplicate environment.

## 4. Verify root code

```bash
cd code
python -m pytest
cd ..
```

The searchable reusable-function inventory is:

`code/FUNCTION_INDEX.md`

Regenerate it after root-code Python changes with:

```bash
python code/scripts/generate_function_index.py
```

The repository workflow also refreshes this file after Python changes under `code/`.

## 5. Verify the methodology report boundary

Without controlled data:

```bash
python reports/methodology_report/code/methodology_report.py --check
```

This verifies that the atomic report entry point can resolve the required reusable functions from root `code/` and that the report's required structural assets are present.

## 6. Controlled inputs

The principal controlled inputs are:

- academic/course records (`materias`);
- CMAT advisory/visit records (`asesorias`).

They must remain outside GitHub.

## 7. Reproduce the methodology report

Canonical command:

```bash
python reports/methodology_report/code/methodology_report.py \
  --materias <academic-file> \
  --asesorias <visits-file>
```

On Windows PowerShell:

```powershell
python reports/methodology_report/code/methodology_report.py --materias "C:\path\Materias.xlsx" --asesorias "C:\path\Asesorias.xlsx"
```

The local script is intentionally thin. It calls the root-code methodology build/pipeline implementation; reusable calculations are not implemented under `reports/`.

Disposable generated working outputs are written inside the atomic report at:

`reports/methodology_report/build/`

This path is ignored by Git. Reviewed/staged aggregate CSVs and figures used by the report remain under the report's `tables/` and `figures/` directories.

### Generate without replacing retained report assets

```bash
python reports/methodology_report/code/methodology_report.py \
  --materias <academic-file> \
  --asesorias <visits-file> \
  --no-stage
```

### Compile the report

```bash
python reports/methodology_report/code/methodology_report.py \
  --materias <academic-file> \
  --asesorias <visits-file> \
  --compile
```

Compilation is presentation/build work; statistical calculations happen in imported root-code functions.

## 8. Data updates

When a new institutional extract arrives:

1. do not create a new report folder or `*_v2.py` runner;
2. verify input schema compatibility;
3. run root-code tests;
4. rerun the same report-local runner with the new controlled paths;
5. compare cohort counts, diagnostics and aggregate outputs with the previous retained state;
6. investigate unexpected differences before replacing retained report assets;
7. update report prose only after outputs are accepted;
8. propagate only the needed validated subset into downstream papers.

A new data vintage is not, by itself, a methodological change.

## 9. Scientific changes

If cohort membership, an estimand, outcome construction, imputation, statistical test/model, standard errors, threshold logic or another result-generating rule changes:

1. modify the reusable implementation in `code/src/visitas_analysis/`;
2. update/add tests;
3. update `code/STUDY_PROTOCOL.md` or relevant methodology documentation;
4. regenerate `code/FUNCTION_INDEX.md`;
5. rerun every affected report-local runner;
6. compare old/new aggregate outputs;
7. only then update downstream papers.

Do not implement the changed estimand only inside a report or paper runner.

## 10. Reports and papers

Reports are broad research-development products. They may contain more analyses than any one manuscript and are the preferred home for methodological brainstorming, sensitivity results and scientific context.

Papers are downstream publication selections. If a final paper needs local copies of approved report tables/figures for submission portability, retain them under `papers/<paper_id>/results/` with provenance to the source report/root code.

A paper-local `code/` folder, if ever needed, is for thin build/packaging orchestration only.

## 11. Shared aggregate archive

`analysis/shared/` may retain aggregate empirical objects that genuinely serve multiple reports/papers or are needed for historical reconciliation. It is not a required stage between code and reports.

Current pre-reconciliation aggregate history is stored under `analysis/shared/historical_outputs/`.

## 12. Troubleshooting / provenance

Start with:

- `code/.ai_handoff.md` — root-code/product-runner boundary;
- `code/FUNCTION_INDEX.md` — locate existing functions;
- `code/STUDY_PROTOCOL.md` — scientific specification;
- `reports/README.md` — report-layer role;
- `reports/methodology_report/README.md` — methodology build/provenance;
- `docs/MIGRATION_STATUS.md` — active/historical methodology status.

If an older implementation is needed, retrieve it from Git history rather than restoring a permanent snapshot directory into the active tree.
