# Paper 4 manuscript

The current full draft is `main.tex`, with bibliography in `references.bib` and a minimal reproducible builder in `build.py`.

The manuscript is written from the empirically frozen design documented in `PROJECT_CONTEXT.md`. Numerical claims in the draft are traceable to the reviewed aggregate outputs under `../results/tables/`, especially confirmatory tables `220`–`233`. `DRAFT_NOTES.md` lists the remaining manuscript-development tasks and interpretation constraints.

The current working title is:

> *From Assigned to Chosen Academic Contexts: Longitudinal Traces of Student Engagement and Adaptation in First-Year University Mathematics*

The draft treats CMAT attendance as a formal help-seeking trace rather than a direct measure of latent engagement, uses strictly prior instructor outcomes for later context measures, and makes no causal claims about support use, course failure, instructor movement, or degree programme.

Run `python paper/build.py` from the repository root (or `python build.py` from this directory) to compile `main.pdf` when a LaTeX toolchain with BibTeX is available.
