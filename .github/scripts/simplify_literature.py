from pathlib import Path
import hashlib
import re
import subprocess

ROOT = Path('.')
LIB = Path('literature/library')
SOURCES = LIB / 'source_material'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_historical_coverage() -> None:
    mappings = {
        'extracted': LIB / 'articles',
        'pdf': LIB / 'pdf',
        'references': LIB / 'references',
    }
    for kind, target_dir in mappings.items():
        candidates: dict[str, list[Path]] = {}
        for corpus in ['visual_corpus', 'pdf_markdown_corpus']:
            d = SOURCES / corpus / kind
            if not d.exists():
                continue
            for p in d.iterdir():
                if p.is_file():
                    candidates.setdefault(p.name, []).append(p)
        missing, mismatched = [], []
        for name, srcs in sorted(candidates.items()):
            target = target_dir / name
            if not target.exists():
                missing.append(name)
                continue
            th = digest(target)
            if th not in {digest(s) for s in srcs}:
                mismatched.append(name)
        if missing or mismatched:
            raise SystemExit(f'{kind}: missing={missing}, mismatched={mismatched}')
        print(f'{kind}: verified {len(candidates)} historical filenames')

    a = subprocess.check_output(['git', 'rev-parse', 'HEAD:literature/library/assets'], text=True).strip()
    b = subprocess.check_output(['git', 'rev-parse', 'HEAD:literature/library/source_material/visual_corpus/assets'], text=True).strip()
    if a != b:
        raise SystemExit(f'assets trees differ: {a} != {b}')
    print(f'assets: exact duplicate Git tree {a}')


def rewrite_historical_paths() -> None:
    for p in ROOT.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        old = text
        text = re.sub(r'library/source_material/(?:visual_corpus|pdf_markdown_corpus)/extracted/', 'library/articles/', text)
        text = re.sub(r'library/source_material/(?:visual_corpus|pdf_markdown_corpus)/pdf/', 'library/pdf/', text)
        text = re.sub(r'library/source_material/(?:visual_corpus|pdf_markdown_corpus)/references/', 'library/references/', text)
        if text != old:
            p.write_text(text, encoding='utf-8')


def build_catalog() -> None:
    articles = sorted(p.stem for p in (LIB / 'articles').glob('*.md'))
    pdfs = {p.stem for p in (LIB / 'pdf').glob('*.pdf')}
    refs = {p.name.removesuffix('.references.md') for p in (LIB / 'references').glob('*.references.md')}
    rows = []
    for ident in articles:
        flags = ['M']
        if ident in pdfs:
            flags.append('P')
        if ident in refs:
            flags.append('R')
        rows.append(f'| `{ident}` | {" ".join(flags)} |')

    text = '''# Master literature catalogue

This is the single canonical inventory for the CMAT research library.

The active physical library is intentionally simple:

- `articles/<id>.md` — extracted/searchable article text;
- `pdf/<id>.pdf` — source PDF when available;
- `references/<id>.references.md` — separated reference list when available.

Historical upload-batch folders and Docling figure/table assets were removed from the active tree after verified consolidation. Their provenance remains in `PROVENANCE.md`, `docs/HEAVY_SNAPSHOT.md`, and Git history. The source PDF is the authoritative visual verification layer.

Legend: `M` = Markdown article record; `P` = source PDF available; `R` = separated reference list available.

## Inventory

| Literature ID | Availability |
|---|---|
''' + '\n'.join(rows) + '''

## Version rules

Keep genuinely distinct scholarly versions separate when analytically useful (for example a working paper and its published article). Do not collapse versions solely because titles are similar. Prefer the published version for manuscript citation unless there is a documented reason not to.

## Scientific views

- [General literature](../general/INDEX.md)
- [Paper 1 — PPA persistence](../papers/paper1_ppa_persistence/INDEX.md)
- [Paper 2 — MU performance](../papers/paper2_mu_performance/INDEX.md)
- [Paper 3 — grading heterogeneity](../papers/paper3_grading_heterogeneity/INDEX.md)
- [Paper 4 — degree/help-seeking heterogeneity](../papers/paper4_degree_help_seeking/INDEX.md)
- [Paper 5 — longitudinal trajectories](../papers/paper5_longitudinal_trajectories/INDEX.md)

A work may appear in several scientific views without physical duplication.
'''
    (LIB / 'CATALOG.md').write_text(text, encoding='utf-8')


def write_core_docs() -> None:
    (LIB / 'README.md').write_text('''# Canonical research library

`literature/library/` is the single shared physical source layer for the CMAT literature system.

## Contents

- `CATALOG.md` — master inventory and preferred lookup entry point.
- `articles/` — extracted/searchable Markdown, one canonical record per literature ID/version.
- `pdf/` — retained source PDFs when available.
- `references/` — separated reference lists when available.
- `PROVENANCE.md` — history of the original literature imports and consolidation.
- `AGENTS.md` — maintenance rules for this library.

There are no paper-specific source copies. General and manuscript-specific folders under `literature/` are scientific views over this shared library.

## Retrieval order

1. start from `../general/INDEX.md` or a paper-specific index under `../papers/`;
2. use `CATALOG.md` to resolve the stable literature ID;
3. read `articles/<id>.md` for efficient targeted retrieval;
4. use `references/` for citation chaining or metadata checks;
5. use the PDF for exact numbers, tables, figures, quotations, page anchors, or extraction ambiguity.

The PDF is the authoritative visual source. Extracted Docling PNG/table assets are not retained in the active library.

## Versions

Preserve genuinely distinct scholarly versions when analytically useful. Prefer the published version for citation unless documented otherwise.

## Publication boundary

This is a private research repository. Source PDFs and extraction artifacts are internal research materials and are not automatically cleared for redistribution.
''', encoding='utf-8')

    (LIB / 'AGENTS.md').write_text('''# Agent instructions — canonical literature library

This is the physical source library, not a manuscript-specific bibliography.

## Required behavior

- Never duplicate an article because it is relevant to more than one paper.
- Resolve works through the stable file stem/ID and `CATALOG.md`.
- Prefer `articles/<id>.md` for efficient reading; open `pdf/<id>.pdf` for exact critical verification or extraction ambiguity.
- Use `references/` for citation chaining and bibliographic verification.
- Do not regenerate or archive extracted figure/table assets by default; the source PDF is the visual authority.
- Preserve distinct scholarly versions when scientifically meaningful.
- Never infer missing coefficients, p-values, confidence intervals, sample sizes, effect sizes, or quotations from corrupted extraction text.
- When changing IDs or canonical paths, update `CATALOG.md`, every affected thematic/paper view, reading-note anchors, and the literature AI handoff.

## Adding a work

Add the canonical Markdown record to `articles/`, the source PDF to `pdf/` when available/appropriate, and a separated reference list to `references/` when useful. Then update `CATALOG.md` and every relevant scientific view.

## Relationship to manuscripts

Paper-specific literature folders contain indices, gap tracking and technical reading notes only. LaTeX `.bib` files belong with manuscripts under root `papers/`.
''', encoding='utf-8')

    Path('literature/README.md').write_text('''# Literature

This subsystem has one shared physical library plus scientific views.

## Structure

- `library/` — canonical Markdown/PDF/reference library and master catalogue.
- `general/` — cross-project conceptual literature map.
- `papers/` — five manuscript-specific literature views, gap trackers and technical reading notes.
- `AI_HANDOFF.md` — literature continuity for future sessions.
- `AGENTS.md` — maintenance/retrieval rules.

## Five paper views

1. `papers/paper1_ppa_persistence/` — incentive-linked first-year support use and later persistence.
2. `papers/paper2_mu_performance/` — CMAT use and classroom-relative first-MU performance.
3. `papers/paper3_grading_heterogeneity/` — instructor-by-term grading heterogeneity and assessment comparability.
4. `papers/paper4_degree_help_seeking/` — disciplinary/degree-programme heterogeneity in support use and persistence.
5. `papers/paper5_longitudinal_trajectories/` — full-degree longitudinal mathematics-support trajectories.

Canonical publication strategy: `../docs/PUBLICATION_PORTFOLIO.md`.

## Core rule

One scholarly source/version has one physical library record. It may be referenced by general and several paper views without duplication.

## Retrieval order

Start from the relevant scientific `INDEX.md` or Paper 1 `READING_GUIDE.md`, resolve the ID in `library/CATALOG.md`, read targeted Markdown in `library/articles/`, use `library/references/` for citation chaining, and consult the source PDF for exact or visual verification.

Extracted figure/table assets are intentionally not retained in the active library; the PDF is the visual authority.

## Publication boundary

The repository is private. Source PDFs and extraction artifacts are internal research materials and are not automatically redistributable in a public release.
''', encoding='utf-8')

    (LIB / 'PROVENANCE.md').write_text('''# Literature provenance

The active library is a verified consolidated derivative of two historical literature imports. Upload-batch structure is no longer preserved in the working tree because it duplicated the canonical flat library.

## Historical source sets

### Original visual corpus

- archive: `Bib.zip`;
- SHA-256: `84ef1c01a85db38ef6b5413621480eba1332f800dddc2523f098209e0745a237`;
- 20 source PDFs;
- 20 extracted Markdown records;
- separated references;
- 136 Docling figure/table assets in the original import.

### Original PDF/Markdown corpus

- archive: `339dc703-470e-407c-bb54-97ab069e4ce7.zip`;
- SHA-256: `cfa14830138c970027a9bf730eab2e62b5bf84fe072ddb3c82c206a5c242478c`;
- curated representation historically contained 30 extracted Markdown records, 29 PDFs and 24 separated reference files;
- visual assets were intentionally omitted from that curated import.

## Consolidation

On 2026-09-08, the historical source-batch folders were verified against the flat `articles/`, `pdf/`, and `references/` library before removal. For each historical filename, the flat canonical file matched at least one historical copy byte-for-byte. The duplicate top-level asset tree and the original visual-corpus asset tree also had the same Git tree hash before both were removed.

The active library therefore preserves the scholarly Markdown/PDF/reference content while dropping redundant migration structure and extracted PNG/table assets. Git history preserves the former folder layout and asset files if forensic provenance is ever required.

`kahu_2018_student-engagement-educational-interface` remains a Markdown-only library record in the historical corpus state.

## Rights boundary

Source PDFs are retained for internal research continuity in this private repository. Their presence does not imply permission for redistribution.
''', encoding='utf-8')


def update_operational_docs() -> None:
    replacements = {
        'literature/general/README.md': [
            ('Sources remain under `../library/source_material/`;', 'Sources remain under `../library/`;'),
        ],
        'literature/general/INDEX.md': [
            ('shared source material under `../library/source_material/`', 'shared canonical library under `../library/`'),
        ],
        'literature/AGENTS.md': [
            ('Historical source imports remain nested under `library/source_material/` for provenance. Their storage boundaries must not dictate scientific interpretation.\n\n', ''),
            ('use `library/CATALOG.md` and the source-material indices to locate the canonical record;', 'use `library/CATALOG.md` to locate the canonical record;'),
            ('use Docling assets only where they actually exist and materially help.', 'use the source PDF for exact visual verification; extracted Docling assets are not retained in the active library.'),
            ('Docling assets are optional visual fallbacks.', 'The source PDF is the visual verification layer.'),
            ('place/register the work in the appropriate canonical source-material layer under `library/source_material/`;', 'add the canonical Markdown record to `library/articles/`;'),
            ('retain the source PDF when available and appropriate for this private repository;', 'add the source PDF to `library/pdf/` when available and appropriate for this private repository;'),
            ('retain separated references when useful;', 'add separated references to `library/references/` when useful;'),
            ('add visual assets only when they already exist or are genuinely needed—do not regenerate hundreds of images for archival completeness;\n', ''),
            ('Do not create `library/articles/`, `Bib3`, `Bib4`, or paper-specific physical source copies unless the architecture is intentionally changed and documented first.', 'Do not recreate upload-batch folders (`Bib`, `Bib2`, `Bib3`, etc.), `source_material/`, extracted asset trees, or paper-specific physical source copies.'),
        ],
        'literature/AI_HANDOFF.md': [
            ('- `literature/library/`: source layer and master catalogue.\n- `literature/library/source_material/visual_corpus/`: historical source set with PDFs, extracted Markdown, references and visual assets.\n- `literature/library/source_material/pdf_markdown_corpus/`: historical source set with PDFs/Markdown/references and no visual assets by design.', '- `literature/library/`: canonical flat source layer with `articles/`, `pdf/`, `references/` and `CATALOG.md`.'),
            ('Do not recreate `Bib`, `Bib2`, `Bib3`, other upload-batch folders, or a parallel `library/articles/` hierarchy.', 'Do not recreate `Bib`, `Bib2`, `Bib3`, `source_material/`, extracted asset trees, or paper-specific physical source copies.'),
            ('use `literature/library/CATALOG.md` and source-material indices to locate the canonical record;', 'use `literature/library/CATALOG.md` to locate the canonical record;'),
            ('use visual assets only where they exist and materially help.', 'use the source PDF for visual verification; extracted asset trees are not retained.'),
            ('place/register the source once in `library/source_material/`;', 'place the Markdown record once in `library/articles/`, the PDF in `library/pdf/` when available, and separated references in `library/references/` when useful;'),
        ],
        'AI_HANDOFF.md': [
            ('The physical corpus is shared under `literature/library/source_material/`.', 'The physical corpus is shared under `literature/library/` (`articles/`, `pdf/`, and `references/`).'),
        ],
        'literature/papers/README.md': [
            ('shared source material', 'shared canonical library'),
        ],
    }
    for filename, reps in replacements.items():
        p = Path(filename)
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        for old, new in reps:
            text = text.replace(old, new)
        p.write_text(text, encoding='utf-8')

    for fn in ['docs/HEAVY_SNAPSHOT.md', 'docs/MIGRATION_STATUS.md']:
        p = Path(fn)
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        text = re.sub(r'`literature/library/source_material/visual_corpus/`', '`literature/library/` (consolidated)', text)
        text = re.sub(r'`literature/library/source_material/pdf_markdown_corpus/`', '`literature/library/` (consolidated)', text)
        text = text.replace('Historical source imports remain nested under:', 'Historical source imports were consolidated into the active flat library from:')
        if '## Literature consolidation update — 2026-09-08' not in text:
            text += '\n\n## Literature consolidation update — 2026-09-08\n\nThe active literature tree was simplified after verification that all historical Markdown/PDF/reference filenames were represented byte-for-byte in the flat canonical library. The historical `source_material/` hierarchy, duplicate Docling `assets/` tree, and redundant `library/INDEX.md` were removed. The single master inventory is now `literature/library/CATALOG.md`; original batch checksums and former layout remain documented in provenance and Git history.\n'
        p.write_text(text, encoding='utf-8')


def sanity_before_delete() -> None:
    assert (LIB / 'articles').is_dir()
    assert (LIB / 'pdf').is_dir()
    assert (LIB / 'references').is_dir()
    assert (LIB / 'CATALOG.md').is_file()


if __name__ == '__main__':
    verify_historical_coverage()
    rewrite_historical_paths()
    build_catalog()
    write_core_docs()
    update_operational_docs()
    sanity_before_delete()
    print('Migration content prepared successfully.')
