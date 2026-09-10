"""Generate the searchable Python symbol inventory for ``cmat_analysis``."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = CODE_ROOT / "FUNCTION_INDEX.md"
SKIP_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv", "outputs", "_build"}

CAPABILITY_MAP = [
    ("Input reading", "input Excel source validation", "src/cmat_analysis/io/"),
    ("Cleaning and preprocessing", "clean normalize transform", "src/cmat_analysis/preprocessing/"),
    ("Cohorts and attempts", "cohort attempt revalidation visit group", "src/cmat_analysis/cohorts/"),
    ("Academic measures", "grade pass classroom z-score imputation", "src/cmat_analysis/measures/"),
    ("Statistical inference", "statistics CI fixed effect robust propensity weighting", "src/cmat_analysis/statistics/"),
    ("Longitudinal diagnostics", "temporal peak spacing periodicity transition", "src/cmat_analysis/longitudinal/"),
    ("PPA progression and persistence", "PPA persistence calculus threshold progression", "src/cmat_analysis/ppa/"),
    ("Visualization", "figure plot style", "src/cmat_analysis/visualization/"),
    ("Reporting and provenance", "report table formatting provenance log", "src/cmat_analysis/reporting/"),
    ("Privacy", "privacy identifier HMAC anonymized", "src/cmat_analysis/privacy.py"),
    ("Compatibility/orchestration", "legacy historical pipeline report", "src/cmat_analysis/analysis/; src/cmat_analysis/study/; src/cmat_analysis/pipeline/"),
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


def _summary(node: ast.AST) -> str:
    doc = ast.get_docstring(node, clean=True)
    if not doc:
        return "No docstring; inspect implementation before reuse."
    first = " ".join(doc.strip().split()).split(". ", 1)[0].rstrip(".")
    return first + "."


def _signature(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> str:
    if isinstance(node, ast.ClassDef):
        bases = ", ".join(ast.unparse(base) for base in node.bases)
        return f"class {node.name}({bases})" if bases else f"class {node.name}"
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    result = f"{prefix} {node.name}({ast.unparse(node.args)})"
    if node.returns is not None:
        result += f" -> {ast.unparse(node.returns)}"
    return result


def _tags(path: str, qualname: str, summary: str) -> str:
    raw = f"{path.replace('/', ' ')} {qualname.replace('.', ' ')} {summary}".lower()
    tokens = re.findall(r"[a-z][a-z0-9_+-]*", raw)
    stop = {"def", "class", "the", "and", "for", "with", "from", "into", "this", "that", "no", "docstring", "inspect", "implementation", "before", "reuse"}
    unique: list[str] = []
    for token in tokens:
        if token not in stop and token not in unique:
            unique.append(token)
    return " ".join(unique[:14])


class Visitor(ast.NodeVisitor):
    def __init__(self, path: str, is_test: bool) -> None:
        self.path = path
        self.is_test = is_test
        self.stack: list[tuple[str, str]] = []
        self.symbols: list[Symbol] = []

    def _qualname(self, name: str) -> str:
        parts = [name_ for name_, _ in self.stack]
        if self.stack and self.stack[-1][1] in {"function", "async function"}:
            parts.append("<locals>")
        return ".".join(parts + [name]) if parts else name

    def _add(self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, kind: str) -> None:
        qualname = self._qualname(node.name)
        summary = _summary(node)
        self.symbols.append(Symbol(self.path, qualname, kind, node.lineno, _signature(node), summary, _tags(self.path, qualname, summary), self.is_test))

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


def collect() -> tuple[list[Path], list[Symbol], list[str]]:
    files = sorted(
        path for path in CODE_ROOT.rglob("*.py")
        if not any(part in SKIP_PARTS for part in path.relative_to(CODE_ROOT).parts)
    )
    symbols: list[Symbol] = []
    errors: list[str] = []
    for path in files:
        rel = path.relative_to(CODE_ROOT).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        except (OSError, SyntaxError, UnicodeError) as exc:
            errors.append(f"{rel}: {exc}")
            continue
        visitor = Visitor(rel, rel.startswith("tests/") or "/tests/" in rel)
        visitor.visit(tree)
        symbols.extend(visitor.symbols)
    return files, symbols, errors


def _escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render(files: list[Path], symbols: list[Symbol], errors: list[str]) -> str:
    reusable = [symbol for symbol in symbols if not symbol.is_test]
    tests = [symbol for symbol in symbols if symbol.is_test]
    lines = [
        "# Python function and symbol index",
        "",
        "> **Generated development inventory.** Search this file before creating a parallel implementation. User/developer API documentation lives in Sphinx under `docs/`.",
        "",
        "## Capability map",
        "",
        "| Capability | Search terms | Canonical path |",
        "|---|---|---|",
    ]
    lines.extend(f"| {name} | `{terms}` | `{path}` |" for name, terms, path in CAPABILITY_MAP)
    lines += ["", "## Inventory", "", f"- Python files scanned: **{len(files)}**", f"- Reusable symbols: **{len(reusable)}**", f"- Test symbols: **{len(tests)}**", ""]
    if errors:
        lines += ["## Parse errors", ""] + [f"- `{error}`" for error in errors] + [""]
    for is_test, heading in ((False, "Reusable symbols"), (True, "Test symbols")):
        lines += [f"## {heading}", ""]
        by_path: dict[str, list[Symbol]] = {}
        for symbol in symbols:
            if symbol.is_test == is_test:
                by_path.setdefault(symbol.path, []).append(symbol)
        for path in sorted(by_path):
            lines += [f"### `{path}`", "", "| Symbol | Kind | Line | Signature | Summary | Tags |", "|---|---|---:|---|---|---|"]
            for symbol in by_path[path]:
                lines.append(f"| `{_escape(symbol.qualname)}` | {symbol.kind} | {symbol.line} | `{_escape(symbol.signature)}` | {_escape(symbol.summary)} | `{_escape(symbol.tags)}` |")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    files, symbols, errors = collect()
    OUTPUT.write_text(render(files, symbols, errors), encoding="utf-8")
    print(f"Wrote {OUTPUT} from {len(files)} Python files.")


if __name__ == "__main__":
    main()
