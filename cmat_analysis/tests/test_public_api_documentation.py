"""Contract tests for the documented public API."""

from __future__ import annotations

import importlib
import inspect
from pathlib import Path


EXPECTED_PUBLIC_API = {
    "cmat_analysis.io": (),
    "cmat_analysis.preprocessing": (
        "clean_materias_df",
        "get_salones_with_imputations",
    ),
    "cmat_analysis.cohorts": (
        "StudyData",
        "attach_visits",
        "build_study_cohorts",
        "first_attempts",
        "load_and_clean_inputs",
        "normalize_identifier",
        "normalize_session",
        "normalize_text",
        "period_index",
        "period_label",
        "visit_group",
    ),
    "cmat_analysis.measures": ("add_primary_outcomes",),
    "cmat_analysis.statistics": (
        "add_exact_visit_group",
        "games_howell_exact_groups",
        "bunching_metrics",
        "career_performance_analysis",
        "career_usage_association",
        "career_visit_interaction_model",
        "clustered_career_omnibus",
        "clustered_omnibus_career_test",
        "clustered_omnibus_visit_group_test",
        "clustered_visit_group_omnibus",
        "continuation_curve",
        "dose_group_fixed_effect_model",
        "exact_visit_count_regularity_summary",
        "exact_visit_index_trend",
        "exact_visit_performance_index",
        "group_summary",
        "longitudinal_summary",
        "one_two_pooling_analysis",
        "primary_fixed_effect_models",
        "propensity_att_sensitivity",
        "robust_two_group_tests",
        "secondary_pass_model",
        "temporal_regularity_performance_models",
        "visit_distribution",
        "welch_anova_visit_groups",
    ),
    "cmat_analysis.longitudinal": (
        "TemporalPeakConfig",
        "daily_service_counts",
        "detect_period_peaks",
        "longitudinal_any_visit_transition",
        "monthly_periodicity_diagnostics",
        "peak_spacing_summary",
        "primary_period_visit_events",
        "same_day_ppa_behavior",
        "student_temporal_regularity",
        "top_daily_dates",
    ),
    "cmat_analysis.ppa": (
        "PPAProgressionCohorts",
        "build_ppa_progression_cohort",
        "classify_revalidation_records",
        "course_specific_transition",
        "form_career_crosswalk",
        "later_performance_models",
        "major_delta_z_welch",
        "major_persistence_joint_test",
        "major_persistence_summary",
        "persistence_by_mu_group",
        "persistence_logistic_models",
        "piecewise_threshold_persistence_model",
        "ppa_behavior_profiles",
        "ppa_persistence_association_tests",
    ),
    "cmat_analysis.visualization": (
        "mpl_apply",
        "plotly_apply",
        "set_style",
    ),
    "cmat_analysis.reporting": ("save_figure_variants", "write_run_log"),
    "cmat_analysis.privacy": (
        "canonical_identifier",
        "hmac_pseudonym",
    ),
}


def test_public_api_is_explicit_and_stable() -> None:
    """Ensure canonical namespaces expose exactly the reviewed API."""
    for module_name, expected in EXPECTED_PUBLIC_API.items():
        module = importlib.import_module(module_name)
        assert tuple(module.__all__) == expected, module_name


def test_public_api_has_numpy_style_docstrings() -> None:
    """Require public callables to carry minimally complete NumPy docstrings."""
    failures: list[str] = []
    for module_name, names in EXPECTED_PUBLIC_API.items():
        module = importlib.import_module(module_name)
        if not inspect.getdoc(module):
            failures.append(f"{module_name}: missing module docstring")
        for name in names:
            obj = getattr(module, name)
            if not (inspect.isfunction(obj) or inspect.isclass(obj)):
                continue
            doc = inspect.getdoc(obj) or ""
            if not doc:
                failures.append(f"{module_name}.{name}: missing docstring")
                continue
            signature = inspect.signature(obj)
            params = [
                p
                for p in signature.parameters.values()
                if p.name not in {"self", "cls"}
            ]
            if params and "Parameters\n----------" not in doc:
                failures.append(f"{module_name}.{name}: missing NumPy Parameters section")
            if inspect.isfunction(obj):
                return_annotation = signature.return_annotation
                void_annotations = {None, type(None), "None", "NoneType"}
                if return_annotation is not inspect.Signature.empty and return_annotation not in void_annotations:
                    if "Returns\n-------" not in doc:
                        failures.append(f"{module_name}.{name}: missing NumPy Returns section")
    assert not failures, "\n" + "\n".join(failures)


def test_sphinx_api_page_excludes_compatibility_and_private_modules() -> None:
    """Keep the main Sphinx reference restricted to namespace-level public API."""
    api_index = Path(__file__).resolve().parents[1] / "docs" / "api" / "index.rst"
    text = api_index.read_text(encoding="utf-8")
    forbidden = (
        "cmat_analysis.study",
        "cmat_analysis.analysis",
        "cmat_analysis.pipeline",
        "._core",
        "._group_comparisons",
        "._progression",
    )
    assert not any(token in text for token in forbidden)
