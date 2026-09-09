# Reports

Technical and internal-facing reports.

## Report structure

### `methodology_report/`

The methodology report is the detailed statistical and methodological record used for review. It should:

- explain mathematical/statistical methods in detail;
- present all validated discoveries, not only those destined for publication;
- distinguish descriptive, associational and causal claims carefully;
- map every reported number to a reproducible aggregate output;
- document methodological assumptions, sensitivities and provenance.

The main source is `methodology_report/methodology_report.tex` and the compiled artifact is `methodology_report/methodology_report.pdf`.

### `research_compendium/`

The research compendium preserves the earlier cumulative LaTeX research record, including exploratory extensions and the PPA1-to-Calculus chapter. It is retained for scientific continuity and historical context rather than treated as the current methodological authority.

The main source is `research_compendium/research_compendium.tex` and the compiled artifact is `research_compendium/research_compendium.pdf`.

## Naming rule

Report and artifact names describe their scientific purpose. Git provides version history, so active paths should not use suffixes such as `v2`, `v5`, or `v8`. Historical version labels may still appear in provenance documentation when they identify a specific imported snapshot or scientific-source fingerprint.

## Current status

`methodology_report/` is the more recent methodology-focused report and `research_compendium/` is the preserved cumulative historical report. The remaining reconciliation task is scientific rather than nominal: the active canonical pipeline still needs to reconcile the later methodology corrections with the refined longitudinal/PPA stage before one report can be treated as a fully unified canonical empirical record.
