"""Backward-compatible wrapper for the dependency-aware Paper 2.1 builder.

Prefer:
    python paper/paper_build.py [--tables] [--figures] [--paper]
"""

from paper_build import main


if __name__ == "__main__":
    raise SystemExit(main())
