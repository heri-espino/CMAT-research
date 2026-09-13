#!/usr/bin/env python3
"""Exploratory Paper 2 analysis of professor-linked CMAT uptake.

This is intentionally an observational diagnostic, not an IV estimator. It asks
whether first-MU students' same-period CMAT use is strongly associated with the
instructor teaching MU, whether that association persists across terms, and
whether it is especially visible at the institutionally salient PPA threshold.

Only aggregate summaries are written to disk/stdout; professor identifiers are
not exported by this script.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

from cmat_analysis.cohorts import (
    build_study_cohorts,
    load_and_clean_inputs,
    normalize_session,
)
from cmat_analysis.config.study_config import get_study_config
from cmat_analysis.measures import add_primary_outcomes


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "results" / "exploratory" / "professor_encouragement"


def _weighted_corr(x: pd.Series, y: pd.Series, w: pd.Series) -> float:
    frame = pd.DataFrame({"x": x, "y": y, "w": w}).dropna()
    if len(frame) < 3 or frame["w"].sum() <= 0:
        return float("nan")
    ww = frame["w"].to_numpy(float)
    xx = frame["x"].to_numpy(float)
    yy = frame["y"].to_numpy(float)
    mx = np.average(xx, weights=ww)
    my = np.average(yy, weights=ww)
    cov = np.average((xx - mx) * (yy - my), weights=ww)
    vx = np.average((xx - mx) ** 2, weights=ww)
    vy = np.average((yy - my) ** 2, weights=ww)
    if vx <= 0 or vy <= 0:
        return float("nan")
    return float(cov / np.sqrt(vx * vy))


def _distribution(series: pd.Series) -> dict[str, float]:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return {}
    return {
        "min": float(s.min()),
        "p10": float(s.quantile(0.10)),
        "p25": float(s.quantile(0.25)),
        "median": float(s.median()),
        "p75": float(s.quantile(0.75)),
        "p90": float(s.quantile(0.90)),
        "max": float(s.max()),
        "sd": float(s.std(ddof=1)),
    }


def _nested_lpm(df: pd.DataFrame, outcome: str) -> dict[str, float | int | None]:
    work = df[[outcome, "PERIOD_LABEL", "CAREER", "CLAVEPROFESOR"]].dropna().copy()
    base = smf.ols(f"{outcome} ~ C(PERIOD_LABEL) + C(CAREER)", data=work).fit()
    full = smf.ols(
        f"{outcome} ~ C(PERIOD_LABEL) + C(CAREER) + C(CLAVEPROFESOR)",
        data=work,
    ).fit()
    f_stat, p_value, df_diff = full.compare_f_test(base)
    delta = float(full.rsquared - base.rsquared)
    partial = float(delta / (1.0 - base.rsquared)) if base.rsquared < 1 else float("nan")
    return {
        "n": int(len(work)),
        "r2_period_career": float(base.rsquared),
        "r2_plus_professor": float(full.rsquared),
        "delta_r2_professor": delta,
        "partial_r2_professor": partial,
        "joint_f": float(f_stat),
        "joint_df": int(df_diff),
        "joint_p": float(p_value),
    }


def _cluster_lpm(df: pd.DataFrame, outcome: str, score_col: str, extra: str = "") -> dict[str, float | int]:
    cols = [outcome, score_col, "PERIOD_LABEL", "CAREER", "CLAVEPROFESOR"]
    if extra:
        cols.append(extra)
    work = df[cols].dropna().copy()
    formula = f"{outcome} ~ {score_col} + C(PERIOD_LABEL) + C(CAREER)"
    if extra:
        formula += f" + {extra}"
    fit = smf.ols(formula, data=work).fit(
        cov_type="cluster", cov_kwds={"groups": work["CLAVEPROFESOR"]}
    )
    return {
        "n": int(len(work)),
        "professors": int(work["CLAVEPROFESOR"].nunique()),
        "coef": float(fit.params[score_col]),
        "se_cluster_professor": float(fit.bse[score_col]),
        "p": float(fit.pvalues[score_col]),
        "ci_low": float(fit.conf_int().loc[score_col, 0]),
        "ci_high": float(fit.conf_int().loc[score_col, 1]),
    }


def _attach_diagnostic(mu: pd.DataFrame) -> pd.DataFrame:
    path = REPO_ROOT / "data" / "controlled" / "Diagnostico_pseudonymized.csv"
    if not path.is_file():
        return mu.assign(DIAGNOSTIC_PERCENT=np.nan)
    d = pd.read_csv(path)
    required = {"student_id", "year", "period", "percentage"}
    if not required.issubset(d.columns):
        return mu.assign(DIAGNOSTIC_PERCENT=np.nan)
    d = d.copy()
    d["STUDENT_ID"] = d["student_id"].astype(str)
    d["YEAR"] = pd.to_numeric(d["year"], errors="coerce").astype("Int64")
    d["SESSION"] = d["period"].map(normalize_session)
    d["DIAGNOSTIC_PERCENT"] = pd.to_numeric(d["percentage"], errors="coerce")
    d = (
        d.dropna(subset=["STUDENT_ID", "YEAR", "SESSION", "DIAGNOSTIC_PERCENT"])
        .groupby(["STUDENT_ID", "YEAR", "SESSION"], as_index=False)["DIAGNOSTIC_PERCENT"]
        .mean()
    )
    out = mu.merge(d, on=["STUDENT_ID", "YEAR", "SESSION"], how="left")
    return out


def main() -> int:
    config = get_study_config(REPO_ROOT)
    data = load_and_clean_inputs(config)
    cohorts = build_study_cohorts(data, config)
    mu = add_primary_outcomes(cohorts["mu_primary"], config).copy()

    visits_col = "VISITS_CMAT_PERIOD" if config.primary_visit_measure != "course_specific" else "VISITS_COURSE"
    mu["ANY_USE"] = (mu[visits_col] > 0).astype(int)
    mu["PPA_GE3"] = (mu[visits_col] >= config.ppa_threshold).astype(int)
    mu["EXACT3"] = (mu[visits_col] == config.ppa_threshold).astype(int)
    mu["CAREER"] = mu["CLAVECARRERA"].fillna("MISSING").astype(str)
    mu["CLAVEPROFESOR"] = mu["CLAVEPROFESOR"].astype(str)

    classroom = (
        mu.groupby(["CLASSROOM_ID", "CLAVEPROFESOR", "PERIOD_LABEL"], as_index=False)
        .agg(
            n=("STUDENT_ID", "size"),
            any_users=("ANY_USE", "sum"),
            ppa_ge3=("PPA_GE3", "sum"),
            exact3=("EXACT3", "sum"),
            mean_visits=(visits_col, "mean"),
        )
    )
    classroom["any_rate"] = classroom["any_users"] / classroom["n"]
    classroom["ppa_rate"] = classroom["ppa_ge3"] / classroom["n"]
    classroom["exact3_rate"] = classroom["exact3"] / classroom["n"]
    classroom["any_overlap"] = (classroom["any_users"] > 0) & (classroom["any_users"] < classroom["n"])
    classroom["ppa_overlap"] = (classroom["ppa_ge3"] > 0) & (classroom["ppa_ge3"] < classroom["n"])

    professor = (
        mu.groupby("CLAVEPROFESOR", as_index=False)
        .agg(
            n=("STUDENT_ID", "size"),
            terms=("PERIOD_LABEL", "nunique"),
            any_users=("ANY_USE", "sum"),
            ppa_ge3=("PPA_GE3", "sum"),
            exact3=("EXACT3", "sum"),
        )
    )
    professor["any_rate"] = professor["any_users"] / professor["n"]
    professor["ppa_rate"] = professor["ppa_ge3"] / professor["n"]
    professor["exact3_rate"] = professor["exact3"] / professor["n"]

    # Leave-current-term-out professor propensity: a cross-term encouragement proxy.
    cell = classroom.copy()
    totals = professor.set_index("CLAVEPROFESOR")
    cell["other_n"] = cell.apply(lambda r: totals.loc[r.CLAVEPROFESOR, "n"] - r.n, axis=1)
    cell["loo_any_rate"] = cell.apply(
        lambda r: (totals.loc[r.CLAVEPROFESOR, "any_users"] - r.any_users) / r.other_n
        if r.other_n > 0 else np.nan,
        axis=1,
    )
    cell["loo_ppa_rate"] = cell.apply(
        lambda r: (totals.loc[r.CLAVEPROFESOR, "ppa_ge3"] - r.ppa_ge3) / r.other_n
        if r.other_n > 0 else np.nan,
        axis=1,
    )
    stable_cells = cell.loc[cell["other_n"] >= 30].copy()

    stable_any_corr = _weighted_corr(stable_cells["any_rate"], stable_cells["loo_any_rate"], stable_cells["n"])
    stable_ppa_corr = _weighted_corr(stable_cells["ppa_rate"], stable_cells["loo_ppa_rate"], stable_cells["n"])

    scores = stable_cells[["CLASSROOM_ID", "loo_any_rate", "loo_ppa_rate", "other_n"]].copy()
    if not scores.empty:
        scores["LOO_ANY_Z"] = (scores["loo_any_rate"] - scores["loo_any_rate"].mean()) / scores["loo_any_rate"].std(ddof=1)
        scores["LOO_PPA_Z"] = (scores["loo_ppa_rate"] - scores["loo_ppa_rate"].mean()) / scores["loo_ppa_rate"].std(ddof=1)
        # Quartiles are defined over professor-period cells, not individual students.
        scores["encouragement_quartile"] = pd.qcut(
            scores["loo_any_rate"].rank(method="first"), 4, labels=["Q1", "Q2", "Q3", "Q4"]
        )
    scored = mu.merge(scores, on="CLASSROOM_ID", how="inner")

    quartiles = (
        scored.groupby("encouragement_quartile", observed=True)
        .agg(
            n=("STUDENT_ID", "size"),
            any_rate=("ANY_USE", "mean"),
            ppa_rate=("PPA_GE3", "mean"),
            exact3_rate=("EXACT3", "mean"),
            mean_visits=(visits_col, "mean"),
        )
        .reset_index()
    ) if not scored.empty else pd.DataFrame()

    any_cross = _cluster_lpm(scored, "ANY_USE", "LOO_ANY_Z") if not scored.empty else {}
    ppa_cross = _cluster_lpm(scored, "PPA_GE3", "LOO_PPA_Z") if not scored.empty else {}

    # Same student-term diagnostic score sensitivity, where available.
    scored_diag = _attach_diagnostic(scored)
    any_diag = (
        _cluster_lpm(scored_diag, "ANY_USE", "LOO_ANY_Z", extra="DIAGNOSTIC_PERCENT")
        if scored_diag["DIAGNOSTIC_PERCENT"].notna().sum() >= 100
        else {}
    )
    ppa_diag = (
        _cluster_lpm(scored_diag, "PPA_GE3", "LOO_PPA_Z", extra="DIAGNOSTIC_PERCENT")
        if scored_diag["DIAGNOSTIC_PERCENT"].notna().sum() >= 100
        else {}
    )

    prof_filtered = professor.loc[professor["n"] >= 50].copy()
    summary = {
        "population": {
            "n_students": int(len(mu)),
            "n_professors": int(mu["CLAVEPROFESOR"].nunique()),
            "n_classrooms_professor_period": int(mu["CLASSROOM_ID"].nunique()),
            "overall_any_use_rate": float(mu["ANY_USE"].mean()),
            "overall_ppa_ge3_rate": float(mu["PPA_GE3"].mean()),
            "overall_exact3_rate": float(mu["EXACT3"].mean()),
        },
        "classroom_overlap": {
            "any_use_mixed_classrooms": int(classroom["any_overlap"].sum()),
            "any_use_mixed_share": float(classroom["any_overlap"].mean()),
            "students_in_any_use_mixed_classrooms": int(mu["CLASSROOM_ID"].isin(classroom.loc[classroom["any_overlap"], "CLASSROOM_ID"]).sum()),
            "ppa_mixed_classrooms": int(classroom["ppa_overlap"].sum()),
            "ppa_mixed_share": float(classroom["ppa_overlap"].mean()),
        },
        "classroom_rate_distribution": {
            "any_use": _distribution(classroom["any_rate"]),
            "ppa_ge3": _distribution(classroom["ppa_rate"]),
        },
        "professor_rate_distribution_min50_students": {
            "n_professors": int(len(prof_filtered)),
            "any_use": _distribution(prof_filtered["any_rate"]),
            "ppa_ge3": _distribution(prof_filtered["ppa_rate"]),
        },
        "professor_fixed_effect_increment": {
            "any_use": _nested_lpm(mu, "ANY_USE"),
            "ppa_ge3": _nested_lpm(mu, "PPA_GE3"),
        },
        "cross_term_stability": {
            "eligible_professor_period_cells": int(len(stable_cells)),
            "eligible_professors": int(stable_cells["CLAVEPROFESOR"].nunique()),
            "weighted_corr_current_any_vs_leave_term_out_any": stable_any_corr,
            "weighted_corr_current_ppa_vs_leave_term_out_ppa": stable_ppa_corr,
        },
        "cross_term_encouragement_lpm": {
            "any_use_per_1sd_leaveout_professor_propensity": any_cross,
            "ppa_ge3_per_1sd_leaveout_professor_propensity": ppa_cross,
        },
        "diagnostic_adjusted_subset": {
            "diagnostic_n": int(scored_diag["DIAGNOSTIC_PERCENT"].notna().sum()),
            "any_use": any_diag,
            "ppa_ge3": ppa_diag,
        },
        "encouragement_quartiles": quartiles.to_dict(orient="records") if not quartiles.empty else [],
        "iv_warning": {
            "professor_propensity_varies_at_classroom_level": True,
            "primary_Z_is_centered_within_professor_period_classroom": True,
            "implication": "A professor-level encouragement proxy has zero reduced-form covariance with the classroom-centered Z outcome by construction; professor identity also has a direct path to learning/grading, so it is not a defensible instrument for the current outcome/design.",
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "summary.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("PROFESSOR_ENCOURAGEMENT_SUMMARY_BEGIN")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("PROFESSOR_ENCOURAGEMENT_SUMMARY_END")
    print(f"Wrote aggregate summary: {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
