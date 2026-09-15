"""Shared Matplotlib, Seaborn, and Plotly style configuration.

The functions in this module change plotting-library defaults only; they do not
construct cohorts, transform analytical data, or alter statistical estimands.
"""

from __future__ import annotations

FONT_CANDIDATES = ("Libertinus Serif", "CMU Serif", "Latin Modern Roman", "DejaVu Serif")

# Seaborn's default ``deep`` palette, with the project blue in its first slot.
# Keeping the remaining colours preserves categorical distinctions in existing
# figures while making the primary series consistently use the CMAT navy.
CMAT_PALETTE = (
    "#00166c",
    "#dd8452",
    "#55a868",
    "#c44e52",
    "#8172b3",
    "#937860",
    "#da8bc3",
    "#8c8c8c",
    "#ccb974",
    "#64b5cd",
)


def _resolve_font_family() -> str:
    """Return the first available publication serif font family."""
    try:
        from matplotlib import font_manager
    except Exception:
        return "DejaVu Serif"

    # Matplotlib does not always discover fonts installed for the current
    # Windows user (rather than system-wide).  Register Libertinus explicitly
    # when it is available in the standard per-user Fonts directory.  Other
    # systems, and installations without Libertinus, continue to use the
    # portable fallbacks below.
    try:
        from os import environ
        from pathlib import Path

        user_fonts = Path(environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"
        for font_path in user_fonts.glob("LibertinusSerif-*.otf"):
            font_manager.fontManager.addfont(font_path)
    except (OSError, ValueError):
        pass

    for family in FONT_CANDIDATES:
        try:
            font_manager.findfont(family, fallback_to_default=False)
        except ValueError:
            continue
        return family
    return "DejaVu Serif"


def mpl_apply() -> None:
    """Apply a reproducible Seaborn whitegrid publication theme."""
    import seaborn as sns

    font_family = _resolve_font_family()
    sns.set_theme(
        context="paper",
        style="whitegrid",
        palette=CMAT_PALETTE,
        font=font_family,
        rc={
            # Libertinus Serif is used for publication text.  The fallbacks
            # cover mathematical Unicode glyphs not included in a font.
            "font.family": [font_family, "DejaVu Serif"],
            "font.serif": [
                font_family,
                "Libertinus Serif",
                "CMU Serif",
                "Latin Modern Roman",
                "DejaVu Serif",
            ],
            "mathtext.fontset": "cm",
            "axes.unicode_minus": False,
            "savefig.dpi": 300,
        },
    )


def set_style() -> None:
    """Apply the project Matplotlib and Seaborn plotting defaults."""
    mpl_apply()


def plotly_apply(
    palette: list[str] = ["#ffa600", "#ffd380"],
    fontsize: float = 18,
    fontstack: str = "Libertinus Serif, CMU Serif, Latin Modern Roman, DejaVu Serif, serif",
) -> None:
    """Apply a light Plotly template aligned with the publication figure style.

    Parameters
    ----------
    palette : list[str], default=['#ffa600', '#ffd380']
        Plotly discrete color sequence used by the registered template.
    fontsize : float, default=18
        Base Plotly font size in points.
    fontstack : str
        CSS-style serif font stack used by Plotly text elements.
    """
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio

    pd.options.plotting.backend = "plotly"
    base = pio.templates["plotly_white"]
    custom = go.layout.Template(base)
    custom.layout.update(
        colorway=palette,
        font=dict(family=fontstack, size=fontsize),
        paper_bgcolor="white",
        plot_bgcolor="white",
        coloraxis=dict(colorscale="Blues"),
        title=dict(font=dict(family=fontstack, size=fontsize * 1.3)),
        xaxis=dict(
            title_font=dict(family=fontstack, size=fontsize),
            tickfont=dict(family=fontstack, size=fontsize * 0.857),
        ),
        yaxis=dict(
            title_font=dict(family=fontstack, size=fontsize),
            tickfont=dict(family=fontstack, size=fontsize * 0.857),
        ),
        legend=dict(font=dict(family=fontstack, size=fontsize * 0.857)),
    )
    pio.templates["cmat_publication"] = custom
    pio.templates.default = "cmat_publication"
    px.defaults.template = "cmat_publication"
    px.defaults.color_discrete_sequence = palette
    px.defaults.color_continuous_scale = "Blues"
