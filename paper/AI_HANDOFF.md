# Paper 2.1 — AI handoff

This file contains branch-specific rules for `paper/paper2.1-visit-frequency`.

Paper 2.1 was created from Paper 2 at commit `1956ef4bfe6073c9b28881a9da34d14cd22239a8`. Read `paper/PROJECT_CONTEXT.md`, `paper/ANALYSIS_PLAN.md`, and `paper/STATUS_AND_ROADMAP.md` before analysis or writing.

## What Paper 2.1 changes

Paper 2.1 is not simply Paper 2 with more categories. Its central estimand is the observational structure of outcomes across **positive CMAT attendance frequencies**.

The inherited Paper 2 rule `0 / 1 / 2 / 3 / 4+` is superseded here. The outcome-blind audit has frozen the primary positive-frequency grouping as **`1 / 2 / 3 / 4 / 5 / 6+`**. The decision must not be changed after inspecting outcome significance; see `paper/VISIT_GROUPING_DECISION.md`.

## What remains inherited from Paper 2

- first eligible MU attempt with CMAT coverage;
- period-wide CMAT attendance irrespective of visit subject label;
- instructor × academic-period grading context;
- pass mark = 7.5;
- BA/BV/RT are adverse/non-passing;
- no causal claims;
- DMU diagnostic is not an acceptable uniform baseline;
- entrance exam, if received and usable, is only an observed-preparation sensitivity;
- exact institutional ethics/data-use wording remains required before submission.

## Principal outcomes and academic-result states

### Binary performance
PASS = numeric grade >=7.5.

non-PASS = numeric grade <7.5, BA, BV, or RT.

### Continuous performance
Use the canonical Paper 2 adverse-outcome imputation and standardise final performance within instructor-period group. Keep the numeric complete-case standardised outcome as a sensitivity.

### Academic-result composition
Primary descriptive states are PASS / numeric <7.5 / BV-RT / BA. Also preserve BV, RT and BA separately in an exact administrative-token table.

Among non-PASS cases, analyse administrative outcome versus numeric failure, BV/RT versus numeric failure, and **BV versus numeric failure**. Current controlled-data evidence is specifically concentrated in BV; RT does not show the same adjusted 0-versus-1+ pattern. Do not generalise the BV result to all administrative codes, and do not merge BA with BV/RT when discussing a student-initiated academic-management mechanism.

In manuscript prose, any timing caveat should normally be limited to one sentence noting that administrative outcomes may occur before the end of the academic period and can therefore provide less opportunity to accumulate visits.

## Inference hierarchy

For continuous Z, primary inference should come from the fixed-effect model with cluster-robust uncertainty; Welch/Games–Howell is secondary.

For PASS, report adjusted probability/risk differences in percentage points using the same basic fixed-effect and clustering logic. Do not present an ANOVA on a binary outcome as the main analysis.

All positive-group pairwise comparisons require a predeclared multiplicity family and adjustment.

## Equivalence

A non-significant pairwise test does not establish that two attendance groups are the same. Use the word **equivalent** only if a formal equivalence design with a pre-specified practical margin is implemented.

Otherwise classify unsupported pairwise comparisons as inconclusive.

## Heatmaps

Heatmap colour represents effect magnitude/direction:

- difference in Z for the continuous outcome;
- difference in pass probability for the binary outcome.

Do not colour by p-value. Statistical/equivalence status may be indicated separately.

The main heatmaps focus on positive attendance-frequency groups. A zero-inclusive version may appear as a benchmark/supplement.

## Academic-management mechanism guardrail

Paper 2.1 may discuss the hypothesis that CMAT attendance marks broader academic engagement or institutional navigation, but only as a mechanism compatible with the observed outcome composition. Read `paper/ACADEMIC_MANAGEMENT_HYPOTHESIS.md`.

Never infer from zero recorded visits that a student did not care about the course, university, GPA, or withdrawal options. Never write that CMAT users are definitively more engaged unless a direct engagement measure is obtained.

Before claiming a specific GPA or transcript consequence of BV/RT, verify the institutional rule and its historical applicability to the study years.

## Literature framing

Paper 2.1 should begin with a dense state of the art. The literature review must lead to the gap concerning the **shape and distinguishability of repeated mathematics-support attendance**, not merely repeat that support users often outperform non-users.

Use prior observational and identification-oriented evidence together, preserving the distinction between association and causal evidence.

Do not claim diminishing returns before the Paper 2.1 analyses support that shape.

## Manuscript status

The inherited Paper 2 LaTeX files are currently baseline/provenance material only. Do not treat them as the Paper 2.1 manuscript until the visit-group support audit and dual-outcome analysis have stabilized.

## Repository governance

Do not merge the whole branch into `main` or Paper 2. Shared scientific functions discovered here should go through the repository upstream-maintainer process before they become canonical across papers.
