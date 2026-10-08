#!/usr/bin/env python3
"""Paper 2.2.1: ordered visit fusion and locked-cluster validation.

Outputs are disclosure-safe aggregates under results/paper221/. The inherited
Paper 2.1 controlled-data cohort/outcome contract is retained unchanged.
Use --check to inspect readiness without loading student data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "paper221" / "tables"
BASE_ORDER = ("0", "1", "2", "3", "4", "5", "6", "7+")
POOLED_ORDER = ("0", "1", "2", "3", "4", "5", "6+")


def imports():
    from cmat_analysis.cohorts import build_study_cohorts, load_and_clean_inputs
    from cmat_analysis.config.study_config import get_study_config
    from cmat_analysis.measures import add_primary_outcomes
    from cmat_analysis.statistics.ordered_fusion import (
        cluster_split, fit_prepared, grouped_cv, prepare_fusion,
        resample_cluster_rows, selected_partition,
    )
    return (build_study_cohorts, load_and_clean_inputs, get_study_config,
            add_primary_outcomes, cluster_split, fit_prepared, grouped_cv,
            prepare_fusion, resample_cluster_rows, selected_partition)


def load_cohort(args, shared):
    build, load, config_get, add_outcomes = shared[:4]
    base = config_get(ROOT)
    configuration = replace(
        base,
        materias_path=(args.materias or base.materias_path).expanduser().resolve(),
        asesorias_path=(args.asesorias or base.asesorias_path).expanduser().resolve(),
    )
    data = load(configuration)
    cohort = build(data, configuration)["mu_primary"].copy()
    cohort = add_outcomes(cohort, configuration)
    visits = pd.to_numeric(cohort["VISITS_CMAT_PERIOD"], errors="coerce")
    cohort["GROUP_7PLUS"] = np.select(
        [visits.ge(7), visits.ge(0)],
        ["7+", "exact"], default="missing"
    )
    cohort["GROUP_7PLUS"] = np.where(
        cohort["GROUP_7PLUS"].eq("exact"),
        visits.fillna(-1).astype(int).astype(str), cohort["GROUP_7PLUS"])
    cohort["GROUP_6PLUS"] = np.where(
        visits.ge(6), "6+", visits.fillna(-1).astype(int).astype(str))
    return cohort


def prepare_rows(cohort, *, outcome, grouping, order):
    needed = [outcome, "CLASSROOM_ID", "CLAVECARRERA", grouping]
    d = cohort.dropna(subset=needed).copy()
    d[outcome] = pd.to_numeric(d[outcome], errors="coerce")
    d = d.loc[d[outcome].notna()].copy()
    d["GROUP"] = d[grouping].astype(str)
    d = d.loc[d["GROUP"].isin(order)].copy()
    if d.empty:
        raise RuntimeError("No eligible complete-case records for " + outcome)
    return d


def support_table(frame, order):
    rows = []
    for i, name in enumerate(order):
        sub = frame.loc[frame["GROUP"].eq(name)]
        rows.append({"order": i, "group": name, "n_students": len(sub),
                     "n_classrooms": sub["CLASSROOM_ID"].nunique(),
                     "n_degrees": sub["CLAVECARRERA"].nunique()})
    return pd.DataFrame(rows)


def refit_validation(test, outcome, order, partition):
    """Fit UNPENALISED selected-block model on locked held-out clusters."""
    mapping = {}
    for group in partition:
        for member in group["members"].split("|"):
            mapping[member] = group["block"]
    d = test.copy()
    d["BLOCK"] = d["GROUP"].map(mapping)
    blocks = [block["block"] for block in partition]
    observed = set(d["BLOCK"].dropna())
    if not set(blocks).issubset(observed):
        raise RuntimeError("Validation contains no observations in a chosen block")
    if d["CLASSROOM_ID"].nunique() < 20:
        raise RuntimeError("Insufficient validation clusters (<20)")
    d["BLOCK"] = pd.Categorical(d["BLOCK"], categories=blocks, ordered=True)
    # Reference B0. With class FE, each block difference is conditional on
    # degree/context; a nonsignificant difference does not prove equivalence.
    formula = (f"{outcome} ~ C(BLOCK, Treatment(reference='B0'))"
               " + C(CLASSROOM_ID) + C(CLAVECARRERA)")
    model = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["CLASSROOM_ID"]},
        use_t=False,
    )
    exog = model.model.exog
    # Nuisance dummies can be collinear while an attendance contrast remains
    # estimable. Check each contrast in the row space, not overall full rank.
    _, singular_values, right_vectors = np.linalg.svd(
        exog, full_matrices=False)
    rank = int(np.sum(singular_values >
        singular_values[0] * max(exog.shape) * np.finfo(float).eps))
    row_space = right_vectors[:rank, :]
    rows = []
    for right in range(1, len(blocks)):
        left = right - 1
        names = model.params.index.to_list()
        contrast = np.zeros(len(names))
        for idx, sign in [(left, -1.0), (right, 1.0)]:
            if idx == 0:
                continue
            key = f"C(BLOCK, Treatment(reference='B0'))[T.B{idx}]"
            contrast[names.index(key)] += sign
        projection = row_space.T @ (row_space @ contrast)
        if np.linalg.norm(contrast - projection) > 1e-6:
            raise RuntimeError(f"Selected block contrast B{right}-B{left} "
                               "is not identifiable in validation")
        test_result = model.t_test(contrast)
        est = float(np.asarray(test_result.effect).item())
        se = float(np.asarray(test_result.sd).item())
        p = float(np.asarray(test_result.pvalue).item())
        rows.append({
            "outcome": outcome, "comparison": f"B{right} minus B{left}",
            "first_block": f"B{left}", "second_block": f"B{right}",
            "estimate": est, "estimate_pp": est * 100 if outcome == "PASS" else np.nan,
            "cluster_robust_se": se, "ci95_low": est - 1.96 * se,
            "ci95_high": est + 1.96 * se, "p_raw": p,
            "n": len(d), "clusters": d["CLASSROOM_ID"].nunique(),
            "validation_design_rank": rank,
            "validation_design_columns": exog.shape[1],
        })
    result = pd.DataFrame(rows)
    if len(result):
        result["p_holm"] = multipletests(result["p_raw"], method="holm")[1]
        result["reject_holm_0_05"] = result["p_holm"] < .05
    return result


def evaluate(args):
    from cmat_analysis.statistics.ordered_fusion import exhaustive_contiguous_partitions
    funcs = imports()
    cluster_split, fit_prepared, grouped_cv, prepare_fusion, bootstrap, partition_fn = funcs[4:]
    cohort = load_cohort(args, funcs)
    TABLES.mkdir(parents=True, exist_ok=True)
    specs = [("7plus", "GROUP_7PLUS", BASE_ORDER)]
    if args.include_pooled:
        specs.append(("6plus_support_sensitivity", "GROUP_6PLUS", POOLED_ORDER))
    source_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT,
        capture_output=True, text=True, check=False
    ).stdout.strip() or "unknown"
    fingerprints = {}
    for name, path in {
        "materias": args.materias or ROOT / "data" / "controlled" / "Materias_pseudonymized.csv",
        "asesorias": args.asesorias or ROOT / "data" / "controlled" / "Asesorias_pseudonymized.csv",
    }.items():
        p = Path(path).expanduser()
        if p.is_file():
            fingerprints[name + "_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = {
        "status": "executed_no_causal_claim",
        "git_commit": source_revision,
        "input_fingerprints": fingerprints,
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "seed": args.seed, "validation_fraction": args.validation_fraction,
        "cv_folds": args.folds, "cv_repeats": args.cv_repeats,
        "lambda_grid_size": args.lambda_grid_size,
        "bootstrap_replicates": args.bootstrap,
        "primary_grouping": "0/1/2/3/4/5/6/7+",
        "outcomes": ["Z_GRADE_PRIMARY", "PASS"],
        "inference": "heldout_cluster_unpenalised_OLS_or_LPM_cluster_Wald",
        "cv_target": "heldout_within_classroom_centered_residual_MSE",
        "results": [], "warnings": [],
    }
    for label, group_col, order in specs:
        for outcome in ["Z_GRADE_PRIMARY", "PASS"]:
            d = prepare_rows(cohort, outcome=outcome, grouping=group_col,
                             order=order)
            prefix = f"{label}_{outcome.lower()}"
            support_table(d, order).to_csv(
                TABLES / f"{prefix}_support.csv", index=False)
            discovery, validation = cluster_split(
                d, validation_fraction=args.validation_fraction, seed=args.seed
            )
            # Fix the discovery/validation split before looking at outcomes.
            cv, lam = grouped_cv(
                discovery, outcome=outcome, group="GROUP", order=order,
                folds=args.folds, repeats=args.cv_repeats,
                seed=args.seed + 1, grid_size=args.lambda_grid_size)
            cv.to_csv(TABLES / f"{prefix}_cv.csv", index=False)
            prepared = prepare_fusion(
                discovery[outcome], discovery["GROUP"],
                discovery["CLASSROOM_ID"], discovery["CLAVECARRERA"], order)
            model = fit_prepared(prepared, lam)
            partitions = exhaustive_contiguous_partitions(prepared)
            partitions.to_csv(
                TABLES / f"{prefix}_exhaustive_partitions.csv", index=False)
            selected_mask = sum(1 << (k - 1) for k in model["boundaries"])
            selected_bic_rank = int(partitions.loc[
                partitions["partition_mask"].eq(selected_mask),
                "rank_bic"].iloc[0])
            blocks = partition_fn(order, model["boundaries"])
            assigned = pd.DataFrame(blocks)
            assigned["selected_lambda"] = lam
            assigned["n_discovery_students"] = len(discovery)
            assigned["n_discovery_clusters"] = discovery["CLASSROOM_ID"].nunique()
            assigned.to_csv(TABLES / f"{prefix}_blocks.csv", index=False)
            levels = pd.DataFrame({
                "group": order,
                "adjusted_level_relative_zero_shrunken": model[
                    "adjusted_levels_relative_zero"],
                "block_id": model["block_ids"],
            })
            levels.to_csv(TABLES / f"{prefix}_fusion_levels.csv", index=False)
            counts = np.zeros(len(order)-1, dtype=int)
            boot_failed = 0
            for b in range(args.bootstrap):
                try:
                    replicate = bootstrap(discovery, seed=args.seed + 1000 + b)
                    _, boot_lam = grouped_cv(
                        replicate, outcome=outcome, group="GROUP", order=order,
                        folds=args.folds, repeats=1,
                        seed=args.seed + 3000 + b,
                        grid_size=args.lambda_grid_size)
                    boot_prepared = prepare_fusion(
                        replicate[outcome], replicate["GROUP"],
                        replicate["CLASSROOM_ID"],
                        replicate["CLAVECARRERA"], order)
                    boot_fit = fit_prepared(boot_prepared, boot_lam)
                    for k in boot_fit["boundaries"]:
                        counts[k-1] += 1
                except (ValueError, RuntimeError, np.linalg.LinAlgError) as error:
                    boot_failed += 1
                    if len(manifest["warnings"]) < 30:
                        manifest["warnings"].append(
                            f"{prefix} bootstrap {b}: {error}")
            successful = args.bootstrap - boot_failed
            boundary = pd.DataFrame({
                "boundary": [f"{order[k-1]}|{order[k]}" for k in range(1, len(order))],
                "selected_full_discovery": [
                    k in model["boundaries"] for k in range(1, len(order))
                ],
                "bootstrap_selected": counts,
                "bootstrap_successful": successful,
                "bootstrap_failed": boot_failed,
                "selection_frequency": (
                    counts / successful if successful else np.full(len(counts), np.nan)
                ),
            })
            boundary.to_csv(TABLES / f"{prefix}_boundary_stability.csv",
                            index=False)
            # Honest test set was never used by CV, selection or bootstrap.
            status = "not_tested"
            try:
                result = refit_validation(validation, outcome, order, blocks)
                result.to_csv(TABLES / f"{prefix}_holdout_wald.csv", index=False)
                status = "completed" if len(result) else "no_boundary_to_test"
            except (ValueError, RuntimeError, KeyError) as exc:
                status = f"blocked: {exc}"
                manifest["warnings"].append(f"{prefix} holdout: {exc}")
            manifest["results"].append({
                "specification": label, "outcome": outcome,
                "n_full": len(d), "clusters_full": d["CLASSROOM_ID"].nunique(),
                "n_discovery": len(discovery),
                "clusters_discovery": discovery["CLASSROOM_ID"].nunique(),
                "n_validation": len(validation),
                "clusters_validation": validation["CLASSROOM_ID"].nunique(),
                "selected_lambda": lam, "selected_blocks": blocks,
                "selected_partition_discovery_bic_rank": selected_bic_rank,
                "bootstrap_successful": successful,
                "validation_status": status,
            })
            print(f"{prefix}: {len(blocks)} blocks; validation={status}")
    output = ROOT / "results" / "paper221" / "run_manifest.json"
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Aggregate tables and manifest:", TABLES.parent)
    return 0


def cli():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    p.add_argument("--materias", type=Path)
    p.add_argument("--asesorias", type=Path)
    p.add_argument("--seed", type=int, default=221)
    p.add_argument("--validation-fraction", type=float, default=.30)
    p.add_argument("--folds", type=int, default=4)
    p.add_argument("--cv-repeats", type=int, default=1)
    p.add_argument("--lambda-grid-size", type=int, default=12)
    p.add_argument("--bootstrap", type=int, default=30)
    p.add_argument("--include-pooled", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    args = cli()
    if args.check:
        required = (ROOT/"paper"/"docs"/"analysis"/"FUSED_LASSO_PROTOCOL.md",
                    ROOT/"cmat_analysis"/"src"/"cmat_analysis"/"statistics"/"ordered_fusion.py")
        missing = [str(p) for p in required if not p.exists()]
        if missing:
            raise SystemExit("Missing: "+", ".join(missing))
        print("Paper 2.2.1 static source layout: OK; data/results NOT checked")
        raise SystemExit(0)
    raise SystemExit(evaluate(args))
