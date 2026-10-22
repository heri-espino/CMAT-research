# Paper 2.1 — reproducible Wald/Holm analysis

Publication-specific runners:
- `run_paper21.py`: support and outcome-blind attendance grouping.
- `run_paper21_outcomes.py`: cohort, adjusted Z/PASS, omnibus and pairwise Wald contrasts with Holm.
- `figures_paper21.py`: the three Holm pairwise figure PDFs.

Only the first two are invoked for primary tables; do not add other statistical experiments to this paper build. Reusable functions belong to the `cmat_analysis` library on `main`.

```powershell
conda activate cmat-research
cd cmat_analysis
python -m pip install -e .
cd ..
python code/run_paper21.py --check
python code/run_paper21_outcomes.py --check
python paper/paper_build.py --check
```

With authorised local controlled inputs, `python paper/paper_build.py --tables --figures --paper` regenerates the publication output. Manuscript compilation alone uses existing figures if complete. No row-level records, keys or student IDs may be committed.

## Exploratory follow-ups (separate from Paper 2.1 publication build)

These scripts are research-only and **must not** be included in the manuscript/figure production workflow until explicitly reviewed:

- `run_paper21_shapley_importance.py`: complete-data grouped Shapley contributions for Z OLS, PASS LPM, PASS logit, and professor-period-held-out predictive skill. Results: `results/paper21/tables/shapley_importance/`; notes `19_SHAPLEY_PREDICTIVE_IMPORTANCE.md`.
- `run_paper21_followup_questions.py`: degree/professor-period overlap and within-mixed-context partial fit, first-vs-additional-visit piecewise regression for PASS and Z with cluster-robust SE, and numeric-grade quantiles around 7.5. Results after a successful authorized run: `results/paper21/tables/followup_questions/`; notes `22_FOLLOWUP_QUESTIONS_RESULTS.md`.

**Canonical navigation:** [three-study research tracker](../notes/20_RESEARCH_TRACKER.md) and [follow-up study protocol](../notes/21_FOLLOWUP_QUESTIONS_PROTOCOL.md). Historical Paper 2.1 EM/GMM results are linked from the tracker because they are preserved on a different branch.

```powershell
conda activate cmat-research
python -m pytest -q cmat_analysis/tests/test_paper21_followup_questions.py
python code/run_paper21_followup_questions.py --check
# Only after approved institutional inputs are available locally:
python code/run_paper21_followup_questions.py
```

Both runners export aggregate-only tables and must be executed where the authorized institutional workbooks are present. Do not commit original grade records, identity keys or any row-level extracts.
