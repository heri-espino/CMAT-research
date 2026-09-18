# Paper 2 — CMAT use and MU performance

This directory contains the publication manuscript and build recipe for Paper 2, currently titled *Attendance at a Mathematics Support Centre and Academic Performance in First-Year University Mathematics*.

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

This regenerates aggregate Paper 2 outputs in `results/tables/`, creates vector PDF figures in `results/figures/`, and records run provenance under `results/logs/`. The main attendance groups are `0 / 1 / 2 / 3 / 4+` CMAT visits during the same academic period as MU; tables `30`–`34` contain the main group comparisons and tables `80+` retain secondary and provenance analyses.

The Paper 2 recipe intentionally does **not** use the optional DMU diagnostic exam. A future commented-manuscript TODO proposes requesting a broadly covered university entrance-exam score as a genuinely pre-enrolment observed-preparation sensitivity.

To compile the official and commented manuscripts after aggregate results are available:

```bash
python paper/build.py
```

Administrative microdata must remain controlled and must not be committed as publication outputs.
