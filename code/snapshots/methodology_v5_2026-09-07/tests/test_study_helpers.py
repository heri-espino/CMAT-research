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


def test_primary_outcome_uses_kde_and_uniform_fallback_as_documented():
    from types import SimpleNamespace
    import numpy as np
    import pandas as pd
    from visitas_analysis.study.outcomes import add_primary_outcomes

    cfg = SimpleNamespace(passing_grade=7.5, random_seed=42, min_classroom_n_for_z=2)
    d = pd.DataFrame({
        "CLASSROOM_ID": ["A"] * 5 + ["B"] * 3,
        "GRADE_CLASS": ["numeric", "numeric", "numeric", "adverse", "adverse", "numeric", "adverse", "adverse"],
        "GRADE_NUMERIC": [5.0, 6.0, 9.0, np.nan, np.nan, 9.0, np.nan, np.nan],
        "SOURCE_ROW": list(range(8)),
    })
    out = add_primary_outcomes(d, cfg)
    audit = out.attrs["imputation_summary"].set_index("CLASSROOM_ID")

    assert audit.loc["A", "method"] == "within_classroom_scipy_gaussian_kde_default_scott"
    assert audit.loc["A", "kde_bw_method"] == "None (SciPy default; Scott factor)"
    assert np.isfinite(float(audit.loc["A", "kde_factor"]))
    assert audit.loc["B", "method"] == "uniform_fallback_no_observed_subpass_grade"

    imputed = out.loc[out["GRADE_CLASS"] == "adverse", "GRADE_PRIMARY"]
    assert (imputed >= 0).all()
    assert (imputed < 7.5).all()
    assert (out.loc[out["GRADE_CLASS"] == "adverse", "PASS"] == 0).all()


def test_exact_visit_grouping_and_all_pairwise_count():
    import pandas as pd
    from visitas_analysis.study.extended_methodology import (
        add_exact_visit_group, games_howell_exact_groups,
    )

    rows = []
    for v in [0, 1, 2, 3, 4]:
        for j in range(5):
            rows.append({"VISITS_CMAT_PERIOD": v, "Z_GRADE_PRIMARY": float(v) + j / 10})
    d = pd.DataFrame(rows)
    grouped = add_exact_visit_group(d)
    assert set(grouped["EXACT_VISIT_GROUP_0_1_2_3_4P"].astype(str)) == {"0", "1", "2", "3", "4+"}
    gh = games_howell_exact_groups(d, population="test")
    assert len(gh) == 10  # C(5,2)
