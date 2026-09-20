# Paper 2.1 — outcome framework

Paper 2.1 does not ask whether students "improve" after visiting CMAT, because the available data do not contain a student-level pre-CMAT and post-CMAT performance measure. The study compares **final academic outcomes** across patterns of same-period CMAT attendance.

The paper distinguishes two substantive margins and organises the analysis in four connected layers.

## Two substantive margins

### Performance margin

How does final academic performance differ across attendance patterns?

Measured with:

- instructor-period-standardised continuous final performance;
- probability of passing at the institutional threshold of 7.5;
- quantiles of the continuous outcome;
- numeric complete-case performance as a sensitivity.

### Academic-management margin

Conditional on an adverse final outcome, how is that outcome recorded?

The primary descriptive classification is:

1. PASS;
2. numeric final grade below 7.5;
3. BV/RT;
4. BA.

A second table keeps BV, RT and BA separate. This margin is descriptive and observational; it does not identify why a student received or selected a particular administrative outcome.

## Layer 1 — attendance benchmark: 0 versus 1+

Purpose: recover the broad result established in Paper 2 and commonly studied in the mathematics-support literature.

Outcomes:

- adjusted difference in standardised final performance;
- adjusted difference in probability of passing.

This layer motivates Paper 2.1 rather than answering its central question. It is an association between final outcomes and recorded attendance, not a pre-post improvement estimate.

## Layer 2 — attendance-frequency structure among users

Primary groups:

`1 / 2 / 3 / 4 / 5 / 6+`

Exploratory sensitivity:

`1 / 2 / 3 / 4 / 5 / 6 / 7+`

For each grouping, analyse in parallel:

1. continuous standardised final performance;
2. probability of passing.

Use instructor-period fixed effects, degree-programme indicators, cluster-robust inference, a user-only omnibus test, all pairwise contrasts with Holm correction, and adjacent-group contrasts.

The two outcomes need not have the same shape. Moving from 8.0 to 9.0 changes continuous performance without changing pass status, whereas moving from 7.4 to 7.6 changes pass status with only a small change in the raw grade.

## Layer 3 — outcome-state composition

For the full zero-inclusive grouping and for positive attendance frequencies, report the shares in:

- PASS;
- numeric grade below 7.5;
- BV/RT;
- BA.

Also report an exact administrative-token decomposition:

- PASS;
- numeric grade below 7.5;
- BV;
- RT;
- BA.

This layer asks whether apparent attendance differences are associated with **what kind of adverse outcome occurs**, rather than treating every non-PASS as substantively identical.

The distributional profile complements this decomposition by reporting at least the 10th, 25th, 50th, 75th and 90th percentiles of the continuous outcome. Compare the primary imputed outcome with the numeric complete-case distribution to assess how much of the lower-tail pattern is linked to administrative outcomes.

## Layer 4 — academic-management composition among non-PASS cases

This is a mechanism-oriented but still observational analysis.

Among students who do not pass, estimate:

1. **administrative outcome vs numeric failure:** BA/BV/RT versus a numeric grade below 7.5;
2. **BV/RT vs numeric failure:** restrict to numeric failures, BV and RT, leaving BA outside this narrower contrast.

Run a zero-versus-any-attendance benchmark and positive-frequency comparisons using the same instructor-period and degree-programme adjustment structure where estimable.

The narrower BV/RT contrast is more directly related to a hypothesis of active academic management because BA must not be assumed to represent the same student-initiated process as BV or RT.

## Academic-management hypothesis

The outcome composition may be compatible with CMAT attendance marking a broader pattern of academic engagement or institutional navigation: students who seek support may also differ in monitoring their academic standing, seeking advice, knowing academic procedures, or using those procedures when a course is going poorly.

This is **not directly measured**. Attendance does not prove engagement, and zero attendance does not prove disinterest. The full mechanism and competing explanations are documented in `paper/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`.

## Interpretation guardrails

Do not describe:

- CMAT attendance as causing improvement;
- zero attendance as lack of interest in the course or university;
- BV/RT as evidence that a student is more engaged;
- BA as equivalent to a voluntary withdrawal;
- conditional non-PASS comparisons as causal subgroup effects.

Preferred language distinguishes what is observed from what is hypothesised:

> Students with recorded CMAT attendance differed not only in final performance but also in the composition of adverse final outcomes; this pattern is compatible with broader differences in academic engagement or use of institutional academic-management options, although those mechanisms are not directly observed.

Before stating that BV or RT has a particular GPA/transcript consequence, verify the exact institutional rule and its stability during the study period.
