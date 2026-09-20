# Paper 2.1 — outcome framework

Paper 2.1 should not be framed as a single question about whether students who attend CMAT "improve". The available data do not contain a student-level pre-CMAT and post-CMAT performance measure, so **improvement is not observed directly**. The study compares final academic outcomes across patterns of same-period CMAT attendance.

The paper therefore uses three connected analytical layers.

## Layer 1 — attendance benchmark: 0 versus 1+

Purpose: recover the broad result already established in Paper 2 and in parts of the mathematics-support literature.

Outcomes:

- adjusted difference in instructor-period-standardised final grade;
- adjusted difference in probability of passing.

Interpretation: students with recorded CMAT attendance may finish the course with different final performance from students with no recorded attendance. This is not a pre-post improvement estimate and not a causal treatment effect.

This layer should remain short in Paper 2.1 because it motivates, rather than answers, the main research question.

## Layer 2 — attendance-frequency structure among users

Primary groups:

`1 / 2 / 3 / 4 / 5 / 6+`

Exploratory sensitivity:

`1 / 2 / 3 / 4 / 5 / 6 / 7+`

For each grouping, analyse in parallel:

1. continuous standardised final performance;
2. probability of passing.

This layer answers whether students with different positive attendance frequencies are distinguishable after accounting for instructor-period grading context and degree programme, and whether adjacent groups appear different, practically equivalent when a defensible equivalence margin exists, or statistically inconclusive.

The two outcomes need not have the same shape. A difference in mean standardised performance can occur without the same-sized change in pass probability because passing is a threshold event at 7.5; conversely, a distribution moving near the threshold can change pass rates substantially while producing a modest mean shift.

## Layer 3 — distribution and non-pass composition

This layer investigates **where the aggregate differences come from** without claiming latent student types.

### Outcome-state composition

Within each attendance-frequency group, report the shares:

- PASS;
- numeric final grade below 7.5;
- BA/BV/RT.

This distinguishes students who remained to receive a numeric non-passing grade from students with an administrative withdrawal.

### Distributional profile

For the continuous standardised outcome, report at least:

- 10th percentile;
- 25th percentile;
- median;
- 75th percentile;
- 90th percentile.

If only upper quantiles increase while the lower tail remains similar, higher means may be driven disproportionately by stronger-performing users. If lower quantiles and the median also shift, the association is broader across the outcome distribution.

Conditional mean Z among passers and non-passers may be shown descriptively, but these are post-outcome strata and must not be interpreted as causal subgroups or as evidence that CMAT creates two latent types of student.

## Why Z and PASS can tell different stories

The continuous Z-score measures position in the final-grade distribution relative to the instructor-period grading environment. PASS reduces the final outcome to whether the institutional threshold of 7.5 was crossed.

These are related but non-equivalent estimands. For example, moving from 8.0 to 9.0 changes Z but not pass status; moving from 7.4 to 7.6 may change pass status substantially while changing the continuous grade only slightly. Paper 2.1 should use this distinction as a substantive feature rather than treating one outcome merely as a robustness check for the other.

## Current Paper 2 benchmark evidence

Before the finer Paper 2.1 grouping is analysed, the inherited Paper 2 results show that the two outcomes already have somewhat different frequency patterns:

- unadjusted pass rates were 72.1% for 0 visits, approximately 81% for 1--3 visits, and 86.4% for 4+ visits;
- adjusted comparisons showed higher pass probability for every positive attendance group relative to 0 visits;
- the adjusted 1-versus-4+ comparison for PASS survived Holm correction in the inherited 0/1/2/3/4+ analysis;
- by contrast, the analogous continuous-Z 1-versus-4+ comparison did not survive Holm correction in Paper 2.

These inherited results motivate, but do not determine, the Paper 2.1 frequency analysis. They must not be projected onto the frozen 1/2/3/4/5/6+ grouping before the Paper 2.1 runner is completed.

## Language guardrail

Avoid wording such as:

- "students improve when they attend";
- "students who do not attend do not improve";
- "CMAT creates two groups of students".

Prefer:

- "students who attended had higher/lower final outcomes";
- "final performance differed across attendance-frequency groups";
- "the association differed depending on whether performance was measured continuously or at the passing threshold";
- "the distributional analysis examined whether group differences were concentrated in particular parts of the outcome distribution".
