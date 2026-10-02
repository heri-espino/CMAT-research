# Observation-level audit for Paper 2.1

This folder contains a local descriptive companion audit motivated by the pre-imputation outcome figure, especially the visible numeric-failure mass in the exact five-visit group.

The committed source is deliberately data-free. Detailed observation-by-observation material and its figures are generated locally from the controlled pseudonymized inputs into `generated/`, which is ignored by Git. Do not commit generated observation-level material, stable student identifiers, professor identifiers, or exact visit-event records.

## Why this audit exists

The exact five-visit group contains 55 students. In the observed-outcome figure, 3.6% of the group has an observed numeric grade below 7.5, which corresponds to only **2 students**. With the revised 0.1-point histogram, those two observations appear directly at 5.7 and 5.8 instead of being smoothed into a density bump. The purpose of this audit is to inspect those observations in classroom and temporal context rather than infer a larger latent subgroup from a very small count.

The local report examines, for every student in the selected visit-frequency group:

- an ephemeral observation label (`O01`, `O02`, ...), not the stored student identifier;
- an ephemeral instructor label (`I01`, `I02`, ...), not the stored professor identifier;
- an ephemeral classroom label (`C01`, `C02`, ...), not `CLASSROOM_ID`;
- academic period;
- observed final outcome and numeric grade when present;
- same-period CMAT visit dates and recorded visit-subject labels;
- the observed numeric-grade distribution in that student's instructor-period classroom;
- classroom size, numeric-grade count, administrative-outcome count, mean, median, interquartile range, pass share, and the student's empirical percentile when defined;
- a classroom histogram/rug plot with the pass mark at 7.5 and the focal observation highlighted.

The report is descriptive. It does not infer why a student attended, why a student obtained a particular final outcome, whether a visit occurred before or after a particular assessment, or whether CMAT attendance caused the outcome.

## Build

From the repository root:

```bash
python -m pip install -e './cmat_analysis[dev]'
python paper/docs/observations/build_observation_audit.py --group 5
```

This writes local-only files under:

```text
paper/docs/observations/generated/
├── group5_observations.tex
├── group5_exact_numeric_grades.pdf
└── figures/
    ├── O01_classroom.pdf
    ├── O02_classroom.pdf
    └── ...
```

To compile the standalone companion document as well:

```bash
python paper/docs/observations/build_observation_audit.py --group 5 --compile
```

The committed standalone source is `group5_observation_audit.tex`. It also compiles without the generated fragment, in which case it contains the aggregate rationale and build instructions but not the local observation-level material.

## Privacy boundary

The controlled CSVs are pseudonymized, but combinations of grade, classroom, period and exact visit dates can still be identifying in small groups. For that reason the generated report is intentionally excluded from version control and is not produced by the normal paper build or uploaded by CI.
