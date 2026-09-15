"""Reusable figure-output helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def save_figure_variants(
    fig: plt.Figure,
    output_dir: Path,
    stem: str,
) -> list[Path]:
    """Save a Matplotlib figure as both PDF and PNG.

    This helper restores the reusable output behavior from the historical
    ``proyecto_visitas`` analysis without changing the current PDF-only
    production plotting pipeline. The destination directory is created when
    needed, the PDF is written first, and the figure is closed after both
    variants are saved.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save and close.
    output_dir : pathlib.Path
        Directory in which the two files are created.
    stem : str
        Filename stem without an extension.

    Returns
    -------
    list[pathlib.Path]
        Paths to the created files in ``[PDF, PNG]`` order.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for suffix in (".pdf", ".png"):
        path = output_dir / f"{stem}{suffix}"
        fig.savefig(path, bbox_inches="tight")
        created.append(path)
    plt.close(fig)
    return created
