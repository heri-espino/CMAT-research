# AGENTS.md — literature subsystem

This file defines how humans and automated agents should operate inside `literature/`.

## 1. Scientific organization is primary

Do not organize literature by upload batch. The user-facing structure is:

- `library/` — canonical source material and master catalogue;
- `general/` — cross-project conceptual literature;
- `papers/paper1_ppa_persistence/` — Paper 1 literature view;
- `papers/paper2_mu_performance/` — Paper 2 literature view.

Historical source imports may remain nested under `library/source_material/` for provenance, but their storage boundaries must not dictate scientific interpretation.

## 2. One physical source, many views

A paper can support several research questions. Do not copy the same PDF/Markdown into general + Paper 1 + Paper 2. Instead, add references to the canonical source from multiple indices/cards.

## 3. Retrieval protocol

For a literature question:

1. identify whether the question is general, Paper 1, Paper 2, or cross-paper;
2. open the corresponding `INDEX.md` first;
3. use `library/CATALOG.md` and source-material indices to locate the canonical record;
4. read only the relevant extracted Markdown sections;
5. inspect `references/` only for citation chaining or bibliography verification;
6. inspect the PDF for exact tables, figures, coefficients, confidence intervals, sample sizes, page-level wording, or extraction ambiguity;
7. use Docling assets only where they actually exist; the PDF/Markdown corpus intentionally has no assets.

Do not load the entire corpus into context when a targeted search is sufficient.

## 4. Source reliability

- Source PDFs are the final verification layer.
- Extracted Markdown is the primary efficient reading layer.
- Separated references are secondary metadata.
- Docling assets are optional visual fallbacks.
- Never infer a material numerical value from visibly corrupted extraction.

## 5. Duplicate/version handling

When apparent duplicates are found:

- compare title, authors, year, DOI and scholarly version;
- collapse exact duplicate copies in the scientific catalogue;
- retain genuinely different versions (e.g. working paper vs published article) when analytically relevant;
- record the preferred canonical source and provenance rather than silently deleting useful history.

## 6. Paper-specific role tagging

Paper views should annotate each source with a role such as:

- `core` — directly supports theory/design/contribution;
- `supporting` — useful framing or interpretation;
- `methods` — supports statistical or measurement choices;
- `context` — institutional/domain background;
- `contrast` — competing explanation or alternative interpretation.

Where useful, also note `used_in` (Introduction, Methods, Discussion) and `do_not_claim` boundaries.

## 7. Paper 1 scope

Paper 1 studies persistence of CMAT support-seeking after an incentive-linked first-year context. Relevant literature families include incentives, removal of incentives, persistence, engagement, academic help-seeking, first-year transitions and mathematics-support context.

Do not describe PPA as an exogenous treatment and do not identify a causal PPA effect from the observational CMAT data.

## 8. Paper 2 scope

Paper 2 studies CMAT use and classroom-relative MU academic performance. Relevant literature families include mathematics/statistics support, tutoring/help-seeking, selection into support, usage intensity, academic performance, classroom adjustment and observational robustness.

Do not convert association into a causal tutoring effect without an identified design.

## 9. Maintenance rule

When adding or materially changing literature:

- update `library/CATALOG.md`;
- update every relevant scientific view;
- update `AI_HANDOFF.md` if architecture, retrieval rules or major literature gaps changed;
- do not rename stable paper IDs casually;
- keep manuscript `.bib` files with manuscripts, not inside this research-library folder.

## 10. Privacy/copyright boundary

This is a private research repository. Literature PDFs and extraction artifacts are internal research materials and are not automatically redistributable in a public release. Administrative student data must never be added here.
