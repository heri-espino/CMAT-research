#!/usr/bin/env python3
"""PPA visit-band FE analysis, with only aggregate outputs and explicit provenance."""
from __future__ import annotations
import argparse
import hashlib
import json
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests
from ppa_groups import SPECS, assign_visit_groups, ppa_family_size, verify_partition

ROOT = Path(__file__).resolve().parents[4]
VISITS = "VISITS_CMAT_PERIOD"
FIXED = "CLASSROOM_ID"
DEGREE = "CLAVECARRERA"
OUTCOMES = ("Z_GRADE_PRIMARY", "PASS")
# Outcome-blind visit distribution from the locked Paper 2.1 analytic cohort.
# Check counts, not historical means or significance values.
EXPECTED_EXACT_SUPPORT = {"0": 5393, "1": 517, "2": 245, "3": 170,
                          "4": 96, "5": 55, "6": 50, "7+": 101}

def _save(table, filename):
    filename.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(filename, index=False, float_format="%.12g")

def _hash(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1048576), b""):
            h.update(block)
    return h.hexdigest()

def _safe_source_label(path):
    """Never put private home directories or external absolute paths in a public manifest."""
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return f"authorized_external_source:{path.name}"

def _estimate(cohort, spec, outcome):
    from cmat_analysis.statistics import fixed_effect_group_comparisons, group_outcome_summary, visit_group_pair_overlap
    d = cohort.copy()
    d["PPA_VISIT_GROUP"] = assign_visit_groups(d[VISITS], spec)
    cc = d.dropna(subset=[outcome, "PPA_VISIT_GROUP", FIXED, DEGREE]).copy()
    if outcome == "PASS" and not set(cc[outcome].unique()).issubset({0, 1, 0., 1.}):
        raise ValueError("PASS is not 0/1")
    pair, omnibus, info = fixed_effect_group_comparisons(
        cc, group_col="PPA_VISIT_GROUP", group_order=list(spec.labels),
        outcome_col=outcome, fixed_effect_col=FIXED, cluster_col=FIXED,
        categorical_covariates=[DEGREE], multiplicity_method="holm",
    )
    if len(pair) != len(spec.labels) * (len(spec.labels) - 1) // 2:
        raise AssertionError("Pair count does not match the categorical specification")
    pair = pair.rename(columns={
        "estimate_group1_minus_group2": "adjusted_group1_minus_group2",
        "p_adjusted": "p_holm_within_model_auxiliary",
        "reject_adjusted": "reject_holm_within_model_auxiliary",
    })
    for frame in (pair, omnibus, info):
        frame.insert(0, "outcome", outcome)
        frame.insert(0, "specification", spec.name)
    pair["family_role"] = "exploratory_PPA_18" if spec.exploratory_ppa else "historical_exact_28_reference"
    pair["n_fixed_effect_levels"] = int(info.loc[0, "n_fixed_effect_levels"])
    pair["comparison_direction"] = "group1_minus_group2"
    descriptive = group_outcome_summary(d, group_col="PPA_VISIT_GROUP",
                         group_order=list(spec.labels), outcome_col="Z_GRADE_PRIMARY", pass_col="PASS")
    descriptive.insert(0, "specification", spec.name)
    descriptive["n_instructor_periods"] = [int(d.loc[d["PPA_VISIT_GROUP"] == g, FIXED].nunique()) for g in spec.labels]
    descriptive["n_numeric_grade"] = [int(d.loc[d["PPA_VISIT_GROUP"] == g, "GRADE_NUMERIC"].notna().sum()) for g in spec.labels]
    # CIs from group_outcome_summary are conventional descriptive intervals;
    # all model comparisons use professor-period clustered uncertainty.
    overlap = visit_group_pair_overlap(d, group_col="PPA_VISIT_GROUP",
                 group_order=list(spec.labels), cluster_col=FIXED)
    overlap.insert(0, "specification", spec.name)
    return pair, omnibus, info, descriptive, overlap

def _adjusted_levels(cohort, spec, outcome):
    """FE-standardized means with clustered delta CIs; verify shared contrasts."""
    import statsmodels.formula.api as smf
    from patsy import build_design_matrices
    from scipy.stats import norm
    from cmat_analysis.statistics import fixed_effect_group_comparisons
    d = cohort.copy()
    d["PPA_VISIT_GROUP"] = assign_visit_groups(d[VISITS], spec)
    d = d.dropna(subset=[outcome, "PPA_VISIT_GROUP", FIXED, DEGREE]).copy()
    term = f"C(PPA_VISIT_GROUP, Treatment(reference='{spec.labels[0]}'))"
    formula = f"{outcome} ~ {term} + C({FIXED}) + C({DEGREE})"
    m = smf.ols(formula, d).fit(cov_type="cluster", cov_kwds={"groups": d[FIXED]})
    beta, cov = np.asarray(m.params), np.asarray(m.cov_params())
    records, levels = [], {}
    for group in spec.labels:
        counterfactual = d.copy()
        counterfactual["PPA_VISIT_GROUP"] = pd.Categorical(
            [group] * len(d), categories=spec.labels, ordered=True
        )
        design = np.asarray(build_design_matrices([m.model.data.design_info], counterfactual)[0])
        xbar = design.mean(axis=0)
        mu = float(xbar @ beta)
        se = float(np.sqrt(max(xbar @ cov @ xbar, 0.0)))
        levels[group] = mu
        records.append({
            "specification": spec.name, "outcome": outcome, "group": group,
            "adjusted_mean": mu, "cluster_robust_se": se,
            "ci95_low": mu - norm.ppf(.975) * se,
            "ci95_high": mu + norm.ppf(.975) * se,
            "units": "probability" if outcome == "PASS" else "within_context_SD",
            "n_model": len(d), "n_contexts": int(d[FIXED].nunique()),
            "interpretation": "FE-standardized mean across observed contexts and degrees; model-based extrapolation",
        })
    pairs, _, _ = fixed_effect_group_comparisons(
        d, group_col="PPA_VISIT_GROUP", group_order=list(spec.labels),
        outcome_col=outcome, fixed_effect_col=FIXED, cluster_col=FIXED,
        categorical_covariates=[DEGREE],
    )
    for row in pairs.itertuples():
        if not np.isclose(levels[row.group1] - levels[row.group2],
                          row.estimate_group1_minus_group2, atol=1e-7, rtol=1e-7):
            raise AssertionError("Reconstructed adjusted mean contrast disagrees with shared estimator")
    return pd.DataFrame(records)

def _focus(allpairs):
    rows = []
    for spec in SPECS[:2]:
        for row in allpairs.loc[allpairs.specification == spec.name].itertuples():
            scale = 100. if row.outcome == "PASS" else 1.
            rows.append({
                "specification": spec.name, "outcome": row.outcome,
                "baseline": row.group1, "target": row.group2,
                "adjusted_target_minus_baseline": -scale * row.adjusted_group1_minus_group2,
                "ci95_low": -scale * row.ci_high,
                "ci95_high": -scale * row.ci_low,
                "units": "percentage_points" if scale == 100. else "within_context_SD",
                "p_raw": row.p_raw,
                "p_holm_ppa_family": row.p_holm_ppa_family,
                "ppa_family_m": row.ppa_family_m,
                "n_model": row.n, "n_clusters": row.n_clusters,
                "comparison_direction": "target_minus_baseline",
            })
    return pd.DataFrame(rows)

def _figures(focus, dest):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    dest.mkdir(parents=True, exist_ok=True)
    for outcome in OUTCOMES:
        q = focus.loc[(focus.outcome == outcome) & (focus.baseline != "0")]
        fig, ax = plt.subplots(figsize=(8.5, 4.1))
        y = np.arange(len(q))
        val = q.adjusted_target_minus_baseline.to_numpy(float)
        err = np.vstack([val - q.ci95_low.to_numpy(float), q.ci95_high.to_numpy(float) - val])
        ax.errorbar(val, y, xerr=err, fmt="o", capsize=3, color="#263b50", ecolor="#899ba8")
        ax.axvline(0, color="#777777", ls="--", lw=.8)
        ax.set(yticks=y, yticklabels=[f"{r.specification.split('_')[0]}: {r.target} vs {r.baseline}" for r in q.itertuples()],
               xlabel="Percentage-point difference" if outcome == "PASS" else "Standard-deviation difference",
               title=f"Observed PPA visit bands: {outcome}")
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=.18)
        fig.text(.5, .01, "Nominal 95% classroom-clustered CIs; Holm-adjusted p-values in CSV; not causal.", ha="center", fontsize=8)
        fig.tight_layout(rect=(0,.06,1,1))
        fig.savefig(dest / f"ppa_{outcome.lower()}.pdf", bbox_inches="tight")
        fig.savefig(dest / f"ppa_{outcome.lower()}.png", dpi=220, bbox_inches="tight")
        plt.close(fig)

def run(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--materias", type=Path)
    p.add_argument("--asesorias", type=Path)
    p.add_argument("--output-root", type=Path,
                   default=ROOT / "papers" / "paper2-beyond-first-attendance" / "results")
    p.add_argument("--check", action="store_true")
    p.add_argument("--include-secondary", action="store_true",
                   help="Additionally fit 0|1-3|4|5+ and apply a joint 18-test exploratory Holm family")
    args = p.parse_args(argv)
    if args.check:
        verify_partition(pd.DataFrame({VISITS: [0,1,2,3,4,5,6,7,8,99]}))
        assert ppa_family_size() == 18
        print("PASS: exclusive group boundaries and exploratory Holm family size 18")
        return 0

    # An explicit institutional input selection avoids an accidental fall back
    # to publicly versioned pseudonymized student records.
    if args.materias is None or args.asesorias is None:
        p.error("Full runs require explicit authorized --materias and --asesorias paths; use --check for synthetic-only checks")
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_primary_outcomes
    config = get_study_config(ROOT)
    config = replace(config,
        materias_path=(args.materias or config.materias_path).expanduser().resolve(),
        asesorias_path=(args.asesorias or config.asesorias_path).expanduser().resolve())
    for source in (config.materias_path, config.asesorias_path):
        if not source.is_file():
            raise FileNotFoundError(f"Missing authorized institutional input: {source}; numerical results PENDING")
    cohort = add_primary_outcomes(
        build_study_cohorts(load_and_clean_inputs(config), config)["mu_primary"], config
    )
    if len(cohort) != 6627 or cohort[FIXED].nunique() != 190 or int((cohort[VISITS]>0).sum()) != 1234:
        raise ValueError("Cohort validation failed: expected N=6,627, 190 professor-period contexts and 1,234 recorded users")
    verify_partition(cohort)
    exact_counts = (assign_visit_groups(cohort[VISITS], SPECS[2])
                    .astype(str).value_counts().to_dict())
    if exact_counts != EXPECTED_EXACT_SUPPORT:
        raise ValueError(
            "Cohort visit distribution differs from the validated historical "
            "exact-frequency support; institutional results must not be published "
            "until this discrepancy is investigated."
        )
    if cohort["PASS"].isna().any() or cohort["Z_GRADE_PRIMARY"].isna().any():
        raise ValueError("Unexpected missing full-cohort main outcome")
    tables = args.output_root / "tables" / "ppa-groups"
    provenance = args.output_root / "provenance" / "ppa-groups"
    allpairs, omnibus, infos, observed, overlaps, adjusted = [], [], [], [], [], []
    active_specs = (SPECS[0], SPECS[1], SPECS[2]) if args.include_secondary else (SPECS[0], SPECS[2])
    exploratory_specs = tuple(spec for spec in active_specs if spec.exploratory_ppa)
    family_size = sum(len(spec.labels) * (len(spec.labels)-1) // 2 for spec in exploratory_specs) * len(OUTCOMES)
    if family_size not in (6, 18):
        raise AssertionError("Unexpected exploratory comparison family size")
    for spec in active_specs:
        for outcome in OUTCOMES:
            a,b,c,d,e = _estimate(cohort,spec,outcome)
            allpairs.append(a); omnibus.append(b); infos.append(c)
            adjusted.append(_adjusted_levels(cohort,spec,outcome))
            if outcome == OUTCOMES[0]:
                observed.append(d); overlaps.append(e)
    pairs = pd.concat(allpairs,ignore_index=True)
    mask = pairs.specification.isin([s.name for s in exploratory_specs])
    assert int(mask.sum()) == family_size
    _, p_holm, _, _ = multipletests(pairs.loc[mask,"p_raw"],method="holm",alpha=.05)
    pairs["ppa_family_m"] = family_size
    pairs["p_holm_ppa_family"] = np.nan
    pairs.loc[mask,"p_holm_ppa_family"] = p_holm
    pairs["reject_holm_ppa_family"] = False
    pairs.loc[mask,"reject_holm_ppa_family"] = p_holm <= .05
    focus = _focus(pairs)
    _save(pairs,tables/"pairwise_all_models.csv")
    _save(focus,tables/"focus_target_minus_baseline.csv")
    _save(pd.concat(omnibus,ignore_index=True),tables/"omnibus.csv")
    _save(pd.concat(infos,ignore_index=True),tables/"model_info.csv")
    _save(pd.concat(observed,ignore_index=True),tables/"observed_groups.csv")
    _save(pd.concat(overlaps,ignore_index=True),tables/"pair_context_overlap.csv")
    _save(pd.concat(adjusted,ignore_index=True),tables/"adjusted_means.csv")
    sensitivity = []
    for outcome in ("GRADE_NUMERIC", "Z_GRADE_COMPLETE_CASE"):
        for spec in exploratory_specs:
            a,b,c,_,_ = _estimate(cohort,spec,outcome)
            a["family_role"] = "numeric_selected_sensitivity_separate_from_PPA_18"
            sensitivity.append(a)
    _save(pd.concat(sensitivity,ignore_index=True),tables/"numeric_selected_sensitivity.csv")
    _figures(focus,args.output_root/"figures"/"ppa-groups")
    provenance.mkdir(parents=True,exist_ok=True)
    manifest = {
      "status":"EXECUTED_ON_VALIDATED_INSTITUTIONAL_DATA",
      "utc":datetime.now(timezone.utc).isoformat(),
      "n":len(cohort), "n_contexts":int(cohort[FIXED].nunique()),
      "n_users":int((cohort[VISITS]>0).sum()),
      "historical_exact_support_revalidated":exact_counts,
      "analysis_script_sha256":_hash(Path(__file__)),
      "group_definitions_sha256":_hash(Path(__file__).with_name("ppa_groups.py")),
      "p_holm_family":family_size,
      "included_specifications":[spec.name for spec in active_specs],
      "secondary_enabled":args.include_secondary,
      "source_sha256":{"materias":_hash(config.materias_path),
                       "asesorias":_hash(config.asesorias_path)},
      "source_paths":{"materias":_safe_source_label(config.materias_path),
                      "asesorias":_safe_source_label(config.asesorias_path)},
      "cohort":"cmat_analysis.cohorts.build_study_cohorts(mu_primary)",
      "outcomes":"cmat_analysis.measures.add_primary_outcomes",
      "estimator":"cmat_analysis.statistics.fixed_effect_group_comparisons",
      "fixed_effect":FIXED,"cluster":FIXED,"degree":DEGREE,
      "seed":config.random_seed,
      "limitations":"Recorded visits are voluntary; PPA intent, eligibility, credits unobserved; not causal.",
    }
    (provenance/"run_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(f"Completed aggregate PPA analysis N={len(cohort)}, exploratory Holm m={family_size}; outputs in {tables}")
    return 0

if __name__ == "__main__":
    raise SystemExit(run())
