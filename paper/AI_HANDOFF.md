# Paper 2 — TEAMAT AI handoff

This file adds Paper-2-specific submission rules on top of the repository-wide `.ai_handoff`.

## Target journal

Primary target: **Teaching Mathematics and its Applications: An International Journal of the IMA (TEAMAT), Section A research article**.

Use the official IMA/Oxford class bundle committed under `paper/ima-authoring-template/`. The class is shared across IMA journals, so a generic IMA header in the draft is expected; do not try to fake a TEAMAT journal header.

## Journal-specific citation exception

The repository-wide house draft currently prefers numerical references, but TEAMAT's current author instructions explicitly require the Harvard author-year system. For **Paper 2 only**, journal compliance overrides the house style:

- compile with the IMA class in author-year (`namedate`) mode;
- use `\citet{...}` and `\citep{...}` through the class/natbib interface;
- use a BibTeX author-year bibliography style compatible with natbib;
- do not reintroduce IEEE-style numerical citations solely for aesthetics.

`cleveref` remains the standard for internal document cross-references.

## Scientific framing

Paper 2 is an observational measurement/interpretation paper, not an impact evaluation.

Primary exposure presentation:

- 0 visits;
- exactly 1 visit;
- exactly 2 visits;
- exactly 3 visits;
- 4 or more visits.

Do not pool 1 and 2 in the main presentation. The 1--2 pooling analysis may be reported only as a secondary parsimony/equivalence sensitivity.

The historical PPA three-visit requirement is not a Paper 2 estimand. Mention it at most briefly as institutional context explaining why exact 3 remains visible. Do not:

- draw a PPA threshold line in primary figures;
- call the design a discontinuity or encouragement design;
- imply that crossing three visits identifies a treatment effect;
- organize the abstract, introduction, or conclusion around PPA.

The contribution should be stated as:

1. aligning formal-support exposure to the same academic period as the focal mathematics course;
2. expressing performance relative to the classroom grading context;
3. transparently examining exact positive-use intensities rather than imposing a linear dose-response;
4. distinguishing a broad zero-versus-positive-use pattern from evidence for progressively larger associations among users.

The comparison with Jacob & Ní Fhloinn should be explicit: their TEAMAT study found a meaningful separation even between one visit and never attending and reported stronger increases at high attendance levels; Paper 2 asks whether the same qualitative dose interpretation persists under same-term exposure and classroom-relative outcomes in a different institutional setting.

## Baseline-preparation covariate

Do **not** use the available DMU diagnostic exam as a baseline covariate for Paper 2. Participation in that exam is incomplete/selective, and its coverage is not sufficiently uniform for the main observational comparison. Do not treat missing diagnostic participation as random and do not build a complete-case Paper 2 analysis around it.

A potentially useful future improvement is to request the **university entrance-exam score**, provided that the institution can supply a genuinely pre-enrolment measure with broad and comparable coverage across the Paper 2 cohorts. This should remain a TODO in the commented manuscript until the data are actually obtained and audited. Before using such a score, verify:

- that it precedes MU and CMAT exposure;
- coverage by cohort/period and visit group;
- whether exam versions/scales are comparable across admission cohorts;
- whether missingness is small enough that a sensitivity analysis is interpretable;
- whether the relevant quantitative/mathematics component can be isolated, if applicable.

If obtained, use the entrance-exam measure only as an observed-preparation sensitivity/control. It still would not eliminate unmeasured confounding or turn the paper into a causal tutoring-effect study.

## TEAMAT ethics requirement

TEAMAT requires a brief research-ethics statement in the Methods description. The commented manuscript must retain a TODO to insert the exact institutional wording concerning:

- use of administrative records;
- pseudonymization/de-identification;
- ethics committee / IRB approval, exemption, or institutional data-use authorization, whichever actually applies;
- authorizing body and reference/permit number when available.

**Never invent an approval status, body, or identifier.** The official manuscript should not contain a guessed statement; it remains incomplete for submission until the real institutional wording is supplied.

## Transferable implications

The Discussion should extract evaluation practices that another mathematics-support centre could reproduce:

- align visits to the focal course period;
- do not merge cumulative lifetime attendance onto a single course outcome;
- inspect whether raw grades are comparable across local grading contexts;
- separate non-use from positive formal help-seeking;
- inspect exact or flexible visit intensities before assuming a linear dose-response;
- distinguish observational association from tutoring efficacy.

## Figures

Primary figures should use exact visit categories and the shared `cmat_analysis.visualization` style. No PPA threshold annotation should appear in the primary visit-distribution figure. Publication figures remain vector PDFs during analysis; journal production requirements for accepted artwork can be handled at submission/acceptance stage.
