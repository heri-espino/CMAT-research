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

## Git LFS and controlled data

Heavy research binaries use Git LFS; run `git lfs install` once and `git lfs pull` after cloning when assets are still pointers. Raw administrative workbooks, row-level student/advising microdata, direct identifiers, credentials, secrets, HMAC keys or salts, and unreviewed identifying free text must not be committed.

## Research runners

Brainstorm-local runners import the installed library, for example:

```bash
python brainstorm/methodology_report/code/methodology_report.py --check
```

On a `paper/*` branch, follow `PAPER_BRANCH.md`; paper-specific `code/` may orchestrate `cmat_analysis`, but reusable calculations must be validated upstream in the library first. Buildable paper branches use `python paper/build.py`, and the shared GitHub Actions paper workflow compiles manuscripts and exports source artifacts automatically.
