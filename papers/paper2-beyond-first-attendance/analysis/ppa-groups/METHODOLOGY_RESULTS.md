# PPA three-band exploratory analysis — method and release status

**User-approved grouping: `0 | 1–3 | 4+` ONLY.** Counts in the historical 2026 cohort:
0 visits N=5,393, 1–3 visits N=932, 4+ visits N=302. These are
**historical aggregate counts**, not fitted PPA regression estimates.
The separately represented 0/1/2/3/4/5/6/7+ exact-frequency comparator is
historical evidence, not an additional PPA grouping.

## Rationale and inference

Three visits are one *optional* first-semester PPA1 activity. Individual PPA
eligibility, motive and credit receipt are not measured. Therefore 1–3 is
"within the possible three-visit threshold" and 4+ is "beyond that threshold",
not directly identified incentive-motivated versus self-motivated students.
Recorded visits are contemporaneous with final grades and observational.

Main outcomes: `Z_GRADE_PRIMARY` and `PASS`. Estimate distinct
professor-period fixed-effect, degree-adjusted models, with clustered
professor-period inference, adjusted group contrasts and omnibus tests.
Report nominal 95% cluster-robust intervals, not adjusted simultaneous CIs.
`PASS` is a linear probability model, so contrast units are percentage
points. Numeric-grade and observed-numeric standardised-Z sensitivities use
selected populations and are labelled accordingly.

**Multiplicity:** Three unordered pairs (0 vs 1–3, 0 vs 4+, 1–3 vs 4+)
are adjusted using Holm **separately in each outcome**: m=3 for primary
Z, m=3 for PASS. These are two separate exploratory families, not one
m=6 pooled family; do not conflate with historical 10/15/21/28-pair
families or the adjacent-visit multiplicity family.

## Reproducibility

```bash
python -m pip install -e './cmat_analysis[dev]'
python -m pytest -q papers/paper2-beyond-first-attendance/analysis/ppa-groups/test_ppa_groups.py papers/paper2-beyond-first-attendance/analysis/ppa-groups/test_synthetic_models.py
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --check
python papers/paper2-beyond-first-attendance/analysis/ppa-groups/run_ppa_groups.py --materias /authorized/Materias.xlsx --asesorias /authorized/Asesorias.xlsx
```

The runner refuses missing sources, empty/degenerate cohorts and mismatched
outcome definitions; it records source SHA-256 and **current** cohort counts.
It does **not** force historical N=6,627 / 190 contexts when new data are supplied.
To reproduce the *original frozen cohort*, add `--require-historical-cohort`
and investigate any failed sample/visit validation. Only approved aggregate
tables and figures may be published, after small-cell disclosure review.

## Output contract

On successful authorized execution (not before):
`results/tables/ppa-groups/{observed_groups,adjusted_means,pairwise_all_models,focus_target_minus_baseline,omnibus,model_info,pair_context_overlap,numeric_selected_sensitivity}.csv`;
`results/figures/ppa-groups/ppa_{z_grade_primary,pass}.{pdf,png}`;
`results/provenance/ppa-groups/run_manifest.json`.

Current branch contains code, synthetic tests, historical-only count reference,
and a pending-status note. **New fitted institutional PPA estimates remain
PENDING** until the runner is executed, checked, and the aggregate outputs
are committed and reviewed. The source manuscript must not borrow fitted
PPA coefficients from unrelated exact-frequency, curve or fused models.
