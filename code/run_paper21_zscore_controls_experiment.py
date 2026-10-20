#!/usr/bin/env python3
"""Four comparable OLS adjustment specifications for standardized grades (Paper 2.1).

This is a sensitivity analysis; it does not modify the paper's canonical figures
or coefficient tables. The cohort is generated from the authorized raw data.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from run_paper21_model_controls_experiment import (
    ROOT, GROUPS, SPECS, PAIR_COUNT,
    prepare_cohort, estimate, _not_estimable_pairs, fmt,
)

OUTCOME = "Z_GRADE_PRIMARY"
OUTPUT = ROOT / "results" / "paper21" / "tables" / "adjustment_experiment"
NOTE = ROOT / "notes" / "17_RESULTADOS_OLS_ZSCORE_CONTROLES.md"
REFERENCE = ROOT / "results" / "paper21" / "tables" / "26a_zero_inclusive_7plus_pairwise_continuous.csv"


def estimate_four_z(frame: pd.DataFrame):
    """Fit A/B/C/D to the same complete-case population using clustered OLS."""
    d = prepare_cohort(frame, outcome_col=OUTCOME)
    pair_frames, diagnostics = [], []
    for code, fe, career, label in SPECS:
        print(f"Fitting standardized Z / model {code}: {label}", flush=True)
        pairs, diagnostic, model = estimate(
            d, code, fe, career, method="Z_OLS"
        )
        diagnostic["adjustment_label"] = label
        if model is not None:
            # Descriptive in-sample fit, NOT prospective predictive performance.
            predictions = np.asarray(model.predict(d), dtype=float)
            actual = d[OUTCOME].to_numpy(dtype=float)
            diagnostic["r_squared_in_sample"] = float(model.rsquared)
            diagnostic["adjusted_r_squared_in_sample"] = float(model.rsquared_adj)
            diagnostic["rmse_in_sample"] = float(
                np.sqrt(np.mean((actual - predictions) ** 2))
            )
        else:
            diagnostic["r_squared_in_sample"] = np.nan
            diagnostic["adjusted_r_squared_in_sample"] = np.nan
            diagnostic["rmse_in_sample"] = np.nan
        diagnostics.append(diagnostic)
        pair_frames.append(
            pairs if pairs is not None else _not_estimable_pairs(diagnostic)
        )
    return (
        pd.concat(pair_frames, ignore_index=True),
        pd.DataFrame(diagnostics),
        d,
    )


def audit_full_adjustment(pairs: pd.DataFrame) -> str:
    """Require D-OLS to reproduce all canonical 0/1/.../7+ Z contrasts."""
    if not REFERENCE.is_file():
        raise RuntimeError(
            "Canonical Z contrast CSV is unavailable. "
            "The sensitivity cannot be validated against Paper 2.1."
        )
    original = pd.read_csv(REFERENCE)
    full = pairs.loc[pairs["model"].eq("D") & pairs["method"].eq("Z_OLS")]
    if len(original) != PAIR_COUNT or len(full) != PAIR_COUNT:
        raise RuntimeError("Expected 28 contrasts in the canonical and new D Z models.")
    lookup = {(str(r.group_low), str(r.group_high)): float(r.estimate)
              for r in full.itertuples()}
    for row in original.itertuples():
        key = (str(row.group1), str(row.group2))
        # Canonical file reports group1 minus group2, while the experiment
        # deliberately uses higher-frequency minus lower-frequency throughout.
        reference_effect = -float(row.adjusted_difference_group1_minus_group2)
        if key not in lookup or not np.isclose(
            lookup[key], reference_effect, atol=1e-7, rtol=0
        ):
            raise RuntimeError(
                f"Z-OLS D does not reproduce canonical {key}: "
                "verify cohort and formula before interpreting results."
            )
    return "PASS: all 28 model D effects match the canonical Z analysis"


def interpretive_note(pairs: pd.DataFrame, models: pd.DataFrame,
                      sample: pd.DataFrame, audit: str) -> str:
    """Write a readable Markdown summary based exclusively on executed estimates."""
    desc = (sample.groupby("VISIT_GROUP", observed=False)[OUTCOME]
            .agg(["size", "mean", "std"]).reindex(GROUPS))
    lines = [
        "# 17 — Resultados OLS sobre Z-score: sensibilidad a los controles",
        "",
        "**Informe producido automáticamente al ejecutar las cuatro regresiones "
        "sobre la cohorte institucional autorizada.**",
        "",
        f"Verificación de reproducción: **{audit}**.",
        "",
        "## Objetivo",
        "",
        "Comparar las 28 diferencias de Z por pares entre ocho frecuencias "
        "(0/1/2/3/4/5/6/7+) mediante OLS con A: ningún ajuste; "
        "B: carrera; C: efectos fijos profesor-periodo; D: ambos. "
        "La muestra y la agrupación de errores estándar por profesor-periodo "
        "se mantienen constantes. Cada uno de los cuatro modelos tiene su propia "
        "familia Holm de 28 pruebas.",
        "",
        "## Estadísticas descriptivas observadas de Z",
        "",
        "| Frecuencia | N | Media Z | SD Z |",
        "|---|---:|---:|---:|",
    ]
    for g, row in desc.iterrows():
        lines.append(
            f"| {g} | {int(row['size'])} | "
            f"{fmt(row['mean'], 3)} | {fmt(row['std'], 3)} |"
        )
    lines += [
        "",
        "## Resultados de los cuatro modelos",
        "",
        "| Modelo | FE profesor-periodo | Carrera | R² (en muestra) | "
        "R² ajustado | RMSE (en muestra) | Estado | Holm significativos / 28 |",
        "|---|---|---|---:|---:|---:|---|---:|",
    ]
    for row in models.itertuples():
        rejected = (
            str(int(row.holm_rejections))
            if pd.notna(row.holm_rejections) else "ND"
        )
        lines.append(
            f"| {row.model} | {'Sí' if row.professor_period_FE else 'No'} | "
            f"{'Sí' if row.career_controls else 'No'} | "
            f"{fmt(row.r_squared_in_sample)} | "
            f"{fmt(row.adjusted_r_squared_in_sample)} | "
            f"{fmt(row.rmse_in_sample)} | {row.status} | {rejected} |"
        )
    lines += [
        "",
        "R² y RMSE aquí son **medidas de ajuste dentro de la muestra**, "
        "no predicciones evaluadas en estudiantes nuevos; los efectos fijos "
        "profesor-periodo pueden aumentar el ajuste sin mejorar la generalización "
        "a profesores o periodos no observados.",
        "",
        "## Contrastes relevantes: diferencias de medias condicionales en Z",
        "",
        "Cada coeficiente expresa **Z del grupo con más visitas menos Z del grupo "
        "con menos visitas**, en unidades de la desviación estándar usada por "
        "el estudio. Los IC del 95% y los valores p se basan en errores estándar "
        "agrupados por profesor-periodo.",
        "",
        "| Modelo | Comparación | Diferencia de Z | IC 95% | p Holm | ¿Rechazo? |",
        "|---|---|---:|---|---:|---|",
    ]
    selected_pairs = [("0", "1"), ("0", "7+"), ("1", "7+"),
                      ("2", "3"), ("3", "4"), ("6", "7+")]
    for code, _, _, _ in SPECS:
        subset = pairs.loc[pairs["model"].eq(code)]
        for low, high in selected_pairs:
            row = subset.loc[subset["group_low"].eq(low)
                             & subset["group_high"].eq(high)]
            if row.empty:
                lines.append(f"| {code} | {low} → {high} | ND | ND | ND | ND |")
                continue
            r = row.iloc[0]
            # The Holm column is "ND" for an entire invalid family.
            decision = (
                "Sí" if r["holm_reject"] is True or r["holm_reject"] == True
                else "No" if pd.notna(r["holm_reject"]) else "ND"
            )
            lines.append(
                f"| {code} | {low} → {high} | {fmt(r['estimate'])} | "
                f"[{fmt(r['ci95_low'])}, {fmt(r['ci95_high'])}] | "
                f"{fmt(r['p_holm'], 4)} | {decision} |"
            )
    lines += [
        "",
        "Los **28 contrastes** de cada especificación, incluidos los no "
        "mostrados aquí, están en el CSV; esta tabla no constituye una nueva "
        "selección de pruebas basada en significancia.",
        "",
        "## Comparación A frente a D",
        "",
    ]
    for low, high in [("0", "1"), ("1", "7+"), ("3", "4")]:
        parts = []
        for code in ("A", "D"):
            subset = pairs.loc[
                pairs["model"].eq(code) & pairs["group_low"].eq(low)
                & pairs["group_high"].eq(high)
            ]
            if subset.empty or subset.iloc[0]["inferential_status"] != "valid":
                parts.append(f"{code}: ND (inferencia no válida)")
            else:
                r = subset.iloc[0]
                parts.append(
                    f"{code}: ΔZ={fmt(r['estimate'])}, "
                    f"Holm p={fmt(r['p_holm'], 4)}"
                )
        lines.append(
            f"- **{low} → {high}:** " + "; ".join(parts)
            + ". Las diferencias entre ajustes no identifican efectos causales."
        )
    lines += [
        "",
        "## Diagnósticos y límites",
        "",
    ]
    for row in models.itertuples():
        if row.status != "valid":
            lines.append(
                f"- Modelo {row.model}: {row.status}. "
                f"{row.diagnostic}; advertencias={row.warning_classes}."
            )
    if models["status"].eq("valid").all():
        lines.append(
            "- Las cuatro especificaciones devolvieron 28 contrastes con "
            "covarianza robusta estimable y corrección Holm definida."
        )
    lines += [
        "",
        "**Z está estandarizada dentro del contexto profesor-periodo**; "
        "sus SD por frecuencia pueden diferir de 1. La variable Z usada "
        "en el paper incluye valores numéricos asignados a las bajas BV/RT/BA "
        "según el procedimiento previamente documentado, a diferencia de PASS. "
        "Por ello, una diferencia de Z puede depender en parte de cómo se "
        "imputaron esos estados; el contraste no equivale a una diferencia "
        "de calificaciones numéricas observadas únicamente.",
        "",
        "Los controles por carrera y profesor-periodo no resuelven la "
        "autoselección, las diferencias en preparación matemática previa ni "
        "la motivación por PPA1. Los umbrales 2|3 y 3|4 son descriptivos; "
        "ninguno prueba que PPA1 o una visita adicional produzcan la diferencia.",
        "",
        "Para valorar predicción futura habría que diseñar validación temporal "
        "o fuera de muestra con variables disponibles antes del desenlace, "
        "evitando fugas de información. Este experimento estima **asociaciones "
        "ajustadas**, no capacidad predictiva prospectiva.",
        "",
        "Este informe es una sensibilidad adicional. Se conserva la "
        "especificación principal originalmente declarada para el artículo.",
        "",
    ]
    return "\n".join(lines)


def cli() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--materias", type=Path)
    p.add_argument("--asesorias", type=Path)
    p.add_argument("--check", action="store_true")
    return p.parse_args()


def main() -> int:
    args = cli()
    if args.check:
        assert PAIR_COUNT == 28 and len(SPECS) == 4
        assert all(len(GROUPS) == 8 for _ in SPECS)
        print("Z sensitivity: four OLS specifications, 28 Holm pairs each.")
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
    for source_path in (config.materias_path, config.asesorias_path):
        if not source_path.is_file():
            raise SystemExit(f"Missing authorised input: {source_path}")

    source = load_and_clean_inputs(config)
    mu = add_primary_outcomes(build_study_cohorts(source, config)["mu_primary"], config)
    pairs, diagnostics, sample = estimate_four_z(mu)

    if len(sample) != 6627 or sample["CLASSROOM_ID"].nunique() != 190:
        raise RuntimeError(
            f"Z experiment sample differs from the paper: N={len(sample)}, "
            f"classrooms={sample['CLASSROOM_ID'].nunique()}. STOP."
        )
    verification = audit_full_adjustment(pairs)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    pairs.to_csv(OUTPUT / "z_pairwise_4ols.csv", index=False)
    diagnostics.to_csv(OUTPUT / "z_model_diagnostics_4ols.csv", index=False)
    NOTE.parent.mkdir(parents=True, exist_ok=True)
    NOTE.write_text(
        interpretive_note(pairs, diagnostics, sample, verification),
        encoding="utf-8"
    )

    print(verification)
    print(f"Pairwise CSV: {OUTPUT / 'z_pairwise_4ols.csv'}")
    print(f"Diagnostics CSV: {OUTPUT / 'z_model_diagnostics_4ols.csv'}")
    print(f"Markdown report: {NOTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
