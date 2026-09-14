# Paper 4 manuscript

Paper 4 uses a single-source two-output LaTeX workflow. `manuscript.tex` aggregates the shared section files under `sections/`; `main.tex` produces the **official clean manuscript**, while `main_commented.tex` produces a **development copy with TODO annotations visible**. The bibliography is stored in `references.bib`, and `build.py` compiles both PDFs.

The manuscript is written from the empirically frozen design documented in `PROJECT_CONTEXT.md`. Numerical claims are traceable to reviewed aggregate outputs under `../results/tables/`, especially confirmatory tables `220`–`233`. `DRAFT_NOTES.md` contains substantive development tasks, while `AI_HANDOFF.md` defines LaTeX, citation, equation, cross-reference, table, and figure-style conventions for future AI-assisted editing.

The current working title is:

> *From Assigned to Chosen Academic Contexts: Longitudinal Traces of Student Engagement and Adaptation in First-Year University Mathematics*

The paper treats CMAT attendance as a formal help-seeking trace rather than a direct measure of latent engagement, uses strictly prior instructor outcomes for later context measures, and makes no causal claims about support use, course failure, instructor movement, or degree programme.

Run `python paper/build.py` from the repository root (or `python build.py` from `paper/`) to compile:

- `paper/main.pdf` — official manuscript, TODO-free;
- `paper/main_commented.pdf` — development manuscript with TODOs visible.
