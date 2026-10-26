# Versioned Paper 2 complete rerun scripts

This directory contains ported **Python source code** from all five long-lived
Paper 2 research branches. The integrations are modifications of the historical
scripts, not a preservation of their byte-identical source blobs:
- root calculation now resolves from
  `papers/paper2-beyond-first-attendance/analysis/runners/` to the repository;
- frozen cohort values in the newer Shapley/curves/controls scripts no longer
  prevent valid **updated-data** reruns;
- historical original 6+ and 7+ grouping, hypotheses and method comparisons
  are preserved for comparability;
- the Holm-only source points to the archived historic grouping specification;
- the PASS-logit export no longer marks unestimable clustered p-values as
  significant rejections.

## Source-to-runner provenance

| Runner in this folder | Origin branch | Source Git blob SHA |
|---|---|---|
| `run_paper21.py` | `paper/paper2.1-visit-frequency` | `662de83797d39b68913820c58dc936b48c8471f5` |
| `run_paper21_outcomes.py` | same | `f6b55d5130f2e1e2d8159907e3f3109ac485feff` |
| `figures_paper21.py` | same | historical figure source; see branch |
| `run_paper21_mixture.py` | `paper/paper2.2.2-distributional-heterogeneity` | `f2e099cd055855b9255815b6c01b87c30eb23fb8` |
| `run_paper21_shape_check.py` | `paper/paper2.2.1-fused-frequency` | `fdac89b62c5104bf6a3783074b1c4a059b74437b` |
| `run_paper221_fused.py` | same | `2f438a6f9cb282524f04c165713e6839cb3466a5` |
| `run_paper21_model_controls_experiment.py` | `research/paper21-shapley-predictive-importance` | `a428abe58a958976679162ded09e2dd9f642895d` |
| `run_paper21_zscore_controls_experiment.py` | same | `f1fbc25614e3451cd20af3baa8f153235cb52d5e` |
| `run_paper21_shapley_importance.py` | same | `3e645f5682454e6a2e679a50f005c97805455205` |
| `run_paper21_followup_questions.py` | same | `a35ac5288b8296be5bb6835e52e1007ec7961249` |
| `run_paper21_attendance_curves.py` | same | `c4333f0fee995b233684e32a12b63517706f6cc0` |

The primary new PPA model is implemented separately under
`../ppa-groups/`. **It fits only `0 | 1–3 | 4+`**, with one three-pair
Holm family for Z and one for PASS; the historic exact-count regression
is a distinct comparison.

## Full rerun procedure

**Do not invoke the individual runners manually in an arbitrary order.**
The canonical command is
`python papers/paper2-beyond-first-attendance/run_all.py --publish`
from the repository root on the canonical integration branch, using the
authorized configured input files (or explicitly specifying both paths).

Full dependencies are pinned in `cmat_analysis/pyproject.toml` for
Python 3.14. The official synthetic code/contract workflow is
`.github/workflows/paper2-reproduction-smoke.yml`.
A successful synthetic `--check` does **not** imply that data-dependent
institutional regressions, bootstrap experiments or fit uncertainty passed.

The consolidated `run_all.py` archives the current aggregate tables and
figures in `papers/paper2-beyond-first-attendance/results/experiments/`
and reports SHA-256 input and output fingerprints in
`results/provenance/latest_full_rerun.json`. Raw rows stay out of the
aggregate staging allowlist; publication requires manual review.

**Critical distinction:** rerunning experiments creates new estimates, but
does not silently rewrite old narrative claims, citations or every static Marp
figure. A new-data paper/deck should only be rebuilt after those corresponding
claims have been reconciled to the new aggregate source.
