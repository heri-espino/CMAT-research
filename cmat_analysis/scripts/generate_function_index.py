"""Generate a compact searchable index of Python symbols in the active code tree.

The generated Markdown is intended for humans and AI agents. It is deliberately
cheap to search so new work starts by reusing existing functions rather than
reimplementing them.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = CODE_ROOT / "FUNCTION_INDEX.md"
SKIP_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv", "outputs"}


CAPABILITY_MAP = [
    ("Cohorts, real attempts, revalidations, visit grouping", "cohort attempt revalidation visit group", "src/cmat_analysis/study/cohort.py"),
    ("Study outcomes, classroom-relative grades, adverse-state imputation", "outcome grade z-score classroom imputation KDE", "src/cmat_analysis/study/outcomes.py"),
    ("PPA / MU→Calculus persistence and longitudinal models", "PPA persistence calculus longitudinal transition threshold", "src/cmat_analysis/study/ppa_progression.py"),
    ("Study-level statistical tests and confidence intervals", "statistics CI odds risk Welch Games-Howell effect", "src/cmat_analysis/study/statistics.py"),
    ("Selection adjustment / weighting", "selection propensity weighting balance", "src/cmat_analysis/study/selection.py"),
    ("Temporal patterns, peaks, spacing, periodicity", "temporal peak spacing periodicity ACF", "src/cmat_analysis/study/temporal.py"),
    ("Extended degree-programme and visit-count analyses", "career degree programme exact visits extended", "src/cmat_analysis/study/extended_analysis.py"),
    ("Main publication-study orchestration", "pipeline study run outputs tables figures", "src/cmat_analysis/study/pipeline.py"),
    ("General data cleaning / legacy-compatible analysis helpers", "clean normalize transform grades visits", "src/cmat_analysis/analysis/cleaning.py"),
    ("Parametric and non-parametric tests", "anova t-test kruskal mann-whitney ks nonparametric", "src/cmat_analysis/analysis/parametric_tests.py; src/cmat_analysis/analysis/nonparametric_tests.py"),
    ("Report-compatible imputation and historical figures", "report compatible KDE imputation professor cluster figure", "src/cmat_analysis/analysis/report_compatible/"),
    ("Reporting metrics, tables, rendering and plots", "report metrics render table plot assets", "src/cmat_analysis/reporting/"),
    ("Privacy / pseudonymisation / release helpers", "privacy identifier HMAC anonymized release", "src/cmat_analysis/privacy.py; src/create_anonymized_release.py"),
    ("Figure release and LaTeX release preparation", "release figure latex copy", "src/cmat_analysis/release_figures.py; src/prepare_release_latex.py"),
    ("Entry points and command-line runners", "CLI run analysis study figures", "src/run_analysis.py; src/run_study.py; src/generador_figuras_cli.py"),
]


@dataclass
class Symbol:
    path: str
    qualname: str
    kind: str
    line: int
    signature: str
    summary: str
    tags: str
    is_test: bool


def _first_doc_line(node: ast.AST) -> str:
    doc = ast.get_docstring(node, clean=True)
    if not doc:
        return "No docstring; inspect implementation before reuse."
    text = " ".join(doc.strip().split())
    return text.split(". ", 1)[0].rstrip(".") + ("." if text else "")


def _signature(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> str:
    if isinstance(node, ast.ClassDef):
        bases = ", ".join(ast.unparse(x) for x in node.bases)
        return f"class {node.name}({bases})" if bases else f"class {node.name}"
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    args = ast.unparse(node.args)
    result = f"{prefix} {node.name}({args})"
    if node.returns is not None:
        result += f" -> {ast.unparse(node.returns)}"
    return result


def _tags(path: str, qualname: str, summary: str) -> str:
    raw = " ".join([path.replace("/", " "), qualname.replace(".", " "), summary])
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9_+-]*", raw.lower())
    stop = {"def", "class", "none", "the", "and", "for", "with", "from", "into", "this", "that", "before", "after", "implementation", "inspect", "docstring", "reuse"}
    unique = []
    for token in tokens:
        if token not in stop and token not in unique:
            unique.append(token)
    return " ".join(unique[:14])


class SymbolVisitor(ast.NodeVisitor):
    def __init__(self, relpath: str, is_test: bool) -> None:
        self.relpath = relpath
        self.is_test = is_test
        self.stack: list[tuple[str, str]] = []
        self.symbols: list[Symbol] = []

    def _qualname(self, name: str) -> str:
        parts = [item[0] for item in self.stack]
        if self.stack and self.stack[-1][1] in {"function", "async function"}:
            parts.append("<locals>")
        return ".".join(parts + [name]) if parts else name

    def _add(self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, kind: str) -> None:
        qualname = self._qualname(node.name)
        summary = _first_doc_line(node)
        self.symbols.append(
            Symbol(
                path=self.relpath,
                qualname=qualname,
                kind=kind,
                line=node.lineno,
                signature=_signature(node),
                summary=summary,
                tags=_tags(self.relpath, qualname, summary),
                is_test=self.is_test,
            )
        )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._add(node, "class")
        self.stack.append((node.name, "class"))
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        kind = "method" if self.stack and self.stack[-1][1] == "class" else "function"
        self._add(node, kind)
        self.stack.append((node.name, "function"))
        self.generic_visit(node)
        self.stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        kind = "async method" if self.stack and self.stack[-1][1] == "class" else "async function"
        self._add(node, kind)
        self.stack.append((node.name, "async function"))
        self.generic_visit(node)
        self.stack.pop()


def _python_files() -> list[Path]:
    files = []
    for path in CODE_ROOT.rglob("*.py"):
        rel = path.relative_to(CODE_ROOT)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(CODE_ROOT).as_posix())


def collect_symbols() -> tuple[list[Path], list[Symbol], list[str]]:
    files = _python_files()
    symbols: list[Symbol] = []
    errors: list[str] = []
    for path in files:
        rel = path.relative_to(CODE_ROOT).as_posix()
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=rel)
        except (OSError, SyntaxError, UnicodeError) as exc:
            errors.append(f"{rel}: {exc}")
            continue
        visitor = SymbolVisitor(rel, rel.startswith("tests/") or "/tests/" in rel)
        visitor.visit(tree)
        symbols.extend(visitor.symbols)
    return files, symbols, errors


def _escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_index(files: list[Path], symbols: list[Symbol], errors: list[str]) -> str:
    reusable = [s for s in symbols if not s.is_test]
    tests = [s for s in symbols if s.is_test]
    lines = [
        "# Python function and symbol index",
        "",
        "> **Canonical search index for `cmat_analysis/`.** Before writing a new function, search this file by concept, symbol name, or tag, then inspect the referenced implementation. The index is generated from the Python AST; descriptions come from docstrings when available.",
        "",
        "## Before writing new code",
        "",
        "1. Search this file for the intended capability (for example `revalidation`, `Games-Howell`, `persistence`, `KDE`, `career`, `privacy`).",
        "2. Open the most relevant existing symbol and its nearby helpers.",
        "3. Prefer extending/reusing an existing function over creating a parallel implementation.",
        "4. If a genuinely new symbol is required, add or improve its docstring.",
        "5. Regenerate this index with `python scripts/generate_function_index.py` and include the updated index in the same commit.",
        "",
        "## Capability map",
        "",
        "| Capability | Search terms | Start here |",
        "|---|---|---|",
    ]
    for capability, terms, paths in CAPABILITY_MAP:
        lines.append(f"| {_escape(capability)} | `{_escape(terms)}` | `{_escape(paths)}` |")
    lines += [
        "",
        "## Inventory summary",
        "",
        f"- Python files scanned: **{len(files)}**",
        f"- Reusable/source symbols: **{len(reusable)}**",
        f"- Test symbols: **{len(tests)}**",
        f"- Total functions/classes/methods/nested functions: **{len(symbols)}**",
        "",
        "Private helpers whose names begin with `_` are included because they often contain reusable project logic even when they are not part of the public API.",
        "",
        "## Reusable/source symbols by module",
        "",
    ]

    by_path: dict[str, list[Symbol]] = {}
    for symbol in reusable:
        by_path.setdefault(symbol.path, []).append(symbol)
    for path in sorted(by_path):
        lines += [f"### `{path}`", "", "| Symbol | Kind | Line | Signature | Purpose | Search tags |", "|---|---|---:|---|---|---|"]
        for s in sorted(by_path[path], key=lambda x: (x.line, x.qualname)):
            lines.append(f"| `{_escape(s.qualname)}` | {s.kind} | {s.line} | `{_escape(s.signature)}` | {_escape(s.summary)} | `{_escape(s.tags)}` |")
        lines.append("")

    lines += [
        "## Test symbols",
        "",
        "These are indexed for completeness and for locating existing coverage, but they are **not** reuse candidates for production analysis.",
        "",
    ]
    test_by_path: dict[str, list[Symbol]] = {}
    for symbol in tests:
        test_by_path.setdefault(symbol.path, []).append(symbol)
    for path in sorted(test_by_path):
        lines += [f"### `{path}`", "", "| Symbol | Kind | Line | Purpose / test intent |", "|---|---|---:|---|"]
        for s in sorted(test_by_path[path], key=lambda x: (x.line, x.qualname)):
            lines.append(f"| `{_escape(s.qualname)}` | {s.kind} | {s.line} | {_escape(s.summary)} |")
        lines.append("")

    if errors:
        lines += ["## Parse warnings", ""] + [f"- `{_escape(err)}`" for err in errors] + [""]
    else:
        lines += ["## Parse status", "", "All scanned Python files parsed successfully.", ""]

    lines += [
        "## Maintenance",
        "",
        "This file is generated. Do not hand-edit symbol tables. Edit `scripts/generate_function_index.py` if the format or capability map needs to change, then regenerate.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    files, symbols, errors = collect_symbols()
    OUTPUT.write_text(render_index(files, symbols, errors), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(CODE_ROOT)}: {len(files)} files, {len(symbols)} symbols, {len(errors)} parse warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
