#!/usr/bin/env python3
"""Exploratory CMAT follow-ups: degree overlap, attendance hurdle, numeric grades.

Uses the authorized Paper 2.1 cohort. Only grouped aggregates leave this runner;
no university identifiers, student-level predictions, or records are written.
The original primary Holm analysis and its 15/21/28 correction families are NOT
changed by these secondary analyses.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

from run_paper21_model_controls_experiment import ROOT, prepare_cohort

OUTDIR = ROOT / "results" / "paper21" / "tables" / "followup_questions"
NOTE = ROOT / "notes" / "22_FOLLOWUP_QUESTIONS_RESULTS.md"
OUTCOMES = (("Z_GRADE_PRIMARY", "OLS_Z"), ("PASS", "LPM_PASS"))
HURDLE_TERMS = ("ANY_VISIT", "EXTRA_VISITS_CAPPED_7")


def _plain(frame: pd.DataFrame) -> pd.DataFrame:
    """Do not propagate large nested DataFrames in source pandas .attrs."""
    result = frame.copy()
    result.attrs.clear()
    return result


def overlap_diagnostics(frame: pd.DataFrame) -> pd.DataFrame:
    """Degree/programme overlap and descriptive degree partial fit in mixed classes.

    A programme observed in only one professor-period class is not separately
    identified from that class's FE; report design overlap before interpretation.
    """
    cols = ("CLASSROOM_ID", "CLAVECARRERA", "VISIT_GROUP", "Z_GRADE_PRIMARY")
    d = _plain(frame.loc[:, list(cols)].dropna(subset=cols))
    n_programmes = d.groupby("CLASSROOM_ID")["CLAVECARRERA"].nunique()
    n_students = d.groupby("CLASSROOM_ID").size()
    mixed = n_programmes.index[n_programmes.gt(1)]
    dm = _plain(d.loc[d["CLASSROOM_ID"].isin(mixed)])
    total = len(d)
    summary = dict(
        n_students=total,
        n_professor_period=int(len(n_programmes)),
        n_mixed_professor_period=int(len(mixed)),
        fraction_contexts_mixed=float(len(mixed) / len(n_programmes)),
        n_students_in_mixed_contexts=int(len(dm)),
        fraction_students_in_mixed_contexts=float(len(dm) / total),
        median_programmes_per_context=float(n_programmes.median()),
        max_programmes_per_context=int(n_programmes.max()),
        median_students_per_context=float(n_students.median()),
        sample="mixed_professor_period_only",
        r2_mixed_without_degree=np.nan,
        r2_mixed_with_degree=np.nan,
        incremental_r2_degree_mixed=np.nan,
        status="insufficient_mixed_contexts",
    )
    # Avoid interpreting a degenerate mixed sample with no within-degree support.
    if len(mixed) >= 2 and dm["CLAVECARRERA"].nunique() >= 2:
        baseline = smf.ols(
            "Z_GRADE_PRIMARY ~ C(VISIT_GROUP) + C(CLASSROOM_ID)", data=dm
        ).fit()
        full = smf.ols(
            "Z_GRADE_PRIMARY ~ C(VISIT_GROUP) + C(CLASSROOM_ID) "
            "+ C(CLAVECARRERA)", data=dm
        ).fit()
        summary.update(
            r2_mixed_without_degree=float(baseline.rsquared),
            r2_mixed_with_degree=float(full.rsquared),
            incremental_r2_degree_mixed=float(full.rsquared - baseline.rsquared),
            status="descriptive_fit_only",
        )
    return pd.DataFrame([summary])


def two_part_attendance(frame: pd.DataFrame, outcome: str) -> pd.DataFrame:
    """Separate 0→1 from the *assumed linear* additional 1→7+ gradient.

    Same professor-period and degree adjustment as model D; SE clustered at
    CLASSROOM_ID. Holm covers exactly the two prespecified attendance terms per
    outcome, not the historical 15/21/28 pairwise families.
    """
    if outcome not in dict(OUTCOMES):
        raise ValueError("Unexpected outcome")
    d = _plain(prepare_cohort(frame, outcome_col=outcome))
    visits = pd.to_numeric(d["VISITS_CMAT_PERIOD"], errors="raise").astype(int)
    d["ANY_VISIT"] = (visits > 0).astype(int)
    d["EXTRA_VISITS_CAPPED_7"] = np.maximum(np.minimum(visits, 7) - 1, 0)
    if not ((d.loc[visits.eq(0), list(HURDLE_TERMS)].sum(axis=1) == 0).all()
            and (d.loc[visits.eq(1), "EXTRA_VISITS_CAPPED_7"] == 0).all()
            and (d.loc[visits.ge(7), "EXTRA_VISITS_CAPPED_7"] == 6).all()):
        raise AssertionError("Incorrect attendance transition encoding")

    formula = (f"{outcome} ~ ANY_VISIT + EXTRA_VISITS_CAPPED_7 "
               "+ C(CLASSROOM_ID) + C(CLAVECARRERA)")
    fit = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]}
    )
    estimates = [float(fit.params[t]) for t in HURDLE_TERMS]
    errors = [float(fit.bse[t]) for t in HURDLE_TERMS]
    pvalues = [float(fit.pvalues[t]) for t in HURDLE_TERMS]
    if not (np.isfinite(estimates + errors + pvalues).all()
            and min(errors) > 0):
        raise RuntimeError(f"Invalid cluster-robust attendance inference: {outcome}")
    adjusted = multipletests(pvalues, alpha=.05, method="holm")[1]
    rows = []
    for term, estimate, se, p_raw, p_holm in zip(
        HURDLE_TERMS, estimates, errors, pvalues, adjusted
    ):
        # Coefficients: Z SD or PASS probability (converted to pp in report).
        rows.append(dict(
            outcome=outcome, model="two_part_clustered_OLS",
            term=term, estimate=estimate, standard_error=se,
            ci95_low=estimate - 1.96 * se,
            ci95_high=estimate + 1.96 * se,
            p_raw=p_raw, p_holm_within_two_term_family=float(p_holm),
            n=len(d), clusters=d["CLASSROOM_ID"].nunique(),
            extra_visit_limit="exact_1_through_6_and_topcoded_7plus",
            formula=formula,
        ))
    return pd.DataFrame(rows)


def _coarse_group(visits: pd.Series) -> pd.Series:
    n = pd.to_numeric(visits, errors="raise")
    if (n < 0).any() or (n % 1 != 0).any():
        raise ValueError("Visits must be nonnegative integers")
    return pd.Series(
        np.select([n.eq(0), n.eq(1), n.between(2, 6), n.ge(7)],
                  ["0", "1", "2-6", "7+"], default="invalid"),
        index=visits.index, name="frequency_group"
    )


def numeric_grade_distribution(frame: pd.DataFrame, threshold: float = 7.5
                               ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Descriptive observed-numeric grade quantiles and near-pass mass.

    Conditioning on having a numeric final grade creates a different population
    from the full Z/PASS models. No imputed grades or individual grades exported.
    Coarse visit bins avoid tiny exact-attendance tail cells.
    """
    required = {"VISITS_CMAT_PERIOD", "GRADE_CLASS", "GRADE_NUMERIC", "PASS"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing grade columns: {sorted(missing)}")
    d = _plain(frame)
    d["freq_coarse"] = _coarse_group(d["VISITS_CMAT_PERIOD"])
    if (d["freq_coarse"] == "invalid").any():
        raise ValueError("Invalid visit frequency group")

    composition = []
    grades = []
    for group in ("0", "1", "2-6", "7+"):
        g = _plain(d.loc[d["freq_coarse"].eq(group)])
        numeric = _plain(g.loc[g["GRADE_CLASS"].eq("numeric")])
        numeric_grades = pd.to_numeric(numeric["GRADE_NUMERIC"], errors="coerce")
        if not np.isfinite(numeric_grades.to_numpy(dtype=float)).all():
            raise ValueError("Numeric outcome contains missing or nonfinite values")
        n = len(g)
        m = len(numeric)
        if n < 30 or m < 30:
            raise RuntimeError(f"Insufficient coarse-group support for {group}")
        grades.append(dict(
            group=group, n_numeric=m, n_all_outcomes=n,
            numeric_pass_rate=float(np.mean(numeric_grades >= threshold)),
            numeric_mean=float(np.mean(numeric_grades)),
            numeric_p10=float(numeric_grades.quantile(.10)),
            numeric_p25=float(numeric_grades.quantile(.25)),
            numeric_median=float(numeric_grades.median()),
            numeric_p75=float(numeric_grades.quantile(.75)),
            numeric_p90=float(numeric_grades.quantile(.90)),
            numeric_share_within_half_point_of_7p5=float(
                np.mean((numeric_grades >= threshold - .5)
                        & (numeric_grades <= threshold + .5))
            ),
            conditioning="received_observed_numeric_final_grade",
        ))
        composition.append(dict(
            group=group, n_all_outcomes=n, n_numeric=m,
            n_adverse=int(g["GRADE_CLASS"].eq("adverse").sum()),
            observed_numeric_fraction=float(m / n),
            administrative_fraction=float(g["GRADE_CLASS"].eq("adverse").mean()),
            full_cohort_pass_rate=float(pd.to_numeric(g["PASS"]).mean()),
        ))
    return pd.DataFrame(grades), pd.DataFrame(composition)


def _fmt(value: float, digits: int = 4) -> str:
    return f"{value:.{digits}f}" if pd.notna(value) else "NA"


def render_report(overlap: pd.DataFrame, piecewise: pd.DataFrame,
                  grades: pd.DataFrame, composition: pd.DataFrame) -> str:
    d = overlap.iloc[0]
    lines = [
        "# 22 — Follow-up questions: exploratory results",
        "",
        "Institutionally authorized Paper 2.1 first-eligible MU cohort.",
        "All outputs are aggregated. These analyses are observational, not causal.",
        "",
        "## 1. Degree mixing within professor-period contexts",
        "",
        f"- Mixed contexts: {int(d.n_mixed_professor_period)}/{int(d.n_professor_period)} "
        f"({_fmt(100*d.fraction_contexts_mixed, 1)}%).",
        f"- Students in mixed contexts: {int(d.n_students_in_mixed_contexts)} "
        f"({_fmt(100*d.fraction_students_in_mixed_contexts, 1)}%).",
        f"- Incremental descriptive in-sample Z R² for degree within mixed "
        f"contexts: {_fmt(d.incremental_r2_degree_mixed)}.",
        "",
        "Classroom overlap and within-mixed-class fit alone cannot establish",
        "self-selection into mathematics-intensive degrees or causal programme effects.",
        "",
        "## 2. First visit versus additional visits (piecewise working model)",
        "",
        "Z uses OLS units of SD; PASS uses LPM coefficients in probability units",
        "(multiply by 100 for percentage points). Both have clustered uncertainty",
        "at professor-period and programme/classroom covariates.",
        "Holm correction here covers **two predeclared terms per outcome**, not",
        "the original 15/21/28 attendance-pair families.",
        "",
        "| Outcome | Term | Coefficient | Nominal CI95 | Holm p |",
        "|---|---|---:|---|---:|",
    ]
    for r in piecewise.itertuples():
        lines.append(f"| {r.outcome} | {r.term} | {_fmt(r.estimate)} | "
                     f"[{_fmt(r.ci95_low)}, {_fmt(r.ci95_high)}] | "
                     f"{_fmt(r.p_holm_within_two_term_family)} |")
    lines += [
        "",
        "ANY_VISIT is the fitted 0→1 contrast. EXTRA_VISITS_CAPPED_7",
        "models a **single linear per-visit slope** for the increase 1→2→...→7+,",
        "so the model-implied 1→7+ difference is six times that slope.",
        "7+ is top-coded, so this is a model assumption rather than a measured",
        "equal-increment response. The historical Holm contrasts remain primary.",
        "",
        "## 3. Observed numeric final grades and passing boundary",
        "",
        "| Visits | Numeric N | P10 | Median | P90 | Numeric PASS rate | Near 7.5 (±0.5) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in grades.itertuples():
        lines.append(f"| {r.group} | {r.n_numeric} | {_fmt(r.numeric_p10,2)} | "
                     f"{_fmt(r.numeric_median,2)} | {_fmt(r.numeric_p90,2)} | "
                     f"{_fmt(r.numeric_pass_rate*100,1)}% | "
                     f"{_fmt(r.numeric_share_within_half_point_of_7p5*100,1)}% |")
    lines += [
        "",
        "| Visits | Total N | Numeric N | Administrative share | Full-cohort PASS |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in composition.itertuples():
        lines.append(f"| {r.group} | {r.n_all_outcomes} | {r.n_numeric} | "
                     f"{_fmt(r.administrative_fraction*100,1)}% | "
                     f"{_fmt(r.full_cohort_pass_rate*100,1)}% |")
    lines += [
        "",
        "These grade quantiles **exclude BA, BV and RT**, whereas primary Z",
        "imputes adverse states and PASS treats them as nonpassing.",
        "Group comparisons above are unadjusted descriptive summaries; they",
        "cannot isolate CMAT effects from self-selection or differences in enrolment.",
        "",
        "## Research interpretation / non-inferences",
        "",
        "- Degree allocation and mathematical preparation remain unmeasured hypotheses.",
        "- One fitted visit coefficient does not identify a causal first-visit effect.",
        "- A weak extra-visit coefficient does not establish equivalence or saturation.",
        "- Descriptive quantiles are not fixed-effect-adjusted quantile regression.",
        "- No claim that a professor grades more easily is identified here.",
        "- Neither this experiment nor Shapley is a true start-of-term forecast.",
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
        assert len(OUTCOMES) == 2 and len(HURDLE_TERMS) == 2
        assert _coarse_group(pd.Series([0,1,2,6,7,20])).tolist() == [
            "0", "1", "2-6", "2-6", "7+", "7+"
        ]
        print("Follow-up exploratory contract valid; no institutional inputs read.")
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
            raise SystemExit(f"Missing authorized institutional input: {path}")
    raw = load_and_clean_inputs(cfg)
    mu = _plain(add_primary_outcomes(
        build_study_cohorts(raw, cfg)["mu_primary"], cfg
    ))
    z = prepare_cohort(mu, outcome_col="Z_GRADE_PRIMARY")
    passed = prepare_cohort(mu, outcome_col="PASS")
    for outcome, cohort in (("Z", z), ("PASS", passed)):
        if len(cohort) == 0 or cohort["CLASSROOM_ID"].nunique() < 2:
            raise RuntimeError(f"Paper cohort mismatch: {outcome}, N={len(cohort)}, "
                               f"contexts={cohort['CLASSROOM_ID'].nunique()}")
    if not z.index.equals(passed.index):
        raise RuntimeError("Different Z and PASS samples; do not compare")
    print("Computing professor-period / degree mixing", flush=True)
    mix = overlap_diagnostics(z)
    print("Fitting two-part attendance model: Z and PASS", flush=True)
    piecewise = pd.concat([
        two_part_attendance(z, "Z_GRADE_PRIMARY"),
        two_part_attendance(passed, "PASS")
    ], ignore_index=True)
    print("Summarizing observed numeric grades and administrative outcomes", flush=True)
    grades, composition = numeric_grade_distribution(mu)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    mix.to_csv(OUTDIR / "degree_professor_period_overlap.csv", index=False)
    piecewise.to_csv(OUTDIR / "two_part_attendance_z_pass.csv", index=False)
    grades.to_csv(OUTDIR / "observed_numeric_grade_quantiles.csv", index=False)
    composition.to_csv(OUTDIR / "numeric_vs_administrative_composition.csv", index=False)
    NOTE.write_text(render_report(mix, piecewise, grades, composition),
                    encoding="utf-8")
    print(f"Aggregate tables: {OUTDIR}")
    print(f"Report: {NOTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
