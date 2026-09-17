# Paper 2 — CMAT use and MU performance

This directory contains the publication manuscript and build recipe for Paper 2, currently titled *Mathematics Support Use and Classroom-Relative Performance in First-Year University Mathematics*.

The manuscript is a decomposition of the historical `proyecto_visitas` work rather than a copy of that report. The scientific boundary and provenance mapping are recorded in `DECOMPOSITION_FROM_PROYECTO_VISITAS.md`; TEAMAT-specific submission rules are recorded in `AI_HANDOFF.md`.

## Check the publication recipe

From the repository root on branch `paper/paper2-mu-performance`:

```bash
python -m pip install -e './cmat_analysis[dev]'
python code/run_paper.py --check
```

The check validates imports and repository structure without reading row-level administrative data.

## Reproduce from controlled institutional inputs

```bash
python code/run_paper.py \
  --materias data/controlled/Materias_pseudonymized.csv \
  --asesorias data/controlled/Asesorias_pseudonymized.csv
```

This regenerates aggregate Paper 2 outputs in `results/tables/`, creates vector PDF figures in `results/figures/`, and records run provenance under `results/logs/`. The primary exposure specification is `0 / 1 / 2 / 3 / 4+` same-term CMAT registrations; tables `30`–`34` are the primary exact-group outputs and tables `80+` retain secondary/provenance analyses.

The Paper 2 recipe intentionally does **not** use the optional DMU diagnostic exam. A future commented-manuscript TODO proposes requesting a broadly covered university entrance-exam score as a genuinely pre-enrolment observed-preparation sensitivity.

To compile the official and commented manuscripts after aggregate results are available:

```bash
python paper/build.py
```

Administrative microdata must remain controlled and must not be committed as publication outputs.
