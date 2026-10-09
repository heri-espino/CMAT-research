# Paper 2.1 — frequency of mathematics support use

**Article scope:** adjusted final grades (Z), probability of passing (PASS) and **Holm-adjusted pairwise visit-frequency contrasts**. The contextual benchmark is zero visits versus any attendance, followed by the original `1/2/3/4/5/6+` positive-frequency grouping and an exploratory `0/1/2/3/4/5/6/7+` profile.

Start with `../notes/README.md` and `docs/README.md`. Source manuscript: `sections/01.tex`–`04.tex`; reference database: `references.bib`.

The official manuscript build outputs are a clean and commented TEAMAT draft. Figures included in the manuscript are:
- `../results/paper21/figures/fig03_04_pairwise_effect_dashboard.pdf` (adjusted Z and PASS risk differences).
- `../results/paper21/figures/fig05_pairwise_z_pvalue_dashboard.pdf` (raw/Holm).
- `../results/paper21/figures/fig06_pairwise_pass_pvalue_dashboard.pdf` (raw/Holm).

The source-level build excludes other analytical pipelines. With authorised institutional data available locally:

```powershell
conda activate cmat-research
cd cmat_analysis
python -m pip install -e .
cd ..
python paper/paper_build.py --check
python paper/paper_build.py --tables --figures --paper
```

If figure inputs already exist, `python paper/paper_build.py --paper` compiles without rerunning the full analysis. Build uses `paper/ima-authoring-template/`; do not check compiled PDFs or protected microdata into the branch. The manual GitHub Actions workflows can produce temporary paper/aggregate artifacts.

**Editorial status:** Holm-only working draft with existing documented numbers. Final numerical reconciliation, ethics/data-use statement, institutional context and journal-format audit remain.