# experiment001 — PPA three-band threshold

User-approved grouping **only**: `0 | 1–3 | 4+`. The historic exact
`0/1/2/3/4/5/6/7+` comparison is separate and has its own Wald/Holm
family. No fourth standalone visit band is fitted in this experiment.

Outcomes: full-cohort Z/PASS, professor-period FE and cluster-robust SE,
degree controls; separate per-outcome 3-pair exploratory Holm families
and optional observed-numeric sensitivity. PPA motive/credit unobserved.

Reproduce using the documented source-root launcher or directly:

```bash
python -m pytest -q papers/paper2-beyond-first-attendance/analysis/ppa-groups/test_ppa_groups.py papers/paper2-beyond-first-attendance/analysis/ppa-groups/test_synthetic_models.py
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --check
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --materias /authorized/Materias.xlsx --asesorias /authorized/Asesorias.xlsx
```

For newly updated data, report the new eligible N, contexts and group counts
instead of assuming historical counts; use `--require-historical-cohort`
only for frozen-cohort reproduction. **No new PPA estimates are committed yet.**
See [full methods](../METHODOLOGY_RESULTS.md).
