# Paper 2 — Beyond First Attendance

**Status (2026-10-26): all five agent PRs have been integrated into this DEVELOPMENT branch; the consolidated manuscript and Marp source are here, and the complete original experiment runners are in `analysis/runners/`.** Empirical PPA estimates remain pending; the previously committed slide PDF is a provisional non-Marp preview, and no new integrated manuscript PDF has been validated or published as final. The historical paper and its PDF remain intact. Read the [administrator audit](docs/ADMIN_INTEGRATION_STATUS.md) and the current `run_all.py` documentation before presenting updated data as validated.

## Publication entry points

- **Current readable historical PDF:** [Paper 2.1 working PDF](https://github.com/heri-espino/CMAT-research/blob/1546c594bfb6867ad52064594469061ec7fd7fc6/paper/paper.pdf), preserved on the original branch (native Git blob, 301,630 bytes). This remains the published/viewable working draft until a new PDF has been built and scientifically approved.
- **Historical editable manuscript:** [Paper 2.1 TeX sources](https://github.com/heri-espino/CMAT-research/tree/1546c594bfb6867ad52064594469061ec7fd7fc6/paper/sections) and [references](https://github.com/heri-espino/CMAT-research/blob/1546c594bfb6867ad52064594469061ec7fd7fc6/paper/references.bib).
- **Integrated manuscript:** `manuscript/` (awaiting manuscript agent; **no** `paper.pdf` is present in this namespace).
- **Marp presentation:** `presentation/marp/` (awaiting presentation agent; **no** compiled deck is present).
- **Provenance and decisions:** [migration map](docs/migration-map.md), [full source register](docs/source-register.md), [decision log](docs/migration-decisions.md), [agent handoff](docs/agent-handoff.md).

## Architecture

```text
papers/paper2-beyond-first-attendance/
  README.md
  manuscript/              # integrated English TeX, bibliography, approved PDF (future)
  analysis/
    holm/                   # historical Wald/Holm anchor
    ppa-groups/             # prospective explicit coarse-group study (post hoc)
    first-visit-curves/     # two-part/functional-shape exploratory sensitivities
    fused/                  # ordered fusion: experimental evidence
    mixture/                # inherited historical GMM; new modality validation pending
    shapley/                # predictive-skill attribution, not causality
  results/
    tables/                 # approved publication-safe aggregate exports (future)
    figures/                # approved figures (future)
    provenance/             # manifests, source checks, disclosure review
  supplement/              # technical details; not assembled yet
  presentation/marp/        # Marp source, referenced figures and built PDF (future)
  docs/                     # source ledger, method conflicts, handoff
```

The inventory [TSV](docs/source-register.tsv) maps **every one of 1,086 source-branch file differences against the creation-time main commit** among the five frozen source branches; unchanged shared-main files are intentionally not recatalogued. Historical assets remain at SHA-pinned URLs, with one 441-byte JSON grouping specification selectively reused by identical Git blob. No entire branch trees or historical output collections were copied.

## Scientific contract

Study subject: first eligible Matemáticas Universitarias (MU) attempts, recorded CMAT attendance during the same academic period, and distinct performance outcomes. **6,627 attempts, 190 instructor-period groups, 1,234 attendees** are the historical cohort numbers—not a freshly revalidated pooled estimate. This is observational; visits are not randomly assigned, PPA1 eligibility/credit is not observed, and ordered association is not causal dose response.

Use original 15/21/28-pair Holm families as labeled. The **only requested new PPA-threshold grouping** is `0 | 1–3 | 4+` (historical counts: 5,393 / 932 / 302). It is exploratory and not interchangeable with historical Holm comparisons. The previously suggested `0 | 1–3 | 4 | 5+` is **not** a required analysis. BA/BV/RT must remain distinguishable from numeric marks and numeric-only complete cases.

See the [consolidation charter](https://github.com/heri-espino/CMAT-research/blob/d6b1670553e9a838339c4c0bebb397667ba3a392/docs/PAPER2_CONSOLIDATION_PLAN.md) before creating downstream branches. Agents branch from `paper/paper2-beyond-first-attendance` and send PRs **to this branch**, not directly to `main`. Upstream shared `cmat_analysis/`, workflows, root README and branch-retirement decisions remain admin-controlled.


## Single command: re-run ALL executable experiments and push the aggregates

This branch contains source-controlled runners for Paper 2.1 group support and
Wald/Holm, numeric failure and EM/GMM/skew-normal shape, controlled PASS and Z
model sensitivity, grouped Shapley, first/additional attendance regression,
five attendance curves, fused lasso with **100 bootstrap fits**, the requested
**only** PPA grouping `0 | 1–3 | 4+`, and four refreshed manuscript
Wald/Holm figures. Every stage runs in dependency order; **no failure is skipped**.

**Windows single-command launcher** (the default executes *all stages* and
asks before committing/pushing approved aggregates):

```powershell
.\papers\paper2-beyond-first-attendance\run_everything.ps1
```

For updated workbooks outside the canonical configured folders:

```powershell
.\papers\paper2-beyond-first-attendance\run_everything.ps1 -Materias "C:\path\to\Materias.xlsx" -Asesorias "C:\path\to\Asesorias.xlsx"
```

The launcher installs the pinned scientific package first, then invokes
`run_all.py --publish`. Use `-CheckOnly` for data-free contracts, or
`-NoPublish` for a full local-only experiment run.

With Python 3.14 in the existing `cmat-research` Conda environment:

```powershell
git switch paper/paper2-beyond-first-attendance
python -m pip install -e "./cmat_analysis[dev]"
python .\papers\paper2-beyond-first-attendance\run_all.py --check
python .\papers\paper2-beyond-first-attendance\run_all.py --publish
```

By default the runner uses the paths returned by the canonical
`cmat_analysis.config.study_config.get_study_config`, preferring local
`data/raw/` workbooks and then the configured `data/controlled/` CSVs.
**Make sure these are the NEW intended data.** For datasets outside this
checkout, replace the last line with:

```powershell
python .\papers\paper2-beyond-first-attendance\run_all.py --materias "C:\path\to\updated\Materias.xlsx" --asesorias "C:\path\to\updated\Asesorias.xlsx" --publish
```

At the publication prompt, review the staged aggregate-only files and type
`PUBLISH`. No raw spreadsheets, person-level student CSVs or pseudonymization
secrets are staged. The script aborts rather than silently skipping failures,
checks required model outputs, records source-file SHA-256 fingerprints and
aggregate output SHA-256 hashes, archives full outputs under
`results/experiments/`, and pushes only the known research results to this
same branch. Detailed execution logs remain **local only**.

**Updated cohorts:** the default PPA runner accepts changed N, contexts and
visit-group sizes and records them in its manifest. Add
`--require-historical-cohort` to reproduce the frozen historical
6,627-student sample intentionally. The other historical methods retain their
fixed visit-bin definitions and may require scientific re-specification if new
cohorts contain unsupported sparse groups; the pipeline will stop on an error
rather than manufacture estimates.

**Paper and slides are not auto-rewritten.** The historical LaTeX narrative,
numbered claims and most Marp SVGs refer to previously audited cohort
results. The new runner refreshes the four mathematical-paper figure PDFs
and archives current aggregates, but cannot scientifically replace every
paragraph/slide figure automatically. Once numerical text and slides have
been reviewed against the updated aggregate output and claims matrix, opt
into a current-source build by adding `--build-publications`, which
requires installed `latexmk` and Node.js/`npx` Marp CLI. Do not call
the previous PDF/deck a new-cohort publication without this step.

For provenance of each ported runner, original branches and commits, see
`analysis/runners/README.md` and `docs/source-register.tsv`. The GitHub
Actions [synthetic reproduction smoke workflow](https://github.com/heri-espino/CMAT-research/actions/workflows/paper2-reproduction-smoke.yml)
needs **no institutional records**, and is manual after the initial CI run.

### Data publication governance

The user has stated they accept the public pseudonymized dataset. However,
the repository's existing `docs/DATA_PRIVACY.md` describes its precise,
linkable student-level datasets as restricted to an authorized private
repository. That scientific/organizational disclosure decision requires
documented permission from the institutional data custodian; this
reproduction workflow does not copy or newly upload any such records.
