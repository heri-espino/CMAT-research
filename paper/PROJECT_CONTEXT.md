# Paper 2.1 — frequency of mathematics-support attendance

**Working title:** *Beyond First Attendance: Visit Frequency at a Mathematics Support Centre and Academic Performance*

**Canonical branch:** `paper/paper2.1-visit-frequency`

## Motivation

Paper 2 establishes a reproducible observational contrast between students with no recorded CMAT attendance and students who attend during the same MU academic period. Paper 2.1 takes that result as a benchmark rather than as its endpoint.

The central question is what happens **among students who actually use CMAT**. A student who attends once may resemble a student who attends twice; two and three visits may also be difficult to distinguish; alternatively, differences may emerge only after attendance frequencies become sufficiently separated. The existing Paper 2 top-code of `4+` cannot answer this because it combines students with four visits and students with substantially higher attendance.

## State-of-the-art orientation

The manuscript should begin with a comparatively dense state-of-the-art section rather than a short conventional introduction.

The literature backbone should distinguish:

- mathematics-support evaluation and the limits of routine usage data: Matthews et al. (2013), Lawson et al. (2020), Mullen et al. (2024);
- observational attendance/performance studies: Mac an Bhaird et al. (2009), Jacob & Ní Fhloinn (2019), Rickard & Mills (2018);
- non-engagement and selection into support: Mac an Bhaird et al. (2013) and the review literature;
- identification-oriented evidence with more mixed performance findings: Paloyo et al. (2016), Pugatch & Wilson (2018), Büchele & Schürmann (2024);
- how prior studies group attendance frequency, especially Jacob & Ní Fhloinn's separation of one visit from no visits and their progressively pooled upper-frequency groups.

The gap is not simply whether mathematics-support users perform differently from non-users. Paper 2.1 asks how finely attendance frequency can be resolved with adequate statistical support, whether adjacent or more distant attendance frequencies are distinguishable or practically similar, and whether attendance is associated with **how adverse course outcomes are recorded** when a student does not pass.

## Population and exposure

Population: the same Paper 2 first-eligible-MU cohort with CMAT coverage, currently N = 6,627.

Exposure: number of CMAT visits during the same academic period as MU, irrespective of the subject label attached to the visit.

The benchmark comparison `0 vs 1+` should be reproduced briefly as a bridge to Paper 2 and prior literature. The main analysis then focuses on students with at least one recorded visit.

The observed positive-visit counts currently include:

- 1: 517
- 2: 245
- 3: 170
- 4: 96
- 5: 55
- 6: 50
- 7: 25
- 8: 19
- 9: 11
- 10: 13
- 11: 2
- 12: 4
- 13: 2
- 14: 6
- 15: 5
- >15: 14

The outcome-blind support audit has now frozen the primary positive-frequency grouping as **`1 / 2 / 3 / 4 / 5 / 6+`**. The more granular `1 / 2 / 3 / 4 / 5 / 6 / 7+` specification is retained only as an exploratory sensitivity. See `paper/VISIT_GROUPING_DECISION.md` for the decision record.

## Performance outcomes and academic-result composition

### 1. PASS / non-PASS

PASS = 1 for a numeric final grade >= 7.5.

PASS = 0 for:

- numeric grade < 7.5;
- BA (baja académica);
- BV (baja voluntaria);
- RT (retiro temporal).

This outcome requires **no latent numeric-grade imputation** and therefore provides the cleanest analysis of academic success versus non-success.

### 2. Continuous standardised grade with adverse-outcome imputation

Retain the Paper 2 continuous construction:

- numeric grades unchanged;
- BA/BV/RT assigned values below 7.5 under the canonical within-instructor-period imputation rule;
- completed final grades standardised within instructor × academic-period grading group.

This captures more information than PASS but depends on the adverse-outcome numerical representation, so it should be interpreted alongside the binary analysis rather than in isolation.

### 3. Academic-result composition

Paper 2.1 also treats the **type of final academic outcome** as substantively informative rather than collapsing all non-PASS cases together.

Primary descriptive states:

- PASS;
- numeric final grade below 7.5;
- BV/RT;
- BA.

An exact table preserves BV, RT and BA separately. Conditional on non-PASS, the analysis compares administrative outcomes with numeric failure and isolates BV versus numeric failure as the most directly relevant observed contrast for the academic-management hypothesis.

This is not a third causal outcome. It is a decomposition of the observed final record intended to distinguish the performance margin from the academic-management margin described in `paper/OUTCOME_FRAMEWORK.md`.

## Main questions

1. Does the established 0-versus-1+ contrast appear under both outcome families?
2. Among CMAT users, is there evidence that outcomes differ across attendance-frequency groups?
3. Which specific pairs differ after multiplicity adjustment?
4. Which adjacent groups are statistically compatible with practical equivalence, if defensible equivalence margins can be specified before testing?
5. Does the pairwise structure suggest a plateau, gradual change, separated attendance regimes, or an irregular pattern?
6. Are conclusions similar for PASS probability and the continuous standardised-grade outcome?
7. Among students who do not pass, does the composition of the final outcome differ between zero attendance and any attendance?
8. Is that composition specifically associated with BV rather than with RT or BA?
9. Does the academic-management composition vary further across positive attendance frequencies, or is the main separation again zero versus any attendance?

## Interpretation

Do not describe increasing visit count as a causal treatment dose. Repeated attendance can reflect continued need, engagement, institutional requirements, or other unmeasured characteristics. Paper 2.1 studies the **shape of an observational association**.

The phrase “diminishing returns” is a hypothesis to investigate, not an established result. It may be used only if the fitted pattern and uncertainty genuinely support it.

Likewise, the academic-management pattern may be discussed as compatible with broader engagement or institutional navigation, but attendance is not a direct measure of motivation, knowledge of university procedures, or concern for GPA. Current evidence is specifically concentrated in BV; do not generalise that pattern to RT or BA. See `paper/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`.
