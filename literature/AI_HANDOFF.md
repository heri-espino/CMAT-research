# AI handoff — literature subsystem

This file is the starting point for future AI sessions working on CMAT literature.

## Purpose

The literature subsystem is organized by scientific use, not by upload batch. The repository exposes one shared research library plus lightweight views for the overall project and five planned papers.

Canonical publication plan: `../docs/PUBLICATION_PORTFOLIO.md`.

## Canonical layout

- `literature/library/`: source layer and master catalogue.
- `literature/library/source_material/visual_corpus/`: historical source set with PDFs, extracted Markdown, references and visual assets.
- `literature/library/source_material/pdf_markdown_corpus/`: historical source set with PDFs/Markdown/references and no visual assets by design.
- `literature/general/`: cross-project literature map and thematic notes.
- `literature/papers/paper1_ppa_persistence/`: incentive-linked persistence literature view.
- `literature/papers/paper2_mu_performance/`: MU performance literature view.
- `literature/papers/paper3_grading_heterogeneity/`: grading/assessment literature view.
- `literature/papers/paper4_degree_help_seeking/`: disciplinary help-seeking literature view.
- `literature/papers/paper5_longitudinal_trajectories/`: full-degree trajectory literature view.

Do not recreate `Bib`, `Bib2`, `Bib3`, or other upload-batch folders as user-facing organization.

## Five-paper portfolio snapshot

### Paper 1
**Working title:** *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*  
**Priority:** highest / active.  
**Journal route:** Studies in Higher Education first/ambitious; IJMEST, TEAMAT and Journal of Further and Higher Education as alternatives.  
**Boundary:** observational persistence across a change in incentive context; no causal PPA claim.

### Paper 2
**Working title:** *Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics*  
**Priority:** high / active after methodology freeze.  
**Journal route:** TEAMAT first; IJMEST second; IJRUME ambitious.  
**Boundary:** primary cohort is first-MU `N=6,627`; future-Calculus `N=4,211` is a selected sensitivity.

### Paper 3
**Working title:** *When the Same Grade Does Not Mean the Same Performance: Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment*  
**Priority:** high but requires dedicated re-analysis.  
**Journal route:** Assessment & Evaluation in Higher Education first; Studies in Educational Evaluation second; IJRUME ambitious.  
**Boundary:** classroom-relative `Z` is contextual relative position, not latent mathematical proficiency.

### Paper 4
**Working title:** *Who Keeps Seeking Mathematics Help? Disciplinary Heterogeneity in University Mathematics Support Use*  
**Priority:** later / conditional on stronger programme-level design.  
**Journal route:** IJMEST first; Journal of Further and Higher Education second; HERD ambitious.  
**Boundary:** programme-level results are ecological; official academic `CLAVECARRERA` is the primary programme variable.

### Paper 5
**Working title:** *Longitudinal Trajectories of Mathematics Support Use Across the Undergraduate Degree*  
**Priority:** future project.  
**Journal route:** not frozen; TEAMAT/IJMEST for substantive mathematics-support framing, Journal of Learning Analytics for a genuine trace/sequence-method contribution, International Journal of STEM Education as an ambitious STEM-progression route.  
**Boundary:** full-degree data coverage/missingness and revalidation logic must be audited before method selection.

## Retrieval order

1. Read `literature/README.md`.
2. Read `docs/PUBLICATION_PORTFOLIO.md` if the task concerns manuscript strategy.
3. Read the relevant paper/general `INDEX.md`.
4. Use `literature/library/CATALOG.md` and source-material indices to locate the canonical record.
5. Read targeted extracted Markdown first.
6. Read separated references only for citation chaining or bibliography verification.
7. Open the source PDF when an exact table, figure, coefficient, wording, page, or extraction ambiguity matters.
8. Visual assets exist only for part of the historical corpus; never assume they exist for every paper.

## Important interpretation rules

- One source may be indexed in general and several papers without duplicating the physical PDF/Markdown.
- Paper-specific folders are views/notes, not separate libraries.
- Keep published and working-paper versions separate when they are genuinely distinct scholarly versions.
- Prefer the most complete/high-fidelity extracted Markdown when true duplicates are discovered, but preserve provenance in the catalogue.
- Do not infer numerical results from corrupted extraction; verify against the PDF.
- Literature PDFs are internal research materials in this private repository and are not automatically redistributable in a public release.
- Literature organization must not dictate scientific results; all papers consume canonical outputs from the shared analysis pipeline.

## Maintenance when adding a source

1. choose a stable ID such as `author_year_short-topic`;
2. place or register the source in the library source-material layer;
3. update `literature/library/CATALOG.md`;
4. add it to every relevant scientific view (`general` and/or Papers 1–5) with a short role/priority note;
5. update the relevant `MISSING_LITERATURE.md` if the source fills a known gap;
6. avoid physical duplication solely because a source supports multiple manuscripts.

## Maintenance when the publication plan changes

If a working title, paper boundary, priority or journal strategy changes:

1. update `docs/PUBLICATION_PORTFOLIO.md` first;
2. update the matching root `papers/<paper_id>/README.md`;
3. update the matching `literature/papers/<paper_id>/README.md` if the literature scope changes;
4. update this handoff and `literature/AGENTS.md` if routing rules or portfolio structure changed.

When true duplicates are discovered, verify title/authors/year/DOI/content before collapsing them. Historical import provenance can remain documented in Git history and `docs/HEAVY_SNAPSHOT.md` even after duplicate working copies are removed.