from __future__ import annotations

from pathlib import Path
import math
import numpy as np
import pandas as pd


def _esc(x: object) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    s = str(x)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#")]:
        s = s.replace(a, b)
    return s


def _f(x: object, digits: int = 3, pct: bool = False) -> str:
    if x is None or pd.isna(x):
        return ""
    if isinstance(x, (int, np.integer)):
        return f"{int(x):,}"
    if isinstance(x, (float, np.floating)):
        x = float(x)
        if pct:
            return f"{100*x:.1f}\\%"
        if x != 0 and abs(x) < 0.001:
            return f"{x:.2e}"
        return f"{x:.{digits}f}"
    return _esc(x)


def _tab(headers: list[str], rows: list[list[str]], align: str) -> str:
    out = [f"\\begin{{tabular}}{{{align}}}", "\\toprule", " & ".join(headers) + " \\\\", "\\midrule"]
    out += [" & ".join(r) + " \\\\" for r in rows]
    out += ["\\bottomrule", "\\end{tabular}", ""]
    return "\n".join(out)


def _read(root: Path, name: str) -> pd.DataFrame:
    p = root / name
    if not p.exists():
        raise FileNotFoundError(f"Required methodology output missing: {p}")
    return pd.read_csv(p)


def write_methodology_table_snippets(generated_tables_dir: Path, report_tables_dir: Path) -> list[Path]:
    """Render report table snippets from already-computed aggregate CSV files."""
    src, dst = Path(generated_tables_dir), Path(report_tables_dir)
    dst.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    def w(name: str, headers: list[str], rows: list[list[str]], align: str) -> None:
        p = dst / name
        p.write_text(_tab(headers, rows, align), encoding="utf-8")
        written.append(p)

    d = _read(src, "01_cohort_flow.csv")
    w("latex_cohort_flow.tex", ["Etapa", "$N$"], [[_esc(r.stage), _f(r.n)] for r in d.itertuples()], "lr")

    d = _read(src, "50_imputation_audit.csv")
    d = d.groupby("method", dropna=False).agg(salones=("CLASSROOM_ID", "nunique"), outcomes=("n_adverse_imputed", "sum")).reset_index()
    w("latex_imputation_summary.tex", ["Método", "Salones", "Outcomes"], [[_esc(r.method), _f(r.salones), _f(r.outcomes)] for r in d.itertuples()], "lrr")

    d = _read(src, "03_continuation_probability.csv")
    d = d[(d.course == "Matemáticas Universitarias") & d.k.isin([0, 1, 2, 3])]
    w("latex_continuation_examples.tex", ["$k$", "$N_k$", "Continuación", "IC 95\\%"], [[_f(r.k), _f(r.n_at_risk), _f(r.continuation_probability, pct=True), f"[{_f(r.ci95_low, pct=True)}, {_f(r.ci95_high, pct=True)}]"] for r in d.itertuples()], "rrrr")

    d = _read(src, "68_peak_spacing_summary.csv")
    w("latex_peak_summary.tex", ["Población", "Periodos", "Picos med.", "Intervalos", "Brecha med.", "24--38 días"], [[_esc(r.population), _f(r.periods_analyzed), _f(r.median_detected_peaks_per_period, 1), _f(r.peak_intervals_n), _f(r.peak_gap_median_days, 1), _f(r.monthly_like_interval_proportion, pct=True)] for r in d.itertuples()], "lrrrrr")

    acf, per = _read(src, "69_monthly_cycle_autocorrelation.csv"), _read(src, "70_monthly_cycle_periodogram_by_term.csv")
    rows = []
    for pop in acf.population.dropna().unique():
        g = acf[(acf.population == pop) & (acf.SESSION == "POOLED")].dropna(subset=["autocorrelation"])
        if not g.empty:
            best = g.loc[g.autocorrelation.idxmax()]
            med = per.loc[per.population == pop, "dominant_period_days_21_42"].median()
            rows.append([_esc(pop), _f(best.lag_days), _f(best.autocorrelation), _f(med, 1)])
    w("latex_periodicity_summary.tex", ["Población", "Rezago ACF", "$r$", "Periodo med."], rows, "lrrr")

    def summary_table(csv: str, tex: str, group_col: str, first_header: str) -> None:
        q = _read(src, csv)
        w(tex, [first_header, "$N$", "Media $Z$", "IC 95\\%"], [[_esc(getattr(r, group_col)), _f(r.n), _f(r.mean_z), f"[{_f(r.ci95_low)}, {_f(r.ci95_high)}]"] for r in q.itertuples()], "lrrr")

    summary_table("80_exact_visit_groups_0_1_2_3_4plus_summary.csv", "latex_exact_groups_summary.tex", "group", "Visitas")
    summary_table("85_progressor4211_exact_visit_summary.csv", "latex_progressor_groups_summary.tex", "group", "Visitas MU")
    summary_table("93_exact_visit_counts_0_to_12_summary.csv", "latex_exact_counts_0_12.tex", "visits_exact", "Visitas")

    gh, fe = _read(src, "82_exact_visit_groups_games_howell_all_pairs.csv"), _read(src, "83_exact_visit_groups_FE_career_all_pairs.csv")
    d = gh.merge(fe, on=["group1", "group2"])
    w("latex_pairwise_all.tex", ["Par", "$\\Delta Z_{GH}$", "$p_{GH}$", "$\\Delta Z_{adj}$", "$p_{Holm}$"], [[f"{_esc(r.group1)} vs {_esc(r.group2)}", _f(r.mean_diff_group1_minus_group2), _f(r.games_howell_p), _f(r.adjusted_mean_difference_group1_minus_group2), _f(r.p_holm_10_pairwise)] for r in d.itertuples()], "lrrrr")

    g1, f1 = _read(src, "11_primary_robust_gt3_vs_le3.csv").iloc[0], _read(src, "12_primary_fixed_effect_models.csv")
    g2, f2 = _read(src, "15_ppa_reached_ge3_vs_lt3_robust.csv").iloc[0], _read(src, "16_ppa_reached_ge3_vs_lt3_fixed_effect.csv")
    a1, a2 = f1[f1.model == "classroom_FE_plus_career"].iloc[0], f2[f2.model == "classroom_FE_plus_career"].iloc[0]
    w("latex_binary_sensitivities.tex", ["Contraste", "$\\Delta Z$", "IC 95\\%", "$\\beta_{adj}$", "IC 95\\% adj."], [
        ["$V>3$ vs $V\\leq3$", _f(g1.mean_diff), f"[{_f(g1.mean_diff_ci95_low)}, {_f(g1.mean_diff_ci95_high)}]", _f(a1.estimate), f"[{_f(a1.ci95_low)}, {_f(a1.ci95_high)}]"],
        ["$V\\geq3$ vs $V<3$", _f(g2.mean_diff), f"[{_f(g2.mean_diff_ci95_low)}, {_f(g2.mean_diff_ci95_high)}]", _f(a2.estimate), f"[{_f(a2.ci95_low)}, {_f(a2.ci95_high)}]"],
    ], "lrrrr")

    d = _read(src, "20_secondary_pass_rate_by_group.csv")
    w("latex_pass_rates.tex", ["Grupo", "$N$", "Aprobación"], [[_esc(r.group), _f(r.n), _f(r.pass_rate, pct=True)] for r in d.itertuples()], "lrr")

    d = _read(src, "90_career_summary_three_populations.csv")
    rows = [[_esc(pop), _f(g.n.sum()), _f(len(g)), _f(g.included_n_ge_min.sum())] for pop, g in d.groupby("population", observed=True)]
    w("latex_career_populations.tex", ["Población", "$N$", "Carreras", "$n\\geq30$"], rows, "lrrr")

    d = _read(src, "92_career_use_vs_mean_z_ecological.csv")
    w("latex_career_ecological.tex", ["Población", "Carreras", "Pearson $r$", "Spearman $\\rho$", "Pendiente WLS"], [[_esc(r.population), _f(r.n_careers), _f(r.pearson_r_unweighted), _f(r.spearman_rho_unweighted), _f(r.weighted_slope_mean_z_per_unit_visit_rate)] for r in d.itertuples()], "lrrrr")

    d = _read(src, "30_longitudinal_persistence_to_calculus.csv")
    w("latex_longitudinal_4211.tex", ["Grupo MU", "$N$", "Uso Cálculo", "Media visitas", "Mediana"], [[_esc(r.mu_visit_group), _f(r.n), _f(r.any_calc_visit_proportion, pct=True), _f(r.mean_calc_visits), _f(r.median_calc_visits, 1)] for r in d.itertuples()], "lrrrr")

    d = _read(src, "91_omitted_careers_first_mu_n_lt30.csv")
    w("latex_omitted_careers.tex", ["Licenciatura", "$N$"], [[_esc(r.CLAVECARRERA), _f(r.n)] for r in d.itertuples()], "lr")

    d = _read(src, "72_temporal_regularity_performance_models.csv")
    w("latex_regularity_models.tex", ["Especificación", "Término", "$\\beta$", "IC 95\\%", "$p$", "$N$"], [[_esc(r.specification), _esc(r.term), _f(r.estimate), f"[{_f(r.ci95_low)}, {_f(r.ci95_high)}]", _f(r.p_value), _f(r.n)] for r in d.itertuples()], "llrrrr")

    return written
