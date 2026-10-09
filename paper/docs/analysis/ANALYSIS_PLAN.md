# Paper 2.1 — attendance-frequency analysis plan

The **original outcome-blind support audit** is recorded separately in `VISIT_GROUPING_DECISION.md`; the analysis text must preserve its chronology rather than rewriting the finer 7+ presentation as preregistered.

## Baseline and outcomes

Full first-eligible MU cohort (N=6,627). Benchmark 0 vs 1+ for two separate outcomes:
- continuous Z, final academic record converted through the canonical adverse-outcome assignment and then standardised inside instructor-period;
- binary PASS, numeric grade ≥7.5 vs numeric nonpassing or BA/BV/RT.

Both adjust for instructor-period fixed effects and degree; point differences are SD for Z and **percentage points** for PASS.

## Positive-frequency inference

Primary support-based groups `1/2/3/4/5/6+` among users (N=1,234): omnibus equal-level hypothesis and all 15 Wald pairs per outcome. Recompute standard errors clustered at the instructor-period, adjust pairwise p-values with **Holm** separately for each outcome/family, and report adjusted estimates and nominal intervals alongside corrected p-values.

The finer positive-grid `1/2/3/4/5/6/7+` is an exploratory sensitivity (21 pairs); the zero-inclusive `0/1/2/3/4/5/6/7+` reporting model has 28 pairs per outcome and a different sample. Explicitly separate all three families and never transfer significant pairs from one model to another.

## Robustness and interpretation

- Higher-tail overlap/count constraints; the cutoff is not driven by significance.
- Cluster at instructor as sensitivity to dependence across different periods.
- Numeric-only grade outcome as sensitivity to adverse-outcome imputation, acknowledging complete-case selection.
- No Holm-rejected pair implies evidence is insufficient to distinguish it at the chosen error rate, not that two frequencies are equivalent.
- Attendance is self-selected and is recorded during the period; a causal interpretation or visit-specific return is not identified.
- The PPA three-visit option is context, not an assigned intervention or exogenous cutoff.

Outputs: reproducible aggregate CSVs and only three adjusted effect/p-value PDFs in the publication. See `paper/README.md` and `notes/10_MATRIZ_DE_AFIRMACIONES.md`.