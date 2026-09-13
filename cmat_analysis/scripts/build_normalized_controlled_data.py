#!/usr/bin/env python3
"""Build the normalized CMAT CSV layer without replacing legacy flat inputs."""
from __future__ import annotations

import argparse, hashlib, json, re, unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ALIASES = {
    "antropologia cultural": ("ANP", "legacy_name_alias"),
    "ingenieria en alimentos": ("IIA", "legacy_name_alias"),
    "ingenieria en logistica": ("ILC", "legacy_name_alias"),
}
SCHOOL_ONLY = {
    "ciencias farmaceuticas": "EDEC",
    "comunicacion e imagen": "EDCS",
    "ingenieria en electronica y comunicaciones": "EDEI",
    "ingenieria en electronica y sistemas inteligentes": "EDEI",
}
PERIOD = {"p": "P", "primavera": "P", "v": "V", "verano": "V", "o": "O", "otono": "O"}
PERIOD_NAME = {"P": "Primavera", "V": "Verano", "O": "Otoño"}


def norm(x):
    s = unicodedata.normalize("NFKD", str(x or "").strip().casefold())
    return re.sub(r"\s+", " ", "".join(c for c in s if not unicodedata.combining(c)))


def clean(x):
    return re.sub(r"\s+", " ", str(x or "").strip())


def sid(prefix, value, n=10):
    return f"{prefix}_{hashlib.sha1(str(value).encode()).hexdigest()[:n].upper()}"


def slug(value, n=56):
    s = re.sub(r"[^A-Z0-9]+", "_", norm(value).upper()).strip("_") or "UNKNOWN"
    return s if len(s) <= n else s[: n - 9].rstrip("_") + "_" + hashlib.sha1(str(value).encode()).hexdigest()[:8].upper()


def pcode(x):
    n = norm(x)
    for key, value in PERIOD.items():
        if n == key or n.startswith(key):
            return value
    return clean(x).upper()


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def build(root: Path):
    c = root / "data" / "controlled"
    cats = root / "data" / "catalogs"
    out = c / "normalized"
    out.mkdir(parents=True, exist_ok=True)

    mpath = c / "Materias_pseudonymized.csv"
    apath = c / "Asesorias_pseudonymized.csv"
    dpath = c / "Diagnostico_pseudonymized.csv"
    spath = cats / "schools.csv"
    cpath = cats / "careers.csv"
    qpath = cats / "course_catalog.csv"
    for path in [mpath, apath, spath, cpath, qpath]:
        if not path.exists():
            raise SystemExit(f"Missing required input: {path}")

    m = pd.read_csv(mpath, dtype=str)
    a = pd.read_csv(apath, dtype=str)
    d = pd.read_csv(dpath, dtype=str) if dpath.exists() else pd.DataFrame()
    schools = pd.read_csv(spath, dtype=str)
    careers = pd.read_csv(cpath, dtype=str)
    catalog = pd.read_csv(qpath, dtype=str)

    school_by_career = careers.set_index("career_id")["school_id"].to_dict()
    career_by_name = {norm(r.career_name): r.career_id for r in careers.itertuples()}

    labels = set(a["carrera"].dropna().map(clean))
    if not d.empty:
        labels |= set(d["career"].dropna().map(clean))
    clrows = []
    for label in sorted(labels, key=lambda x: (norm(x), x)):
        n = norm(label)
        cid = career_by_name.get(n, "")
        method = "normalized_name_exact" if cid else "unresolved"
        if not cid and n in ALIASES:
            cid, method = ALIASES[n]
        clrows.append([sid("CARLBL", label), label, cid, school_by_career.get(cid, SCHOOL_ONLY.get(n, "")), method])
    career_labels = pd.DataFrame(clrows, columns=["career_label_id", "career_label", "career_id", "school_id", "mapping_method"])
    career_label_id = career_labels.set_index("career_label")["career_label_id"].to_dict()

    subj_name = {}
    for x in list(catalog["catalog_name"].dropna()) + list(a["materia"].dropna()):
        x = clean(x)
        subj_name.setdefault(norm(x), x)
    subjects = pd.DataFrame([["SUBJ_" + slug(name), name, "catalog_and_or_advisory"] for name in subj_name.values()], columns=["subject_id", "subject_name", "source_status"])
    subject_id = {norm(r.subject_name): r.subject_id for r in subjects.itertuples()}
    code_counts = catalog["course_code"].value_counts().to_dict()
    variants = catalog.copy()
    variants["catalog_name"] = variants["catalog_name"].map(clean)
    variants["subject_id"] = variants["catalog_name"].map(lambda x: subject_id[norm(x)])
    variants["course_code_ambiguous"] = variants["course_code"].map(lambda x: code_counts[x] > 1)
    variants = variants[["course_code", "subject_id", "catalog_name", "course_code_ambiguous"]].sort_values(["course_code", "catalog_name"])

    subject_labels = pd.DataFrame(
        [[sid("SUBLBL", x), x, subject_id[norm(x)]] for x in sorted(set(a["materia"].dropna().map(clean)), key=lambda x: (norm(x), x))],
        columns=["subject_label_id", "subject_label", "subject_id"],
    )
    subject_label_id = subject_labels.set_index("subject_label")["subject_label_id"].to_dict()

    termset = {(int(float(r.anio)), pcode(r.CLAVESESION)) for r in m.itertuples()}
    termset |= {(int(str(r.fecha)[:4]), pcode(r.periodo)) for r in a.itertuples() if str(r.fecha)[:4].isdigit()}
    if not d.empty:
        termset |= {(int(float(r.year)), pcode(r.period)) for r in d.itertuples() if pd.notna(r.year)}
    terms = pd.DataFrame([[f"{y}_{p}", y, p, PERIOD_NAME.get(p, p)] for y, p in sorted(termset)], columns=["term_id", "year", "period_code", "period_name"])

    topics = pd.DataFrame(
        [[sid("TOPIC", x, 12), x] for x in sorted(set(a["tema"].dropna().map(clean)), key=lambda x: (norm(x), x))],
        columns=["topic_id", "topic_text"],
    )
    topic_id = topics.set_index("topic_text")["topic_id"].to_dict()
    students = sorted(set(m["CLAVEALUMNO"].dropna()) | set(a["id"].dropna()) | (set(d["student_id"].dropna()) if not d.empty else set()))

    diagnostics = pd.DataFrame(columns=["diagnostic_id", "student_id", "career_label_id", "term_id", "partial_1", "partial_2", "partial_3", "partial_4", "total", "exam_type", "percentage"])
    detail = {}
    if not d.empty:
        dd = d.copy()
        dd["career_label_id"] = dd["career"].map(lambda x: career_label_id.get(clean(x), ""))
        dd["term_id"] = dd.apply(lambda r: f"{int(float(r.year))}_{pcode(r.period)}", axis=1)
        dd.insert(0, "diagnostic_id", [f"DIAG_{i:05d}" for i in range(1, len(dd) + 1)])
        diagnostics = dd[["diagnostic_id", "student_id", "career_label_id", "term_id", "partial_1", "partial_2", "partial_3", "partial_4", "total", "exam_type", "percentage"]]
        label_to_career = career_labels.set_index("career_label_id")["career_id"].to_dict()
        diag_map = {(r.student_id, r.term_id): label_to_career.get(r.career_label_id, "") for r in diagnostics.itertuples()}
        for r in m.itertuples():
            t = f"{int(float(r.anio))}_{pcode(r.CLAVESESION)}"
            cid = diag_map.get((r.CLAVEALUMNO, t), "")
            if cid:
                detail.setdefault(r.CLAVECARRERA, Counter())[cid] += 1

    current_ids = set(careers["career_id"])
    ccrows = []
    ccid = {}
    for code in sorted(set(m["CLAVECARRERA"].dropna().map(clean))):
        rid = "CARCODE_" + slug(code, 24)
        ccid[code] = rid
        cid = ""
        method = "unresolved_legacy_code"
        n = 0
        share = ""
        if code in current_ids:
            cid = code
            method = "current_catalog_code_exact"
        if code in detail:
            n = sum(detail[code].values())
            top, topn = detail[code].most_common(1)[0]
            share = topn / n
            if not cid and topn >= 10 and share >= 0.85:
                cid = top
                method = "same_term_diagnostic_high_confidence"
        ccrows.append([rid, code, cid, school_by_career.get(cid, ""), method, n, share])
    career_codes = pd.DataFrame(ccrows, columns=["career_code_id", "career_code", "career_id", "school_id", "mapping_method", "evidence_n", "top_share"])

    pair = {(r.course_code, norm(r.catalog_name)): r.subject_id for r in variants.itertuples()}
    unique = {code: next(iter(set(group.subject_id))) for code, group in variants.groupby("course_code") if len(set(group.subject_id)) == 1}
    attempts = []
    for i, r in enumerate(m.itertuples(), 1):
        code = clean(r.CLAVEVARIANTEMATERIA)
        desc = clean(r.DESCRIBEMATERIA)
        sub = pair.get((code, norm(desc)))
        method = "catalog_code_name_exact"
        if not sub:
            sub = unique.get(code)
            method = "catalog_code_unique" if sub else "description_only"
            sub = sub or subject_id.get(norm(desc), "")
        attempts.append([f"ATTEMPT_{i:06d}", r.CLAVEALUMNO, ccid.get(clean(r.CLAVECARRERA), ""), f"{int(float(r.anio))}_{pcode(r.CLAVESESION)}", str(r.NUMORDEN).replace(".0", ""), code, sub, clean(r.CALIFICACION), r.CLAVEPROFESOR, method])
    course_attempts = pd.DataFrame(attempts, columns=["attempt_id", "student_id", "career_code_id", "term_id", "attempt_number", "course_code", "subject_id", "grade", "instructor_id", "subject_mapping_method"])

    visits = []
    for i, r in a.iterrows():
        ts = clean(r["fecha"])
        visits.append([r["_VISIT_UID"], ts, r["id"], career_label_id.get(clean(r["carrera"]), ""), str(r["semestre"]).replace(".0", ""), r["profesor"], subject_label_id.get(clean(r["materia"]), ""), topic_id.get(clean(r["tema"]), ""), f"{int(ts[:4])}_{pcode(r['periodo'])}"])
    advisory_visits = pd.DataFrame(visits, columns=["visit_id", "timestamp", "student_id", "career_label_id", "semester_number", "advisor_id", "subject_label_id", "topic_id", "term_id"])

    obs = set((r.student_id, r.term_id, "academic", r.career_code_id, "") for r in course_attempts.itertuples())
    obs |= set((r.student_id, r.term_id, "advisory", "", r.career_label_id) for r in advisory_visits.itertuples())
    obs |= set((r.student_id, r.term_id, "diagnostic", "", r.career_label_id) for r in diagnostics.itertuples())
    student_careers = pd.DataFrame([[f"SC_{i:06d}", *x] for i, x in enumerate(sorted(obs), 1)], columns=["observation_id", "student_id", "term_id", "source", "career_code_id", "career_label_id"])

    tables = {
        "schools": schools,
        "careers": careers,
        "career_labels": career_labels,
        "career_codes": career_codes,
        "subjects": subjects,
        "course_variants": variants,
        "subject_labels": subject_labels,
        "terms": terms,
        "topics": topics,
        "students": pd.DataFrame({"student_id": students}),
        "instructors": pd.DataFrame({"instructor_id": sorted(set(m["CLAVEPROFESOR"].dropna()))}),
        "advisors": pd.DataFrame({"advisor_id": sorted(set(a["profesor"].dropna()))}),
        "student_careers": student_careers,
        "course_attempts": course_attempts,
        "advisory_visits": advisory_visits,
        "diagnostics": diagnostics,
    }
    for name, df in tables.items():
        df.to_csv(out / f"{name}.csv", index=False)

    lmap = career_labels.set_index("career_label_id")["career_id"].to_dict()
    cmap = career_codes.set_index("career_code_id")["career_id"].to_dict()
    manifest = {
        "schema_version": 2,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "exact_advisory_timestamp_retained": True,
        "flat_compatibility_sources_preserved": True,
        "table_rows": {k: len(v) for k, v in tables.items()},
        "career_mapping": {
            "mapped_advisory_visits": sum(bool(lmap.get(x)) for x in advisory_visits.career_label_id),
            "total_advisory_visits": len(advisory_visits),
            "academic_career_codes_mapped": sum(bool(x) for x in career_codes.career_id),
            "academic_career_codes_total": len(career_codes),
            "academic_attempts_with_mapped_career": sum(bool(cmap.get(x)) for x in course_attempts.career_code_id),
            "academic_attempts_total": len(course_attempts),
            "rule": "current catalog code exact or same-term diagnostic top_n>=10 and share>=0.85",
        },
        "source_sha256": {p.name: sha(p) for p in [mpath, apath, spath, cpath, qpath] + ([dpath] if dpath.exists() else [])},
    }
    (out / "NORMALIZATION_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = ap.parse_args()
    print(json.dumps(build(args.repo_root.resolve()), ensure_ascii=False, indent=2))
