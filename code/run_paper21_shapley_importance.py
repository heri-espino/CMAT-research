#!/usr/bin/env python3
"""Exact grouped Shapley importance for Paper 2.1; descriptive and held-out.

No student-level rows are exported. In-sample relative importance is *not*
prospective predictive accuracy or a causal attribution.
"""
from __future__ import annotations

import argparse
import math
import warnings
from dataclasses import replace
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tools.sm_exceptions import PerfectSeparationWarning
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

from run_paper21_model_controls_experiment import ROOT, SPECS, prepare_cohort

DEST = ROOT / "results/paper21/tables/shapley_importance"
NOTE = ROOT / "notes/19_SHAPLEY_PREDICTIVE_IMPORTANCE.md"

# Treat entire one-hot-encoded categorical factors as indivisible players.
# Otherwise a 190-level professor-period variable receives 189 'votes'.
BLOCKS = {
    "attendance": "C(VISIT_GROUP, Treatment(reference='0'))",
    "degree": "C(CLAVECARRERA)",
    "professor_period": "C(CLASSROOM_ID)",
}
METHODS = (
    ("Z_GRADE_PRIMARY", "Z_OLS", "r2_in_sample"),
    ("PASS", "PASS_LPM", "r2_in_sample"),
    ("PASS", "PASS_LOGIT", "mcfadden_pseudo_r2_in_sample"),
)
MODEL_BLOCKS = {
    code: tuple(b for b, allowed in (
        ("attendance", True),
        ("degree", has_degree),
        ("professor_period", has_context),
    ) if allowed)
    for code, has_context, has_degree, _ in SPECS
}
CV_BLOCKS = ("attendance", "degree")
CV_COLUMNS = {"attendance": "VISIT_GROUP", "degree": "CLAVECARRERA"}


def coalitions(players: tuple[str, ...]):
    """Every subset, including the intercept-only model."""
    for k in range(len(players) + 1):
        yield from combinations(players, k)


def shapley(players: tuple[str, ...], values: dict[tuple[str, ...], float]):
    """Exact factorial-weighted Shapley contributions from coalition utilities."""
    p = len(players)
    if not p:
        return {}
    out = {}
    for player in players:
        others = tuple(x for x in players if x != player)
        contribution = 0.0
        for prior in coalitions(others):
            with_player = tuple(x for x in players if x in prior or x == player)
            weight = (math.factorial(len(prior))
                      * math.factorial(p - len(prior) - 1)
                      / math.factorial(p))
            contribution += weight * (values[with_player] - values[prior])
        out[player] = float(contribution)
    if not np.isclose(sum(out.values()),
                      values[players] - values[()], atol=1e-8, rtol=0):
        raise AssertionError("Shapley contributions do not sum to model skill")
    return out


def in_sample_value(d: pd.DataFrame, outcome: str, method: str,
                    players: tuple[str, ...]) -> float:
    """Classical OLS R², or McFadden's likelihood pseudo-R² for logit.

    Logistic estimates are unclustered because this measures *fit only*.
    Invalid or nonconverged likelihoods fail rather than yielding a ranking.
    """
    if not players:
        return 0.0
    formula = outcome + " ~ " + " + ".join(BLOCKS[p] for p in players)
    with warnings.catch_warnings():
        warnings.simplefilter("error", PerfectSeparationWarning)
        if method == "PASS_LOGIT":
            fit = smf.glm(formula, data=d, family=sm.families.Binomial()).fit(
                maxiter=200
            )
            if not fit.converged or not np.isfinite(fit.llf):
                raise RuntimeError("Logit failed to converge with finite likelihood")
            y = d[outcome].to_numpy(dtype=float)
            mean = float(np.mean(y))
            null_ll = float(np.sum(
                y * np.log(mean) + (1 - y) * np.log1p(-mean)
            ))
            score = 1.0 - float(fit.llf) / null_ll
        else:
            fit = smf.ols(formula, data=d).fit()
            score = float(fit.rsquared)
    if not np.isfinite(score):
        raise RuntimeError("Nonfinite model fit")
    return score


def in_sample_shapley(d: pd.DataFrame, outcome: str, method: str,
                      measure: str):
    """Cache all eight possible coalitions; reuse for A/B/C/D."""
    cache = {(): 0.0}
    diagnostics = []
    for subset in list(coalitions(tuple(BLOCKS)))[1:]:
        try:
            cache[subset] = in_sample_value(d, outcome, method, subset)
            status = "ok"
        except (ValueError, RuntimeError, np.linalg.LinAlgError,
                PerfectSeparationWarning, OverflowError, FloatingPointError) as exc:
            cache[subset] = float("nan")
            status = f"failed: {type(exc).__name__}"
        diagnostics.append(dict(outcome=outcome, method=method,
                                coalition="+".join(subset), score=cache[subset],
                                metric=measure, status=status, n=len(d)))
    rows = []
    for code, members in MODEL_BLOCKS.items():
        required = tuple(coalitions(members))
        if not all(np.isfinite(cache.get(s, np.nan)) for s in required):
            for member in members:
                rows.append(dict(outcome=outcome, method=method, model=code,
                                 block=member, contribution=np.nan,
                                 model_score=np.nan, share_of_model=np.nan,
                                 metric=measure, status="not_estimable"))
            continue
        value = {s: cache[s] for s in required}
        for member, contribution in shapley(members, value).items():
            total = value[members]
            rows.append(dict(outcome=outcome, method=method, model=code,
                             block=member, contribution=contribution,
                             model_score=total,
                             share_of_model=(contribution / total
                                             if total > 0 else np.nan),
                             metric=measure, status="valid"))
    return pd.DataFrame(rows), pd.DataFrame(diagnostics)


def cross_validated_value(d: pd.DataFrame, outcome: str,
                          players: tuple[str, ...], folds: int = 5):
    """Held-out skill versus a training-fold mean, grouped by professor-period.

    Uses only attendance and degree: a never-before-seen classroom has no
    estimable classroom fixed effect. Full-term attendance is retrospective.
    """
    y = d[outcome].to_numpy(dtype=float)
    group = d["CLASSROOM_ID"].astype(str).to_numpy()
    if len(set(group)) < folds:
        raise ValueError("Too few professor-period contexts for group CV")
    # Build a metadata-free model matrix. The source cohort may carry a
    # DataFrame in pandas .attrs; selecting multiple columns and then calling
    # .astype(str) internally concatenates Series and attempts to compare
    # their attrs. pandas 3 raises an ambiguous DataFrame truth-value error.
    # Explicit NumPy values prevent metadata from reaching the CV matrix.
    columns = [CV_COLUMNS[b] for b in players]
    cat = pd.DataFrame(
        {column: d[column].to_numpy(dtype=str) for column in columns},
        index=d.index,
    )
    pred = np.empty(len(d), dtype=float)
    baseline = np.empty(len(d), dtype=float)
    for train, test in GroupKFold(n_splits=folds).split(d, y, group):
        mean = float(np.mean(y[train]))
        baseline[test] = mean
        if not players:
            pred[test] = mean
            continue
        columns = list(cat.columns)
        transformer = ColumnTransformer(
            [("categorical", OneHotEncoder(handle_unknown="ignore"), columns)]
        )
        predictor = (LogisticRegression(max_iter=2000)
                     if outcome == "PASS" else LinearRegression())
        pipe = make_pipeline(transformer, predictor)
        pipe.fit(cat.iloc[train], y[train])
        pred[test] = (pipe.predict_proba(cat.iloc[test])[:, 1]
                      if outcome == "PASS" else pipe.predict(cat.iloc[test]))
    numerator = float(np.sum((y - pred) ** 2))
    denominator = float(np.sum((y - baseline) ** 2))
    if denominator <= 0 or not np.isfinite(numerator):
        raise RuntimeError("Invalid cross-validated skill denominator")
    return 1 - numerator / denominator


def cross_validated_shapley(d: pd.DataFrame, outcome: str, folds: int = 5):
    """Out-of-context Shapley of Z R² skill or binary Brier skill."""
    values = {subset: cross_validated_value(d, outcome, subset, folds)
              for subset in coalitions(CV_BLOCKS)}
    contributions = shapley(CV_BLOCKS, values)
    metric = ("out_of_context_brier_skill" if outcome == "PASS"
              else "out_of_context_r2_skill")
    overall = values[CV_BLOCKS]
    scores = pd.DataFrame([
        dict(outcome=outcome, coalition="+".join(s), score=v, metric=metric,
             folds=folds, n=len(d)) for s, v in values.items()
    ])
    importance = pd.DataFrame([
        dict(outcome=outcome, block=k, contribution=v, model_score=overall,
             metric=metric, folds=folds, n=len(d)) for k, v in contributions.items()
    ])
    return importance, scores


def report(importance: pd.DataFrame, cv: pd.DataFrame) -> str:
    lines = [
        "# 19 — Shapley predictive importance (exploratory)",
        "",
        "Exact grouped Shapley attribution; no student microdata exported.",
        "Attributions represent **model fit or predictive skill**, not causal effects.",
        "The player blocks are attendance frequency, degree, and professor-period.",
        "The R² and McFadden pseudo-R² columns have different denominators and",
        "must not be compared as if they were the same quantity.",
        "",
        "## In-sample decompositions for all 12 historical specifications",
        "",
        "| Outcome | Method | Model | Block | Contribution | Total fit | Share | Status |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]
    for r in importance.itertuples():
        fmt = lambda v: f"{v:.5f}" if pd.notna(v) else "ND"
        lines.append(f"| {r.outcome} | {r.method} | {r.model} | {r.block} | "
                     f"{fmt(r.contribution)} | {fmt(r.model_score)} | "
                     f"{fmt(r.share_of_model)} | {r.status} |")
    lines += [
        "",
        "## Out-of-professor-period prediction (five-fold GroupKFold)",
        "",
        "Held-out groups never appear in training. Only attendance and degree can",
        "enter these predictions; an unseen professor-period fixed effect cannot",
        "be estimated. Baseline is the training-fold average in each fold.",
        "",
        "| Outcome | Block | Contribution to held-out skill | Full held-out skill |",
        "|---|---|---:|---:|",
    ]
    for r in cv.itertuples():
        lines.append(f"| {r.outcome} | {r.block} | {r.contribution:.5f} | "
                     f"{r.model_score:.5f} |")
    lines += [
        "",
        "For PASS, the held-out metric is Brier skill (larger is better),",
        "not an odds ratio, p-value, or classical OLS R².",
        "Held-out scores and Shapley values may be negative when predictions",
        "are worse than the training-fold baseline.",
        "",
        "## Essential restrictions",
        "",
        "- Z is standardized within professor-period and imputes adverse states;",
        "  the dependent variable itself is not a directly available early grade.",
        "- Full-semester visits are measured contemporaneously with final grades;",
        "  this is **retrospective prediction**, not a semester-start forecast.",
        "- Prior mathematical achievement, diagnostic tests, motivation, and",
        "  socioeconomic resources are not included: this experiment cannot",
        "  identify the most important determinant of grades in general.",
        "- Correlated predictors share credit by convention, not causally.",
        "- The full logistic model previously lacked valid clustered inference;",
        "  descriptive pseudo-R² here cannot repair that problem.",
        "- Do not replace the Paper 2.1 Wald/Holm hypothesis tests with these",
        "  exploratory importance rankings.",
        "",
    ]
    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materias", type=Path)
    parser.add_argument("--asesorias", type=Path)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.check:
        v = {(): 0.0, ("attendance",): .10, ("degree",): .20,
             ("attendance", "degree"): .25}
        assert np.isclose(sum(shapley(("attendance", "degree"), v).values()), .25)
        print("Shapley contract valid; no institutional inputs loaded.")
        return 0

    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_primary_outcomes

    cfg = get_study_config(ROOT)
    cfg = replace(
        cfg,
        materias_path=(args.materias or cfg.materias_path).expanduser().resolve(),
        asesorias_path=(args.asesorias or cfg.asesorias_path).expanduser().resolve(),
    )
    for path in (cfg.materias_path, cfg.asesorias_path):
        if not path.is_file():
            raise SystemExit(f"Missing authorised institutional data: {path}")
    raw = load_and_clean_inputs(cfg)
    mu = add_primary_outcomes(build_study_cohorts(raw, cfg)["mu_primary"], cfg)
    prepared = {
        outcome: prepare_cohort(mu, outcome_col=outcome)
        for outcome in ("Z_GRADE_PRIMARY", "PASS")
    }
    for outcome, d in prepared.items():
        if len(d) != 6627 or d["CLASSROOM_ID"].nunique() != 190:
            raise RuntimeError(f"Paper cohort mismatch for {outcome}: "
                               f"N={len(d)} clusters={d['CLASSROOM_ID'].nunique()}")
    if not prepared["Z_GRADE_PRIMARY"].index.equals(prepared["PASS"].index):
        raise RuntimeError("Outcome samples differ; report populations separately")

    all_importance, all_coalitions, all_cv, all_cv_scores = [], [], [], []
    for outcome, method, metric in METHODS:
        print(f"Shapley in-sample: {outcome} / {method}", flush=True)
        a, c = in_sample_shapley(prepared[outcome], outcome, method, metric)
        all_importance.append(a)
        all_coalitions.append(c)
    for outcome in prepared:
        print(f"Group CV: {outcome}", flush=True)
        a, c = cross_validated_shapley(prepared[outcome], outcome)
        all_cv.append(a)
        all_cv_scores.append(c)

    imp = pd.concat(all_importance, ignore_index=True)
    coalition = pd.concat(all_coalitions, ignore_index=True)
    cv = pd.concat(all_cv, ignore_index=True)
    cv_scores = pd.concat(all_cv_scores, ignore_index=True)

    # Fail rather than silently compare a changed Z model to Paper 2.1.
    target = 0.05822819493413134
    fit_d = imp.query("outcome == 'Z_GRADE_PRIMARY' and model == 'D'")
    if not fit_d["model_score"].notna().all() or not np.isclose(
        fit_d["model_score"].iloc[0], target, atol=1e-6, rtol=0
    ):
        raise RuntimeError("Z model D R² differs from the validated Paper 2.1 run")

    DEST.mkdir(parents=True, exist_ok=True)
    imp.to_csv(DEST / "in_sample_shapley_12_models.csv", index=False)
    coalition.to_csv(DEST / "in_sample_coalitions.csv", index=False)
    cv.to_csv(DEST / "out_of_context_shapley.csv", index=False)
    cv_scores.to_csv(DEST / "out_of_context_coalitions.csv", index=False)
    NOTE.write_text(report(imp, cv), encoding="utf-8")
    print(f"Aggregate outputs: {DEST}; report: {NOTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
