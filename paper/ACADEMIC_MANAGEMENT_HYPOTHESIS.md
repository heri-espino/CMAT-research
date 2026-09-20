# Paper 2.1 — academic-management hypothesis

**Status:** mechanism hypothesis motivated by the observed outcome composition; not an identified causal explanation.

## Core idea

CMAT attendance may be associated with more than final course performance. It may also mark a broader pattern of active academic engagement or institutional navigation: students who seek mathematics support may be more likely to monitor their academic situation, seek advice, know the available academic procedures, or use those procedures when a course is going poorly.

Under this mechanism, two students with similarly adverse academic prospects could end the course differently:

- one may remain enrolled and receive a numeric grade below the 7.5 pass mark;
- another may end with an administrative status such as BV or RT.

The administrative records do not reveal the student's motivation, knowledge, advice received, or the date at which the decision was made. The mechanism is therefore **compatible with the data only if its observable predictions are supported**; it cannot be asserted directly.

## Two margins

Paper 2.1 distinguishes two related but conceptually different margins.

### 1. Performance margin

How does final academic performance differ across CMAT attendance patterns?

Measured with:

- instructor-period-standardised continuous final performance;
- probability of crossing the institutional pass mark of 7.5;
- distributional summaries of the continuous outcome.

### 2. Academic-management margin

Conditional on not passing, how is the adverse final outcome recorded?

Primary descriptive states:

1. PASS;
2. numeric final grade below 7.5;
3. BV/RT;
4. BA.

The exact administrative-token table additionally reports BV, RT and BA separately.

For mechanism-oriented regression, use two contrasts among non-PASS cases:

- **administrative outcome vs numeric failure:** BA/BV/RT = 1, numeric <7.5 = 0;
- **BV/RT vs numeric failure:** restrict to numeric <7.5, BV and RT; code BV/RT = 1 and numeric <7.5 = 0, leaving BA outside this narrower contrast.

The second contrast is more directly connected to the proposed active academic-management mechanism because BA should not be assumed to represent the same student-initiated decision as BV or RT.

## Observable predictions

The mechanism becomes more plausible if the data show some combination of:

1. among students who do not pass, CMAT users are more likely than non-users to end with an administrative result rather than a numeric grade below 7.5;
2. the contrast is also present when focusing specifically on BV/RT versus numeric failure;
3. the imputed continuous outcome shows larger attendance-frequency differences in its lower tail than the numeric complete-case outcome;
4. the exact BV/RT composition varies with attendance in a way consistent with the broader administrative-result contrast.

These predictions remain observational. Even if all hold, they do not show that CMAT caused greater institutional engagement or caused a student to withdraw.

## Competing explanations

Patterns consistent with this mechanism may also reflect:

- differences in prior academic preparation;
- academic difficulty that simultaneously prompts help-seeking and withdrawal;
- advice from professors or academic staff;
- institutional requirements affecting CMAT attendance;
- differences in schedule, course persistence, or opportunity to accumulate visits;
- unobserved socioeconomic, motivational, or administrative factors.

The requested university entrance-exam measure can address part of prior preparation, but it cannot measure institutional knowledge, motivation, or advice received.

## Language guardrails

Do not write that students with zero visits:

- did not care about the course;
- did not care about the university or their GPA;
- were unaware of withdrawal procedures;
- would not have sought help later.

Zero recorded attendance measures only absence of recorded CMAT use in the academic period.

Similarly, do not write that CMAT users are definitively more engaged. Preferred wording is:

> The outcome composition is compatible with CMAT attendance marking broader differences in academic engagement or use of institutional academic-management options, although the administrative data do not measure those mechanisms directly.

## Institutional-rule verification

Before the manuscript states that a BV or RT protects the student's GPA or has a specific transcript consequence, verify the exact UDLAP rule and whether it was stable throughout the 2019--2024 study period. Do not infer historical policy from current practice or user recollection alone.

## Manuscript role

If the empirical predictions are supported, this mechanism belongs in the Discussion as an interpretation of the outcome-composition results, not as the main causal conclusion. The Results section should report the observed four-state composition and conditional non-PASS comparisons without motivational language.
