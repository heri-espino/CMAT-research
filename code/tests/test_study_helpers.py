from visitas_analysis.study.cohort import normalize_identifier, normalize_session, normalize_text, period_index, visit_group


def test_normalization_and_period_order():
    assert normalize_text("Matemáticas Universitarias ") == "MATEMATICAS UNIVERSITARIAS"
    assert normalize_session("P") == "PRIMAVERA"
    assert normalize_session("V") == "VERANO"
    assert normalize_session("OTOÑO") == "OTONO"
    assert period_index(2023, "PRIMAVERA") < period_index(2023, "VERANO") < period_index(2023, "OTONO")
    assert normalize_identifier(123456.0) == "123456"
    assert normalize_identifier("stu_abc123") == "stu_abc123"


def test_visit_groups():
    assert visit_group(0, 3) == "0"
    assert visit_group(1, 3) == "1-2"
    assert visit_group(2, 3) == "1-2"
    assert visit_group(3, 3) == "3"
    assert visit_group(4, 3) == "4+"


def test_hmac_pseudonym_is_stable_across_excel_numeric_types():
    from visitas_analysis.privacy import hmac_pseudonym
    key = b"test-key-that-is-long-enough-for-unit-tests"
    assert hmac_pseudonym(123456, key, "stu") == hmac_pseudonym(123456.0, key, "stu")
    assert hmac_pseudonym(123456, key, "stu") != hmac_pseudonym(123456, key, "prof")


def test_same_day_ppa_behavior_identifies_first_three_same_day():
    import pandas as pd
    from visitas_analysis.study.temporal import same_day_ppa_behavior

    mu = pd.DataFrame({
        "STUDENT_ID": ["a", "b"],
        "YEAR": [2024, 2024],
        "SESSION": ["PRIMAVERA", "PRIMAVERA"],
        "VISITS_CMAT_PERIOD": [3, 3],
    })
    events = pd.DataFrame({
        "STUDENT_ID": ["a", "a", "a", "b", "b", "b"],
        "YEAR": [2024] * 6,
        "SESSION": ["PRIMAVERA"] * 6,
        "VISIT_DATETIME": pd.to_datetime([
            "2024-02-01 09:00", "2024-02-01 11:00", "2024-02-01 14:00",
            "2024-02-01 09:00", "2024-02-02 09:00", "2024-02-03 09:00",
        ]),
    })
    events["VISIT_DATE"] = events["VISIT_DATETIME"].dt.normalize()
    student, summary, _, _ = same_day_ppa_behavior(mu, events, threshold=3)
    a = student.set_index("STUDENT_ID").loc["a"]
    b = student.set_index("STUDENT_ID").loc["b"]
    assert a["FIRST_3_VISITS_SAME_DAY"] == 1
    assert a["MAX_VISITS_ONE_DAY"] == 3
    assert b["FIRST_3_VISITS_SAME_DAY"] == 0
    assert b["MAX_VISITS_ONE_DAY"] == 1


def test_detect_period_peaks_finds_monthly_pattern():
    import numpy as np
    import pandas as pd
    from visitas_analysis.study.temporal import TemporalPeakConfig, detect_period_peaks

    dates = pd.date_range("2024-01-01", "2024-05-15", freq="D")
    peak_dates = pd.to_datetime(["2024-02-01", "2024-03-01", "2024-04-01", "2024-05-01"])
    rows = []
    sid = 0
    for date in dates:
        n = 1
        if min(abs((date - p).days) for p in peak_dates) <= 2:
            n = 20
        for _ in range(n):
            sid += 1
            rows.append({
                "STUDENT_ID": f"s{sid}",
                "YEAR": 2024,
                "SESSION": "PRIMAVERA",
                "VISIT_DATETIME": date,
                "VISIT_DATE": date,
            })
    events = pd.DataFrame(rows)
    peaks, _, intervals = detect_period_peaks(
        events,
        TemporalPeakConfig(min_prominence=2, prominence_fraction=0.05),
        population="test",
    )
    assert len(peaks) >= 4
    assert intervals["gap_days"].median() >= 27
    assert intervals["gap_days"].median() <= 32



def test_temporal_regularity_distinguishes_concentrated_and_distributed_use():
    import pandas as pd
    from visitas_analysis.study.temporal import student_temporal_regularity

    mu = pd.DataFrame({
        "STUDENT_ID": ["a", "b"],
        "YEAR": [2024, 2024],
        "SESSION": ["PRIMAVERA", "PRIMAVERA"],
        "VISITS_CMAT_PERIOD": [4, 4],
    })
    events = pd.DataFrame({
        "STUDENT_ID": ["a"] * 4 + ["b"] * 4,
        "YEAR": [2024] * 8,
        "SESSION": ["PRIMAVERA"] * 8,
        "VISIT_DATETIME": pd.to_datetime([
            "2024-02-01 09:00", "2024-02-02 09:00", "2024-02-03 09:00", "2024-02-04 09:00",
            "2024-02-01 09:00", "2024-03-01 09:00", "2024-04-01 09:00", "2024-05-01 09:00",
        ]),
    })
    events["VISIT_DATE"] = events["VISIT_DATETIME"].dt.normalize()
    r = student_temporal_regularity(mu, events).set_index("STUDENT_ID")
    assert r.loc["a", "ACTIVE_CALENDAR_MONTHS"] == 1
    assert r.loc["b", "ACTIVE_CALENDAR_MONTHS"] == 4
    assert r.loc["a", "REGULARITY_MONTHLY_4"] == 0.25
    assert r.loc["b", "REGULARITY_MONTHLY_4"] == 1.0
    assert r.loc["b", "EFFECTIVE_WEEKS_PER_VISIT"] > r.loc["a", "EFFECTIVE_WEEKS_PER_VISIT"]


def test_monthly_periodicity_diagnostics_recovers_30_day_cycle():
    import pandas as pd
    from visitas_analysis.study.temporal import monthly_periodicity_diagnostics

    dates = pd.date_range("2024-01-01", periods=150, freq="D")
    rows = []
    sid = 0
    for j, date in enumerate(dates):
        n = 1 + (15 if j % 30 == 0 else 0)
        for _ in range(n):
            sid += 1
            rows.append({
                "STUDENT_ID": f"s{sid}", "YEAR": 2024, "SESSION": "PRIMAVERA",
                "VISIT_DATE": date, "VISIT_DATETIME": date,
            })
    events = pd.DataFrame(rows)
    acf, periods = monthly_periodicity_diagnostics(events)
    pooled = acf.loc[acf["SESSION"] == "POOLED"]
    best_lag = int(pooled.loc[pooled["autocorrelation"].idxmax(), "lag_days"])
    assert 29 <= best_lag <= 31
    assert len(periods) == 1


def test_extended_one_two_equivalence_and_transition():
    import pandas as pd
    import numpy as np
    from visitas_analysis.study.extended_analysis import one_two_pooling_analysis, longitudinal_any_visit_transition

    rng = np.random.default_rng(123)
    d = pd.DataFrame({
        "V": [1]*120 + [2]*120,
        "Z": np.r_[rng.normal(0.10, 0.5, 120), rng.normal(0.11, 0.5, 120)],
    })
    eq = one_two_pooling_analysis(d, visits_col="V", outcome_col="Z", equivalence_margin_z=0.20)
    assert eq.loc[0, "status"] == "ok"
    assert bool(eq.loc[0, "equivalent_within_margin_at_05"])

    long = pd.DataFrame({
        "MU_VISITS_CMAT_PERIOD": [0,0,1,1,1,0],
        "VISITS_CMAT_PERIOD": [0,1,0,1,2,0],
        "CALC_VISIT_COVERAGE": [True]*6,
        "MU_VISIT_COVERAGE": [True]*6,
    })
    combos, stat = longitudinal_any_visit_transition(long)
    assert int(combos["n"].sum()) == 6
    assert stat.loc[0, "p_calc_visit_given_mu_visit"] > stat.loc[0, "p_calc_visit_given_no_mu_visit"]


def test_extended_welch_anova_and_career_association_outputs():
    import numpy as np
    import pandas as pd
    from visitas_analysis.study.extended_analysis import (
        welch_anova_visit_groups,
        career_usage_association,
    )

    rng = np.random.default_rng(321)
    groups = np.repeat(["0", "1-2", "3", "4+"], [160, 90, 55, 45])
    means = {"0": 0.0, "1-2": 0.25, "3": 0.35, "4+": 0.37}
    sds = {"0": 1.1, "1-2": 0.8, "3": 0.6, "4+": 0.7}
    z = np.array([rng.normal(means[g], sds[g]) for g in groups])
    career = np.tile(np.repeat(["A", "B", "C", "D", "E"], 70), 1)[: len(groups)]
    d = pd.DataFrame({"G": groups, "Z": z, "CAREER": career})

    omnibus, summary, posthoc = welch_anova_visit_groups(d, group_col="G", outcome_col="Z")
    assert omnibus.loc[0, "test"] == "Welch one-way ANOVA"
    assert omnibus.loc[0, "df_num"] == 3
    assert set(summary["group"]) == {"0", "1-2", "3", "4+"}
    assert len(posthoc) == 6

    assoc, binary, long = career_usage_association(
        d,
        career_col="CAREER",
        group_col="G",
        min_career_n=20,
        permutation_reps=99,
        seed=7,
    )
    assert assoc.loc[0, "careers_included"] >= 4
    assert 0 <= assoc.loc[0, "permutation_p"] <= 1
    assert 0 <= binary.loc[0, "cramers_v_bias_corrected"] <= 1
    assert len(long) > 0


def test_exact_visit_index_uses_career_relative_standardization_and_sparse_tail_sensitivity():
    import numpy as np
    import pandas as pd
    from visitas_analysis.study.extended_analysis import exact_visit_performance_index, exact_visit_index_trend

    rng = np.random.default_rng(2026)
    rows = []
    sid = 0
    for career, career_shift in [("A", 0.20), ("B", -0.15)]:
        for v in range(1, 13):
            n = 24 if v <= 7 else (8 if v <= 10 else 3)
            for _ in range(n):
                sid += 1
                rows.append({
                    "STUDENT_ID": sid,
                    "CLAVECARRERA": career,
                    "VISITS_CMAT_PERIOD": v,
                    "Z_GRADE_PRIMARY": career_shift + 0.02 * v + rng.normal(0, 0.6),
                    "CLASSROOM_ID": f"room{sid % 12}",
                })
    d = pd.DataFrame(rows)
    index, by_career = exact_visit_performance_index(
        d,
        min_career_n_for_standardization=30,
        min_visit=1,
        max_visit=12,
    )
    assert list(index["visits"]) == list(range(1, 13))
    assert "career_relative_index_student_weighted" in index.columns
    assert "ci_method" in index.columns
    assert index.loc[index["visits"] == 11, "stability_flag"].iloc[0] == "low_n"
    assert len(by_career) > 0

    trend = exact_visit_index_trend(
        d,
        min_career_n=30,
        min_visit=1,
        max_visit=12,
        min_exact_group_n_for_stable_trend=20,
    )
    assert set(trend["specification"]) == {"all_exact_counts_1_12", "stable_exact_cells_n_ge_20"}
    stable = trend.loc[trend["specification"] == "stable_exact_cells_n_ge_20"].iloc[0]
    assert stable["exact_visit_counts_included"] == "1,2,3,4,5,6,7"


def test_ppa_revalidation_classifier_flags_post_pass_and_same_period_replica():
    import pandas as pd
    from visitas_analysis.study.ppa_progression import classify_revalidation_records

    d = pd.DataFrame({
        "STUDENT_ID": ["a", "a", "b", "b"],
        "SUBJECT_CODE": ["MAT1012"] * 4,
        "YEAR": [2021, 2023, 2021, 2021],
        "SESSION": ["OTONO", "OTONO", "PRIMAVERA", "PRIMAVERA"],
        "PERIOD_INDEX": [2021 * 3 + 2, 2023 * 3 + 2, 2021 * 3, 2021 * 3],
        "SOURCE_ROW": [0, 1, 2, 3],
        "GRADE_CLASS": ["numeric"] * 4,
        "GRADE_NUMERIC": [9.0, 9.0, 8.0, 8.0],
        "GRADE_TOKEN": ["9", "9", "8", "8"],
        "CLAVECARRERA": ["LAT", "LDS", "LAT", "LDS"],
    })
    out = classify_revalidation_records(d, passing_grade=7.5)
    assert out.loc[out.SOURCE_ROW.eq(1), "ACADEMIC_EVENT_TYPE"].iloc[0] == "likely_post_pass_revalidation"
    assert out.loc[out.SOURCE_ROW.eq(3), "ACADEMIC_EVENT_TYPE"].iloc[0] == "likely_same_period_career_replication"
    assert out.loc[out.SOURCE_ROW.eq(0), "ACADEMIC_EVENT_TYPE"].iloc[0] == "real_attempt_candidate"


def test_ppa_persistence_summary_orders_threshold_groups():
    import pandas as pd
    from visitas_analysis.study.ppa_progression import persistence_by_mu_group

    d = pd.DataFrame({
        "MU_VISIT_GROUP": pd.Categorical(
            ["0", "0", "1-2", "1-2", "3", "3", "4+", "4+"],
            categories=["0", "1-2", "3", "4+"], ordered=True,
        ),
        "CALC_ANY_VISIT": [0, 1, 0, 1, 1, 1, 1, 1],
        "MU_VISITS_CMAT_PERIOD": [0, 0, 1, 2, 3, 3, 4, 5],
        "CALC_VISITS_CMAT_PERIOD": [0, 1, 0, 1, 1, 2, 1, 3],
    })
    s = persistence_by_mu_group(d)
    assert s["mu_visit_group"].tolist() == ["0", "1-2", "3", "4+"]
    assert s.loc[s.mu_visit_group.eq("3"), "p_calc_any_visit"].iloc[0] == 1.0
