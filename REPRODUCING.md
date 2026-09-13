# Reproducing CMAT research

CMAT Research supports Python 3.14. The installable scientific package is defined by `cmat_analysis/pyproject.toml`; the root `pyproject.toml` contains repository-level tooling configuration only.

## Pip setup

From the repository root:

```bash
python -m pip install -e './cmat_analysis[dev,docs]'
```

Verify the shared library with:

```bash
(cd cmat_analysis && pytest -q)
python cmat_analysis/scripts/generate_function_index.py
```

## Conda setup

From the repository root:

```bash
conda env create -f environment.yml
conda activate cmat-research
git lfs install
git lfs pull
```

The Conda environment delegates Python package installation to the same editable `cmat_analysis` package used by the pip workflow, so scientific dependency pins remain centralized in `cmat_analysis/pyproject.toml`.

## Local controlled data

Raw administrative data are not stored in GitHub. After cloning, place the controlled source workbooks in the canonical local directory:

```text
data/raw/
├── Materias estudiantes-profesores 2019-2025 P y O.xlsx
├── Asesorias2024.xlsx
└── pre_treatment_covariates.xlsx   # optional
```

`data/raw/` is ignored by Git except for its README. The shared configuration discovers the two canonical workbooks automatically, so paper runners that use `get_study_config()` can normally be invoked without `--materias` or `--asesorias`. The shorter aliases `Materias.xlsx` and `Asesorias.xlsx` are also accepted, while explicit CLI paths still override automatic discovery.

A temporary compatibility fallback recognizes the historical locations directly under `data/`. New setups should use `data/raw/`.

## Git LFS and controlled data

Heavy research binaries use Git LFS; run `git lfs install` once and `git lfs pull` after cloning when assets are still pointers. Raw administrative workbooks, row-level student/advising microdata, direct identifiers, credentials, secrets, HMAC keys or salts, and unreviewed identifying free text must not be committed.

## Research runners

Brainstorm-local runners import the installed library, for example:

```bash
python brainstorm/methodology_report/code/methodology_report.py --check
```

On a `paper/*` branch, follow `PAPER_BRANCH.md`; paper-specific `code/` may orchestrate `cmat_analysis`, but reusable calculations must be validated upstream in the library first. Buildable paper branches use `python paper/build.py`, and the shared GitHub Actions paper workflow compiles manuscripts and exports source artifacts automatically.
