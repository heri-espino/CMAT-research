"""Shared Matplotlib, Seaborn, and Plotly style configuration.

The functions in this module change plotting-library defaults only; they do not
construct cohorts, transform analytical data, or alter statistical estimands.
"""

from __future__ import annotations

DEFAULT_FONT_FAMILY = "CMU Serif"
FALLBACK_FONT_FAMILY = "Computer Modern"


def _resolve_font_family() -> str:
    """Return the installed Computer Modern family used in publication plots."""
    try:
        from matplotlib import font_manager
    except Exception:
        return FALLBACK_FONT_FAMILY

    try:
        font_manager.findfont(DEFAULT_FONT_FAMILY, fallback_to_default=False)
    except ValueError:
        return FALLBACK_FONT_FAMILY
    return DEFAULT_FONT_FAMILY


def mpl_apply() -> None:
    """Apply Seaborn's native ``whitegrid`` theme with CMU Serif text."""
    import seaborn as sns

    font_family = _resolve_font_family()
    sns.set_theme(
        style="whitegrid",
        font=font_family,
        rc={"font.family": [font_family, "DejaVu Serif"]},
    )

def set_style() -> None:
    """Apply the project Matplotlib and Seaborn plotting defaults.
    """
    mpl_apply()




def plotly_apply(
    palette: list[str] = ["#ffa600", "#ffd380"],
    fontsize: float = 18,
    fontstack: str = "CMU Serif, Computer Modern, serif",
) -> None:
    """Aplica un estilo personalizado a las gráficas de Plotly, poner:
    from style import plotly_apply
    plotly_apply()
    
    Parameters
    ----------
    palette : list[str], default=['#ffa600', '#ffd380']
        Plotly discrete color sequence used by the registered template.
    fontsize : float, default=18
        Base Plotly font size in points.
    fontstack : str, default="EB Garamond, Garamond, Georgia, 'Times New Roman', serif"
        CSS-style Computer Modern font stack used by Plotly text elements.
    """
    import pandas as pd
    pd.options.plotting.backend = "plotly"
    import plotly.io as pio
    pio.templates.default = "gridon"
    import plotly.graph_objects as go
    import plotly.express as px

    # Parte de 'gridon' y personalizaa
    base = pio.templates["gridon"]
    custom = go.layout.Template(base)

    font_stack = fontstack
    font_size = fontsize

    custom.layout.update(
    colorway=palette,                # Colores discretos por defecto
    font=dict(family=font_stack, size=font_size, color="#2b2b2b"),
    paper_bgcolor="#181818",
    plot_bgcolor="#181818",

    coloraxis=dict(colorscale="Blues"),  # Escala continua por defecto

    title=dict(font=dict(family=font_stack, size=font_size * 1.3, color="white")),
    xaxis=dict(title_font=dict(family=font_stack, size=font_size),
            tickfont=dict(family=font_stack, size=font_size * 0.857), 
            gridcolor="#e5e5e5", zerolinecolor="#cccccc", color="white"),
    yaxis=dict(title_font=dict(family=font_stack, size=font_size),
            tickfont=dict(family=font_stack, size=font_size * 0.857), 
            gridcolor="#e5e5e5", zerolinecolor="#cccccc", color="white"),
    legend=dict(font=dict(family=font_stack, size=font_size * 0.857, color="white"))
    )

    # Registra y usa como template global
    pio.templates["mi_tema"] = custom
    pio.templates.default = "mi_tema"

    # (Opcional) Defaults de Plotly Express
    px.defaults.template = "mi_tema"
    px.defaults.color_discrete_sequence = palette
    px.defaults.color_continuous_scale = "Blues"
