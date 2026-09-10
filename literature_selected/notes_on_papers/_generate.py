#!/usr/bin/env python3
"""Generate annotated full-text Markdown reading copies for Paper 1.

The canonical scholarly text remains under literature/library/articles/.
This utility creates derived Paper 1 reading copies and inserts GitHub-native
callouts around source blocks that contain manuscript-relevant ideas, numeric
results, and methodology/statistical assumptions.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "literature" / "library" / "articles"
NOTES_ROOT = ROOT / "literature_selected" / "reading_notes"
OUTPUT_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Annotation:
    category: str
    terms: tuple[str, ...]
    min_hits: int = 2


@dataclass(frozen=True)
class SourceSpec:
    source: str
    note: str
    annotations: tuple[Annotation, ...]


CATEGORY_META = {
    "idea": ("IMPORTANT", "1 · IDEA PRINCIPAL"),
    "numeric": ("TIP", "2 · RESULTADO NUMÉRICO"),
    "method": ("NOTE", "3 · METODOLOGÍA / PRUEBA / SUPUESTO"),
}


SOURCES: tuple[SourceSpec, ...] = (
    SourceSpec(
        "fong_2023_academic-help-seeking-achievement.md",
        "general/fong_2023.md",
        (
            Annotation("idea", ("quality", "help-seeking", "matters"), 2),
            Annotation("numeric", ("formal help-seeking", "0.12", "confidence"), 2),
            Annotation("method", ("robust variance estimation", "meta-analytic", "dependent"), 2),
        ),
    ),
    SourceSpec(
        "kahu_2013_student-engagement-framework.md",
        "general/kahu_2013.md",
        (
            Annotation("idea", ("fundamentally situational", "context", "individual"), 2),
            Annotation("method", ("behavioural", "psychological", "sociocultural", "holistic"), 3),
            Annotation("method", ("longitudinal", "qualitative", "measures"), 2),
        ),
    ),
    SourceSpec(
        "kahu_2018_student-engagement-educational-interface.md",
        "general/kahu_nelson_2018.md",
        (
            Annotation("idea", ("educational interface", "engagement", "dynamically"), 2),
            Annotation("method", ("self-efficacy", "emotions", "belonging", "well-being"), 3),
        ),
    ),
    SourceSpec(
        "lawson_2019_mathematics-support-literature-review.md",
        "general/lawson_2020.md",
        (
            Annotation("idea", ("in addition to", "regular", "teaching"), 2),
            Annotation("method", ("systematic", "review", "grey literature"), 2),
        ),
    ),
    SourceSpec(
        "mullen_2024_mathematics-statistics-support-review.md",
        "general/mullen_2024.md",
        (
            Annotation("idea", ("positive impact", "not all"), 2),
            Annotation("numeric", ("148", "136", "12"), 2),
            Annotation("method", ("scoping review", "PRISMA", "databases"), 2),
        ),
    ),
    SourceSpec(
        "van-herpen_2020_head-start-higher-education.md",
        "general/van_herpen_2020.md",
        (
            Annotation("idea", ("lasted", "throughout", "year"), 2),
            Annotation("numeric", ("6.44", "6.07", "5.26", "0.023"), 2),
            Annotation("method", ("MANOVA", "chi-square", "academic"), 2),
        ),
    ),
    SourceSpec(
        "wilcox_2005_social-support-first-year-experience.md",
        "general/wilcox_2005.md",
        (
            Annotation("idea", ("compatible friends", "retention"), 2),
            Annotation("numeric", ("34", "22", "12"), 2),
            Annotation("method", ("constant comparative", "grounded theory"), 2),
        ),
    ),
    SourceSpec(
        "agnew_2021_removing-incentives-online-formative-assessments.md",
        "incentives/agnew_2021.md",
        (
            Annotation("idea", ("incentive", "removed", "participation"), 2),
            Annotation("numeric", ("55", "6", "51", "quizzes"), 3),
            Annotation("method", ("OLS", "historical", "cohort"), 2),
        ),
    ),
    SourceSpec(
        "angrist_2009_incentives-services-college-achievement.md",
        "incentives/angrist_2009.md",
        (
            Annotation("idea", ("random", "services", "incentives", "first-year"), 3),
            Annotation("numeric", ("0.210", "0.092", "GPA"), 2),
            Annotation("method", ("intention-to-treat", "instrument", "participation"), 2),
        ),
    ),
    SourceSpec(
        "blondeel_2023_nudging-procrastination-attendance-preparation.md",
        "incentives/blondeel_2023.md",
        (
            Annotation("idea", ("nudge", "no significant", "performance"), 2),
            Annotation("numeric", ("0.30", "0.417", "performance"), 2),
            Annotation("method", ("Repeated measures ANCOVA", "procrastination", "211"), 2),
        ),
    ),
    SourceSpec(
        "damgaard_2018_nudging-education-published.md",
        "incentives/damgaard_nielsen_2018.md",
        (
            Annotation("idea", ("significantly changing", "economic incentives"), 2),
            Annotation("numeric", ("122", "57", "studies"), 2),
            Annotation("method", ("active", "passive", "decision", "environment"), 3),
        ),
    ),
    SourceSpec(
        "gneezy_2011_when-incentives-dont-work.md",
        "incentives/gneezy_2011.md",
        (
            Annotation("idea", ("after", "incentive", "removed"), 3),
            Annotation("method", ("direct", "price effect", "psychological"), 2),
        ),
    ),
    SourceSpec(
        "leuven_2010_effect-financial-rewards-student-achievement.md",
        "incentives/leuven_2010.md",
        (
            Annotation("idea", ("no", "significant", "passing", "credit"), 3),
            Annotation("numeric", ("0.23", "0.20", "credit"), 2),
            Annotation("method", ("random", "high reward", "low reward", "control"), 3),
        ),
    ),
    SourceSpec(
        "oreopoulos_2019_unresponsiveness-college-students-nudging.md",
        "incentives/oreopoulos_petronijevic_2019.md",
        (
            Annotation("idea", ("none", "significantly", "academic", "outcomes"), 3),
            Annotation("numeric", ("0.07", "standard deviation", "academic"), 2),
            Annotation("numeric", ("2", "hours", "week", "study"), 3),
            Annotation("method", ("random", "five", "years", "students"), 3),
        ),
    ),
)


def normalize(text: str) -> str:
    """Normalize Markdown text for tolerant block matching."""
    text = html.unescape(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("–", "-").replace("—", "-")
    text = re.sub(r"[`*_~\[\]()>#|]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_blocks(text: str) -> list[str]:
    """Split Markdown into blank-line-delimited blocks while preserving content."""
    return re.split(r"\n[ \t]*\n", text)


def is_frontmatter(block: str) -> bool:
    stripped = block.strip()
    return stripped.startswith("---") and stripped.endswith("---")


def find_block(blocks: list[str], annotation: Annotation) -> tuple[int, int]:
    """Return the best matching source block index and hit count."""
    wanted = [normalize(term) for term in annotation.terms]
    best_index = -1
    best_hits = -1
    best_weight = -1

    for idx, block in enumerate(blocks):
        stripped = block.strip()
        if not stripped or is_frontmatter(block):
            continue
        norm = normalize(block)
        if len(norm) < 50:
            continue
        hits = sum(term in norm for term in wanted)
        weight = sum(len(term) for term in wanted if term in norm)
        if (hits, weight) > (best_hits, best_weight):
            best_index = idx
            best_hits = hits
            best_weight = weight

    if best_index < 0 or best_hits < annotation.min_hits:
        raise RuntimeError(
            f"Could not match {annotation.category} annotation "
            f"{annotation.terms!r}; best hit count={best_hits}"
        )
    return best_index, best_hits


def quote_lines(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def underline_prose(block: str) -> str:
    """Underline prose without breaking Markdown tables or code fences."""
    stripped = block.strip()
    if "```" in stripped or re.search(r"(?m)^\s*\|.*\|\s*$", stripped):
        return quote_lines(stripped)
    lines = stripped.splitlines()
    if not lines:
        return ">"
    lines[0] = "<u>" + lines[0]
    lines[-1] = lines[-1] + "</u>"
    return quote_lines("\n".join(lines))


def wrap_block(block: str, categories: list[str]) -> str:
    """Wrap one original source block in a visible GitHub alert."""
    ordered = [c for c in ("idea", "numeric", "method") if c in categories]
    alert = CATEGORY_META[ordered[0]][0]
    labels = " · ".join(CATEGORY_META[c][1] for c in ordered)
    body = underline_prose(block)
    marker = "+".join(ordered).upper()
    return (
        f"<!-- PAPER1-ANNOTATION:{marker}-START -->\n"
        f"> [!{alert}]\n"
        f"> **{labels}**\n"
        ">\n"
        f"{body}\n"
        f"<!-- PAPER1-ANNOTATION:{marker}-END -->"
    )


def insert_header(text: str, spec: SourceSpec, sha256: str) -> str:
    header = f"""
> [!CAUTION]
> **COPIA ANOTADA PARA PAPER 1 — DERIVADO DE LECTURA, NO FUENTE CANÓNICA**
>
> Fuente canónica: `../../../../literature/library/articles/{spec.source}`
>
> Nota técnica: `../reading_notes/{spec.note}`
>
> SHA-256 del Markdown fuente al generar esta copia: `{sha256}`
>
> `IMPORTANT` = **1. Idea principal** · `TIP` = **2. Resultado numérico** · `NOTE` = **3. Metodología / prueba / supuesto**
>
> El texto científico se conserva; las únicas adiciones son esta cabecera y los callouts/subrayados. Para citas o verificación exacta, volver siempre al Markdown/PDF canónico.

""".lstrip()
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            pos = end + len("\n---\n")
            return text[:pos] + "\n" + header + text[pos:]
    return header + text


def annotate_source(spec: SourceSpec) -> tuple[str, dict[str, int], list[str]]:
    source_path = LIBRARY / spec.source
    note_path = NOTES_ROOT / spec.note
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    if not note_path.exists():
        raise FileNotFoundError(note_path)
    original = source_path.read_text(encoding="utf-8")
    blocks = split_blocks(original)
    matched: dict[int, list[str]] = {}
    diagnostics: list[str] = []
    for annotation in spec.annotations:
        idx, hits = find_block(blocks, annotation)
        matched.setdefault(idx, []).append(annotation.category)
        preview = normalize(blocks[idx])[:110]
        diagnostics.append(
            f"{annotation.category}: block={idx}, hits={hits}, preview={preview!r}"
        )
    for idx, categories in matched.items():
        blocks[idx] = wrap_block(blocks[idx], categories)
    annotated = "\n\n".join(blocks)
    sha256 = hashlib.sha256(original.encode("utf-8")).hexdigest()
    annotated = insert_header(annotated, spec, sha256)
    counts = {category: 0 for category in CATEGORY_META}
    for categories in matched.values():
        for category in set(categories):
            counts[category] += 1
    return annotated, counts, diagnostics


def render_readme() -> str:
    return """# Paper 1 — annotated source Markdown

This folder contains **generated, full-text reading copies** of the canonical extracted Markdown articles used most directly in Paper 1.

The canonical physical/source layer remains in `../../../../literature/library/`. These files are **derived annotations**, not new source records and not a replacement for the source PDF.

## Visual convention

GitHub-native alerts are used because they remain visible without custom CSS:

> [!IMPORTANT]
> **1 · IDEA PRINCIPAL** — the source passage carrying a main conceptual claim used in Paper 1.

> [!TIP]
> **2 · RESULTADO NUMÉRICO** — a source passage/table containing a result, effect size, test statistic, sample quantity or other numerical evidence.

> [!NOTE]
> **3 · METODOLOGÍA / PRUEBA / SUPUESTO** — design, statistical method, identification condition, measurement definition or explicit assumption.

Prose passages are additionally wrapped with `<u>...</u>`. Tables/code blocks are not underlined because doing so can break Markdown rendering.

## Scope

The initial collection is intentionally restricted to articles that already have technical evidence cards in `../reading_notes/`. This keeps every annotation traceable to an existing Paper 1 note.

`INDEX.md` lists the generated papers and annotation counts.

## Regeneration

Run from the repository root:

```bash
python literature_selected/notes_on_papers/_generate.py --write
```

Validation without writing:

```bash
python literature_selected/notes_on_papers/_generate.py --check
```

Do not hand-edit generated article copies. If an annotation is wrong or incomplete, edit `_generate.py` or the underlying technical reading note and regenerate.

## Citation rule

Use these copies for **reading/navigation**. For manuscript quotations, page-specific claims, tables, or final numerical verification, return to the canonical Markdown and source PDF.
"""


def render_index(rows: list[tuple[SourceSpec, dict[str, int]]]) -> str:
    lines = [
        "# Paper 1 — annotated papers index",
        "",
        "Generated full-text reading copies with inline Paper 1 signals.",
        "",
        "| Annotated paper | Technical note | Ideas | Numeric | Method / assumptions |",
        "|---|---|---:|---:|---:|",
    ]
    for spec, counts in rows:
        lines.append(
            f"| [{spec.source}]({spec.source}) "
            f"| [note](../reading_notes/{spec.note}) "
            f"| {counts['idea']} | {counts['numeric']} | {counts['method']} |"
        )
    lines.extend([
        "",
        "The source text remains canonical under `literature/library/articles/`; this index is a Paper 1 reading layer only.",
        "",
    ])
    return "\n".join(lines)


def generate(write: bool) -> None:
    rows: list[tuple[SourceSpec, dict[str, int]]] = []
    failures: list[str] = []
    for spec in SOURCES:
        try:
            annotated, counts, diagnostics = annotate_source(spec)
        except Exception as exc:
            failures.append(f"{spec.source}: {exc}")
            continue
        rows.append((spec, counts))
        print(spec.source)
        for diagnostic in diagnostics:
            print(f"  {diagnostic}")
        if write:
            (OUTPUT_DIR / spec.source).write_text(annotated, encoding="utf-8")
    if failures:
        raise RuntimeError("Annotation generation failed:\n- " + "\n- ".join(failures))
    if write:
        (OUTPUT_DIR / "README.md").write_text(render_readme(), encoding="utf-8")
        (OUTPUT_DIR / "INDEX.md").write_text(render_index(rows), encoding="utf-8")
    print(f"Validated {len(rows)} annotated Paper 1 source copies.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate annotated full-text Markdown reading copies for Paper 1."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Write generated Markdown files.")
    mode.add_argument("--check", action="store_true", help="Validate annotation anchors only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate(write=args.write or not args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
