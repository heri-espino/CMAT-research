# Paper 2 — CMAT use and MU performance

This directory contains the publication manuscript and build recipe for Paper 2, currently titled *Mathematics Support Use and Classroom-Relative Performance in First-Year University Mathematics*.

The manuscript is a decomposition of the historical `proyecto_visitas` work rather than a copy of that report. The scientific boundary and provenance mapping are recorded in `DECOMPOSITION_FROM_PROYECTO_VISITAS.md`.

## Build from the retained aggregate snapshot

From the repository root on branch `paper/paper2-mu-performance`:

```bash
python -m pip install -e './cmat_analysis[dev]'
python code/run_paper.py --check
python paper/build.py
```

`paper/build.py` generates the publication figures as vector PDFs from the retained aggregate tables under `brainstorm/shared/historical_outputs/study/` and then compiles `main.tex`. No private microdata are needed for this mode.

## Reproduce from controlled institutional inputs

```bash
python code/run_paper.py \
  --materias '/path/to/Materias.xlsx' \
  --asesorias '/path/to/Asesorias.xlsx' \
  --compare-retained \
  --compile
```

This regenerates the Paper 2 tables in `results/tables/`, checks the core outputs against the retained snapshot, creates vector PDF figures in `results/figures/`, records provenance under `results/logs/`, and compiles the manuscript using the generated outputs.

Administrative microdata must remain local and must not be committed to Git.

## Numerical provenance

The current first draft uses one internally consistent retained state: `brainstorm/shared/historical_outputs/study/`. A later methodology-restoration workspace contains some exact-dose summaries from another retained state; those values must not be mixed into this manuscript before a controlled rerun reconciles the difference.
