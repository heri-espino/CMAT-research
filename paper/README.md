# Paper 2.1 — frequency of mathematics support use

**Article scope:** adjusted final grades (Z), probability of passing (PASS) and **Holm-adjusted pairwise visit-frequency contrasts**. The contextual benchmark is zero visits versus any attendance, followed by the original `1/2/3/4/5/6+` positive-frequency grouping and an exploratory `0/1/2/3/4/5/6/7+` profile.

Start with `../notes/README.md` and `docs/README.md`. Source manuscript: `sections/01.tex`–`04.tex`; reference database: `references.bib`.

The pairwise figures now show the **upper triangle only** with descriptive separators after **0, 3 and 6** visits, representing `0 | 1–3 (PPA1 completion) | 4–6 | 7+`. PPA1 is a first-semester social/cultural integration programme. Three CMAT visits are one optional qualifying activity available throughout all eleven periods; the fourth exceeds this particular requirement. Individual eligibility and credit are not observed. The complete 28-pair Holm families are retained.

The descriptive attendance table in the opening Results section has been replaced with `fig01_cohort_outcome_attendance.pdf`. This three-panel figure reports PASS (blue), observed numeric failure with grade strictly below 7.5 (orange), and administrative non-numeric outcomes BV/RT/BA (gold) as shares of each frequency (left), stacked group-specific histograms (PASS, numeric failure, BV/RT/BA) of the imputed instructor-period Z outcome (centre, pre-aggregated range -2 to 2 only), and attendance counts on an explicitly labelled log scale (right). All eight attendance groups and the PPA1 at-three-visits interpretation remain visible; the figure is descriptive and does not change the Wald/Holm tests.

The middle Z histogram now overlays each full visit-group's **descriptive mean with its unadjusted 95% confidence interval** and a **conservative binned-median location range** (approximate centre marker, not a median CI). All eight full-group **SDs** and mean/median approximations are printed in the figure; the corresponding values and data limitations are documented in `../notes/13_DESCRIPTIVE_Z_HISTOGRAM_STATS.md`. Mean/SD/CI use all Z outcomes, whereas the histogram only shows bins from -2 to 2; no newly fitted models are involved.

The official manuscript build outputs are a clean and commented TEAMAT draft. Figures included in the manuscript are:
- `../results/paper21/figures/fig01_cohort_outcome_attendance.pdf` (three-panel cohort overview from aggregate histograms and percentages).
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
**New contextual hypothesis (2026-10-12):** An exploratory previously estimated non-PASS comparison shows more administrative versus numeric outcomes among attending students conditional on not passing. This does not reveal motives, scholarship ownership or a mechanism of academic grade protection. Read `../notes/12_NONPASS_SCHOLARSHIP_PPA_HYPOTHESES.md` for source provenance and the two proposed follow-up studies (scholarship/withdrawal rules; causal evaluation of PPA1 incentives). The main Holm contrasts remain unchanged.
