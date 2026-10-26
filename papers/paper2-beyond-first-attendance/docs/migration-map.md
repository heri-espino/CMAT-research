# Paper 2 migration map (architecture stage)

**Rule:** keep the original file at its immutable source URL, log its SHA and intended canonical namespace, and import only a small compatible, non-sensitive artifact after review. The full path-by-path mapping, including exclusions and upstream-review candidates, is [source-register.tsv](source-register.tsv). Paths listed below are mappings and ownership decisions, **not a claim of physical copies**.

| Frozen branch / historical path family | Intended namespace | Disposition |
|---|---|---|
| `paper/paper2-mu-performance:code/run_paper.py`, `code/figures.py`; `results/{tables,figures}` | `analysis/mu-baseline/`, `results/{tables,figures}/mu-baseline/` | SHA-pin; historical 0/1/2/3/4+ model not silently adopted |
| `paper/paper2-mu-performance:paper/{sections,main.tex,references.bib}` | `manuscript/historical/mu/` | reference; do not promote whole manuscript |
| `paper/paper2.1-visit-frequency:code/run_paper21{,_outcomes}.py`, `code/figures_paper21.py` | `analysis/holm/` | reference; preserve original Holm family definitions and comparison support |
| `paper/paper2.1-visit-frequency:paper/paper.pdf`, `paper/{sections,references.bib,velvetblue.sty}` | `manuscript/` | source/reference only; historical published working PDF remains on original branch |
| `paper/paper2.1-visit-frequency:paper/visit_grouping_spec.json` | `analysis/holm/historical_visit_grouping_spec.json` | **only frozen blob copied**, original SHA unchanged; not an integrated new grouping |
| `paper/paper2.1-visit-frequency:results/paper21/{tables,figures}` | `results/{tables,figures}/holm/` | reference aggregate families; do not mass-duplicate |
| `paper/paper2.2.1-fused-frequency:code/run_paper221_fused.py`, `code/figures_paper221.py` | `analysis/fused/` | reference; inspect caller imports, source SHA and run contract before rehoming |
| `paper/paper2.2.1-fused-frequency:results/paper221/{tables,figures,run_manifest.json}`, `notes/2026-10-07_*.md` | `results/{tables,figures,provenance}/fused/`, `docs/historical/fused/` | immutable reference; 100-fit experiment done, prospective additional robustness pending |
| `paper/paper2.2.2-distributional-heterogeneity:paper/docs/analysis/*222*.md`, `paper/docs/results/*222*.md` | `analysis/mixture/`, `docs/historical/mixture/` | reference design notes; novel tests pending |
| `paper/paper2.2.2-distributional-heterogeneity:code/run_paper21_mixture.py`, `paper/docs/results/MIXTURE_ANALYSIS_RESULTS.md`, GMM/skewnormal CSVs | `analysis/mixture/`, `results/tables/mixture/` | **inherited Paper 2.1** evidence, not 2.2.2 modality output |
| `research/paper21-shapley-predictive-importance:code/run_paper21_shapley_importance.py`, `results/paper21/tables/shapley_importance/*` | `analysis/shapley/`, `results/tables/shapley/` | reference completed exploratory output |
| `research/paper21-shapley-predictive-importance:code/run_paper21_{followup_questions,attendance_curves}.py`, `results/paper21/tables/{followup_questions,attendance_curves}/*`, `results/paper21/figures/attendance_curves/*` | `analysis/first-visit-curves/`, `results/{tables,figures}/first-visit-curves/` | reference verified follow-up and curve output; no scientific promotion |
| All source `cmat_analysis/**` differing from `main`; branch-specific synthetic tests | future `main/cmat_analysis/` minimal PR | **upstream-review only**; no shared-library changes |
| Historical `literature_selected/`, `submission/`, protocol `notes/`, older manuscripts | `docs/historical/`, `supplement/` candidate sections | reference; bibliography/reuse and rights require separate review |
| Branch `.github/**` and root policy, `tmp/**` | admin-maintained repo root; **no temp migration** | do not merge workflows; temp output excluded with source trace in TSV |

## Actual files created in this migration

Documentation, README placeholders and one 441-byte `analysis/holm/historical_visit_grouping_spec.json` frozen from Paper 2.1; no figure, data table, executable analysis, legacy manuscript, PDF or slide deck has been copied. Git directories are established through tracked `README.md` markers rather than empty Git directories.

## Conflict rules and publication gates

1. `0 | 1–3 | 4 | 4+` is **overlapping**: 4 belongs to two groups. The **only requested** PPA grouping is `0 | 1–3 | 4+` (historical Ns 5,393 / 932 / 302), exploratory. The former `0 | 1–3 | 4 | 5+` assistant proposal is **not** required.
2. Avoid comparing tables from incompatible `Z_GRADE_PRIMARY`, `Z_GRADE_COMPLETE_CASE`, raw numeric grade, PASS, or BA/BV/RT handling as though they shared one estimand.
3. `1/2/3/4/5/6+` support-based and exploratory `0/1/2/3/4/5/6/7+` fine-tail groupings answer different inferential questions; maintain separate 15-, 21-, 28-pair Holm scopes. New contrasts need new transparent families.
4. Fused-lasso partitions and Shapley predictive contributions are model-selection/fit descriptions, **not** repetitions of fixed-effect Wald tests. A K=2 GMM is neither evidence of two density modes nor two latent populations.
5. Publish a replacement top-level PDF link **only after** a real reviewed PDF is generated, bytes validated (not Git LFS pointer), and GitHub link tested. The existing Paper 2.1 PDF and all original branches remain untouched.
