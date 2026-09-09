# AI handoff — literature subsystem

This is the starting point for future AI sessions working on CMAT literature.

## Purpose

The literature subsystem is organized by scientific use, not by upload batch. The repository exposes one shared research library plus a cross-project view. Paper-specific literature work is co-located with each paper rather than mirrored inside `literature/`.

Canonical publication plan: `../docs/PUBLICATION_PORTFOLIO.md`.

## Canonical layout

- `literature/library/`: canonical flat source layer with `articles/`, `pdf/`, `references/` and `CATALOG.md`.
- `literature/general/`: cross-project literature map and thematic notes.
- `papers/paper1_ppa_persistence/literature/`: incentive-linked persistence literature view.
- `papers/paper2_mu_performance/literature/`: MU performance literature view.
- `papers/paper3_grading_heterogeneity/literature/`: grading/assessment literature view.
- `papers/paper4_degree_help_seeking/literature/`: disciplinary help-seeking literature view.
- `papers/paper5_longitudinal_trajectories/literature/`: full-degree trajectory literature view.

There is intentionally no `literature/papers/` mirror. Each paper has one canonical home under `papers/<paper_id>/`.

Do not recreate `Bib`, `Bib2`, `Bib3`, `source_material/`, extracted asset trees, or paper-specific physical source copies.

## Five-paper portfolio snapshot

The detailed source of truth for each paper is its root `papers/<paper_id>/README.md`; `docs/PUBLICATION_PORTFOLIO.md` is the cross-paper planning summary. The snapshot below is retained for literature routing, not as a second editorial source of truth.

### Paper 1
**Working title:** *Beyond the Incentive Threshold: Academic Support Use and Persistence After a First-Year Participation Incentive*  
**Priority:** highest / active.  
**Journal route:** *Studies in Higher Education* first/ambitious; IJMEST, TEAMAT and *Journal of Further and Higher Education* as alternatives.  
**Boundary:** observational persistence across a change in incentive context; no causal PPA claim.

### Paper 2
**Working title:** *Mathematics Support Use and Classroom-Relative Academic Performance in First-Year University Mathematics*  
**Priority:** high / active after methodology freeze.  
**Journal route:** TEAMAT first; IJMEST second; IJRUME ambitious.  
**Boundary:** primary cohort is first-MU `N=6,627`; future-Calculus `N=4,211` is a selected sensitivity.

### Paper 3
**Working title:** *When the Same Grade Does Not Mean the Same Performance: Instructor-by-Term Heterogeneity in Undergraduate Mathematics Assessment*  
**Priority:** high but requires dedicated re-analysis.  
**Journal route:** *Assessment & Evaluation in Higher Education* first; *Studies in Educational Evaluation* second; IJRUME ambitious.  
**Boundary:** classroom-relative `Z` is contextual relative position, not latent mathematical proficiency.

### Paper 4
**Working title:** *Who Keeps Seeking Mathematics Help? Disciplinary Heterogeneity in University Mathematics Support Use*  
**Priority:** later / conditional on stronger programme-level design.  
**Journal route:** IJMEST first; *Journal of Further and Higher Education* second; HERD ambitious.  
**Boundary:** programme-level results are ecological; official academic `CLAVECARRERA` is the primary programme variable.

### Paper 5
**Working title:** *Longitudinal Trajectories of Mathematics Support Use Across the Undergraduate Degree*  
**Priority:** future project.  
**Journal route:** not frozen; TEAMAT/IJMEST for substantive mathematics-support framing, *Journal of Learning Analytics* for a genuine trace/sequence-method contribution, *International Journal of STEM Education* as an ambitious STEM-progression route.  
**Boundary:** full-degree data coverage/missingness and revalidation logic must be audited before method selection.

## Paper 1 technical reading-note layer

Paper 1 has a human-readable technical evidence layer:

- `papers/paper1_ppa_persistence/literature/READING_GUIDE.md` — rapid overview;
- `papers/paper1_ppa_persistence/literature/reading_notes/README.md` — required schema and subfolder-routing policy;
- `papers/paper1_ppa_persistence/literature/reading_notes/general/` — foundational/cross-cutting technical notes;
- `papers/paper1_ppa_persistence/literature/reading_notes/incentives/` — incentive/removal/behavioural-intervention technical notes.

### Reading-note taxonomy

The reading-note tree is organized by **scientific function**. It must never reproduce upload batches, providers, file types, extraction stages or arbitrary chronology.

Active categories:

- `general/` — engagement, help-seeking, mathematics-support, first-year-transition, persistence and other broad/foundational literature whose primary contribution is cross-cutting rather than intervention-specific.
- `incentives/` — sources whose central contribution concerns incentives, incentive removal/expiration, participation contingencies, thresholds, or behavioural interventions that help interpret the PPA change in incentive context.

For `incentives/`, prioritize extraction of intervention type, target behaviour, assignment/exposure, incentive magnitude or threshold when applicable, timing, removal/expiration, follow-up horizon, compliance/take-up, post-incentive behaviour, identification strategy, mechanism evidence, and transportability to the CMAT/PPA setting. Do not route a source there merely because it mentions motivation or engagement.

Keep **one canonical technical note per source**. If a source serves multiple functions, cross-reference it from guides/indices rather than duplicating note files.

Only create another reading-note subfolder when it has:

1. a distinct manuscript-relevant scientific purpose;
2. several substantive sources or a clearly committed review stream;
3. a stable inclusion/exclusion rule;
4. clear retrieval/synthesis value;
5. no need to duplicate sources already represented elsewhere.

When a new scientific-function folder is introduced, document it first in `papers/paper1_ppa_persistence/literature/reading_notes/README.md` and then update this handoff plus `literature/AGENTS.md` when the routing rule is important for future sessions.

### Completed general/foundational notes

- Kahu (2013) — conceptual engagement framework;
- Kahu & Nelson (2018) — educational-interface framework;
- Fong et al. (2023) — postsecondary help-seeking meta-analysis;
- Mullen et al. (2024) — systematic scoping review of MSS evaluation;
- Lawson, Grove & Croft (2020) — mathematics-support literature review;
- Wilcox, Winn & Fyvie-Gauld (2005) — qualitative first-year social-support/retention study;
- van Herpen et al. (2020) — quasi-experimental first-year transition intervention.

### Completed incentive/removal/behavioural notes

- Gneezy, Meier & Rey-Biel (2011) — direct incentive effects, crowd-out and post-removal mechanisms;
- Angrist, Lang & Oreopoulos (2009) — randomized services/incentives experiment; offer versus uptake; persistent female academic differences;
- Leuven, Oosterbeek & van der Klaauw (2010) — randomized financial rewards; average null with ability/background heterogeneity;
- Agnew, Kerr & Watt (2021) — removal of 1%-per-quiz incentives; sharp participation/intensity decline and historical-cohort achievement comparison;
- Oreopoulos & Petronijevic (2019) — multi-year RCT program of low-touch college nudges/coaching with precise academic nulls and some intermediate behavioural effects;
- Blondeel, Everaert & Opdecam (2023) — randomized nudge assignment with null group effects but selected click-intensity associations; direct *Studies in Higher Education* comparator;
- Damgaard & Nielsen (2018) — education-nudging review/typology; mechanism, targeting, heterogeneity, and nudge-versus-material-incentive distinction.

These notes record methods, sample sizes, important findings, effect sizes/test statistics/p-values/CI where genuinely reported, claim boundaries and local verification paths. Conceptual/review papers are not forced into a false primary-study statistical template.

### Next Paper 1 literature expansion

Do not create another folder automatically. Expand `incentives/` only when a source fills a concrete scientific role not already covered well. Candidate existing-library sources include Barrow et al. (2018), Lavecchia et al. (2014/2016), Koch et al. (2015), Lintner et al. (2024), and the alternate Damgaard version. Highest priority should go to evidence on post-incentive persistence/decay, explicit participation thresholds, and incentive-linked academic-support use rather than adding redundant general behavioural-economics reviews.

Highest-priority missing comparator currently tracked for Papers 1–2: Büchele & Schürmann (2024), *Studies in Higher Education*, DOI `10.1080/03075079.2023.2271029`.

## Retrieval order

1. read `literature/README.md`;
2. read `docs/PUBLICATION_PORTFOLIO.md` if cross-paper manuscript strategy matters;
3. for a specific manuscript, read `papers/<paper_id>/README.md` then `papers/<paper_id>/literature/INDEX.md`;
4. for Paper 1, read `READING_GUIDE.md` and the relevant article note before reopening the full source;
5. use `literature/library/CATALOG.md` to locate the canonical record;
6. read targeted extracted Markdown first;
7. read separated references only for citation chaining or bibliography verification;
8. open the source PDF when an exact table, figure, coefficient, wording, page, or extraction ambiguity matters;
9. use the source PDF for visual verification; extracted asset trees are not retained.

## Important interpretation rules

- One source may be indexed in general and several papers without physical duplication.
- Paper-specific folders are views/notes, not separate libraries.
- Keep published and working-paper versions separate when genuinely distinct.
- Prefer the most complete/high-fidelity extracted Markdown when true duplicates are discovered, while preserving provenance.
- Do not infer numerical results from corrupted extraction; verify against the PDF.
- Never invent p-values, coefficients, `R²`, effect sizes or sample sizes for a source that does not report them.
- Preserve null results in technical reading notes.
- For interventions, separate randomized offer/exposure from voluntary uptake/intensity; post-treatment intensity does not inherit randomization.
- Literature PDFs are internal research materials in this private repository and are not automatically redistributable.
- Literature organization must not dictate scientific results; all papers consume canonical outputs from the shared analysis pipeline.

## Maintenance when adding a source

1. choose a stable ID such as `author_year_short-topic`;
2. place the Markdown record once in `literature/library/articles/`, the PDF in `literature/library/pdf/` when available, and separated references in `literature/library/references/` when useful;
3. update `literature/library/CATALOG.md`;
4. add it to every relevant scientific view (`literature/general/` and/or `papers/<paper_id>/literature/`) with a short role/priority note;
5. update the relevant `MISSING_LITERATURE.md` if it fills a known gap;
6. if substantive for an active paper, create/update its technical reading note;
7. avoid physical duplication solely because the source supports multiple manuscripts.

## Maintenance when the publication plan changes

If a working title, paper boundary, priority or journal strategy changes:

1. update `docs/PUBLICATION_PORTFOLIO.md` for cross-paper implications;
2. update the matching `papers/<paper_id>/README.md` as the detailed paper source of truth;
3. update `papers/<paper_id>/literature/README.md` only if literature routing/scope changes;
4. update this handoff and `literature/AGENTS.md` if routing rules or portfolio structure changed.
