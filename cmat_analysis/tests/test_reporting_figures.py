"""Tests for reusable reporting figure helpers."""

from __future__ import annotations

import matplotlib.pyplot as plt

from cmat_analysis.reporting import save_figure_variants


def test_save_figure_variants_writes_pdf_and_png(tmp_path) -> None:
    """Write both variants in a deterministic order and close the figure."""
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    number = fig.number

    created = save_figure_variants(fig, tmp_path / "nested", "example")

    assert created == [
        tmp_path / "nested" / "example.pdf",
        tmp_path / "nested" / "example.png",
    ]
    assert all(path.is_file() and path.stat().st_size > 0 for path in created)
    assert number not in plt.get_fignums()
