# Paper 1 results

This directory contains generated or deliberately selected **publication-level aggregate outputs** for Paper 1. The canonical recipe is `../code/run_paper.py`; reusable calculations remain in the shared `cmat_analysis` library.

Expected generated structure:

```text
results/
├── tables/
│   ├── 98_ppa_progression_cohort_flow.csv
│   ├── 99_revalidation_audit.csv
│   ├── 100_student_official_career_count_distribution.csv
│   ├── 101_ppa_behavior_profiles.csv
│   ├── 102_ppa_persistence_by_mu_group.csv
│   ├── 103_ppa_persistence_omnibus.csv
│   ├── 104_ppa_exact3_vs_4plus_persistence.csv
│   ├── 105_ppa_persistence_logistic_models.csv
│   ├── 106_ppa_piecewise_threshold_persistence.csv
│   └── 107_ppa_later_performance_models.csv
├── figures/
│   └── ppa_persistence_by_mu_group.png
├── logs/
└── run_summary.json
```

Tables `101`--`107` are the primary reproducibility bridge to the retained longitudinal snapshot currently cited by the manuscript. `python code/run_paper.py --compare-retained ...` checks them against `brainstorm/shared/historical_outputs/study/tables/` and fails rather than silently changing published numbers.

Do not hand-edit numerical outputs. Administrative row-level data, student identifiers, raw joined cohorts, and local input files must never be committed here. Aggregate CSVs or figures should only be committed after privacy/provenance review. Local run logs may contain local file paths and are not publication artifacts.
