# Paper 2.2.1 — Research notes and interpretation log

Use `notes/` as the **dated, version-controlled working memory** of this paper. It records design discussions, execution attempts, unexpected patterns, interpretation updates, rejected explanations, robustness decisions, and what should migrate into the final manuscript.

## Ground rules

- Create `notes/YYYY-MM-DD_<topic>.md` for each meaningful milestone or changed interpretation.
- Prefix content with **Observed**, **Derived**, **Hypothesis**, **Limitation**, **Decision** or **To verify**; never blend unexecuted expectations with findings.
- Every empirical note must link the Git SHA, workflow run/artifact ID, input contract, outcome/grouping, analysis flags, sample size and clusters, aggregate table/figure paths, uncertainties, limitations and next action.
- Do not overwrite earlier interpretations silently. Append a superseding dated note or link a replacement; retain change history.
- Any interpretation in the final paper must be traceable back to a verified results table or a cited source.
- Keep exploratory decisions distinct from pre-outcome Paper 2.1 design contracts.
- No student IDs, microdata, confidential spreadsheets, small identifying cells or secrets in notes.
- Empty result placeholders are not findings.

## Index

- [2026-10-07 — implementation handoff and first experiment contract](2026-10-07_initial-implementation.md)
- [2026-10-07 — bootstrap metadata failure and fix](2026-10-07_bootstrap_metadata_fix.md)
- [2026-10-07 — successful 100-bootstrap run and outcome interpretation](2026-10-07_fused_lasso_100_bootstrap_results.md)
- [Scientific decision register](DECISIONS.md)
- [Results-reading template](RESULT_NOTE_TEMPLATE.md)

## Next notes expected

Completed: first full local institutional run, discovered blocks for Z and PASS, 100-replicate boundary stability, reserved-cluster Z Wald test, pooled-6+ sensitivity and manuscript results update. Next: repeated grouped CV and minimum-loss lambda sensitivity for PASS; numeric-complete-case Z; instructor-level sensitivity; editorial review and independent-cohort validation.