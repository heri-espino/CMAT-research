# Paper-specific code

This directory owns only the recipe for this publication: specification choices, execution order, paper-specific tables/figures and calls into the installed `cmat_analysis` library.

Install the shared library from the repository root with:

```bash
python -m pip install -e ./cmat_analysis
```

Do not implement reusable estimators, cohort definitions, statistical tests, transformations, confidence intervals, model primitives or reusable plotting functions here; those belong upstream in `main/cmat_analysis`.
