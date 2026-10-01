# Paper 2.1 results

The canonical Paper 2.1 aggregate outputs live under:

```text
results/paper21/
├── tables/
└── figures/
```

`tables/` contains publication-safe aggregate analysis outputs produced by the Paper 2.1 runners, while `figures/` contains vector PDFs generated from those tables. The dependency-aware interface in `paper/paper_build.py` is the preferred way to regenerate them.

The top-level `results/tables/`, `results/figures/`, `results/logs/` and `results/run_summary.json` are inherited Paper 2 artifacts from the parent branch; they are not inputs to the Paper 2.1 manuscript and should not be treated as canonical Paper 2.1 results.

Generated microdata or student-level analytical datasets must never be written here or committed.
