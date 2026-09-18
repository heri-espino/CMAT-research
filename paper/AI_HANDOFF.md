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


## Fourth-pass microstyle rules

- Use British English consistently: **analysed, standardised, programme, centre, modelling, pass mark**.
- Prefer **students who attended / students with no recorded visits** to shorthand such as `attendees/non-attendees` in manuscript prose.
- Prefer **non-passing outcome**, **grade below the pass mark**, and **uniform imputation below the pass mark** to `non-pass`, `failing grade`, or `below-pass imputation` when writing for readers.
- Write regression specifications compactly as **instructor--period fixed effects**, **degree-programme indicators**, and **standard errors clustered at the instructor--period level**.
- Report extreme p-values at an informative precision (for example, `p < 0.001`) unless an exact value changes interpretation. Retain exact adjusted p-values when they matter, such as the one-versus-four-or-more comparison after Holm correction.
- Avoid reviewer-directed wording such as `should not be read as evidence`; state the empirical result directly instead.
- Avoid unnecessary connectors (`therefore`, `thus`, `consequently`) when the logical relation is already clear from the sentence sequence.
- Keep terminology stable across text and figures: **attendance group** for the 0/1/2/3/4+ grouping; **attendance frequency** when discussing how often students attended; **standardised grade** for Z after its definition.


## Fifth-pass prose rules

- Keep Methods and Results predominantly in the past tense; reserve present tense for definitions, general claims, and interpretation.
- Develop `Matemáticas Universitarias (MU)` at first manuscript use before relying on the abbreviation.
- Prefer direct descriptions of students and visits to abstractions such as `attendance--non-attendance difference` when space permits.
- Treat **usage data** as attendance information: they record whether/how often students attended, not what happened during a visit or how useful it was.
- Avoid long speculative lists of reasons for repeated attendance; it is enough to note that repeated attendance may reflect both continuing need and continued engagement.
- Avoid repeating the causal disclaimer in every subsection. State the observational interpretation clearly in the abstract/Introduction/Methods and let Results report the comparisons directly.
- In comparisons with prior studies, identify differences in setting, attendance grouping, or outcome definition rather than speculating about unobserved mechanisms.
- Keep the conclusion concrete: visit counts represent **attendance frequency**, not the amount of support received.


## Corpus-grounded construct rules

- Treat CMAT visit counts as **usage data / attendance records**, not as a direct measure of a student's academic help-seeking tendency. Fong et al. distinguish formal help sources (including academic support centres) from behavioural indicators such as tutoring-attendance frequency; the latter do not directly measure help-seeking dispositions.
- Use Lawson et al.'s meaning of **usage data** narrowly: who uses mathematics support, when, and how often. Usage records do not by themselves establish motivation for attendance, what occurred during a visit, the quality of the student experience, or the success of the support.
- Because the institutional three-visit requirement affected part of the study period, avoid treating every recorded visit as voluntary or intrinsically motivated engagement.
- CMAT operates as a dedicated mathematics-support room with tables and whiteboards, staffed by mathematics professors from 08:00 to 17:50 Monday to Friday. Students are informed about the service by their mathematics professors, may seek assistance from a professor other than their course instructor, and register attendance on entry. Preserve these details when describing the institutional setting, but do not infer visit duration, visit content, or which staff member assisted a student from the attendance records.
- The official meanings of the non-numeric administrative codes are: BV = baja voluntaria (voluntary withdrawal), RT = retiro temporal (temporary withdrawal), and BA = baja académica (academic withdrawal). In the analysis all three are adverse/non-passing outcomes; retain the Spanish institutional label alongside an English gloss when first introduced.
- When reporting null comparisons among attendance-frequency groups, say that the relevant pairwise contrasts were not statistically significant after the stated multiplicity adjustment; do not translate this into evidence that the groups were equal or equivalent unless an equivalence design is actually reported.

## Scientific-referee priorities

The next review layer is scientific rather than stylistic. Preserve these priorities:

- **Inferential hierarchy:** descriptive means are useful, but the primary inferential comparisons are the instructor--period fixed-effect models with cluster-robust standard errors and Holm adjustment. Welch/Games--Howell is secondary because it does not model instructor--period dependence.
- **Withdrawal opportunity window:** BV/RT/BA cases may leave before the end of the term, and exact withdrawal dates are unavailable. They may therefore have less opportunity to accumulate visits. Numeric complete cases remove these outcomes but condition on completion; neither approach fully solves the timing problem.
- **Exposure definition is intentionally period-wide:** count all CMAT visits during the MU academic period, irrespective of the subject label attached to a visit. CMAT is a shared mathematics-support room and students may consult professors other than their MU instructor, so do not narrow the Paper 2 estimand to MU-tagged visits.
- **Outcome robustness:** regenerate adjusted exact-group results for numeric complete cases and for the binary PASS outcome. PASS requires no latent numeric grade for BV/RT/BA and is therefore an important check on the continuous-outcome construction.
- **Period stability:** attendance rates vary substantially across the 11 observed periods. The recipe now produces leave-one-period-out FE estimates so the aggregate result can be checked for dependence on a particular term.
- **Dependence across periods:** many MU instructors recur across academic periods. Before submission, compare the current instructor--period clustered standard errors with an instructor-level clustering sensitivity.
- **Grading context is substantive, not cosmetic:** preserve standardisation within the existing instructor × academic-period grouping. MU instructors set and grade their own assessments, so exam difficulty and grading practices differ across these groups; the Z-score is intended to compare students relative to the grading environment in which their MU grade was produced, not to create a university-wide raw-grade scale.
- **Baseline confounding:** do not treat propensity-score methods as a substitute for missing prior attainment. With the current covariates they can balance only observed baseline variables; the entrance-exam score, if obtained and audited, would be a materially stronger sensitivity.

## Fifth-pass literature alignment

- Prefer wording already established in the mathematics-support literature where it fits the data. In particular, **usage data** can refer to who uses mathematics support, when, and how often; do not imply that visit counts measure the quality or success of support.
- Keep literature claims at the level actually supported by the cited source. Do not add detailed lists of possible self-selection mechanisms unless the cited literature supports them directly.
- Once the instructor--period grouping has been defined precisely, avoid repeating the full term in every sentence; use **group** where the referent is unambiguous and **instructor--period level** for fixed effects or clustering.
- Present the 0/1/2/3/4+ attendance categories in prose rather than as a displayed equation. They are descriptive categories, not a mathematical estimand requiring display notation.
- Research questions should be concrete and map directly onto the reported comparisons. For the second question, name the one-, two-, three-, and four-or-more-visit groups rather than asking abstractly whether performance `varies with intensity`.
- Avoid unexplained institution-specific English. If equivalency/revalidation records must be mentioned, make clear that they are administrative records that do not represent observed course attempts; do not invent expanded meanings for the underlying institutional codes.
- Prefer direct statements of what sensitivity analyses preserve or change rather than abstract phrases such as `robust pattern` or `inferential separation`.
