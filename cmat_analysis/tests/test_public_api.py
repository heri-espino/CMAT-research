"""Import-contract tests for the responsibility-based public API."""


def test_root_import_is_small_and_versioned():
    import cmat_analysis

    assert isinstance(cmat_analysis.__version__, str)
    assert "study" not in cmat_analysis.__all__
    assert "analysis" not in cmat_analysis.__all__


def test_representative_public_imports():
    from cmat_analysis.cohorts import build_study_cohorts
    from cmat_analysis.longitudinal import TemporalPeakConfig, student_temporal_regularity
    from cmat_analysis.measures import add_primary_outcomes
    from cmat_analysis.ppa import build_ppa_progression_cohort
    from cmat_analysis.reporting import write_run_log
    from cmat_analysis.statistics import propensity_att_sensitivity, robust_two_group_tests
    from cmat_analysis.visualization import mpl_apply

    objects = [
        build_study_cohorts,
        student_temporal_regularity,
        add_primary_outcomes,
        build_ppa_progression_cohort,
        write_run_log,
        propensity_att_sensitivity,
        robust_two_group_tests,
        mpl_apply,
    ]
    assert all(callable(obj) for obj in objects)
    assert TemporalPeakConfig.__name__ == "TemporalPeakConfig"


def test_compatibility_paths_delegate_to_canonical_objects():
    from cmat_analysis.cohorts import build_study_cohorts as canonical_cohort
    from cmat_analysis.study.cohort import build_study_cohorts as legacy_cohort
    from cmat_analysis.statistics import robust_two_group_tests as canonical_test
    from cmat_analysis.study.statistics import robust_two_group_tests as legacy_test

    assert canonical_cohort is legacy_cohort
    assert canonical_test is legacy_test
