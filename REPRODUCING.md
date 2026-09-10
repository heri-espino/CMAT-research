# Reproducing CMAT research

Use Python 3.14 and install the shared library from the repository root:

```bash
python -m pip install -e './cmat_analysis[dev]'
```

Verify it with `(cd cmat_analysis && pytest -q)` and regenerate the function inventory with `python cmat_analysis/scripts/generate_function_index.py`.

Heavy binaries use Git LFS: run `git lfs install` once and `git lfs pull` after cloning when necessary.

Brainstorm-local runners import the installed library, for example `python brainstorm/methodology_report/code/methodology_report.py --check`. On a `paper/*` branch, follow `PAPER_BRANCH.md`; paper-specific `code/` may orchestrate `cmat_analysis`, but reusable calculations must be validated upstream in the library first.
