# Paper 2.2.1 — Scientific context and research questions

## Where we come from

Paper 2 compared no recorded CMAT use with any use in the first eligible MU attempt. Paper 2.1 exposed an ordinal visit count (current reporting grid `0/1/2/3/4/5/6/7+`) and fitted instructor-period FE models with degree adjustment, cluster-robust uncertainty, pairwise comparisons and Holm. Its dominant pattern was the observed association between 0 and positive attendance, whereas differentiation within positive frequencies was weaker and less monotone. These historical observations **motivate** the new study but do not determine its outcome. The pre-outcome Paper 2.1 audit judged pooled 6+ better supported than separating exact 6 and 7+; preserve this chronology.

CMAT is observational; students self-select into visits. Three visits also have contextual significance for an institutional PPA attendance credit in at least part of the study period. The data do not measure the treatment effect of an additional visit.

## Main scientific question

Can the association between recorded visit frequency and final performance be represented by a small, stable collection of **adjacent frequency regimes**, with explicit uncertainty rather than exploratory p-value-driven bins?

Secondary questions:
- Is the major break between 0 and 1, or is there a reproducible additional break in repeated use?
- Are any proposed boundaries (e.g. 4|5, 6|7+) robust to cluster resampling, tail pooling, training splits and tuning?
- Do `Z_GRADE_PRIMARY` and PASS yield compatible or different regimes? Differences are expected because grade levels and pass threshold capture distinct dimensions.
- How much predictive/within-context information is lost when 8 coefficients are replaced by 2–4 fused blocks?
- Can detected boundaries survive independent cluster-level validation without post-selection significance inflation?
- Can sparse overlap, degree composition, or administrative-outcome imputation explain apparent boundaries?

## Target population and outcomes

Retain canonical first eligible MU attempt, period-wide CMAT count, `CLASSROOM_ID` instructor × period, `CLAVECARRERA` degree; preserve the exact eligibility/exclusion and anonymisation contracts of Paper 2.1. Main outcomes: `PASS=1` for numeric final grade >=7.5, 0 for numeric <7.5 or BA/BV/RT; `Z_GRADE_PRIMARY` for the canonical adverse-outcome-imputed instructor-period-standardised final grade. Numeric complete-case standardised Z is a sensitivity, not a replacement of primary binary/continuous definitions.

## Interpretive limits

A selected boundary is an association pattern, not a causal threshold, individual propensity class, independent proof of equivalence within merged bins, or a policy cut-off. Failure to reject adjacent differences is not evidence of equal effects. No final number of regimes has been determined. The 2/3 PPA boundary must be reported even if fused away, without treating it as a causal regression discontinuity.

## Publication framing

Working title: *Detecting stable attendance regimes in university mathematics support: ordered fusion and clustered validation*. Determine journal and standalone-paper merit only after adding a targeted literature review on ordered categorical effects, fused lasso/total variation, stability selection, clustered post-selection inference and mathematics-support attendance.