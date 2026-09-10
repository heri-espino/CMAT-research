# CMAT publication portfolio

Canonical **cross-paper** planning document for the five-paper CMAT research programme.

This file owns portfolio-level information: stable IDs, working titles, priority/order, broad paper boundaries and journal routes. Detailed research questions, estimands, populations, interpretation rules and current manuscript status belong in each `papers/<paper_id>/README.md`.

Last journal-fit review: 2026-09-07. Journal targets are strategic, not commitments; re-check current scope, manuscript type, data policies and fees before submission.

## Portfolio rules

1. Reusable scientific computation lives in root `code/`; papers do not maintain independent estimators or cohort definitions.
2. Broad empirical development, sensitivities and methodological reasoning should be preserved in `reports/` before publication-specific selection.
3. Papers select validated evidence from one or more source reports and root-code outputs; they are downstream publication products rather than parallel analysis projects.
4. Each paper has one canonical home under `papers/<paper_id>/`.
5. Paper-specific literature lives under `papers/<paper_id>/literature/`; physical source records remain shared under `literature/library/`.
6. If manuscript work exposes a methodological problem, fix/validate it in root `code/`, regenerate the relevant report outputs, and only then revise manuscript numbers.
7. Changes to detailed paper scope/status belong in that paper README; update this file only when the portfolio-level boundary, title, priority or journal route changes.

## Portfolio overview

| Priority | Paper ID | Working title | Portfolio boundary | Current journal route |
|---:|---|---|---|---|
| 1 | `paper1_ppa_persistence` | *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive* | Later CMAT use/persistence across the change from the incentive-linked first-year MU/PPA1 context to later Calculus; observational, not causal PPA identification. | *Studies in Higher Education* ambitious primary; IJMEST; TEAMAT; *Journal of Further and Higher Education*. |
| 2 | `paper2_mu_performance` | *Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics* | Contemporaneous first-MU support use and classroom-relative performance; distinguishes any-use/non-use from intensity among users. | TEAMAT primary; IJMEST second; IJRUME ambitious. |
| 3 | `paper3_grading_heterogeneity` | *When the Same Grade Does Not Mean the Same Performance: Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment* | Measurement/assessment comparability across instructor × course × period; requires dedicated inferential re-analysis before drafting. | *Assessment & Evaluation in Higher Education* primary; *Studies in Educational Evaluation* second; IJRUME ambitious. |
| 4 | `paper4_degree_help_seeking` | *Who Keeps Seeking Mathematics Help? Disciplinary Heterogeneity in University Mathematics Support Use* | Degree-programme heterogeneity in support use/persistence; programme-level results remain ecological and official `CLAVECARRERA` is primary. | IJMEST primary; *Journal of Further and Higher Education* second; HERD ambitious. |
| 5 | `paper5_longitudinal_trajectories` | *Longitudinal Trajectories of Mathematics Support Use Across the Undergraduate Degree* | Future full-degree repeated-use/transition trajectories beyond the MU→Calculus pair; requires coverage/missingness/revalidation audit first. | Not frozen: TEAMAT/IJMEST for substantive MSS; *Journal of Learning Analytics* for genuine sequence/state contribution; *International Journal of STEM Education* ambitious broader route. |

## Key boundary checks

### Paper 1 vs Paper 2

Paper 1 is longitudinal and centers **later support persistence after a change in incentive context**. Paper 2 is contemporaneous and centers **first-MU support use versus classroom-relative MU performance**. Do not let Paper 1 become a generic tutoring-performance paper or let Paper 2 inherit causal incentive claims.

Current population distinction to protect:

- Paper 2 primary first-MU cohort: `N=6,627` in the documented methodology state;
- Paper 1 broad linked MU→Calculus cohort: `N=4,211` in that state;
- Paper 1 stricter historical next-regular-term longitudinal/PPA cohort: `N=3,241`, later work that must remain explicitly distinguished until fully reintegrated.

### Paper 3 vs Paper 2

Paper 2 **uses** classroom-relative standardisation as an outcome strategy. Paper 3 studies the **grading/assessment heterogeneity itself** as the substantive object. Do not collapse Paper 3 into a methodological appendix for Paper 2.

### Paper 4 vs Papers 1–2

Paper 4's central contribution is disciplinary/programme heterogeneity. Programme-level patterns are ecological; they should not be used to infer individual help-seeking mechanisms.

### Paper 5 vs Paper 1

Paper 1 is a focused two-context persistence design. Paper 5 is reserved for full-degree repeated states/trajectories and should not start as a manuscript until longitudinal coverage and data-quality requirements are audited.

## Canonical paper homes

- `../papers/paper1_ppa_persistence/`
- `../papers/paper2_mu_performance/`
- `../papers/paper3_grading_heterogeneity/`
- `../papers/paper4_degree_help_seeking/`
- `../papers/paper5_longitudinal_trajectories/`

For detailed scope, read the corresponding `README.md`. For literature, read its `literature/` subdirectory.

## Shared production infrastructure

```text
code/src/visitas_analysis/      reusable scientific/computational functions
reports/<report_id>/code/       thin product-local runners importing root code
reports/<report_id>/            broad empirical/methodological workspace
papers/<paper_id>/              publication-specific final selection
analysis/shared/                optional cross-report aggregate archive
literature/library/             one physical source record per scholarly version
```

Do not create permanent paper-specific scientific pipelines or duplicate source PDFs.

The current canonical report-runner example is:

```bash
python reports/methodology_report/code/methodology_report.py --check
```

## Journal-fit maintenance

The journal-fit review dated 2026-09-07 informed the routes above. Before actual submission, verify the current official journal website rather than treating the historical review as permanent policy.

When a route changes:

1. update this portfolio if it changes cross-paper strategy;
2. update the relevant `papers/<paper_id>/README.md` with detailed rationale/status;
3. do not copy the change into unrelated handoffs.
