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