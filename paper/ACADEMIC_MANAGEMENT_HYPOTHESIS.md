# Paper 2.1 — academic-management hypothesis

**Status:** mechanism hypothesis motivated by the observed outcome composition; not an identified causal explanation.

## Core idea

CMAT attendance may be associated with more than final course performance. It may also mark a broader pattern of active academic engagement or institutional navigation: students who seek mathematics support may be more likely to monitor their academic situation, seek advice, know the available academic procedures, or use those procedures when a course is going poorly.

Under this mechanism, two students with similarly adverse academic prospects could end the course differently:

- one may remain enrolled and receive a numeric grade below the 7.5 pass mark;
- another may actively use an institutional option such as BV.

RT and BA must not be assumed to represent the same process as BV; the current data in fact show different attendance patterns across these codes.

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

For mechanism-oriented regression, preserve a hierarchy of contrasts among non-PASS cases:

- **administrative outcome vs numeric failure:** BA/BV/RT = 1, numeric <7.5 = 0;
- **BV/RT vs numeric failure:** exclude BA;
- **BV vs numeric failure:** exclude RT and BA; this is the current preferred contrast for the active academic-management hypothesis;
- **RT vs numeric failure:** exclude BV and BA and treat this mainly as a diagnostic because RT is sparse among users.

BA remains primarily descriptive because it is rare among users and should not be interpreted as the same student-initiated decision as BV.

## Observable predictions

The mechanism becomes more plausible if the data show some combination of:

1. among students who do not pass, CMAT users are more likely than non-users to end with an administrative result rather than a numeric grade below 7.5;
2. the contrast is concentrated in BV rather than mechanically appearing for every administrative code;
3. the imputed continuous outcome shows larger attendance-frequency differences in its lower tail than the numeric complete-case outcome;
4. the exact administrative-token composition is consistent with the broader conditional result.

These predictions remain observational. Even if all hold, they do not show that CMAT caused greater institutional engagement or caused a student to withdraw.

## Current controlled-data evidence

The mechanism-oriented predictions have now been tested in the controlled Paper 2.1 recipe (GitHub Actions run `35515296397`, commit `871c0583fc76cd8f22e2bbe8882219acbd5a3467`).

Among students who did not pass:

- with zero visits, 923 of 1,504 non-PASS outcomes were administrative (61.4%); with one or more visits, 178 of 217 were administrative (82.0%);
- after instructor-period fixed effects and degree-programme adjustment, any attendance was associated with **+13.2 percentage points** in the probability that a non-PASS outcome was administrative rather than a numeric grade below 7.5 (95% CI 6.8 to 19.6 pp; p < 0.001);
- for **BV versus numeric failure**, excluding RT and BA, any attendance was associated with **+16.8 percentage points** (95% CI 9.5 to 24.1 pp; p < 0.001);
- for **RT versus numeric failure**, excluding BV and BA, the adjusted difference was **+0.5 percentage points** (95% CI -15.1 to 16.2 pp; p = 0.945).

The absolute outcome composition also matters. CMAT users did **not** have a higher overall administrative-outcome rate: zero-visit students had 17.1% BA/BV/RT compared with 14.4% among users. The conditional difference arises because numeric failures were much less common among users (3.2% versus 10.8%) and because BV was somewhat more common, while RT and BA were less common.

This pattern makes **BV**, not administrative withdrawal in general, the most relevant observed component for the engagement/institutional-navigation hypothesis. It remains an observational mechanism: the data do not record why a student used BV or whether CMAT attendance, advising, prior preparation, or another factor produced that choice.

Within positive attendance frequencies, the management-outcome omnibus tests were not significant, so the current evidence again points mainly to the distinction between **zero attendance and any attendance**, not to a clear monotone frequency gradient among users.

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
