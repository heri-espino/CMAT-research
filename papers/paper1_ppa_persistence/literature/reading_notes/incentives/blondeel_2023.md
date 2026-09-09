# Blondeel, Everaert & Opdecam (2023) — *A Little Push in the Back*

## Citation

Blondeel, E., Everaert, P., & Opdecam, E. (2023). A little push in the back: Nudging students to improve procrastination, class attendance and preparation. *Studies in Higher Education*. https://doi.org/10.1080/03075079.2023.2288170

## 60-second summary

This randomized first-year higher-education experiment tested five nudges delivered through a virtual learning environment. The important result is a **split between randomized assignment and post-treatment engagement**: simply being assigned to receive nudges did not significantly change procrastination, attendance, preparation, or final performance. Within the treatment group, however, students who clicked on more nudges had better behavioural outcomes and higher exam performance.

For Paper 1, this is methodologically valuable because it shows exactly why exposure, uptake, and intensity must not be conflated. The positive click-intensity relationships are not randomized and may reflect selection by motivation, ability, or engagement.

## Role in Paper 1

- **Priority:** core methodological/behavioural comparator.
- **Used in:** literature review, methods/identification discussion, Discussion.
- **Main job:** distinguish randomized intervention offer from voluntary uptake/intensity.
- **Journal relevance:** direct precedent from *Studies in Higher Education*.
- **CMAT connection:** highly relevant to the distinction between being in an incentive context and actually using CMAT.

## Design and sample

- **Setting:** first-year undergraduate accounting exercise classes at Ghent University.
- **Sample:** `N = 211`.
- **Design:** random assignment to treatment versus control.
- **Treatment:** five different VLE nudges distributed during the semester.
- **Outcomes:** procrastination measured four times, weekly class attendance, weekly class preparation, final exam performance.
- **Post-treatment intensity variable:** number/intensity of nudge clicks among treatment students (`N = 110` in the reported intensity regressions).
- **Methods:** correlations, repeated-measures ANCOVA, OLS regression, mediation analysis with bootstrap inference.

## Key results

### Randomized treatment-group variable

OLS models found no significant effect of assignment to the nudge group on:

| Outcome | Coefficient | p-value |
|---|---:|---:|
| procrastination at week 12 | `-0.08` | `.367` |
| class attendance | `0.06` | `.883` |
| class preparation | `3.26` | `.532` |
| performance | `0.30` | `.417` |

This is the cleanest experimental result and should be prioritized when discussing causal effects of the intervention offer.

### Nudge-click intensity within treatment group

Correlations reported for intensity:

- attendance: `r = .41`, `p < .001`;
- preparation: `r = .58`, `p < .001`;
- procrastination at week 12: `r = -.35`, `p < .001`;
- final performance: `r = .32`, `p < .001`.

OLS models using click intensity reported:

- lower week-12 procrastination: `p = .014`;
- higher attendance: `p < .001`;
- higher preparation: `p < .001`;
- higher final performance: `p = .003`.

The paper reports a direct click-intensity coefficient of about `0.68` for performance before mediation terms are added.

### Procrastination trajectory

Repeated-measures ANCOVA found change over time:

`F = 45.266`, `p < .001`, partial `η² = .397`, `N = 211`.

Procrastination rose from week 2 to week 5 (`p < .001`), then fell from week 5 to week 9 (`p < .001`) and again from week 9 to week 12 (`p = .034`).

### Mediation results among treatment-group clickers

Bootstrap mediation analyses reported:

- indirect effect through end-semester procrastination: `p = .072` (authors treat as support at a 10% threshold);
- indirect effect through attendance: `p = .152` (not supported);
- indirect effect through preparation: `p = .030` (supported).

## Identification warning

The paper itself notes that more motivated students may be more likely to click the nudges, procrastinate less, attend/prepare more, and earn higher grades. Therefore:

- randomized **assignment to nudges** supports causal interpretation of the group comparison;
- voluntary **click intensity** does not inherit randomization and should be interpreted as observational/post-treatment association.

This distinction is directly analogous to the problem of interpreting CMAT visit intensity.

## What this paper lets us say

- Offering a nudge can have a null average experimental effect even when voluntary engagement with it is positively associated with outcomes.
- Uptake/intensity variables can be strongly selected.
- Procrastination and engagement can vary meaningfully over the semester.
- *Studies in Higher Education* publishes rigorous intervention work that retains null findings and identification caveats.

## What it does **not** let us say

- Clicking more nudges causally improves performance.
- More CMAT visits necessarily cause better outcomes.
- PPA is a nudge; the authors define nudges as not materially changing incentives.
- A null treatment-offer effect means the intervention contains no useful information about behaviour.

## Local verification

Markdown: `literature/library/articles/blondeel_2023_nudging-procrastination-attendance-preparation.md`

PDF: `literature/library/pdf/blondeel_2023_nudging-procrastination-attendance-preparation.pdf`

Key anchors: pp. 10–16; Tables 4–7.