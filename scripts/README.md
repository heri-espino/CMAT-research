# Repository scripts

Utilities here are for repository maintenance, **not** statistical analysis. Scientific analysis scripts belong under `code/`.

The historical `import_heavy_literature.sh` script is retained only as provenance for the original ingestion workflow. It must not be used against the current repository because it recreates deprecated `literature/Bib` and `literature/Bib2` paths.

Current literature additions should follow `literature/AGENTS.md`: add each work once under `literature/library/` and update the semantic indexes.
