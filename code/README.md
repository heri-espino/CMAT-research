# Paper 2 code

This directory contains only the thin publication recipe for Paper 2. Reusable cohort definitions, outcome construction, estimators, tests, confidence intervals, and shared plotting primitives belong in `main/cmat_analysis` and must be imported through its public API.

## Entry points

- `run_paper.py` reconstructs the first-MU analytical cohort from controlled local inputs, produces the Paper 2 aggregate tables, optionally checks them against the retained canonical snapshot, and can compile the manuscript.
- `figures.py` converts either retained or freshly generated aggregate tables into English-language vector PDF figures.

## Setup and validation

```bash
python -m pip install -e './cmat_analysis[dev]'
python code/run_paper.py --check
python code/figures.py --source retained
```

## Controlled-data rerun

```bash
python code/run_paper.py \
  --materias '/path/to/Materias.xlsx' \
  --asesorias '/path/to/Asesorias.xlsx' \
  --compare-retained
```

The historical `proyecto_visitas` source code is not imported here. It is provenance for how the question developed; the current runner uses only the canonical `cmat_analysis` definitions and same-period support exposure.
