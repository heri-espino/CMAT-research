# Reports

`reports/` is the CMAT project's **research-development, experimentation, diagnostic and brainstorming layer** between reusable computation and publication manuscripts.

Before substantive work here, read `AI_HANDOFF.md`. The complete project-wide production method is in `../docs/RESEARCH_WORKFLOW.md`.

The production flow is:

```text
root/code
    reusable scientific functions
        ↓
reports/<report_id>/
    experiments + diagnostics + robustness + broad scientific synthesis
        ↓
papers/<paper_id>/
    selected publication argument
```

A useful analogy is that root `code/` behaves like an internal scientific package: reports **use** that package to ask questions, just as an analysis script might use scikit-learn, while papers consume the validated evidence that survives the broader report-level investigation.

Reports should preserve more of the scientific record than a journal article normally can: null findings, sensitivity analyses, alternative specifications, methodological concerns, exploratory extensions, diagnostic failures, assumptions, unresolved questions and reasoning that may later feed one or several papers.

## Atomic report rule

A report should be operationally self-contained while **not** becoming a second scientific codebase.

Preferred layout when the components exist:

```text
reports/<report_id>/
├── README.md
├── AI_HANDOFF.md      # optional when report-specific state becomes complex
├── code/              # thin product-local runner(s)
├── notes/             # brainstorming / interpretation / future analyses
├── tables/            # retained aggregate report tables
├── figures/           # retained aggregate report figures
├── provenance/        # report-specific historical/methodological records
├── build/             # disposable local generated workspace; ignored by Git
├── <report>.tex
└── <report>.pdf
```

The local `code/` directory may parse arguments, resolve paths, choose configuration, call root-code functions and specify execution order. **Reusable cohort logic, statistics, models, estimators, transformations, confidence intervals, imputation rules and plotting functions remain in `../code/src/visitas_analysis/`.**

If a report needs a new scientific capability:

1. define the question/need in the report;
2. search `../code/FUNCTION_INDEX.md`;
3. reuse an existing root-code function when possible;
4. otherwise implement the reusable function in root `code/`, with tests/documentation;
5. import it from the report-local runner;
6. evaluate the result in the report before promoting it into a paper.

Do not write the new estimator directly in the report merely because the experiment originated there.

## Research idea lifecycle

The default path for a new idea is:

```text
question / hypothesis
        ↓
report README or notes
        ↓
search root-code library
        ↓
add/test reusable capability in root code if needed
        ↓
report-local runner calls canonical functions
        ↓
diagnostics + results + sensitivities + interpretation
        ↓
scientific review
        ↓
selected evidence enters a paper
```

If manuscript writing later exposes a missing analysis, return upstream to the relevant report/root code rather than calculating the missing number inside the paper.

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

A single report may feed multiple papers, and a paper may select evidence from multiple reports.

## Data updates

When a new institutional extract arrives but methodology is unchanged, rerun the same report-local recipe with the new controlled inputs, compare outputs and diagnostics, and propagate accepted changes downstream. Do not create a new report version or duplicate script simply because the data vintage changed.

## Naming

Report names describe scientific purpose. Git provides version history, so active paths should not use suffixes such as `v2`, `v5`, `v8`, `final`, `new` or dates. Historical version labels may remain inside provenance records when they identify a specific frozen state.

## Handoff rule

Durable report-development rules belong in `reports/AI_HANDOFF.md`; report-specific scientific state belongs in the corresponding report README/notes. Do not rely on chat history as the only record of how reports are supposed to be developed.