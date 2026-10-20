#!/usr/bin/env python3
"""Paper 2.1: four adjustment specifications x LPM and logistic PASS models.

Separate sensitivity analysis; no existing paper tables are overwritten.
Only aggregate coefficients, contrasts, and model diagnostics leave this script.
"""
from __future__ import annotations

import argparse
import warnings
from dataclasses import replace
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "results" / "paper21" / "tables" / "adjustment_experiment"
NOTES_DIR = ROOT / "notes"
GROUPS = ("0", "1", "2", "3", "4", "5", "6", "7+")
SPECS = (
    ("A", False, False, "Sin controles"),
    ("B", False, True, "Solo carrera"),
    ("C", True, False, "Solo profesor-periodo"),
    ("D", True, True, "Profesor-periodo y carrera"),
)
PAIR_COUNT = len(GROUPS) * (len(GROUPS) - 1) // 2


def prepare_cohort(frame: pd.DataFrame) -> pd.DataFrame:
    """Identical complete-case cohort for all 8 models; retain cluster IDs."""
    required = ["PASS", "VISITS_CMAT_PERIOD", "CLASSROOM_ID", "CLAVECARRERA"]
    missing = set(required).difference(frame.columns)
    if missing:
        raise ValueError(f"Required columns missing: {sorted(missing)}")
    d = frame.dropna(subset=required).copy()
    d["PASS"] = pd.to_numeric(d["PASS"], errors="raise")
    if not d["PASS"].isin([0.0, 1.0]).all():
        raise ValueError("PASS must contain only zero and one")
    count = pd.to_numeric(d["VISITS_CMAT_PERIOD"], errors="raise")
    if (count < 0).any() or (count % 1 != 0).any():
        raise ValueError("Visits must be nonnegative integers")
    d["VISIT_GROUP"] = np.where(count >= 7, "7+", count.astype(int).astype(str))
    if set(d["VISIT_GROUP"]) != set(GROUPS):
        raise ValueError("All 8 visit categories must be present")
    d["VISIT_GROUP"] = pd.Categorical(d["VISIT_GROUP"], GROUPS, ordered=True)
    return d


def group_formula(has_fe: bool, has_career: bool) -> str:
    """Treatment-coded categories, with zero visits as the reference."""
    form = "PASS ~ C(VISIT_GROUP, Treatment(reference='0'))"
    if has_fe:
        form += " + C(CLASSROOM_ID)"
    if has_career:
        form += " + C(CLAVECARRERA)"
    return form


def _inference(model, method: str, code: str, n: int, n_clusters: int,
               has_fe: bool, has_career: bool, diagnostic: str):
    """28 estimates; Holm is defined ONLY when all 28 raw p-values are valid."""
    names = list(model.params.index)
    coeff = np.asarray(model.params, dtype=float)
    cov = np.asarray(model.cov_params(), dtype=float)
    term = "C(VISIT_GROUP, Treatment(reference='0'))"
    terms = {g: names.index(f"{term}[T.{g}]") for g in GROUPS[1:]}
    rows = []
    valid = True
    if not np.isfinite(coeff).all():
        valid = False
    for first, second in combinations(GROUPS, 2):
        contrast = np.zeros(len(names), dtype=float)
        if second != "0":
            contrast[terms[second]] += 1.0
        if first != "0":
            contrast[terms[first]] -= 1.0
        effect = float(contrast @ coeff)
        variance = float(contrast @ cov @ contrast)
        se = float(np.sqrt(variance)) if np.isfinite(variance) and variance > 0 else np.nan
        good = bool(np.isfinite(effect) and np.isfinite(se) and se > 0)
        valid = valid and good
        p = float(2 * norm.sf(abs(effect / se))) if good else np.nan
        lower = effect - 1.959963984540054 * se if good else np.nan
        upper = effect + 1.959963984540054 * se if good else np.nan
        rows.append({
            "model": code, "method": method, "group_low": first,
            "group_high": second, "contrast": "high_minus_low",
            "estimate": effect, "se_clustered": se, "ci95_low": lower,
            "ci95_high": upper, "p_raw": p, "p_holm": np.nan,
            "holm_reject": pd.NA,
            "effect_scale": "probability difference" if method == "LPM" else "log odds difference",
            "effect_pp": 100.0 * effect if method == "LPM" else np.nan,
            "odds_ratio": float(np.exp(effect)) if method == "logit" and -700 < effect < 700 else np.nan,
            "or_ci95_low": float(np.exp(lower)) if method == "logit" and np.isfinite(lower) and -700 < lower < 700 else np.nan,
            "or_ci95_high": float(np.exp(upper)) if method == "logit" and np.isfinite(upper) and -700 < upper < 700 else np.nan,
            "n": n, "clusters": n_clusters, "professor_period_FE": has_fe,
            "career_controls": has_career,
            "inferential_status": "pending",
        })
    if valid and len(rows) == PAIR_COUNT and all(np.isfinite(r["p_raw"]) for r in rows):
        reject, p_holm, _, _ = multipletests(
            [r["p_raw"] for r in rows], alpha=.05, method="holm"
        )
        for row, p_adj, is_reject in zip(rows, p_holm, reject):
            row["p_holm"] = float(p_adj)
            row["holm_reject"] = bool(is_reject)
            row["inferential_status"] = "valid"
        status = "valid"
    else:
        for row in rows:
            row["inferential_status"] = "not_estimable"
        status = "not_estimable"
    return pd.DataFrame(rows), status


def estimate(d: pd.DataFrame, code: str, has_fe: bool,
             has_career: bool, method: str):
    formula = group_formula(has_fe, has_career)
    n, clusters = len(d), int(d["CLASSROOM_ID"].nunique())
    warnings_seen = []
    model = None
    fitted_robust = False
    problem = ""
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            model = (
                smf.ols(formula, data=d).fit(
                    cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]}
                ) if method == "LPM" else
                smf.glm(formula, data=d, family=sm.families.Binomial()).fit(
                    cov_type="cluster",
                    cov_kwds={"groups": d["CLASSROOM_ID"]},
                    maxiter=200,
                )
            )
        warnings_seen = sorted({w.category.__name__ for w in caught})
        fitted_robust = True
    except (ValueError, np.linalg.LinAlgError, FloatingPointError,
            ZeroDivisionError) as error:
        problem = type(error).__name__ + ": " + str(error)[:120]
        # Fallback is used for point estimates ONLY; it must never
        # fabricate clustered p-values or Holm rejection indicators.
        try:
            model = (smf.ols(formula, data=d).fit()
                     if method == "LPM" else
                     smf.glm(formula, data=d, family=sm.families.Binomial()).fit(maxiter=200))
        except Exception as error2:
            problem += "; fallback: " + type(error2).__name__
    base = dict(model=code, method=method, formula=formula, n=n,
                clusters=clusters, professor_period_FE=has_fe,
                career_controls=has_career, covariance="cluster CLASSROOM_ID",
                converged=(bool(getattr(model, "converged", True))
                           if model is not None else False),
                robust_fitted=fitted_robust, warning_classes="; ".join(warnings_seen),
                diagnostic=problem, holm_rejections=pd.NA, valid_contrasts=0)
    if model is None:
        base["status"] = "fit_failed"
        return None, base, None
    if not fitted_robust or not base["converged"] or (
        method == "logit" and any("Separation" in w for w in warnings_seen)
    ):
        base["status"] = "no_valid_clustered_inference"
        base["diagnostic"] = (
            problem + ("; separation warning" if any(
                "Separation" in w for w in warnings_seen
            ) else "")
        )
        return None, base, model
    try:
        pairs, status = _inference(
            model, method, code, n, clusters, has_fe, has_career, problem
        )
    except (KeyError, ValueError, np.linalg.LinAlgError) as error:
        pairs = None
        status = "invalid_covariance_" + type(error).__name__
    base["status"] = status
    base["valid_contrasts"] = (
        int(np.isfinite(pairs["p_raw"]).sum()) if pairs is not None else 0
    )
    base["holm_rejections"] = (
        int(pairs["holm_reject"].eq(True).sum()) if status == "valid" else pd.NA
    )
    return pairs, base, model


def run_four_by_two(frame: pd.DataFrame):
    d = prepare_cohort(frame)
    pairs, status, estimates = [], [], []
    for method in ("LPM", "logit"):
        for code, fe, career, _ in SPECS:
            print(f"Fitting {method} / {code}...", flush=True)
            p, info, model = estimate(d, code, fe, career, method)
            status.append(info)
            if p is not None:
                pairs.append(p)
            # Do not calculate standardized probabilities after an invalid
            # logistic fit; output only the identified pairwise ORs.
    return (
        pd.concat(pairs, ignore_index=True) if pairs else pd.DataFrame(),
        pd.DataFrame(status),
        d,
    )


def check_reference_lpm(pairs: pd.DataFrame) -> str:
    """Audit model D LPM against the frozen canonical Holm point estimates."""
    src = ROOT / "results" / "paper21" / "tables" / "26k_zero_inclusive_7plus_pairwise_pass_lpm.csv"
    if not src.is_file():
        return "not_checked_reference_missing"
    ref = pd.read_csv(src)
    x = pairs.loc[pairs["method"].eq("LPM") & pairs["model"].eq("D")]
    if len(x) != PAIR_COUNT or len(ref) != PAIR_COUNT:
        raise RuntimeError("Full LPM D/reference have different contrast counts")
    current = {
        (str(r.group_low), str(r.group_high)): float(r.estimate)
        for r in x.itertuples()
    }
    for row in ref.itertuples():
        key = (str(row.group1), str(row.group2))
        if key not in current or not np.isclose(
            current[key], -float(row.adjusted_difference_group1_minus_group2),
            rtol=0, atol=1e-7
        ):
            raise RuntimeError(
                f"Model D LPM disagrees with canonical paper contrast {key}; "
                "do not publish until cohort, formula and preprocessing agree"
            )
    return "matched_all_28_reference_differences"


def fmt(value: object, decimals: int = 3) -> str:
    return f"{float(value):.{decimals}f}" if pd.notna(value) and np.isfinite(float(value)) else "ND"


def report(pairs: pd.DataFrame, models: pd.DataFrame, d: pd.DataFrame):
    counts = (d.groupby("VISIT_GROUP", observed=False)["PASS"]
              .agg(["size", "mean"]).reindex(GROUPS))
    lines = [
        "# Paper 2.1 — comparación de controles en LPM y logística",
        "",
        "**Resultados generados únicamente al ejecutar el script sobre datos institucionales autorizados.**",
        "Todos los modelos usan la misma muestra completa, PASS binario, ocho grupos 0/1/2/3/4/5/6/7+ y errores estándar agrupados por profesor-periodo.",
        "En cada modelo y método Holm se aplica a las 28 comparaciones, únicamente si las 28 pruebas son estimables.",
        "La omisión de controles no implica ausencia de dependencia intraclúster ni identifica causalidad.",
        "",
        "## Tamaños y tasas observadas",
        "| Visitas | N | PASS observado |",
        "|---|---:|---:|",
    ]
    for group, row in counts.iterrows():
        lines.append(f"| {group} | {int(row['size'])} | {100*float(row['mean']):.1f}% |")
    lines += [
        "",
        "## Estado de las ocho regresiones",
        "| Método | Modelo | FE profesor-periodo | Carrera | N | Estado inferencial | Holm significativos / 28 |",
        "|---|---|---|---|---:|---|---:|",
    ]
    for row in models.itertuples():
        h = row.holm_rejections if pd.notna(row.holm_rejections) else "ND"
        lines.append(f"| {row.method} | {row.model} | {'Sí' if row.professor_period_FE else 'No'} | "
                     f"{'Sí' if row.career_controls else 'No'} | {row.n} | {row.status} | {h} |")
    lines += [
        "",
        "## Comparaciones seleccionadas (grupo alto menos grupo bajo)",
        "Se preservan los 28 pares en el CSV. Los contrastes mostrados son 0–1, 0–7+, 1–7+ y 3–4. "
        "El 3–4 **no** es una prueba causal de PPA1.",
        "",
        "| Método | Modelo | Comparación | Diferencia PASS (pp) / OR | IC 95% | p Holm |",
        "|---|---|---|---|---|---|",
    ]
    for model_type in ("LPM", "logit"):
        for code, *_ in SPECS:
            select = (pairs.loc[pairs["method"].eq(model_type) & pairs["model"].eq(code)]
                      if not pairs.empty else pd.DataFrame())
            for low, high in [("0", "1"), ("0", "7+"), ("1", "7+"), ("3", "4")]:
                if select.empty:
                    lines.append(f"| {model_type} | {code} | {low} → {high} | ND | ND | ND |")
                    continue
                r = select.loc[select["group_low"].eq(low) & select["group_high"].eq(high)]
                if r.empty:
                    lines.append(f"| {model_type} | {code} | {low} → {high} | ND | ND | ND |")
                    continue
                v = r.iloc[0]
                est = (fmt(v["effect_pp"], 2) + " pp" if model_type == "LPM"
                       else "OR " + fmt(v["odds_ratio"], 2))
                lo = v["ci95_low"]*100 if model_type == "LPM" else v["or_ci95_low"]
                hi = v["ci95_high"]*100 if model_type == "LPM" else v["or_ci95_high"]
                lines.append(f"| {model_type} | {code} | {low} → {high} | {est} | "
                             f"[{fmt(lo, 2)}, {fmt(hi, 2)}] | {fmt(v['p_holm'], 4)} |")
    lines += [
        "",
        "## Cómo interpretar la comparación",
        "A = sin controles; B = solo carrera; C = solo efectos fijos profesor-periodo; D = ambos.",
        "El LPM expresa diferencias ajustadas de probabilidad en puntos porcentuales. "
        "La logística expresa **odds ratios condicionales**, no razones de probabilidades "
        "ni incrementos constantes en puntos porcentuales. "
        "Un OR más grande no implica automáticamente un efecto educativo más grande.",
        "Los cambios entre especificaciones pueden reflejar composición, falta de soporte, "
        "no colapsabilidad de las odds ratios o dificultades inferenciales. "
        "No atribuir el cambio de un valor p a un mecanismo causal sin mayor evidencia.",
        "Las familias Holm se mantienen separadas por especificación y método. "
        "Si un modelo tiene covarianza singular, fallos de separación o valores p indefinidos, "
        "los resultados afectados deben declararse ND, nunca significativos.",
        "",
        "## Diagnóstico y límites",
    ]
    for row in models.itertuples():
        if row.status != "valid":
            lines.append(f"- {row.method} {row.model}: {row.status}. "
                         f"{row.diagnostic}; warnings={row.warning_classes}.")
    if models["status"].eq("valid").all():
        lines.append("Todos los modelos devolvieron contrastes con incertidumbre finita.")
    lines += [
        "",
        "Los modelos no incorporan habilidad matemática previa ni motivación por PPA1; "
        "ninguna asociación constituye un efecto causal. "
        "No se ha modificado el modelo principal ni la inferencia del manuscrito.",
        "",
    ]
    return "\n".join(lines)


def cli():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--materias", type=Path, help="Institutionally authorised input")
    p.add_argument("--asesorias", type=Path, help="Institutionally authorised input")
    p.add_argument("--check", action="store_true", help="Validate contract without data")
    return p.parse_args()


def main():
    args = cli()
    if args.check:
        assert len(SPECS) == 4 and PAIR_COUNT == 28
        print("Adjustment experiment contract: four specifications x two models; 28 Holm pairs each.")
        return 0
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_primary_outcomes
    base = get_study_config(ROOT)
    config = replace(
        base,
        materias_path=(args.materias or base.materias_path).expanduser().resolve(),
        asesorias_path=(args.asesorias or base.asesorias_path).expanduser().resolve(),
    )
    for p in (config.materias_path, config.asesorias_path):
        if not p.is_file():
            raise SystemExit(f"Missing authorised input: {p}")
    source = load_and_clean_inputs(config)
    mu = add_primary_outcomes(build_study_cohorts(source, config)["mu_primary"], config)
    pairs, models, d = run_four_by_two(mu)
    reference_audit = check_reference_lpm(pairs)
    print(f"Canonical LPM D audit: {reference_audit}")
    if len(d) != 6627 or d["CLASSROOM_ID"].nunique() != 190:
        raise RuntimeError(
            f"Sample differs from paper: {len(d)} students, "
            f"{d['CLASSROOM_ID'].nunique()} professor-period clusters; "
            "STOP: inspect missingness/cohort rules before interpreting."
        )
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    pairs.to_csv(TABLE_DIR / "pass_pairwise_4x2.csv", index=False)
    models.to_csv(TABLE_DIR / "pass_model_diagnostics_4x2.csv", index=False)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    note_path = NOTES_DIR / "15_RESULTADOS_COMPARACION_LPM_LOGIT_CONTROLES.md"
    note_path.write_text(report(pairs, models, d), encoding="utf-8")
    print(f"Pairwise comparisons: {TABLE_DIR / 'pass_pairwise_4x2.csv'}")
    print(f"Diagnostics: {TABLE_DIR / 'pass_model_diagnostics_4x2.csv'}")
    print(f"Report: {note_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
