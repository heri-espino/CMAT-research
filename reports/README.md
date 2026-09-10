# Reports

`reports/` is the CMAT project's **research-development and brainstorming layer** between reusable computation and publication manuscripts.

The production flow is:

```text
root/code
    reusable scientific functions
        ↓
reports/<report_id>/
    broad scientific synthesis + local build recipe
        ↓
papers/<paper_id>/
    selected publication argument
```

Reports should preserve more of the scientific record than a journal article normally can: null findings, sensitivity analyses, alternative specifications, methodological concerns, exploratory extensions and reasoning that may later feed one or several papers.

## Atomic report rule

A report should be operationally self-contained while **not** becoming a second scientific codebase.

Preferred layout when the components exist:

```text
reports/<report_id>/
├── README.md
├── code/             # thin product-local runner(s)
├── notes/            # brainstorming / interpretation / future analyses
├── tables/           # retained aggregate report tables
├── figures/          # retained aggregate report figures
├── provenance/       # report-specific historical/methodological records
├── build/            # disposable local generated workspace; ignored by Git
├── <report>.tex
└── <report>.pdf
```

The local `code/` directory may parse arguments, resolve paths and call root-code functions. **Reusable cohort logic, statistics, models, estimators, transformations and plotting functions remain in `../code/src/visitas_analysis/`.**

If a report needs a new scientific function, implement/test/index it in root `code/` first, then import it from the report runner.

## `methodology_report/`

This is the detailed current statistical/methodological review workspace. Its canonical runner is co-located with the report:

```bash
python reports/methodology_report/code/methodology_report.py --check
```

With controlled inputs it regenerates the methodology tables/figures by calling the reusable implementation in root `code/`.

See `methodology_report/README.md` for the exact build/provenance boundary.

## `research_compendium/`

This preserves the earlier cumulative research record, including exploratory extensions and the refined PPA1→Calculus chapter. It is broader than any paper and remains useful as brainstorming/scientific continuity, but it is not yet wired to its own atomic computational runner.

Do not create that runner by copying calculations into this directory; when it is added, it should import the relevant root-code functions just like the methodology report.

## Reports → papers

Papers are downstream selections, not replacements for the broad reports. A paper should be able to say, in effect, "these are the subset of validated report results needed for this manuscript."

If a final paper needs local copies of figures/tables for submission, retain them under that paper with provenance back to the source report/root code. Do not use the paper directory as the place where the result is first calculated.

## Naming

Report names describe scientific purpose. Git provides version history, so active paths should not use suffixes such as `v2`, `v5`, `v8`, `final` or dates. Historical version labels may remain inside provenance records when they identify a specific frozen state.
