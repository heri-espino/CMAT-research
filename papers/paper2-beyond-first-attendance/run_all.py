#!/usr/bin/env python3
"""Re-run the complete executable Paper 2 analysis programme on updated data.

Runs the ported source-controlled runners IN THIS BRANCH in dependency order:
cohort support, fixed-effect Wald/Holm and outcomes, numeric failure and
mixture/shape, four specification controls, Z controls, Shapley, piecewise
follow-up, attendance curves, 100-bootstrap fused lasso, and PPA 0|1–3|4+.

Only aggregate research products are collected and (optionally) pushed.
The historical source manuscripts/decks contain cohort-specific numerical
claims and cannot be scientifically rewritten merely by recompiling LaTeX.
Use --build-publications only AFTER checking/refreshing those claims.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
RUNNERS = BASE / "analysis" / "runners"
PPA = BASE / "analysis" / "ppa-groups" / "run_ppa_groups.py"
RESULTS = BASE / "results"
REPORTS = (
    "15_RESULTADOS_COMPARACION_LPM_LOGIT_CONTROLES.md",
    "17_RESULTADOS_OLS_ZSCORE_CONTROLES.md",
    "19_SHAPLEY_PREDICTIVE_IMPORTANCE.md",
    "22_FOLLOWUP_QUESTIONS_RESULTS.md",
    "24_ATTENDANCE_CURVE_RESULTS.md",
)
# Each runner comes from one named historical analysis and its origin is in
# docs/source-register.tsv. None is a separate paper requiring a checkout.
STAGES = (
    ("visit_support", "run_paper21.py", ()),
    ("holm_outcomes", "run_paper21_outcomes.py", ()),
    ("mixtures_numeric_failure", "run_paper21_mixture.py",
     ("--gmm-bootstrap", "199", "--shape-cv-repeats", "10")),
    ("mixture_shape_checks", "run_paper21_shape_check.py",
     ("--shape-bootstrap", "199", "--shape-cv-repeats", "10")),
    ("four_model_pass_controls", "run_paper21_model_controls_experiment.py", ()),
    ("zscore_controls", "run_paper21_zscore_controls_experiment.py", ()),
    ("grouped_shapley", "run_paper21_shapley_importance.py", ()),
    ("first_and_additional_visits", "run_paper21_followup_questions.py", ()),
    ("attendance_curves", "run_paper21_attendance_curves.py", ()),
    ("fused_100_bootstraps", "run_paper221_fused.py",
     ("--bootstrap", "100", "--include-pooled")),
    ("ppa_three_bands", str(PPA), ()),
    ("holm_figures", "figures_paper21.py", ()),
)

def invoke(cmd: list[str], *, cwd: Path = ROOT, env=None, logdir: Path, name: str):
    print("\n" + name + ": running", flush=True)
    result = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, errors="replace")
    (logdir / (name + ".log")).write_text(result.stdout, encoding="utf-8")
    excerpt = result.stdout.strip().splitlines()[-12:]
    for line in excerpt:
        print(line[:250], flush=True)
    if result.returncode:
        raise RuntimeError(
            f"{name} FAILED (exit {result.returncode}). Full LOCAL log: "
            f"{logdir / (name + '.log')}. Nothing was committed or pushed.")
    return result

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def checked_file(path: Path):
    p = path.expanduser().resolve()
    if not p.is_file():
        raise SystemExit("Authorized local input does not exist: " + str(p))
    return p

def locate_inputs(args):
    if bool(args.materias) != bool(args.asesorias):
        raise SystemExit("Supply BOTH --materias and --asesorias, or neither.")
    if args.materias:
        return checked_file(args.materias), checked_file(args.asesorias)
    from cmat_analysis.config.study_config import get_study_config
    cfg = get_study_config(ROOT)
    m, a = checked_file(cfg.materias_path), checked_file(cfg.asesorias_path)
    print("Using configured study input paths. Check these are the UPDATED "
          "authorized files; supply --materias/--asesorias to override.")
    return m, a

def check_outputs():
    required = (
        ROOT / "results/paper21/tables/10_benchmark_0_vs_1plus.csv",
        ROOT / "results/paper21/tables/26k_zero_inclusive_7plus_pairwise_pass_lpm.csv",
        ROOT / "results/paper21/tables/37_complete_case_gmm_selection.csv",
        ROOT / "results/paper21/tables/shapley_importance/in_sample_shapley_12_models.csv",
        ROOT / "results/paper21/tables/followup_questions/two_part_attendance_z_pass.csv",
        ROOT / "results/paper21/tables/attendance_curves/adjacent_differences_holm.csv",
        ROOT / "results/paper221/run_manifest.json",
        RESULTS / "tables/ppa-groups/pairwise_all_models.csv",
        RESULTS / "provenance/ppa-groups/run_manifest.json",
        ROOT / "results/paper21/figures/fig01_cohort_outcome_attendance.pdf",
    )
    bad = [str(p.relative_to(ROOT)) for p in required if not p.is_file() or not p.stat().st_size]
    if bad:
        raise RuntimeError("Required outputs absent or empty: " + ", ".join(bad))

def check_aggregate_disclosure(path: Path):
    # Fail closed on direct or pseudonymized row-level IDs in public exports.
    names = {"student_id", "id_student", "matricula", "nomina", "student_name",
             "nombre", "correo", "email", "stu_id", "prof_id", "source_row",
             "record_id", "classroom_id", "clavematricula", "claveprofesor"}
    if path.suffix.lower() != ".csv":
        return
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f)
        header = next(r, [])
        unsafe = {x.strip().casefold() for x in header} & names
        if unsafe:
            raise RuntimeError(f"Potential row-level columns in {path}: {unsafe}")
        for i, row in enumerate(r):
            if i >= 1000: break
            if any(cell.startswith(("stu_", "prof_", "advisor_")) for cell in row):
                raise RuntimeError(f"Linked pseudonyms detected in public output: {path}")

def publish_paths(copied: list[Path], extra: list[Path], logdir: Path):
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    if branch != "paper/paper2-beyond-first-attendance":
        raise RuntimeError("For --publish, checkout canonical integration branch; got " + branch)
    files = [*copied, *extra]
    uniq = sorted(set(p.resolve() for p in files if p.is_file()))
    if not uniq:
        raise RuntimeError("Nothing to publish")
    for p in uniq:
        if not p.is_relative_to(ROOT):
            raise RuntimeError("Refusing to stage outside repository: " + str(p))
        if any(bit in ("data", "controlled", "raw") for bit in p.relative_to(ROOT).parts):
            raise RuntimeError("Protected data path may not be staged: " + str(p))
        if p.suffix.lower() in (".csv",):
            check_aggregate_disclosure(p)
    # NEVER stage . or data. Review exact files, not whole directories.
    print(f"\nPreparing {len(uniq)} aggregate/result files for public GitHub.")
    print("Original or pseudonymized student-level files are NEVER staged.")
    for p in uniq:
        print("   " + str(p.relative_to(ROOT)))
    if input("Type PUBLISH to commit these reviewed aggregates: ").strip() != "PUBLISH":
        raise RuntimeError("Canceled before git staging; generated files remain locally.")
    for p in uniq:
        cmd = ["git", "add"]
        if p.suffix.lower() == ".pdf":
            cmd.append("-f")
        cmd.extend(["--", str(p.relative_to(ROOT))])
        invoke(cmd, logdir=logdir, name="git_add_" + str(len(cmd)) + "_" +
               hashlib.sha1(str(p).encode()).hexdigest()[:8])
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).splitlines()
    allowed = {str(p.relative_to(ROOT)).replace("\\", "/") for p in uniq}
    if not set(staged).issubset(allowed):
        raise RuntimeError("Unexpected pre-staged paths found; refusing commit: " +
                           ", ".join(sorted(set(staged) - allowed)))
    if staged:
        invoke(["git", "commit", "-m", "Regenerate complete Paper 2 aggregate experiments"],
               logdir=logdir, name="commit")
    invoke(["git", "push", "origin", "paper/paper2-beyond-first-attendance"],
           logdir=logdir, name="push")
    print("GITHUB PUSH COMPLETED: paper/paper2-beyond-first-attendance")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--materias", type=Path)
    ap.add_argument("--asesorias", type=Path)
    ap.add_argument("--publish", action="store_true",
                    help="Commit/push only reviewed aggregate results on canonical branch")
    ap.add_argument("--build-publications", action="store_true",
                    help="Compile manuscript and Marp from CURRENT source after manual numerical-text review")
    ap.add_argument("--skip-tests", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="Environment and source contracts without reading institutional inputs")
    ap.add_argument("--require-historical-cohort", action="store_true",
                    help="PPA N=6627 historical lock, OFF for updated data")
    args = ap.parse_args()
    logdir = Path(tempfile.mkdtemp(prefix="cmat-paper2-local-logs-"))
    print("Local execution logs (NOT staged):", logdir)
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    if args.check:
        for stage, runner, flags in STAGES:
            if stage in ("mixture_shape_checks", "holm_figures"):
                continue
            p = Path(runner) if Path(runner).is_absolute() else RUNNERS / runner
            invoke([sys.executable, str(p), "--check"],
                   logdir=logdir, name="check_"+stage, env=env)
        print("Checks passed; cohort data NOT read. Run without --check to regenerate.")
        return
    materias, asesorias = locate_inputs(args)
    print("Input fingerprints recorded without storing private paths or microdata.")
    fingerprints = {"materias_sha256": sha256(materias),
                    "asesorias_sha256": sha256(asesorias)}
    if not args.skip_tests:
        invoke([sys.executable, "-m", "pytest", "-q", "cmat_analysis/tests",
                str(BASE / "analysis/ppa-groups/test_ppa_groups.py"),
                str(BASE / "analysis/ppa-groups/test_synthetic_models.py")],
               logdir=logdir, name="synthetic_tests", env=env)
    for stage, runner, flags in STAGES:
        p = Path(runner) if Path(runner).is_absolute() else RUNNERS / runner
        source_flags = [] if stage == "holm_figures" else [
            "--materias", str(materias), "--asesorias", str(asesorias)]
        # PPA historical lock is opt-in; refreshed data are first-class.
        if stage == "ppa_three_bands" and args.require_historical_cohort:
            source_flags += ["--require-historical-cohort"]
        invoke([sys.executable, str(p), *source_flags, *flags],
               logdir=logdir, name=stage, env=env)
    check_outputs()
    # Preserve an audit trail for EACH whole-programme rerun under one paper.
    exports = RESULTS / "experiments"
    exports.mkdir(parents=True, exist_ok=True)
    copied = []
    for rel in ("results/paper21/tables", "results/paper21/figures",
                "results/paper221"):
        src = ROOT / rel
        if not src.is_dir():
            raise RuntimeError("Expected experiment output tree absent: "+ rel)
        dst = exports / rel.removeprefix("results/")
        for path in src.rglob("*"):
            if not path.is_file(): continue
            relative = path.relative_to(src)
            target = dst / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            if target.suffix.lower() == ".csv":
                check_aggregate_disclosure(target)
            copied.append(target)
    notes = exports / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    for name in REPORTS:
        p = ROOT / "notes" / name
        if p.is_file():
            d = notes / name
            shutil.copy2(p, d)
            copied.append(d)
    ppa_files = [p for root in ("tables/ppa-groups", "figures/ppa-groups",
                                "provenance/ppa-groups")
                 for p in (RESULTS / root).rglob("*") if p.is_file()]
    copied.extend(ppa_files)
    # Refresh figures from current aggregates before any publication build.
    latest_figs = ROOT / "results/paper21/figures"
    manuscript_figs = BASE / "manuscript" / "figures"
    for name in ("fig01_cohort_outcome_attendance.pdf",
                 "fig03_04_pairwise_effect_dashboard.pdf",
                 "fig05_pairwise_z_pvalue_dashboard.pdf",
                 "fig06_pairwise_pass_pvalue_dashboard.pdf"):
        src = latest_figs / name
        if not src.is_file():
            raise RuntimeError("Missing regenerated manuscript figure "+name)
        dst = manuscript_figs / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(dst)
    manifest_dir = RESULTS / "provenance"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest = manifest_dir / "latest_full_rerun.json"
    provenance = {
       "run_utc": datetime.now(timezone.utc).isoformat(),
       "runner": "papers/paper2-beyond-first-attendance/run_all.py",
       "pipeline_steps": [n for n,_,__ in STAGES],
       "analysis_finished": True,
       "files_regenerated": len(copied),
       "controlled_input_sha256": fingerprints,
       "publication_note": (
          "Manuscript text, old source citations, slide SVGs and claim wording "
          "are NOT automatically changed by statistical reruns. Scientific "
          "review and regeneration of manuscript/slide text is required after "
          "data updates; do not present old PDFs as new cohort estimates."),
       "source_summary": [{"path": str(p.relative_to(ROOT)), "sha256": sha256(p)}
                          for p in copied if p.is_file()],
    }
    manifest.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    copied.append(manifest)
    print("All executable analysis stages completed. New aggregate files:", len(copied))
    print("NOTE: Manuscript prose and preexisting Marp SVGs are cohort-specific.")
    extra = []
    if args.build_publications:
        manuscript = BASE / "manuscript"
        deck = BASE / "presentation" / "marp"
        # This is an intentional opt-in because these files contain historical
        # claims that cannot be updated from CSVs by ordinary LaTeX compilation.
        invoke(["latexmk", "-pdf", "-interaction=nonstopmode",
                "-halt-on-error", "-outdir=build", "main.tex"],
               cwd=manuscript, logdir=logdir, name="latexmk_manuscript")
        pdf = manuscript / "build/main.pdf"
        if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError("Compiled manuscript PDF invalid")
        shutil.copy2(pdf, manuscript / "paper.pdf")
        extra.append(manuscript / "paper.pdf")
        marp = shutil.which("npx")
        if not marp:
            raise RuntimeError("Missing Node.js/npx; install Marp CLI to build slides")
        invoke([marp, "--yes", "@marp-team/marp-cli@4.2.0",
                "--allow-local-files", "slides.md", "-o", "deck.pdf"],
               cwd=deck, logdir=logdir, name="marp_cli")
        rendered = deck / "deck.pdf"
        if not rendered.is_file() or not rendered.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError("Marp CLI output missing or invalid")
        extra.append(rendered)
    if args.publish:
        publish_paths(copied, extra, logdir)
    else:
        print("No push requested. Use --publish to stage approved aggregate outputs.")
    print("Every report on new data requires rechecking manuscript and slide claims.")

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print("RUN INCOMPLETE:", exc, file=sys.stderr)
        raise SystemExit(1)
