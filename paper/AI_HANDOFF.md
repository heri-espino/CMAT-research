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

Paper 2 is an observational study of mathematics-support attendance and academic performance, not a causal impact evaluation.

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

The contribution should be stated in the terminology normally used in the mathematics-support literature:

1. matching CMAT attendance to the same academic period as the mathematics course being analysed;
2. standardising final grades within instructor--period grading groups;
3. examining students with 0, 1, 2, 3, and 4+ recorded visits separately rather than assuming a linear relationship between number of visits and performance;
4. distinguishing the attendance--non-attendance difference from evidence of differences associated with attendance frequency among students who used CMAT.

The comparison with Jacob & Ní Fhloinn should be explicit: their TEAMAT study found that students who attended once should be distinguished from those who never attended and reported more favourable outcomes at higher levels of attendance. Paper 2 asks whether differences among attendance-frequency groups remain clear when visits are matched to the course period and grades are standardised within instructor--period groups in a different institutional setting.

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

## Terminology and disciplinary wording

Use wording that is standard in mathematics learning support (MLS) and TEAMAT rather than econometric shorthand.

Preferred manuscript vocabulary:

- **mathematics learning support / mathematics support** for the provision;
- **mathematics support centre** for CMAT when a generic English description is needed;
- **attendance**, **visits**, **number/frequency of visits**, and **attendance records** for the administrative measure;
- **students who attended**, **students with no recorded visits**, **users/non-users** where concise labels are needed;
- **engagement with mathematics support** when discussing the broader behavioural literature;
- **academic help-seeking** only when explicitly connecting the findings to the help-seeking literature;
- **prior mathematical attainment/background/preparation**;
- **academic performance**, **final grades**, and **standardised grade (Z)** after the metric has been defined;
- **self-selection bias**, **association/relationship**, and **observational analysis**.

Avoid manuscript prose such as **positive-use group**, **support contact**, **formal help-seeking contact**, **dose/dose-response/dose gradient**, **production-function measure**, **performance regime**, **measurement contamination**, **temporal exogeneity**, **exchangeable students**, **exposure overlap**, **identified from fewer classrooms**, **exact/folded groups**, **analytical cohort/population**, **outcome construction**, **treatment intensity**, and **provenance checks**. These may be meaningful technical shorthand in code or internal notes, but they are not the natural register of the target literature. Prefer **study sample**, **sensitivity analysis**, and direct descriptions of attendance and grades. Keep `classroom-relative` in code/variable documentation if needed, but in manuscript prose normally describe the outcome as a **standardised grade** once the Z-score has been defined; the grouping variable is instructor × academic period, not an observed section ID.

## Transferable implications

The Discussion should extract evaluation practices that another mathematics-support centre could reproduce:

- match attendance records to the academic period of the course outcome being analysed;
- do not assign attendance accumulated across unrelated periods to a single course grade;
- consider whether raw grades are comparable across local grading contexts;
- distinguish students who did not attend from students who attended at least once;
- examine attendance-frequency groups before assuming a linear relationship between number of visits and performance;
- distinguish an observational association from evidence of mathematics-support effectiveness.

## Figures

Primary figures should use exact visit categories and the shared `cmat_analysis.visualization` style. No PPA threshold annotation should appear in the primary visit-distribution figure. Publication figures remain vector PDFs during analysis; journal production requirements for accepted artwork can be handled at submission/acceptance stage.


## Second-pass wording guardrails

- Do not state without qualification that CMAT attendance is fully **voluntary**: during part of the study period attendance could also be influenced by the institutional three-visit requirement. Prefer **attendance was not randomly assigned** and describe both student choice and institutional incentives where relevant.
- Prefer **main analysis** to **primary specification** unless distinguishing formally defined estimands.
- Prefer **students who attended / students with no recorded visits** to abstract labels when space permits.
- Prefer **number/frequency of visits** to **intensity** in manuscript prose.
- Describe the non-numeric grade handling concretely: BV/RT/BA are treated as non-passes; the continuous outcome imputes below-pass values within instructor--period group and is checked against uniform-imputation and numeric-only sensitivities.
- Figure axes and captions should follow the same terminology as the manuscript; do not use `registrations`, `dose`, or `classroom-relative performance` in user-visible figure labels. Do not call the analytic instructor--period grouping an observed class/section unless section identifiers become available.


## Third-pass prose rules

- Write from the study rather than from the reviewer: avoid sentences such as `a new study needs to...`, `the reader should...`, or other meta-commentary about how the paper ought to be interpreted.
- State results concretely before summarising them. Prefer `each attendance group differed from students with no recorded visits, whereas the attendance-frequency groups did not differ from one another` to abstract phrases such as `the strongest inferential separation`.
- Keep the abstract intelligible to general TEAMAT readers and below the journal's 300-word limit; include the main sample, attendance definition, outcome, central result, and observational limitation without reproducing every diagnostic statistic.
- Make the educational rationale explicit: explain why the distinction between no attendance, a single visit, and repeated attendance matters for evaluation and interpretation of routine mathematics-support usage data.
- Avoid repeating the same attendance-versus-non-attendance conclusion in adjacent Results or Discussion paragraphs. Sensitivity results should add what changes under alternative outcome definitions, not restate the main result verbatim.
- Do not add generic limitations unless they are supported by an actual audit or by the data structure. For example, do not claim duplicate attendance records may exist unless duplication has been assessed.
- When comparing with prior studies, describe methodological or contextual differences without implying that one result invalidates another and without inventing mechanisms.
