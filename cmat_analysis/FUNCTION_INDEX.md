# Python function and symbol index

> **Generated development inventory.** Search this file before creating a parallel implementation. User/developer API documentation lives in Sphinx under `docs/`.

## Capability map

| Capability | Search terms | Canonical path |
|---|---|---|
| Input reading | `input Excel source validation` | `src/cmat_analysis/io/` |
| Cleaning and preprocessing | `clean normalize transform` | `src/cmat_analysis/preprocessing/` |
| Cohorts and attempts | `cohort attempt revalidation visit group` | `src/cmat_analysis/cohorts/` |
| Academic measures | `grade pass classroom z-score imputation` | `src/cmat_analysis/measures/` |
| Statistical inference | `statistics CI fixed effect robust propensity weighting` | `src/cmat_analysis/statistics/` |
| Longitudinal diagnostics | `temporal peak spacing periodicity transition` | `src/cmat_analysis/longitudinal/` |
| PPA progression and persistence | `PPA persistence calculus threshold progression` | `src/cmat_analysis/ppa/` |
| Visualization | `figure plot style` | `src/cmat_analysis/visualization/` |
| Reporting and provenance | `report table formatting provenance log` | `src/cmat_analysis/reporting/` |
| Privacy | `privacy identifier HMAC anonymized` | `src/cmat_analysis/privacy.py` |
| Compatibility/orchestration | `legacy historical pipeline report` | `src/cmat_analysis/analysis/; src/cmat_analysis/study/; src/cmat_analysis/pipeline/` |

## Inventory

- Python files scanned: **103**
- Reusable symbols: **405**
- Test symbols: **21**

## Reusable symbols

### `scripts/generate_function_index.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `Symbol` | class | 30 | `class Symbol` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py symbol` |
| `_summary` | function | 41 | `def _summary(node: ast.AST) -> str` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py summary` |
| `_signature` | function | 49 | `def _signature(node: ast.FunctionDef \| ast.AsyncFunctionDef \| ast.ClassDef) -> str` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py signature` |
| `_tags` | function | 60 | `def _tags(path: str, qualname: str, summary: str) -> str` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py tags` |
| `Visitor` | class | 71 | `class Visitor(ast.NodeVisitor)` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py visitor` |
| `Visitor.__init__` | method | 72 | `def __init__(self, path: str, is_test: bool) -> None` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py visitor init__` |
| `Visitor._qualname` | method | 78 | `def _qualname(self, name: str) -> str` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py visitor qualname` |
| `Visitor._add` | method | 84 | `def _add(self, node: ast.FunctionDef \| ast.AsyncFunctionDef \| ast.ClassDef, kind: str) -> None` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py visitor add` |
| `Visitor.visit_ClassDef` | method | 89 | `def visit_ClassDef(self, node: ast.ClassDef) -> None` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py visitor visit_classdef` |
| `Visitor.visit_FunctionDef` | method | 95 | `def visit_FunctionDef(self, node: ast.FunctionDef) -> None` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py visitor visit_functiondef` |
| `Visitor.visit_AsyncFunctionDef` | method | 102 | `def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py visitor visit_asyncfunctiondef` |
| `collect` | function | 110 | `def collect() -> tuple[list[Path], list[Symbol], list[str]]` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py collect` |
| `_escape` | function | 130 | `def _escape(text: str) -> str` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py escape` |
| `render` | function | 134 | `def render(files: list[Path], symbols: list[Symbol], errors: list[str]) -> str` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py render` |
| `main` | function | 165 | `def main() -> None` | No docstring; inspect implementation before reuse. | `scripts generate_function_index py main` |

### `src/cmat_analysis/analysis/raw_report_figures.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `ProfessorColorScale` | class | 61 | `class ProfessorColorScale` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py professorcolorscale` |
| `ReportContext` | class | 69 | `class ReportContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py reportcontext` |
| `ClusterContext` | class | 85 | `class ClusterContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py clustercontext` |
| `ParametricSummary` | class | 96 | `class ParametricSummary` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py parametricsummary` |
| `NonParametricSummary` | class | 107 | `class NonParametricSummary` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py nonparametricsummary` |
| `parse_args` | function | 123 | `def parse_args() -> argparse.Namespace` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py parse_args` |
| `main` | function | 151 | `def main() -> int` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py main` |
| `resolve_path` | function | 206 | `def resolve_path(path: Path) -> Path` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py resolve_path` |
| `load_report_context` | function | 210 | `def load_report_context(materias_path: Path, asesorias_path: Path, threshold: float, visit_split: int) -> ReportContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py load_report_context` |
| `build_professor_color_scale` | function | 282 | `def build_professor_color_scale(profes_value_counts: pd.Series) -> ProfessorColorScale` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py build_professor_color_scale` |
| `compute_zscore` | function | 303 | `def compute_zscore(series: pd.Series) -> pd.Series` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py compute_zscore` |
| `summarize_salones` | function | 315 | `def summarize_salones(salones: dict[tuple[int, str, int, str], pd.DataFrame], threshold: float) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py summarize_salones` |
| `pick_comparison_salon_key` | function | 339 | `def pick_comparison_salon_key(summary: pd.DataFrame) -> tuple[int, str, int, str]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py pick_comparison_salon_key` |
| `pick_outlier_salon_key` | function | 350 | `def pick_outlier_salon_key(summary: pd.DataFrame, fallback_key: tuple[int, str, int, str]) -> tuple[int, str, int, str]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py pick_outlier_salon_key` |
| `format_salon_key` | function | 364 | `def format_salon_key(salon_key: tuple[int, str, int, str]) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py format_salon_key` |
| `numeric_array` | function | 369 | `def numeric_array(values: Iterable[object]) -> np.ndarray` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py numeric_array` |
| `ensure_parent_dirs` | function | 373 | `def ensure_parent_dirs(*paths: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py ensure_parent_dirs` |
| `save_figure` | function | 378 | `def save_figure(fig: plt.Figure, *paths: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py save_figure` |
| `save_cluster_grid` | function | 385 | `def save_cluster_grid(grid: sns.matrix.ClusterGrid, *paths: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py save_cluster_grid` |
| `add_relative_colorbar` | function | 392 | `def add_relative_colorbar(ax: plt.Axes, label: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py add_relative_colorbar` |
| `_density_bandwidth` | function | 400 | `def _density_bandwidth(sample: np.ndarray) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py density_bandwidth` |
| `_gaussian_kernel_density` | function | 411 | `def _gaussian_kernel_density(x_grid: np.ndarray, sample: np.ndarray, bandwidth: float) -> np.ndarray` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py gaussian_kernel_density` |
| `extract_kde_curve` | function | 416 | `def extract_kde_curve(ax: plt.Axes, values: Iterable[object], clip: tuple[float, float]=KDE_CLIP, bw_adjust: float=KDE_BW_ADJUST) -> tuple[np.ndarray, np.ndarray] \| None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py extract_kde_curve` |
| `add_split_density` | function | 439 | `def add_split_density(ax: plt.Axes, values: Iterable[object], threshold: float, fail_color: tuple[float, float, float], pass_color: tuple[float, float, float], clip: tuple[float, float]=KDE_CLIP, bw_adjust: float=KDE_BW_ADJUST, alpha: float=0.3, linewidth: float=0.5) -> bool` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py add_split_density` |
| `add_filled_density` | function | 470 | `def add_filled_density(ax: plt.Axes, values: Iterable[object], label: str, clip: tuple[float, float], alpha: float=0.25) -> bool` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py add_filled_density` |
| `average_professor_pass_rates` | function | 494 | `def average_professor_pass_rates(df: pd.DataFrame, score_col: str, profes_ids: np.ndarray, threshold: float) -> tuple[float, float]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py average_professor_pass_rates` |
| `global_pass_rates` | function | 513 | `def global_pass_rates(df: pd.DataFrame, score_col: str, threshold: float) -> tuple[float, float]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py global_pass_rates` |
| `add_pass_rate_legend` | function | 521 | `def add_pass_rate_legend(ax: plt.Axes, below: float, above: float, threshold: float) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py add_pass_rate_legend` |
| `compute_parametric_summary` | function | 533 | `def compute_parametric_summary(group_1: np.ndarray, group_2: np.ndarray) -> ParametricSummary` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py compute_parametric_summary` |
| `cliffs_delta` | function | 546 | `def cliffs_delta(group_1: np.ndarray, group_2: np.ndarray, max_pairs: int=5000000, seed: int=DEFAULT_SEED) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py cliffs_delta` |
| `bootstrap_diff_median` | function | 569 | `def bootstrap_diff_median(group_1: np.ndarray, group_2: np.ndarray, bootstraps: int, seed: int) -> tuple[float, tuple[float, float]]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py bootstrap_diff_median` |
| `bootstrap_ci_two_sample` | function | 587 | `def bootstrap_ci_two_sample(group_1: np.ndarray, group_2: np.ndarray, stat_fn, bootstraps: int, seed: int) -> tuple[float, float]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py bootstrap_ci_two_sample` |
| `compute_non_parametric_summary` | function | 608 | `def compute_non_parametric_summary(group_1: np.ndarray, group_2: np.ndarray, bootstraps: int, seed: int) -> NonParametricSummary` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py compute_non_parametric_summary` |
| `compute_non_parametric_summary.<locals>.stat_cl` | function | 643 | `def stat_cl(sample_1: np.ndarray, sample_2: np.ndarray) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py compute_non_parametric_summary locals stat_cl` |
| `plot_professor_mean_trends` | function | 683 | `def plot_professor_mean_trends(ctx: ReportContext) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_professor_mean_trends` |
| `plot_all_professors_raw` | function | 718 | `def plot_all_professors_raw(ctx: ReportContext) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_all_professors_raw` |
| `plot_split_professor_densities` | function | 739 | `def plot_split_professor_densities(df: pd.DataFrame, score_col: str, profes_ids: np.ndarray, color_scale: ProfessorColorScale, threshold: float, title: str, output_paths: list[Path], y_limit: float \| None, share_mode: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_split_professor_densities` |
| `plot_imputation_comparison` | function | 779 | `def plot_imputation_comparison(data: pd.DataFrame, series: list[tuple[str, str]], title: str, x_label: str, output_paths: list[Path], clip: tuple[float, float]) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_imputation_comparison` |
| `generate_professor_figures` | function | 799 | `def generate_professor_figures(ctx: ReportContext) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py generate_professor_figures` |
| `generate_imputation_figures` | function | 829 | `def generate_imputation_figures(ctx: ReportContext) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py generate_imputation_figures` |
| `plot_visits_histograms` | function | 907 | `def plot_visits_histograms(ctx: ReportContext) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_visits_histograms` |
| `plot_visit_scatter` | function | 943 | `def plot_visit_scatter(df: pd.DataFrame, score_col: str, title: str, y_label: str, output_path: Path, visit_split: int) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_visit_scatter` |
| `plot_parametric_comparison` | function | 978 | `def plot_parametric_comparison(group_1: np.ndarray, group_2: np.ndarray, title: str, output_path: Path, visit_split: int) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_parametric_comparison` |
| `plot_non_parametric_comparison` | function | 1017 | `def plot_non_parametric_comparison(group_1: np.ndarray, group_2: np.ndarray, title: str, output_path: Path, visit_split: int, bootstraps: int, seed: int) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_non_parametric_comparison` |
| `plot_mean_z_by_visits` | function | 1059 | `def plot_mean_z_by_visits(ctx: ReportContext) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_mean_z_by_visits` |
| `generate_visit_figures` | function | 1083 | `def generate_visit_figures(ctx: ReportContext, stats_bootstraps: int, seed: int) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py generate_visit_figures` |
| `build_cluster_context` | function | 1143 | `def build_cluster_context(ctx: ReportContext, min_observations: int, cluster_count: int) -> ClusterContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py build_cluster_context` |
| `plot_cluster_heatmap` | function | 1225 | `def plot_cluster_heatmap(cluster_ctx: ClusterContext) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_cluster_heatmap` |
| `plot_cluster_selection` | function | 1252 | `def plot_cluster_selection(cluster_ctx: ClusterContext) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_cluster_selection` |
| `silverman_bandwidth` | function | 1278 | `def silverman_bandwidth(sample: np.ndarray) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py silverman_bandwidth` |
| `kde_gaussian_grid` | function | 1289 | `def kde_gaussian_grid(x_grid: np.ndarray, sample: np.ndarray, bandwidth: float) -> np.ndarray` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py kde_gaussian_grid` |
| `kde_bootstrap_ci` | function | 1294 | `def kde_bootstrap_ci(x_grid: np.ndarray, sample: np.ndarray, bandwidth: float, bootstraps: int, seed: int) -> tuple[np.ndarray, np.ndarray]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py kde_bootstrap_ci` |
| `plot_cluster_distributions` | function | 1310 | `def plot_cluster_distributions(ctx: ReportContext, cluster_ctx: ClusterContext, with_ci: bool, cluster_ci_bootstraps: int, seed: int) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py plot_cluster_distributions` |
| `generate_cluster_figures` | function | 1387 | `def generate_cluster_figures(ctx: ReportContext, cluster_ctx: ClusterContext, cluster_ci_bootstraps: int, seed: int) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis raw_report_figures py generate_cluster_figures` |

### `src/cmat_analysis/analysis/report_compatible/context.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `BaseContext` | class | 19 | `class BaseContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible context py basecontext` |
| `VisitsContext` | class | 32 | `class VisitsContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible context py visitscontext` |
| `load_base_context` | function | 37 | `def load_base_context(materias_path: Path) -> BaseContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible context py load_base_context` |
| `load_visits_context` | function | 91 | `def load_visits_context(asesorias_path: Path, materias: pd.DataFrame) -> VisitsContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible context py load_visits_context` |

### `src/cmat_analysis/analysis/report_compatible/figures_clusters.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `ClusterContext` | class | 23 | `class ClusterContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py clustercontext` |
| `_initial_medoids` | function | 34 | `def _initial_medoids(distance_matrix: np.ndarray, k: int, seed: int) -> np.ndarray` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py initial_medoids` |
| `_assign_to_medoids` | function | 45 | `def _assign_to_medoids(distance_matrix: np.ndarray, medoids: np.ndarray) -> np.ndarray` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py assign_to_medoids` |
| `_kmedoids_inertia` | function | 49 | `def _kmedoids_inertia(distance_matrix: np.ndarray, medoids: np.ndarray, labels: np.ndarray) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py kmedoids_inertia` |
| `_fit_kmedoids` | function | 53 | `def _fit_kmedoids(distance_matrix: np.ndarray, k: int, seed: int, max_iter: int=100) -> tuple[np.ndarray, float]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py fit_kmedoids` |
| `build_cluster_context` | function | 81 | `def build_cluster_context(ultramerge: pd.DataFrame) -> ClusterContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py build_cluster_context` |
| `plot_cluster_heatmap` | function | 122 | `def plot_cluster_heatmap(cluster_ctx: ClusterContext, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py plot_cluster_heatmap` |
| `plot_cluster_selection` | function | 150 | `def plot_cluster_selection(cluster_ctx: ClusterContext, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py plot_cluster_selection` |
| `assign_notebook_clusters` | function | 171 | `def assign_notebook_clusters(ultramerge: pd.DataFrame, cluster_ctx: ClusterContext) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py assign_notebook_clusters` |
| `_cluster_legend` | function | 177 | `def _cluster_legend(ax, base: BaseContext, below: float, above: float, *, fontsize: str='small') -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py cluster_legend` |
| `_add_shared_cluster_colorbar` | function | 187 | `def _add_shared_cluster_colorbar(fig: plt.Figure, axes) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py add_shared_cluster_colorbar` |
| `_plot_cluster_distribution_axis` | function | 195 | `def _plot_cluster_distribution_axis(ax: plt.Axes, *, base: BaseContext, ultramerge: pd.DataFrame, cluster_id: int, with_ci: bool) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py plot_cluster_distribution_axis` |
| `plot_cluster_distributions` | function | 262 | `def plot_cluster_distributions(base: BaseContext, ultramerge: pd.DataFrame, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py plot_cluster_distributions` |
| `plot_cluster_distributions_with_ci` | function | 278 | `def plot_cluster_distributions_with_ci(base: BaseContext, ultramerge: pd.DataFrame, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_clusters py plot_cluster_distributions_with_ci` |

### `src/cmat_analysis/analysis/report_compatible/figures_imputation.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `plot_single_classroom_comparison` | function | 14 | `def plot_single_classroom_comparison(mean_only_salones, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_imputation py plot_single_classroom_comparison` |
| `plot_global_imputation_phase1` | function | 33 | `def plot_global_imputation_phase1(phase1_salones, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_imputation py plot_global_imputation_phase1` |
| `plot_outlier_phase1` | function | 51 | `def plot_outlier_phase1(legacy_visit_salones, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_imputation py plot_outlier_phase1` |
| `plot_outlier_phase2` | function | 64 | `def plot_outlier_phase2(corrected_visit_salones, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_imputation py plot_outlier_phase2` |
| `plot_global_imputation_phase2` | function | 77 | `def plot_global_imputation_phase2(ultramerge, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_imputation py plot_global_imputation_phase2` |

### `src/cmat_analysis/analysis/report_compatible/figures_professors.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `plot_yearly_professor_variance` | function | 14 | `def plot_yearly_professor_variance(base: BaseContext, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_professors py plot_yearly_professor_variance` |
| `plot_all_professors_png` | function | 45 | `def plot_all_professors_png(base: BaseContext, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_professors py plot_all_professors_png` |
| `plot_reported_professors_split` | function | 70 | `def plot_reported_professors_split(base: BaseContext, ultramerge: pd.DataFrame, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_professors py plot_reported_professors_split` |
| `plot_imputed_professors_split` | function | 108 | `def plot_imputed_professors_split(base: BaseContext, ultramerge: pd.DataFrame, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_professors py plot_imputed_professors_split` |

### `src/cmat_analysis/analysis/report_compatible/figures_tests.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_plot_ecdf` | function | 13 | `def _plot_ecdf(ax, values, *, label: str, color: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_ecdf` |
| `_plot_ecdf_comparison` | function | 21 | `def _plot_ecdf_comparison(group1, group2, *, title: str, xlabel: str, output_name: str, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_ecdf_comparison` |
| `_bootstrap_diff_median` | function | 34 | `def _bootstrap_diff_median(x, y, B=10000, seed=0)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py bootstrap_diff_median` |
| `_bootstrap_ci_two_sample` | function | 46 | `def _bootstrap_ci_two_sample(x, y, stat_fn, B=5000, seed=0, alpha=0.05)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py bootstrap_ci_two_sample` |
| `_cliffs_delta` | function | 60 | `def _cliffs_delta(x, y, max_pairs=5000000, seed=0)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py cliffs_delta` |
| `plot_parametric_student` | function | 77 | `def plot_parametric_student(ultramerge_means, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_parametric_student` |
| `plot_ecdf_student` | function | 102 | `def plot_ecdf_student(ultramerge_means, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_ecdf_student` |
| `plot_parametric_salon` | function | 115 | `def plot_parametric_salon(ultramerge, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_parametric_salon` |
| `plot_ecdf_salon` | function | 131 | `def plot_ecdf_salon(ultramerge, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_ecdf_salon` |
| `plot_nonparametric_student` | function | 144 | `def plot_nonparametric_student(ultramerge_means, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_nonparametric_student` |
| `plot_nonparametric_student.<locals>.stat_median` | function | 156 | `def stat_median(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_nonparametric_student locals stat_median` |
| `plot_nonparametric_student.<locals>.stat_CL` | function | 169 | `def stat_CL(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_nonparametric_student locals stat_cl` |
| `plot_nonparametric_student.<locals>.stat_r_rb` | function | 177 | `def stat_r_rb(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_nonparametric_student locals stat_r_rb` |
| `plot_nonparametric_student.<locals>.stat_delta` | function | 182 | `def stat_delta(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_nonparametric_student locals stat_delta` |
| `plot_nonparametric_salon` | function | 211 | `def plot_nonparametric_salon(ultramerge, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_nonparametric_salon` |
| `plot_nonparametric_salon.<locals>.stat_median` | function | 223 | `def stat_median(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_tests py plot_nonparametric_salon locals stat_median` |

### `src/cmat_analysis/analysis/report_compatible/figures_visits.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `plot_visit_histograms` | function | 12 | `def plot_visit_histograms(asesoria_counts, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_visits py plot_visit_histograms` |
| `plot_salon_scatter` | function | 60 | `def plot_salon_scatter(ultramerge, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_visits py plot_salon_scatter` |
| `plot_student_scatter` | function | 74 | `def plot_student_scatter(ultramerge_means, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_visits py plot_student_scatter` |
| `plot_mean_z_by_visits` | function | 101 | `def plot_mean_z_by_visits(ultramerge_means, layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible figures_visits py plot_mean_z_by_visits` |

### `src/cmat_analysis/analysis/report_compatible/imputation.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `StageContext` | class | 13 | `class StageContext` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py stagecontext` |
| `_add_mean_imputation` | function | 19 | `def _add_mean_imputation(sesion_materias: pd.DataFrame) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py add_mean_imputation` |
| `_silverman_bandwidth` | function | 30 | `def _silverman_bandwidth(sample)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py silverman_bandwidth` |
| `_sample_kde_truncated` | function | 43 | `def _sample_kde_truncated(x_obs, size, low=0.0, high=7.5, rng=None)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py sample_kde_truncated` |
| `_sample_empirical` | function | 64 | `def _sample_empirical(x_obs, size, rng=None)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py sample_empirical` |
| `legacy_impute_nans_from_pre75_kde_df` | function | 71 | `def legacy_impute_nans_from_pre75_kde_df(df, value_col='CALIFICACION', out_col='IMPKDE', low=0.0, high=7.5, min_kde_n=20, seed=42)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py legacy_impute_nans_from_pre75_kde_df` |
| `corrected_impute_nans_from_pre75_kde_df` | function | 104 | `def corrected_impute_nans_from_pre75_kde_df(df, value_col='CALIFICACION', out_col='IMPKDE', low=0.0, high=7.4, min_kde_n=20, seed=42, fallback='uniform', constant_value=6.5, global_source=None)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py corrected_impute_nans_from_pre75_kde_df` |
| `corrected_impute_nans_from_pre75_kde_df.<locals>._borrow_pool` | function | 128 | `def _borrow_pool()` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py corrected_impute_nans_from_pre75_kde_df locals borrow_pool` |
| `build_salones_mean_only` | function | 174 | `def build_salones_mean_only(materias: pd.DataFrame, profes_ids) -> dict[SalonKey, pd.DataFrame]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py build_salones_mean_only` |
| `build_salones_with_imputer` | function | 188 | `def build_salones_with_imputer(materias: pd.DataFrame, profes_ids, imputer, *, imputer_kwargs: dict \| None=None) -> dict[SalonKey, pd.DataFrame]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py build_salones_with_imputer` |
| `concat_salones` | function | 219 | `def concat_salones(salones: dict[SalonKey, pd.DataFrame]) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py concat_salones` |
| `compute_ultramerge_means` | function | 225 | `def compute_ultramerge_means(ultramerge: pd.DataFrame, materias: pd.DataFrame) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible imputation py compute_ultramerge_means` |

### `src/cmat_analysis/analysis/report_compatible/kde_safe.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `numeric_values` | function | 11 | `def numeric_values(values) -> np.ndarray` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py numeric_values` |
| `scott_bandwidth` | function | 15 | `def scott_bandwidth(sample: np.ndarray, bw_adjust: float=1.0) -> float \| None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py scott_bandwidth` |
| `silverman_bandwidth` | function | 25 | `def silverman_bandwidth(sample: np.ndarray) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py silverman_bandwidth` |
| `gaussian_kde_grid` | function | 37 | `def gaussian_kde_grid(x_grid: np.ndarray, sample: np.ndarray, bandwidth: float) -> np.ndarray` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py gaussian_kde_grid` |
| `kde_curve` | function | 42 | `def kde_curve(values, *, clip: tuple[float, float] \| None, bw_adjust: float=0.5, cut: float=0.0, gridsize: int=200) -> tuple[np.ndarray, np.ndarray] \| None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py kde_curve` |
| `_next_color` | function | 68 | `def _next_color(ax, color)` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py next_color` |
| `plot_filled_kde` | function | 72 | `def plot_filled_kde(ax, values, *, label: str, clip: tuple[float, float] \| None=None, bw_adjust: float=0.5, alpha: float=0.2, color=None) -> tuple[np.ndarray, np.ndarray] \| None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py plot_filled_kde` |
| `plot_split_kde` | function | 92 | `def plot_split_kde(ax, values, *, threshold: float, left_color, right_color, clip: tuple[float, float]=(0.0, 10.0), bw_adjust: float=0.5, alpha: float=0.3, linewidth: float=0.5) -> tuple[np.ndarray, np.ndarray] \| None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py plot_split_kde` |
| `plot_hist_with_kde` | function | 126 | `def plot_hist_with_kde(ax, values, *, bins: int, clip: tuple[float, float] \| None=None, bw_adjust: float=0.5) -> tuple[np.ndarray, np.ndarray] \| None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py plot_hist_with_kde` |
| `kde_bootstrap_ci` | function | 146 | `def kde_bootstrap_ci(x_grid: np.ndarray, sample: np.ndarray, bandwidth: float, *, bootstraps: int=200, q: tuple[float, float]=(2.5, 97.5), rng=None) -> tuple[np.ndarray, np.ndarray]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible kde_safe py kde_bootstrap_ci` |

### `src/cmat_analysis/analysis/report_compatible/main.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `parse_args` | function | 65 | `def parse_args() -> argparse.Namespace` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible main py parse_args` |
| `run_raw_report_figures` | function | 73 | `def run_raw_report_figures(*, materias_path: Path=DEFAULT_MATERIAS, asesorias_path: Path=DEFAULT_ASESORIAS, output_root: Path=DEFAULT_OUTPUT_ROOT, figures_dir: Path \| None=None) -> dict[str, Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible main py run_raw_report_figures` |
| `main` | function | 152 | `def main() -> int` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible main py` |

### `src/cmat_analysis/analysis/report_compatible/plot_helpers.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `OutputLayout` | class | 13 | `class OutputLayout` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible plot_helpers py outputlayout` |
| `build_output_layout` | function | 20 | `def build_output_layout(root: Path) -> OutputLayout` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible plot_helpers py build_output_layout` |
| `ensure_output_dirs` | function | 30 | `def ensure_output_dirs(layout: OutputLayout) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible plot_helpers py ensure_output_dirs` |
| `save_figure` | function | 36 | `def save_figure(fig: plt.Figure, *paths: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible plot_helpers py save_figure` |
| `save_cluster_grid` | function | 43 | `def save_cluster_grid(grid, *paths: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible plot_helpers py save_cluster_grid` |
| `add_half_blues_colorbar` | function | 50 | `def add_half_blues_colorbar(ax: plt.Axes, label: str='Proporción de estudiantes') -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible plot_helpers py add_half_blues_colorbar` |
| `pass_rate_handles` | function | 58 | `def pass_rate_handles(left_color, right_color, left_label: str, right_label: str) -> tuple[list[Line2D], list[str]]` | No docstring; inspect implementation before reuse. | `src cmat_analysis analysis report_compatible plot_helpers py pass_rate_handles` |

### `src/cmat_analysis/cohorts/_core.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `normalize_text` | function | 26 | `def normalize_text(value: object) -> str \| None` | Normalize free text to uppercase, accent-free, whitespace-collapsed form. | `src cmat_analysis cohorts core py normalize_text normalize free text to uppercase accent-free whitespace-collapsed form` |
| `normalize_session` | function | 49 | `def normalize_session(value: object) -> str \| None` | Normalize an academic-session label to the canonical CMAT session vocabulary. | `src cmat_analysis cohorts core py normalize_session normalize an academic-session label to canonical cmat session` |
| `period_index` | function | 66 | `def period_index(year: int \| float, session: object) -> int` | Map an academic year and session to the project chronological period index. | `src cmat_analysis cohorts core py period_index map an academic year session to project chronological` |
| `period_label` | function | 87 | `def period_label(year: int \| float, session: object) -> str` | Build the canonical textual label for an academic period. | `src cmat_analysis cohorts core py period_label build canonical textual label an academic period` |
| `visit_group` | function | 105 | `def visit_group(visits: int \| float, threshold: int=3) -> str` | Map an observed visit count to the configured threshold group. | `src cmat_analysis cohorts core py visit_group map an observed visit count to configured threshold` |
| `StudyData` | class | 131 | `class StudyData` | Container for normalized study inputs and audit metadata. | `src cmat_analysis cohorts core py studydata container normalized study inputs audit metadata` |
| `normalize_identifier` | function | 156 | `def normalize_identifier(value: object) -> str \| None` | Normalize numeric or pseudonymized identifiers without requiring numbers. | `src cmat_analysis cohorts core py normalize_identifier normalize numeric or pseudonymized identifiers without requiring numbers` |
| `_read_table` | function | 179 | `def _read_table(path: Path) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis cohorts core py read_table` |
| `_classify_grade` | function | 188 | `def _classify_grade(value: object, adverse: set[str], non_attempt: set[str]) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis cohorts core py classify_grade` |
| `load_and_clean_inputs` | function | 200 | `def load_and_clean_inputs(config) -> StudyData` | Read and normalize academic and CMAT advisory source tables. | `src cmat_analysis cohorts core py load_and_clean_inputs read normalize academic cmat advisory source tables` |
| `_subject_mask` | function | 329 | `def _subject_mask(df: pd.DataFrame, code: str, name: str) -> pd.Series` | No docstring; inspect implementation before reuse. | `src cmat_analysis cohorts core py subject_mask` |
| `_eligible_attempts` | function | 333 | `def _eligible_attempts(df: pd.DataFrame, code: str, name: str) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis cohorts core py eligible_attempts` |
| `first_attempts` | function | 339 | `def first_attempts(df: pd.DataFrame, code: str, name: str) -> pd.DataFrame` | Select the first eligible attempt of a named subject for each student. | `src cmat_analysis cohorts core py first_attempts select first eligible attempt of a named subject` |
| `_visit_counts` | function | 361 | `def _visit_counts(advisories: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]` | No docstring; inspect implementation before reuse. | `src cmat_analysis cohorts core py visit_counts` |
| `attach_visits` | function | 377 | `def attach_visits(attempts: pd.DataFrame, advisories: pd.DataFrame, *, threshold: int) -> pd.DataFrame` | Attach course-level and period-level CMAT visit counts to academic attempts. | `src cmat_analysis cohorts core py attach_visits attach course-level period-level cmat visit counts to academic` |
| `build_study_cohorts` | function | 417 | `def build_study_cohorts(data: StudyData, config) -> dict[str, pd.DataFrame]` | Construct the reusable MU, Calculus, and longitudinal study cohorts. | `src cmat_analysis cohorts core py build_study_cohorts construct reusable mu calculus longitudinal study` |

### `src/cmat_analysis/config/settings.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `VisitAnalysisSettings` | class | 8 | `class VisitAnalysisSettings` | No docstring; inspect implementation before reuse. | `src cmat_analysis config settings py visitanalysissettings` |
| `get_settings` | function | 20 | `def get_settings(project_root: Path \| None=None) -> VisitAnalysisSettings` | No docstring; inspect implementation before reuse. | `src cmat_analysis config settings py get_settings` |

### `src/cmat_analysis/config/study_config.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `CMATStudyConfig` | class | 8 | `class CMATStudyConfig` | Pre-specified choices shared by the reproducible CMAT study runners. | `src cmat_analysis config study_config py cmatstudyconfig pre-specified choices shared by reproducible cmat study runners` |
| `get_study_config` | function | 57 | `def get_study_config(project_root: Path \| None=None) -> CMATStudyConfig` | No docstring; inspect implementation before reuse. | `src cmat_analysis config study_config py get_study_config` |

### `src/cmat_analysis/io/concentrado_reader.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `read_concentrado` | function | 9 | `def read_concentrado()` | No docstring; inspect implementation before reuse. | `src cmat_analysis io concentrado_reader py read_concentrado` |

### `src/cmat_analysis/longitudinal/_temporal.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `TemporalPeakConfig` | class | 11 | `class TemporalPeakConfig` | Configuration for descriptive temporal peak detection. | `src cmat_analysis longitudinal temporal py temporalpeakconfig configuration descriptive peak detection` |
| `primary_period_visit_events` | function | 43 | `def primary_period_visit_events(mu: pd.DataFrame, advisories: pd.DataFrame) -> pd.DataFrame` | Return every CMAT visit made during each student's first-MU academic period. | `src cmat_analysis longitudinal temporal py primary_period_visit_events return every cmat visit made during each student` |
| `daily_service_counts` | function | 73 | `def daily_service_counts(events: pd.DataFrame, population: str) -> pd.DataFrame` | Aggregate visit events to daily service volume within academic periods. | `src cmat_analysis longitudinal temporal py daily_service_counts aggregate visit events to daily service volume within` |
| `same_day_ppa_behavior` | function | 104 | `def same_day_ppa_behavior(mu: pd.DataFrame, mu_events: pd.DataFrame, threshold: int=3) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]` | Characterize concentrated same-day attendance around the PPA threshold. | `src cmat_analysis longitudinal temporal py same_day_ppa_behavior characterize concentrated same-day attendance around ppa threshold` |
| `same_day_ppa_behavior.<locals>._max_bucket` | function | 215 | `def _max_bucket(v: int) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis longitudinal temporal py same_day_ppa_behavior locals max_bucket` |
| `top_daily_dates` | function | 246 | `def top_daily_dates(daily: pd.DataFrame, n: int=25) -> pd.DataFrame` | Return the busiest observed service dates from an aggregated daily table. | `src cmat_analysis longitudinal temporal py top_daily_dates return busiest observed service dates an aggregated daily` |
| `detect_period_peaks` | function | 268 | `def detect_period_peaks(events: pd.DataFrame, config: TemporalPeakConfig \| None=None, population: str='All CMAT') -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]` | Detect separated local peaks in daily CMAT activity. | `src cmat_analysis longitudinal temporal py detect_period_peaks detect separated local peaks in daily cmat activity` |
| `peak_spacing_summary` | function | 392 | `def peak_spacing_summary(peaks: pd.DataFrame, intervals: pd.DataFrame, config: TemporalPeakConfig \| None=None) -> pd.DataFrame` | Summarize the number and spacing of detected service-use peaks. | `src cmat_analysis longitudinal temporal py peak_spacing_summary summarize number spacing of detected service-use peaks` |
| `student_temporal_regularity` | function | 447 | `def student_temporal_regularity(mu: pd.DataFrame, mu_events: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', assessment_cycles: int=4) -> pd.DataFrame` | Construct student-level temporal-distribution measures for CMAT use. | `src cmat_analysis longitudinal temporal py student_temporal_regularity construct student-level temporal-distribution measures cmat use` |
| `monthly_periodicity_diagnostics` | function | 572 | `def monthly_periodicity_diagnostics(events: pd.DataFrame, *, lag_min: int=14, lag_max: int=45, candidate_period_low: int=21, candidate_period_high: int=42, population: str='All CMAT') -> tuple[pd.DataFrame, pd.DataFrame]` | Estimate descriptive monthly-cycle diagnostics from daily service load. | `src cmat_analysis longitudinal temporal py monthly_periodicity_diagnostics estimate descriptive monthly-cycle diagnostics daily service load` |

### `src/cmat_analysis/measures/_grades.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_scipy_default_kde_draws` | function | 8 | `def _scipy_default_kde_draws(obs: np.ndarray, size: int, low: float, high: float, rng: np.random.Generator) -> tuple[np.ndarray, float \| None, str]` | Draw from scipy.stats.gaussian_kde using SciPy's default bandwidth. | `src cmat_analysis measures grades py scipy_default_kde_draws draw scipy stats gaussian_kde using s default bandwidth` |
| `_uniform_draws` | function | 69 | `def _uniform_draws(size: int, low: float, high: float, rng: np.random.Generator) -> np.ndarray` | Random U(low, high) draws; high is exclusive for NumPy's Generator. | `src cmat_analysis measures grades py uniform_draws random u low high draws is exclusive numpy` |
| `_uniform_quantiles` | function | 76 | `def _uniform_quantiles(size: int, low: float, high: float) -> np.ndarray` | Deterministic interior points from a uniform distribution. | `src cmat_analysis measures grades py uniform_quantiles deterministic interior points a uniform distribution` |
| `add_primary_outcomes` | function | 88 | `def add_primary_outcomes(df: pd.DataFrame, config) -> pd.DataFrame` | Create continuous classroom-relative performance and pass/fail outcomes. | `src cmat_analysis measures grades py add_primary_outcomes create continuous classroom-relative performance pass fail outcomes` |
| `add_primary_outcomes.<locals>.zscore` | function | 180 | `def zscore(series: pd.Series) -> pd.Series` | No docstring; inspect implementation before reuse. | `src cmat_analysis measures grades py add_primary_outcomes locals zscore` |

### `src/cmat_analysis/pipeline/main_pipeline.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `run_visitas_pipeline` | function | 10 | `def run_visitas_pipeline(settings: Any, *, include_report_assets: bool=True, include_raw_figures: bool=True) -> dict[str, object]` | Regenerate project outputs from the canonical raw Excel inputs. | `src cmat_analysis pipeline main_pipeline py run_visitas_pipeline regenerate project outputs canonical raw excel inputs` |

### `src/cmat_analysis/ppa/_progression.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `PPAProgressionCohorts` | class | 43 | `class PPAProgressionCohorts` | Container for reconstructed PPA progression cohorts and audits. | `src cmat_analysis ppa progression py ppaprogressioncohorts container reconstructed cohorts audits` |
| `_subject_mask` | function | 76 | `def _subject_mask(df: pd.DataFrame, code: str, name: str) -> pd.Series` | No docstring; inspect implementation before reuse. | `src cmat_analysis ppa progression py subject_mask` |
| `classify_revalidation_records` | function | 82 | `def classify_revalidation_records(academics: pd.DataFrame, *, passing_grade: float=7.5) -> pd.DataFrame` | Flag later rows after an observed pass as likely revalidation/replication. | `src cmat_analysis ppa progression py classify_revalidation_records flag later rows after an observed pass as` |
| `_numeric_classroom_reference_z` | function | 174 | `def _numeric_classroom_reference_z(history: pd.DataFrame, *, code: str, name: str, min_classroom_n: int=5) -> pd.DataFrame` | Compute numeric-grade Z using the actual course classroom as reference. | `src cmat_analysis ppa progression py numeric_classroom_reference_z compute numeric-grade z using actual course classroom as` |
| `_next_regular_term` | function | 216 | `def _next_regular_term(year: int, session: str) -> tuple[int, str] \| None` | No docstring; inspect implementation before reuse. | `src cmat_analysis ppa progression py next_regular_term` |
| `_period_form_career` | function | 227 | `def _period_form_career(advisories: pd.DataFrame) -> pd.DataFrame` | Most frequently recorded Google-Form career for each student-period. | `src cmat_analysis ppa progression py period_form_career most frequently recorded google-form career each student-period` |
| `build_ppa_progression_cohort` | function | 259 | `def build_ppa_progression_cohort(data, config) -> PPAProgressionCohorts` | Build strict MU -> Calculus cohorts under the PPA1 first-semester assumption. | `src cmat_analysis ppa progression py build_ppa_progression_cohort build strict mu calculus cohorts under ppa1 first-semester` |
| `ppa_behavior_profiles` | function | 455 | `def ppa_behavior_profiles(df: pd.DataFrame) -> pd.DataFrame` | Eight observable MU-group x later-Calculus-use profiles. | `src cmat_analysis ppa progression py ppa_behavior_profiles eight observable mu-group x later-calculus-use profiles` |
| `persistence_by_mu_group` | function | 487 | `def persistence_by_mu_group(df: pd.DataFrame) -> pd.DataFrame` | P(Calculus CMAT use \| MU visit group) with Wilson intervals. | `src cmat_analysis ppa progression py persistence_by_mu_group p calculus cmat use mu visit group wilson` |
| `_two_group_risk_comparison` | function | 520 | `def _two_group_risk_comparison(df: pd.DataFrame, *, group_col: str, event_col: str, exposed_value: str, reference_value: str, label: str) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis ppa progression py two_group_risk_comparison` |
| `ppa_persistence_association_tests` | function | 575 | `def ppa_persistence_association_tests(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]` | Omnibus 4x2 association plus the pre-specified exact-3 vs 4+ contrast. | `src cmat_analysis ppa progression py ppa_persistence_association_tests omnibus x2 association plus pre-specified exact-3 vs contrast` |
| `_collapse_rare` | function | 612 | `def _collapse_rare(series: pd.Series, min_n: int=30) -> pd.Series` | No docstring; inspect implementation before reuse. | `src cmat_analysis ppa progression py collapse_rare` |
| `persistence_logistic_models` | function | 619 | `def persistence_logistic_models(df: pd.DataFrame, *, min_career_n: int=30) -> pd.DataFrame` | Cluster-robust logistic models for later CMAT use. | `src cmat_analysis ppa progression py persistence_logistic_models cluster-robust logistic models later cmat use` |
| `piecewise_threshold_persistence_model` | function | 673 | `def piecewise_threshold_persistence_model(df: pd.DataFrame, *, cap_visits: int=12) -> pd.DataFrame` | Descriptive piecewise logit around V=3; explicitly not an RD design. | `src cmat_analysis ppa progression py piecewise_threshold_persistence_model descriptive piecewise logit around v explicitly not an` |
| `later_performance_models` | function | 717 | `def later_performance_models(df: pd.DataFrame, *, min_career_n: int=30) -> pd.DataFrame` | Predict later Calculus classroom-relative performance from prior MU information. | `src cmat_analysis ppa progression py later_performance_models predict later calculus classroom-relative performance prior mu information` |
| `major_persistence_summary` | function | 773 | `def major_persistence_summary(df: pd.DataFrame, *, min_n: int=30) -> pd.DataFrame` | Descriptive adoption/persistence/academic trajectory by official MU major. | `src cmat_analysis ppa progression py major_persistence_summary descriptive adoption persistence academic trajectory by official mu` |
| `course_specific_transition` | function | 810 | `def course_specific_transition(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]` | 2x2 transition using course-tagged MU and Calculus advisory records. | `src cmat_analysis ppa progression py course_specific_transition x2 transition using course-tagged mu calculus advisory records` |
| `form_career_crosswalk` | function | 845 | `def form_career_crosswalk(df: pd.DataFrame) -> pd.DataFrame` | Observed official-code x Google-Form-career pairs among users in the cohort. | `src cmat_analysis ppa progression py form_career_crosswalk observed official-code x google-form-career pairs among users in` |
| `major_persistence_joint_test` | function | 875 | `def major_persistence_joint_test(df: pd.DataFrame, *, min_career_n: int=30) -> pd.DataFrame` | Joint Wald test for official MU degree program in the adjusted persistence logit. | `src cmat_analysis ppa progression py major_persistence_joint_test joint wald test official mu degree program in` |
| `major_delta_z_welch` | function | 915 | `def major_delta_z_welch(df: pd.DataFrame, *, min_n: int=30) -> pd.DataFrame` | Welch ANOVA of classroom-relative academic change (Delta Z) across majors. | `src cmat_analysis ppa progression py major_delta_z_welch welch anova of classroom-relative academic change delta z` |

### `src/cmat_analysis/preprocessing/_cleaning.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `clean_materias_df` | function | 14 | `def clean_materias_df(materias: pd.DataFrame) -> pd.DataFrame` | Clean the historical academic-record table used by legacy CMAT analyses. | `src cmat_analysis preprocessing cleaning py clean_materias_df clean historical academic-record table used by legacy cmat` |
| `_silverman_bandwidth` | function | 47 | `def _silverman_bandwidth(x)` | No docstring; inspect implementation before reuse. | `src cmat_analysis preprocessing cleaning py silverman_bandwidth` |
| `_sample_kde_truncated` | function | 60 | `def _sample_kde_truncated(x_obs, size, low=0.0, high=7.5, rng=None)` | No docstring; inspect implementation before reuse. | `src cmat_analysis preprocessing cleaning py sample_kde_truncated` |
| `_sample_empirical` | function | 79 | `def _sample_empirical(x_obs, size, rng=None)` | No docstring; inspect implementation before reuse. | `src cmat_analysis preprocessing cleaning py sample_empirical` |
| `impute_nans_from_pre75_kde_df` | function | 85 | `def impute_nans_from_pre75_kde_df(df, value_col='CALIFICACION', out_col='IMPKDE', low=0.0, high=7.4, min_kde_n=20, seed=42, fallback='uniform', constant_value=6.5, prefer_empirical_if_small=True, global_source=None, debug=False)` | No docstring; inspect implementation before reuse. | `src cmat_analysis preprocessing cleaning py impute_nans_from_pre75_kde_df` |
| `impute_nans_from_pre75_kde_df.<locals>._borrow_pool` | function | 107 | `def _borrow_pool()` | No docstring; inspect implementation before reuse. | `src cmat_analysis preprocessing cleaning py impute_nans_from_pre75_kde_df locals borrow_pool` |
| `get_salones_with_imputations` | function | 165 | `def get_salones_with_imputations(materias: pd.DataFrame) -> dict[tuple[object, object, object, object], pd.DataFrame]` | Split academic records by classroom and add the historical imputed grade measures. | `src cmat_analysis preprocessing cleaning py get_salones_with_imputations split academic records by classroom add historical imputed` |
| `limpieza_datos` | function | 244 | `def limpieza_datos()` | No docstring; inspect implementation before reuse. | `src cmat_analysis preprocessing cleaning py limpieza_datos` |

### `src/cmat_analysis/privacy.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `canonical_identifier` | function | 18 | `def canonical_identifier(value: object) -> str` | Convert an identifier to a stable textual representation. | `src cmat_analysis privacy py canonical_identifier convert an identifier to a stable textual representation` |
| `hmac_pseudonym` | function | 48 | `def hmac_pseudonym(value: object, key: bytes, namespace: str, length: int=32) -> str` | Create a deterministic keyed pseudonym for an identifier. | `src cmat_analysis privacy py hmac_pseudonym create a deterministic keyed pseudonym an identifier` |

### `src/cmat_analysis/release_figures.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `figure_name` | function | 75 | `def figure_name(key: str) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis release_figures py figure_name` |
| `figure_path` | function | 79 | `def figure_path(figures_dir: Path, key: str) -> Path` | No docstring; inspect implementation before reuse. | `src cmat_analysis release_figures py figure_path` |
| `figure_stem` | function | 83 | `def figure_stem(key: str) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis release_figures py figure_stem` |
| `report_figure_names` | function | 87 | `def report_figure_names() -> list[str]` | No docstring; inspect implementation before reuse. | `src cmat_analysis release_figures py report_figure_names` |

### `src/cmat_analysis/reporting/descriptive_pipeline.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `AnalyticalBundle` | class | 72 | `class AnalyticalBundle` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting descriptive_pipeline py analyticalbundle` |
| `make_classroom_unit_id` | function | 88 | `def make_classroom_unit_id(df: pd.DataFrame) -> pd.Series` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting descriptive_pipeline py make_classroom_unit_id` |
| `clean_materias_with_tracking` | function | 93 | `def clean_materias_with_tracking(materias_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting descriptive_pipeline py clean_materias_with_tracking` |
| `enrich_materias_with_visits` | function | 185 | `def enrich_materias_with_visits(materias_cleaned: pd.DataFrame, asesorias_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting descriptive_pipeline py enrich_materias_with_visits` |
| `build_analytical_bundle` | function | 233 | `def build_analytical_bundle(project_root: Path, materias_path: Path, asesorias_path: Path) -> AnalyticalBundle` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting descriptive_pipeline py build_analytical_bundle` |

### `src/cmat_analysis/reporting/methodology_build.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_sha256` | function | 26 | `def _sha256(path: Path) -> str` | Return the SHA-256 digest of a controlled input file. | `src cmat_analysis reporting methodology_build py sha256 return sha-256 digest of a controlled input file` |
| `_stage_generated_assets` | function | 35 | `def _stage_generated_assets(output_dir: Path, report_dir: Path, repo_root: Path) -> dict[str, list[str]]` | Stage generated aggregate assets into the atomic report directory. | `src cmat_analysis reporting methodology_build py stage_generated_assets stage generated aggregate assets atomic report directory` |
| `_compile_report` | function | 64 | `def _compile_report(report_dir: Path) -> Path` | Compile the methodology report after scientific outputs have been staged. | `src cmat_analysis reporting methodology_build py compile_report compile methodology report after scientific outputs have been` |
| `_check_structure` | function | 102 | `def _check_structure(code_root: Path, report_dir: Path) -> list[str]` | Validate the root-code/report boundary without loading controlled data. | `src cmat_analysis reporting methodology_build py check_structure validate root-code report boundary without loading controlled data` |
| `_parse_args` | function | 121 | `def _parse_args(default_output_dir: Path, argv: list[str] \| None) -> argparse.Namespace` | Parse the stable methodology-report runner interface. | `src cmat_analysis reporting methodology_build py parse_args parse stable methodology-report runner interface` |
| `methodology_report_cli` | function | 148 | `def methodology_report_cli(repo_root: Path, report_dir: Path, argv: list[str] \| None=None) -> int` | Run the methodology-report recipe while keeping scientific functions in root/code. | `src cmat_analysis reporting methodology_build py methodology_report_cli run methodology-report recipe while keeping scientific functions in` |

### `src/cmat_analysis/reporting/methodology_report.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_esc` | function | 9 | `def _esc(x: object) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting methodology_report py esc` |
| `_f` | function | 18 | `def _f(x: object, digits: int=3, pct: bool=False) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting methodology_report py f` |
| `_tab` | function | 33 | `def _tab(headers: list[str], rows: list[list[str]], align: str) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting methodology_report py tab` |
| `_read` | function | 40 | `def _read(root: Path, name: str) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting methodology_report py read` |
| `write_methodology_table_snippets` | function | 47 | `def write_methodology_table_snippets(generated_tables_dir: Path, report_tables_dir: Path) -> list[Path]` | Render report table snippets from already-computed aggregate CSV files. | `src cmat_analysis reporting methodology_report py write_methodology_table_snippets render report table snippets already-computed aggregate csv files` |
| `write_methodology_table_snippets.<locals>.w` | function | 53 | `def w(name: str, headers: list[str], rows: list[list[str]], align: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting methodology_report py write_methodology_table_snippets locals w` |
| `write_methodology_table_snippets.<locals>.summary_table` | function | 82 | `def summary_table(csv: str, tex: str, group_col: str, first_header: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting methodology_report py write_methodology_table_snippets locals summary_table` |

### `src/cmat_analysis/reporting/metrics.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_safe_prop` | function | 44 | `def _safe_prop(numerator: float \| int, denominator: float \| int) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py safe_prop` |
| `_safe_number` | function | 50 | `def _safe_number(value: object) -> object` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py safe_number` |
| `_series_to_numeric` | function | 64 | `def _series_to_numeric(series: pd.Series) -> pd.Series` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py series_to_numeric` |
| `_describe_numeric` | function | 68 | `def _describe_numeric(series: pd.Series) -> dict[str, float \| int \| None]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py describe_numeric` |
| `_summary_metric_row` | function | 102 | `def _summary_metric_row(metric: str, value: object, unit: str, definition: str) -> dict[str, object]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py summary_metric_row` |
| `_top_share` | function | 111 | `def _top_share(values: pd.Series, share: float) -> tuple[int, float]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py top_share` |
| `gini_coefficient` | function | 121 | `def gini_coefficient(values: Iterable[float \| int]) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py gini_coefficient` |
| `compute_source_data_overview` | function | 135 | `def compute_source_data_overview(bundle: AnalyticalBundle) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_source_data_overview` |
| `compute_student_visit_distribution` | function | 235 | `def compute_student_visit_distribution(student_visits: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_student_visit_distribution` |
| `compute_year_summary` | function | 358 | `def compute_year_summary(bundle: AnalyticalBundle) -> tuple[pd.DataFrame, pd.DataFrame]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_year_summary` |
| `compute_classroom_unit_summary` | function | 404 | `def compute_classroom_unit_summary(bundle: AnalyticalBundle) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_classroom_unit_summary` |
| `compute_classroom_size_distribution` | function | 433 | `def compute_classroom_size_distribution(classroom_summary: pd.DataFrame) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_classroom_size_distribution` |
| `compute_professor_summary` | function | 445 | `def compute_professor_summary(bundle: AnalyticalBundle, classroom_summary: pd.DataFrame) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_professor_summary` |
| `compute_subject_summary` | function | 473 | `def compute_subject_summary(bundle: AnalyticalBundle, classroom_summary: pd.DataFrame) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_subject_summary` |
| `compute_student_summary` | function | 502 | `def compute_student_summary(bundle: AnalyticalBundle) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_student_summary` |
| `compute_grade_variable_summary` | function | 521 | `def compute_grade_variable_summary(bundle: AnalyticalBundle) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_grade_variable_summary` |
| `compute_non_numeric_grade_tokens` | function | 563 | `def compute_non_numeric_grade_tokens(bundle: AnalyticalBundle) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_non_numeric_grade_tokens` |
| `compute_threshold_summaries` | function | 579 | `def compute_threshold_summaries(bundle: AnalyticalBundle) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_threshold_summaries` |
| `compute_top_students_by_visits` | function | 625 | `def compute_top_students_by_visits(student_summary: pd.DataFrame, top_n: int=25) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_top_students_by_visits` |
| `compute_concentration_outputs` | function | 636 | `def compute_concentration_outputs(bundle: AnalyticalBundle, student_summary: pd.DataFrame, year_summary: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_concentration_outputs` |
| `compute_summary_json` | function | 755 | `def compute_summary_json(bundle: AnalyticalBundle, visit_summary: pd.DataFrame, year_summary: pd.DataFrame, grade_summary: pd.DataFrame, concentration_summary: pd.DataFrame) -> dict[str, object]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting metrics py compute_summary_json` |

### `src/cmat_analysis/reporting/plots.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `save_figure_pdf` | function | 19 | `def save_figure_pdf(fig: plt.Figure, output_dir: Path, stem: str) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py save_figure_pdf` |
| `plot_visits_histogram` | function | 27 | `def plot_visits_histogram(student_visits: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py plot_visits_histogram` |
| `plot_visits_histogram_low_counts` | function | 39 | `def plot_visits_histogram_low_counts(student_visits: pd.DataFrame, output_dir: Path, max_visits_shown: int=10) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py plot_visits_histogram_low_counts` |
| `plot_visits_ecdf` | function | 56 | `def plot_visits_ecdf(student_visits: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py plot_visits_ecdf` |
| `plot_visits_tail_curve` | function | 68 | `def plot_visits_tail_curve(visit_tail: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py plot_visits_tail_curve` |
| `plot_visits_continuation_curve` | function | 83 | `def plot_visits_continuation_curve(visit_tail: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py plot_visits_continuation_curve` |
| `plot_visits_by_year` | function | 98 | `def plot_visits_by_year(student_year_visits: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py plot_visits_by_year` |
| `plot_classroom_size_distribution` | function | 115 | `def plot_classroom_size_distribution(classroom_summary: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py plot_classroom_size_distribution` |
| `plot_visits_lorenz_curve` | function | 126 | `def plot_visits_lorenz_curve(lorenz: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py plot_visits_lorenz_curve` |
| `generate_figures` | function | 141 | `def generate_figures(student_visits: pd.DataFrame, visit_tail: pd.DataFrame, student_year_visits: pd.DataFrame, classroom_summary: pd.DataFrame, lorenz: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting plots py generate_figures` |

### `src/cmat_analysis/reporting/provenance.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_file_info` | function | 15 | `def _file_info(path: Path) -> dict[str, object]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting provenance py file_info` |
| `write_run_log` | function | 34 | `def write_run_log(*, logs_dir: Path, materias_path: Path, asesorias_path: Path, mode: str, status: str, details: dict[str, object] \| None=None) -> Path` | Write reproducibility metadata for an analysis run. | `src cmat_analysis reporting provenance py write_run_log write reproducibility metadata an analysis run` |

### `src/cmat_analysis/reporting/render.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_format_value` | function | 11 | `def _format_value(value: object, decimals: int=3) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py format_value` |
| `_format_pct` | function | 19 | `def _format_pct(value: object, decimals: int=1) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py format_pct` |
| `_format_tex_pct` | function | 25 | `def _format_tex_pct(value: object, decimals: int=1) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py format_tex_pct` |
| `_markdown_table` | function | 31 | `def _markdown_table(df: pd.DataFrame, max_rows: int \| None=None) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py markdown_table` |
| `_latex_table` | function | 47 | `def _latex_table(df: pd.DataFrame) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py latex_table` |
| `write_csv_tables` | function | 58 | `def write_csv_tables(tables: dict[str, pd.DataFrame], output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py write_csv_tables` |
| `write_json_summary` | function | 68 | `def write_json_summary(summary: dict[str, object], path: Path) -> Path` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py write_json_summary` |
| `write_tex_snippets` | function | 73 | `def write_tex_snippets(summary: dict[str, object], source_overview: pd.DataFrame, cleaning_summary: pd.DataFrame, visit_thresholds: pd.DataFrame, year_summary: pd.DataFrame, concentration_summary: pd.DataFrame, grade_summary: pd.DataFrame, non_numeric_grade_tokens: pd.DataFrame, output_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py write_tex_snippets` |
| `write_readme` | function | 292 | `def write_readme(path: Path, summary: dict[str, object], source_overview: pd.DataFrame, cleaning_summary: pd.DataFrame, visit_summary: pd.DataFrame, visit_thresholds: pd.DataFrame, year_summary: pd.DataFrame, classroom_summary: pd.DataFrame, professor_summary: pd.DataFrame, grade_summary: pd.DataFrame, concentration_summary: pd.DataFrame, table_paths: list[Path], figure_paths: list[Path], tex_paths: list[Path]) -> Path` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py write_readme` |
| `write_readme.<locals>.rel_path` | function | 308 | `def rel_path(target: Path) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting render py write_readme locals rel_path` |

### `src/cmat_analysis/reporting/report_assets.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_reset_output_dir` | function | 53 | `def _reset_output_dir(path: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting report_assets py reset_output_dir` |
| `_reset_descriptive_figures` | function | 60 | `def _reset_descriptive_figures(path: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting report_assets py reset_descriptive_figures` |
| `_log_paths` | function | 81 | `def _log_paths(label: str, paths: list[Path], project_root: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting report_assets py log_paths` |
| `generate_report_assets` | function | 87 | `def generate_report_assets(*, project_root: Path=PROJECT_ROOT, materias_path: Path=DEFAULT_MATERIAS_PATH, asesorias_path: Path=DEFAULT_ASESORIAS_PATH, output_dir: Path=REPORT_ASSETS_DIR) -> dict[str, object]` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting report_assets py generate_report_assets` |
| `main` | function | 209 | `def main() -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis reporting report_assets py main` |

### `src/cmat_analysis/statistics/_core.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `group_summary` | function | 15 | `def group_summary(df: pd.DataFrame, group_col: str, outcome_col: str) -> pd.DataFrame` | Summarize a continuous outcome within ordered analytical groups. | `src cmat_analysis statistics core py group_summary summarize a continuous outcome within ordered analytical groups` |
| `_cliffs_delta` | function | 53 | `def _cliffs_delta(x: np.ndarray, y: np.ndarray) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics core py cliffs_delta` |
| `robust_two_group_tests` | function | 59 | `def robust_two_group_tests(df: pd.DataFrame, treatment_col: str, outcome_col: str, seed: int=42) -> pd.DataFrame` | Compare treated and control groups with robust parametric and rank-based diagnostics. | `src cmat_analysis statistics core py robust_two_group_tests compare treated control groups robust parametric rank-based diagnostics` |
| `_coef_table` | function | 127 | `def _coef_table(result, model_name: str, keep_terms: tuple[str, ...] \| None=None) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics core py coef_table` |
| `primary_fixed_effect_models` | function | 146 | `def primary_fixed_effect_models(df: pd.DataFrame, outcome_col: str, treatment_col: str) -> pd.DataFrame` | Estimate the primary classroom fixed-effect treatment specifications. | `src cmat_analysis statistics core py primary_fixed_effect_models estimate primary classroom fixed-effect treatment specifications` |
| `dose_group_fixed_effect_model` | function | 180 | `def dose_group_fixed_effect_model(df: pd.DataFrame, outcome_col: str, group_col: str) -> pd.DataFrame` | Estimate classroom fixed-effect contrasts for ordered visit groups. | `src cmat_analysis statistics core py dose_group_fixed_effect_model estimate classroom fixed-effect contrasts ordered visit groups` |
| `secondary_pass_model` | function | 206 | `def secondary_pass_model(df: pd.DataFrame, treatment_col: str) -> pd.DataFrame` | Secondary pass/fail sensitivity using a linear probability model. | `src cmat_analysis statistics core py secondary_pass_model secondary pass fail sensitivity using a linear probability` |
| `visit_distribution` | function | 236 | `def visit_distribution(df: pd.DataFrame, visits_col: str, course_label: str, max_exact: int=15) -> pd.DataFrame` | Tabulate exact visit-count frequencies and upper-tail proportions. | `src cmat_analysis statistics core py visit_distribution tabulate exact visit-count frequencies upper-tail proportions` |
| `continuation_curve` | function | 276 | `def continuation_curve(df: pd.DataFrame, visits_col: str, course_label: str, max_k: int=10) -> pd.DataFrame` | Estimate the conditional probability of continuing from k to k+1 visits. | `src cmat_analysis statistics core py continuation_curve estimate conditional probability of continuing k to k+1` |
| `bunching_metrics` | function | 313 | `def bunching_metrics(df: pd.DataFrame, visits_col: str, threshold: int, course_label: str) -> pd.DataFrame` | Compute descriptive visit-count concentration diagnostics around a threshold. | `src cmat_analysis statistics core py bunching_metrics compute descriptive visit-count concentration diagnostics around a threshold` |
| `longitudinal_summary` | function | 352 | `def longitudinal_summary(longitudinal: pd.DataFrame, *, mu_group_col: str, calc_visits_col: str, coverage_col: str) -> pd.DataFrame` | Summarize later Calculus use by prior MU visit group among covered observations. | `src cmat_analysis statistics core py longitudinal_summary summarize later calculus use by prior mu visit` |
| `temporal_regularity_performance_models` | function | 388 | `def temporal_regularity_performance_models(df: pd.DataFrame, *, outcome_col: str, visits_col: str, regularity_col: str='REGULARITY_MONTHLY_4', min_visits: int=3) -> pd.DataFrame` | RQ2b: regularity-performance association conditional on visit intensity. | `src cmat_analysis statistics core py temporal_regularity_performance_models rq2b regularity-performance association conditional on visit intensity` |
| `exact_visit_count_regularity_summary` | function | 439 | `def exact_visit_count_regularity_summary(df: pd.DataFrame, *, visits_col: str, outcome_col: str, exact_visits: int=3) -> pd.DataFrame` | Descriptive regularity-performance comparison at exactly V=3. | `src cmat_analysis statistics core py exact_visit_count_regularity_summary descriptive regularity-performance comparison at exactly v` |

### `src/cmat_analysis/statistics/_group_comparisons.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_mean_ci_t` | function | 40 | `def _mean_ci_t(values: np.ndarray, alpha: float=0.05) -> tuple[float, float, float, float]` | Student-t confidence interval for a sample mean. | `src cmat_analysis statistics group_comparisons py mean_ci_t student-t confidence interval a sample mean` |
| `_welch_mean_ci` | function | 60 | `def _welch_mean_ci(x: np.ndarray, y: np.ndarray, alpha: float=0.05) -> tuple[float, float, float, float]` | Difference mean(x)-mean(y), Welch SE/df and two-sided CI. | `src cmat_analysis statistics group_comparisons py welch_mean_ci difference mean x y welch se df two-sided` |
| `one_two_pooling_analysis` | function | 74 | `def one_two_pooling_analysis(df: pd.DataFrame, *, visits_col: str, outcome_col: str='Z_GRADE_PRIMARY', equivalence_margin_z: float=0.2) -> pd.DataFrame` | Formal justification for pooling V=1 and V=2. | `src cmat_analysis statistics group_comparisons py one_two_pooling_analysis formal justification pooling v` |
| `_games_howell` | function | 162 | `def _games_howell(groups: dict[str, np.ndarray], alpha: float=0.05) -> pd.DataFrame` | Games-Howell all-pairs comparisons for unequal variances/sample sizes. | `src cmat_analysis statistics group_comparisons py games_howell games-howell all-pairs comparisons unequal variances sample sizes` |
| `welch_anova_visit_groups` | function | 204 | `def welch_anova_visit_groups(df: pd.DataFrame, *, group_col: str, outcome_col: str='Z_GRADE_PRIMARY') -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]` | Welch one-way ANOVA + Brown-Forsythe + Games-Howell for visit cohorts. | `src cmat_analysis statistics group_comparisons py welch_anova_visit_groups welch one-way anova brown-forsythe games-howell visit cohorts` |
| `_bias_corrected_cramers_v` | function | 258 | `def _bias_corrected_cramers_v(table: np.ndarray) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics group_comparisons py bias_corrected_cramers_v` |
| `career_usage_association` | function | 272 | `def career_usage_association(df: pd.DataFrame, *, career_col: str='CLAVECARRERA', group_col: str='VISIT_GROUP_PERIOD', min_career_n: int=30, permutation_reps: int=3000, seed: int=42) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]` | Association between degree programme and use pattern. | `src cmat_analysis statistics group_comparisons py career_usage_association association between degree programme use pattern` |
| `career_performance_analysis` | function | 377 | `def career_performance_analysis(df: pd.DataFrame, *, career_col: str='CLAVECARRERA', outcome_col: str='Z_GRADE_PRIMARY', visits_col: str='VISITS_CMAT_PERIOD', min_career_n: int=30) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]` | Career-specific classroom-relative performance and Welch comparisons. | `src cmat_analysis statistics group_comparisons py career_performance_analysis career-specific classroom-relative performance welch comparisons` |
| `career_visit_interaction_model` | function | 452 | `def career_visit_interaction_model(df: pd.DataFrame, *, career_col: str='CLAVECARRERA', group_col: str='VISIT_GROUP_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', min_career_n: int=100, min_cell_n: int=5) -> pd.DataFrame` | Exploratory heterogeneity of the visit-performance association by career. | `src cmat_analysis statistics group_comparisons py career_visit_interaction_model exploratory heterogeneity of visit-performance association by career` |
| `clustered_visit_group_omnibus` | function | 531 | `def clustered_visit_group_omnibus(df: pd.DataFrame, *, group_col: str='VISIT_GROUP_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', classroom_col: str='CLASSROOM_ID') -> pd.DataFrame` | Cluster-robust omnibus test for the four visit cohorts. | `src cmat_analysis statistics group_comparisons py clustered_visit_group_omnibus cluster-robust omnibus test four visit cohorts` |
| `clustered_career_omnibus` | function | 590 | `def clustered_career_omnibus(df: pd.DataFrame, *, career_col: str='CLAVECARRERA', outcome_col: str='Z_GRADE_PRIMARY', classroom_col: str='CLASSROOM_ID', min_career_n: int=30) -> pd.DataFrame` | Joint career test after classroom fixed effects with clustered covariance. | `src cmat_analysis statistics group_comparisons py clustered_career_omnibus joint career test after classroom fixed effects clustered` |
| `exact_visit_performance_index` | function | 655 | `def exact_visit_performance_index(df: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', career_col: str='CLAVECARRERA', min_visit: int=1, max_visit: int=12, min_career_n_for_standardization: int=30, min_cell_n_for_balanced: int=2) -> tuple[pd.DataFrame, pd.DataFrame]` | Performance index by exact visit count (1..12), adjusted to career context. | `src cmat_analysis statistics group_comparisons py exact_visit_performance_index performance index by exact visit count adjusted to` |
| `longitudinal_any_visit_transition` | function | 756 | `def longitudinal_any_visit_transition(longitudinal: pd.DataFrame, *, mu_visits_col: str='MU_VISITS_CMAT_PERIOD', calc_visits_col: str='VISITS_CMAT_PERIOD', calc_coverage_col: str='CALC_VISIT_COVERAGE', mu_coverage_col: str \| None='MU_VISIT_COVERAGE') -> tuple[pd.DataFrame, pd.DataFrame]` | 2x2 longitudinal transition and association statistics for any CMAT use. | `src cmat_analysis statistics group_comparisons py longitudinal_any_visit_transition x2 longitudinal transition association any cmat use` |
| `clustered_omnibus_visit_group_test` | function | 859 | `def clustered_omnibus_visit_group_test(df: pd.DataFrame, *, group_col: str='VISIT_GROUP_PERIOD', outcome_col: str='Z_GRADE_PRIMARY') -> pd.DataFrame` | Cluster-robust classroom-FE omnibus complement to marginal Welch ANOVA. | `src cmat_analysis statistics group_comparisons py clustered_omnibus_visit_group_test cluster-robust classroom-fe omnibus complement to marginal welch anova` |
| `clustered_omnibus_career_test` | function | 902 | `def clustered_omnibus_career_test(df: pd.DataFrame, *, career_col: str='CLAVECARRERA', outcome_col: str='Z_GRADE_PRIMARY', min_career_n: int=30) -> pd.DataFrame` | Classroom-FE, cluster-robust joint test of career coefficients. | `src cmat_analysis statistics group_comparisons py clustered_omnibus_career_test classroom-fe cluster-robust joint test of career coefficients` |
| `exact_visit_index_trend` | function | 947 | `def exact_visit_index_trend(df: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', career_col: str='CLAVECARRERA', min_visit: int=1, max_visit: int=12, min_career_n: int=30, min_exact_group_n_for_stable_trend: int=20) -> pd.DataFrame` | Exploratory trend for the career-relative exact-dose index. | `src cmat_analysis statistics group_comparisons py exact_visit_index_trend exploratory trend career-relative exact-dose index` |

### `src/cmat_analysis/statistics/_selection.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_weighted_mean` | function | 12 | `def _weighted_mean(x: np.ndarray, w: np.ndarray) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics selection py weighted_mean` |
| `_smd_binary` | function | 16 | `def _smd_binary(x: np.ndarray, t: np.ndarray, w: np.ndarray \| None=None) -> float` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics selection py smd_binary` |
| `propensity_att_sensitivity` | function | 29 | `def propensity_att_sensitivity(df: pd.DataFrame, *, treatment_col: str, outcome_col: str, categorical_covariates: list[str], numeric_covariates: list[str] \| None=None) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float \| int \| str]]` | Observed-covariate ATT weighting sensitivity analysis. | `src cmat_analysis statistics selection py propensity_att_sensitivity observed-covariate att weighting sensitivity analysis` |

### `src/cmat_analysis/statistics/methodology.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `exact_visit_group` | function | 34 | `def exact_visit_group(v: int \| float) -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics methodology py exact_visit_group` |
| `add_exact_visit_group` | function | 47 | `def add_exact_visit_group(df: pd.DataFrame, visits_col: str='VISITS_CMAT_PERIOD') -> pd.DataFrame` | Add the ordered 0, 1, 2, 3, and 4+ exact-visit grouping variable. | `src cmat_analysis statistics methodology py add_exact_visit_group add ordered exact-visit grouping variable` |
| `exact_visit_group_summary` | function | 69 | `def exact_visit_group_summary(df: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', population: str) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics methodology py exact_visit_group_summary` |
| `exact_visit_count_summary` | function | 97 | `def exact_visit_count_summary(df: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', population: str, max_visits: int=12) -> pd.DataFrame` | Descriptive outcome summary for each exact visit count from 0 to max_visits. | `src cmat_analysis statistics methodology py exact_visit_count_summary descriptive outcome summary each exact visit count to` |
| `exact_visit_count_trend_diagnostics` | function | 128 | `def exact_visit_count_trend_diagnostics(df: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', population: str, max_visits: int=12, stable_max_visits: int=7) -> pd.DataFrame` | Student-level monotonic/linear diagnostics over exact positive counts. | `src cmat_analysis statistics methodology py exact_visit_count_trend_diagnostics student-level monotonic linear diagnostics over exact positive counts` |
| `welch_anova_exact_groups` | function | 166 | `def welch_anova_exact_groups(df: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', population: str) -> pd.DataFrame` | Welch one-way ANOVA plus Brown--Forsythe variance diagnostic. | `src cmat_analysis statistics methodology py welch_anova_exact_groups welch one-way anova plus brown--forsythe variance diagnostic` |
| `games_howell_exact_groups` | function | 209 | `def games_howell_exact_groups(df: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', population: str, alpha: float=0.05) -> pd.DataFrame` | All pairwise Games--Howell contrasts for 0,1,2,3,4+ visit groups. | `src cmat_analysis statistics methodology py games_howell_exact_groups all pairwise games--howell contrasts visit groups` |
| `fixed_effect_pairwise_exact_groups` | function | 285 | `def fixed_effect_pairwise_exact_groups(df: pd.DataFrame, *, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', population: str, include_career: bool=True) -> tuple[pd.DataFrame, pd.DataFrame]` | All pairwise adjusted contrasts from one additive classroom-FE model. | `src cmat_analysis statistics methodology py fixed_effect_pairwise_exact_groups all pairwise adjusted contrasts one additive classroom-fe model` |
| `fixed_effect_pairwise_exact_groups.<locals>.coef_name` | function | 306 | `def coef_name(group: str) -> str \| None` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics methodology py fixed_effect_pairwise_exact_groups locals coef_name` |
| `_coverage_set` | function | 366 | `def _coverage_set(data) -> set[tuple[int, str]]` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics methodology py coverage_set` |
| `build_all_math_attempts_with_outcomes` | function | 371 | `def build_all_math_attempts_with_outcomes(data, config) -> pd.DataFrame` | Build all eligible observed math-course attempts in CMAT-covered periods. | `src cmat_analysis statistics methodology py build_all_math_attempts_with_outcomes build all eligible observed math-course attempts in cmat-covered` |
| `career_summary` | function | 386 | `def career_summary(df: pd.DataFrame, *, population: str, visits_col: str='VISITS_CMAT_PERIOD', outcome_col: str='Z_GRADE_PRIMARY', min_n: int=30) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics methodology py career_summary` |
| `career_ecological_association` | function | 413 | `def career_ecological_association(summary: pd.DataFrame) -> pd.DataFrame` | Descriptive career-level association between CMAT use rate and mean Z. | `src cmat_analysis statistics methodology py career_ecological_association descriptive career-level association between cmat use rate mean` |
| `calc_progressor_mu_cohort` | function | 439 | `def calc_progressor_mu_cohort(mu_with_outcomes: pd.DataFrame, longitudinal: pd.DataFrame) -> pd.DataFrame` | MU rows for students whose first later Calculus attempt has CMAT coverage. | `src cmat_analysis statistics methodology py calc_progressor_mu_cohort mu rows students whose first later calculus attempt` |
| `calc_progressor_followup_cohort` | function | 445 | `def calc_progressor_followup_cohort(longitudinal_with_outcomes: pd.DataFrame) -> pd.DataFrame` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics methodology py calc_progressor_followup_cohort` |

### `src/cmat_analysis/statistics/nonparametric.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_output_path` | function | 9 | `def _output_path(path_root, filename: str) -> Path` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py output_path` |
| `pruebas_no_parametricas` | function | 13 | `def pruebas_no_parametricas(group1, group2, split, estudiante_o_calificacion='Salón', PATH=None, MATERIA=None)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas` |
| `pruebas_no_parametricas.<locals>.bootstrap_diff_median` | function | 29 | `def bootstrap_diff_median(x, y, B=10000, seed=0)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas locals bootstrap_diff_median` |
| `pruebas_no_parametricas.<locals>.stat_median` | function | 43 | `def stat_median(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas locals stat_median` |
| `pruebas_no_parametricas.<locals>.cliffs_delta` | function | 52 | `def cliffs_delta(x, y, max_pairs=5000000, seed=0)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas locals cliffs_delta` |
| `pruebas_no_parametricas.<locals>.bootstrap_ci_two_sample` | function | 70 | `def bootstrap_ci_two_sample(x, y, stat_fn, B=5000, seed=0, alpha=0.05)` | Generic bootstrap CI for a two-sample statistic. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas locals bootstrap_ci_two_sample generic bootstrap ci a two-sample statistic` |
| `pruebas_no_parametricas.<locals>.stat_CL` | function | 100 | `def stat_CL(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas locals stat_cl` |
| `pruebas_no_parametricas.<locals>.stat_r_rb` | function | 112 | `def stat_r_rb(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas locals stat_r_rb` |
| `pruebas_no_parametricas.<locals>.stat_delta` | function | 119 | `def stat_delta(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas locals stat_delta` |
| `pruebas_no_parametricas.<locals>.stat_median_diff` | function | 127 | `def stat_median_diff(x, y)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics nonparametric py pruebas_no_parametricas locals stat_median_diff` |

### `src/cmat_analysis/statistics/parametric.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_output_path` | function | 9 | `def _output_path(path_root, filename: str) -> Path` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics parametric py output_path` |
| `pruebas_parametricas` | function | 13 | `def pruebas_parametricas(group1, group2, split, estudiante_o_calificacion='Salón', PATH=None, MATERIA=None)` | No docstring; inspect implementation before reuse. | `src cmat_analysis statistics parametric py pruebas_parametricas` |

### `src/cmat_analysis/study/methodology_pipeline.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_save_csv` | function | 39 | `def _save_csv(df: pd.DataFrame, path: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis study methodology_pipeline py save_csv` |
| `run_methodology_pipeline` | function | 44 | `def run_methodology_pipeline(config) -> dict[str, object]` | Run shared study outputs, then add the methodology-report extensions. | `src cmat_analysis study methodology_pipeline py run_methodology_pipeline run shared outputs then add methodology-report extensions` |

### `src/cmat_analysis/study/pipeline.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_json_default` | function | 88 | `def _json_default(obj)` | No docstring; inspect implementation before reuse. | `src cmat_analysis study pipeline py json_default` |
| `_save_csv` | function | 100 | `def _save_csv(df: pd.DataFrame, path: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis study pipeline py save_csv` |
| `_merge_extra_covariates` | function | 105 | `def _merge_extra_covariates(mu: pd.DataFrame, config) -> tuple[pd.DataFrame, list[str], str]` | No docstring; inspect implementation before reuse. | `src cmat_analysis study pipeline py merge_extra_covariates` |
| `run_study_pipeline` | function | 120 | `def run_study_pipeline(config) -> dict[str, object]` | No docstring; inspect implementation before reuse. | `src cmat_analysis study pipeline py run_study_pipeline` |

### `src/cmat_analysis/visualization/_exploratory.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_finish` | function | 12 | `def _finish(fig, path: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization exploratory py finish` |
| `plot_exact_visit_performance_index` | function | 19 | `def plot_exact_visit_performance_index(index_df: pd.DataFrame, figures: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization exploratory py plot_exact_visit_performance_index` |
| `plot_career_performance` | function | 40 | `def plot_career_performance(career_summary: pd.DataFrame, figures: Path, min_n: int=30) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization exploratory py plot_career_performance` |
| `plot_longitudinal_any_visit_transition` | function | 60 | `def plot_longitudinal_any_visit_transition(combos: pd.DataFrame, stats_df: pd.DataFrame, figures: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization exploratory py plot_longitudinal_any_visit_transition` |
| `plot_career_usage_rates` | function | 94 | `def plot_career_usage_rates(career_summary: pd.DataFrame, figures: Path, min_n: int=30) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization exploratory py plot_career_usage_rates` |

### `src/cmat_analysis/visualization/_grade_distributions.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_output_path` | function | 7 | `def _output_path(path_root, filename: str) -> Path` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization grade_distributions py output_path` |
| `salon` | function | 11 | `def salon(ultramerge, split, PATH, MATERIA=None)` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization grade_distributions py salon` |
| `estudiante_ultramerge_means` | function | 62 | `def estudiante_ultramerge_means(ultramerge_means, split, PATH)` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization grade_distributions py estudiante_ultramerge_means` |

### `src/cmat_analysis/visualization/_ppa.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_save` | function | 12 | `def _save(fig, path: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization ppa py save` |
| `plot_ppa_persistence_by_mu_group` | function | 19 | `def plot_ppa_persistence_by_mu_group(summary: pd.DataFrame, figures: Path) -> None` | Plot later Calculus-use probability by 0/1-2/3/4+ MU visits. | `src cmat_analysis visualization ppa py plot_ppa_persistence_by_mu_group plot later calculus-use probability by mu visits` |
| `plot_ppa_academic_trajectory_profiles` | function | 41 | `def plot_ppa_academic_trajectory_profiles(profiles: pd.DataFrame, figures: Path) -> None` | Plot mean Delta-Z for the eight observable MU-group x Calculus-use profiles. | `src cmat_analysis visualization ppa py plot_ppa_academic_trajectory_profiles plot mean delta-z eight observable mu-group x calculus-use` |

### `src/cmat_analysis/visualization/_study.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_save` | function | 13 | `def _save(fig, path: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization study py save` |
| `plot_visit_distribution` | function | 20 | `def plot_visit_distribution(mu: pd.DataFrame, calc: pd.DataFrame, out: Path, visits_col: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization study py plot_visit_distribution` |
| `plot_continuation` | function | 37 | `def plot_continuation(curves: pd.DataFrame, out: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization study py plot_continuation` |
| `plot_primary_group_means` | function | 50 | `def plot_primary_group_means(summary: pd.DataFrame, out: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization study py plot_primary_group_means` |
| `plot_longitudinal_persistence` | function | 63 | `def plot_longitudinal_persistence(summary: pd.DataFrame, out: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization study py plot_longitudinal_persistence` |
| `plot_daily_cmat_timeline` | function | 74 | `def plot_daily_cmat_timeline(daily: pd.DataFrame, out: Path) -> None` | Calendar-day service load with a 7-day rolling mean of unique students. | `src cmat_analysis visualization study py plot_daily_cmat_timeline calendar-day service load a day rolling mean of` |
| `plot_term_peak_profiles` | function | 92 | `def plot_term_peak_profiles(profiles: pd.DataFrame, peaks: pd.DataFrame, out: Path) -> None` | Small multiples of smoothed within-period attendance with detected peaks. | `src cmat_analysis visualization study py plot_term_peak_profiles small multiples of smoothed within-period attendance detected peaks` |
| `plot_same_day_ppa_behavior` | function | 121 | `def plot_same_day_ppa_behavior(maxdist: pd.DataFrame, out: Path) -> None` | Maximum number of same-day visits among students who reached the PPA threshold. | `src cmat_analysis visualization study py plot_same_day_ppa_behavior maximum number of same-day visits among students who` |
| `plot_peak_spacing` | function | 137 | `def plot_peak_spacing(intervals: pd.DataFrame, summary: pd.DataFrame, out: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization study py plot_peak_spacing` |
| `plot_monthly_periodicity_acf` | function | 154 | `def plot_monthly_periodicity_acf(acf: pd.DataFrame, out: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization study py plot_monthly_periodicity_acf` |
| `plot_exact3_regularity_performance` | function | 171 | `def plot_exact3_regularity_performance(summary: pd.DataFrame, out: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization study py plot_exact3_regularity_performance` |

### `src/cmat_analysis/visualization/methodology.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_save` | function | 15 | `def _save(fig, path: Path) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization methodology py save` |
| `plot_pairwise_exact_group_means` | function | 22 | `def plot_pairwise_exact_group_means(summary: pd.DataFrame, out: Path, filename: str, title: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization methodology py plot_pairwise_exact_group_means` |
| `plot_career_mean_z` | function | 41 | `def plot_career_mean_z(summary: pd.DataFrame, population: str, out: Path, filename: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization methodology py plot_career_mean_z` |
| `plot_career_use_vs_z` | function | 55 | `def plot_career_use_vs_z(summary: pd.DataFrame, population: str, out: Path, filename: str) -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization methodology py plot_career_use_vs_z` |
| `plot_periodicity_acf_by_population` | function | 71 | `def plot_periodicity_acf_by_population(acf: pd.DataFrame, out: Path, filename: str='09_monthly_periodicity_acf_by_population.png') -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization methodology py plot_periodicity_acf_by_population` |
| `plot_peak_spacing_by_population` | function | 89 | `def plot_peak_spacing_by_population(intervals: pd.DataFrame, out: Path, filename: str='08_peak_spacing_by_population.png') -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization methodology py plot_peak_spacing_by_population` |
| `plot_exact_visit_count_curve` | function | 104 | `def plot_exact_visit_count_curve(summary: pd.DataFrame, out: Path, filename: str='13_exact_visit_counts_0_to_12.png') -> None` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization methodology py plot_exact_visit_count_curve` |

### `src/cmat_analysis/visualization/style.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_candidate_font_roots` | function | 16 | `def _candidate_font_roots() -> list[Path]` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization style py candidate_font_roots` |
| `_register_local_eb_garamond` | function | 25 | `def _register_local_eb_garamond() -> str` | No docstring; inspect implementation before reuse. | `src cmat_analysis visualization style py register_local_eb_garamond` |
| `mpl_apply` | function | 42 | `def mpl_apply() -> None` | Aplica un estilo personalizado a las gráficas de Matplotlib y Seaborn. | `src cmat_analysis visualization style py mpl_apply aplica un estilo personalizado a las gr ficas` |
| `set_style` | function | 109 | `def set_style() -> None` | Apply the project Matplotlib and Seaborn plotting defaults. | `src cmat_analysis visualization style py set_style apply project matplotlib seaborn plotting defaults` |
| `plotly_apply` | function | 117 | `def plotly_apply(palette: list[str]=['#ffa600', '#ffd380'], fontsize: float=18, fontstack: str="EB Garamond, Garamond, Georgia, 'Times New Roman', serif") -> None` | Aplica un estilo personalizado a las gráficas de Plotly, poner: from style import plotly_apply plotly_apply() Parameters ---------- palette : list[str], default=['#ffa600', '#ffd380'] Plotly discrete color sequence used by the registered template. | `src cmat_analysis visualization style py plotly_apply aplica un estilo personalizado a las gr ficas` |

### `src/create_anonymized_release.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `_load_key` | function | 24 | `def _load_key(args) -> bytes` | No docstring; inspect implementation before reuse. | `src create_anonymized_release py load_key` |
| `_term_anchor` | function | 39 | `def _term_anchor(year: int, period: str) -> str` | No docstring; inspect implementation before reuse. | `src create_anonymized_release py term_anchor` |
| `_make_anonymized_data` | function | 45 | `def _make_anonymized_data(project: Path, destination: Path, key: bytes) -> dict` | No docstring; inspect implementation before reuse. | `src create_anonymized_release py make_anonymized_data` |
| `_copy_public_code` | function | 105 | `def _copy_public_code(project: Path, release_root: Path) -> None` | No docstring; inspect implementation before reuse. | `src create_anonymized_release py copy_public_code` |
| `create_release` | function | 120 | `def create_release(project: Path, output_zip: Path, key: bytes) -> Path` | No docstring; inspect implementation before reuse. | `src create_anonymized_release py create_release` |
| `main` | function | 154 | `def main() -> int` | No docstring; inspect implementation before reuse. | `src create_anonymized_release py main` |

### `src/generador_figuras_cli.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `UserFacingError` | class | 48 | `class UserFacingError(Exception)` | No docstring; inspect implementation before reuse. | `src generador_figuras_cli py userfacingerror` |
| `get_base_dir` | function | 52 | `def get_base_dir() -> Path` | No docstring; inspect implementation before reuse. | `src generador_figuras_cli py get_base_dir` |
| `validate_excel_path` | function | 58 | `def validate_excel_path(path: Path, relative_label: str) -> None` | No docstring; inspect implementation before reuse. | `src generador_figuras_cli py validate_excel_path` |
| `validate_required_columns` | function | 68 | `def validate_required_columns(df: pd.DataFrame, required: tuple[str, ...], file_name: str) -> None` | No docstring; inspect implementation before reuse. | `src generador_figuras_cli py validate_required_columns` |
| `validate_inputs` | function | 78 | `def validate_inputs(base_dir: Path) -> tuple[Path, Path, Path]` | No docstring; inspect implementation before reuse. | `src generador_figuras_cli py validate_inputs` |
| `generate_descriptive_figures` | function | 106 | `def generate_descriptive_figures(base_dir: Path, catalogo_path: Path, visitas_path: Path, figures_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src generador_figuras_cli py generate_descriptive_figures` |
| `generate_all_figures` | function | 131 | `def generate_all_figures(base_dir: Path, visitas_path: Path, catalogo_path: Path, figures_dir: Path) -> list[Path]` | No docstring; inspect implementation before reuse. | `src generador_figuras_cli py generate_all_figures` |
| `main` | function | 170 | `def main() -> int` | No docstring; inspect implementation before reuse. | `src generador_figuras_cli py main` |

### `src/prepare_release_latex.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `should_copy_latex_file` | function | 23 | `def should_copy_latex_file(path: Path) -> bool` | No docstring; inspect implementation before reuse. | `src prepare_release_latex py should_copy_latex_file` |
| `copy_tree_filtered` | function | 28 | `def copy_tree_filtered(src: Path, dst: Path) -> None` | No docstring; inspect implementation before reuse. | `src prepare_release_latex py copy_tree_filtered` |
| `prepare_release_latex` | function | 38 | `def prepare_release_latex(release_dir: Path) -> None` | No docstring; inspect implementation before reuse. | `src prepare_release_latex py` |
| `main` | function | 65 | `def main() -> int` | No docstring; inspect implementation before reuse. | `src prepare_release_latex py main` |

### `src/run_analysis.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `parse_args` | function | 21 | `def parse_args() -> argparse.Namespace` | No docstring; inspect implementation before reuse. | `src run_analysis py parse_args` |
| `main` | function | 38 | `def main() -> int` | No docstring; inspect implementation before reuse. | `src run_analysis py main` |

### `src/run_study.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `main` | function | 17 | `def main() -> int` | No docstring; inspect implementation before reuse. | `src run_study py main` |

## Test symbols

### `tests/test_methodology_report_helpers.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `test_methodology_primary_outcome_uses_scipy_kde_and_uniform_fallback` | function | 12 | `def test_methodology_primary_outcome_uses_scipy_kde_and_uniform_fallback()` | No docstring; inspect implementation before reuse. | `tests test_methodology_report_helpers py test_methodology_primary_outcome_uses_scipy_kde_and_uniform_fallback` |
| `test_methodology_exact_visit_grouping_has_all_ten_pairwise_contrasts` | function | 31 | `def test_methodology_exact_visit_grouping_has_all_ten_pairwise_contrasts()` | No docstring; inspect implementation before reuse. | `tests test_methodology_report_helpers py test_methodology_exact_visit_grouping_has_all_ten_pairwise_contrasts` |
| `test_methodology_report_atomic_runner_resolves_root_code_dependencies` | function | 42 | `def test_methodology_report_atomic_runner_resolves_root_code_dependencies()` | No docstring; inspect implementation before reuse. | `tests test_methodology_report_helpers py test_methodology_report_atomic_runner_resolves_root_code_dependencies` |

### `tests/test_public_api.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `test_root_import_is_small_and_versioned` | function | 4 | `def test_root_import_is_small_and_versioned()` | No docstring; inspect implementation before reuse. | `tests test_public_api py test_root_import_is_small_and_versioned` |
| `test_representative_public_imports` | function | 12 | `def test_representative_public_imports()` | No docstring; inspect implementation before reuse. | `tests test_public_api py test_representative_public_imports` |
| `test_compatibility_paths_delegate_to_canonical_objects` | function | 35 | `def test_compatibility_paths_delegate_to_canonical_objects()` | No docstring; inspect implementation before reuse. | `tests test_public_api py test_compatibility_paths_delegate_to_canonical_objects` |

### `tests/test_public_api_documentation.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `test_public_api_is_explicit_and_stable` | function | 98 | `def test_public_api_is_explicit_and_stable() -> None` | Ensure canonical namespaces expose exactly the reviewed API. | `tests test_public_api_documentation py test_public_api_is_explicit_and_stable ensure canonical namespaces expose exactly reviewed api` |
| `test_public_api_has_numpy_style_docstrings` | function | 105 | `def test_public_api_has_numpy_style_docstrings() -> None` | Require public callables to carry minimally complete NumPy docstrings. | `tests test_public_api_documentation py test_public_api_has_numpy_style_docstrings require public callables to carry minimally complete numpy docstrings` |
| `test_sphinx_api_page_excludes_compatibility_and_private_modules` | function | 137 | `def test_sphinx_api_page_excludes_compatibility_and_private_modules() -> None` | Keep the main Sphinx reference restricted to namespace-level public API. | `tests test_public_api_documentation py test_sphinx_api_page_excludes_compatibility_and_private_modules keep main sphinx reference restricted to namespace-level public api` |

### `tests/test_study_helpers.py`

| Symbol | Kind | Line | Signature | Summary | Tags |
|---|---|---:|---|---|---|
| `test_normalization_and_period_order` | function | 4 | `def test_normalization_and_period_order()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_normalization_and_period_order` |
| `test_visit_groups` | function | 14 | `def test_visit_groups()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_visit_groups` |
| `test_hmac_pseudonym_is_stable_across_excel_numeric_types` | function | 22 | `def test_hmac_pseudonym_is_stable_across_excel_numeric_types()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_hmac_pseudonym_is_stable_across_excel_numeric_types` |
| `test_same_day_ppa_behavior_identifies_first_three_same_day` | function | 29 | `def test_same_day_ppa_behavior_identifies_first_three_same_day()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_same_day_ppa_behavior_identifies_first_three_same_day` |
| `test_detect_period_peaks_finds_monthly_pattern` | function | 58 | `def test_detect_period_peaks_finds_monthly_pattern()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_detect_period_peaks_finds_monthly_pattern` |
| `test_temporal_regularity_distinguishes_concentrated_and_distributed_use` | function | 92 | `def test_temporal_regularity_distinguishes_concentrated_and_distributed_use()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_temporal_regularity_distinguishes_concentrated_and_distributed_use` |
| `test_monthly_periodicity_diagnostics_recovers_30_day_cycle` | function | 120 | `def test_monthly_periodicity_diagnostics_recovers_30_day_cycle()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_monthly_periodicity_diagnostics_recovers_30_day_cycle` |
| `test_extended_one_two_equivalence_and_transition` | function | 143 | `def test_extended_one_two_equivalence_and_transition()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_extended_one_two_equivalence_and_transition` |
| `test_extended_welch_anova_and_career_association_outputs` | function | 169 | `def test_extended_welch_anova_and_career_association_outputs()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_extended_welch_anova_and_career_association_outputs` |
| `test_exact_visit_index_uses_career_relative_standardization_and_sparse_tail_sensitivity` | function | 205 | `def test_exact_visit_index_uses_career_relative_standardization_and_sparse_tail_sensitivity()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_exact_visit_index_uses_career_relative_standardization_and_sparse_tail_sensitivity` |
| `test_ppa_revalidation_classifier_flags_post_pass_and_same_period_replica` | function | 250 | `def test_ppa_revalidation_classifier_flags_post_pass_and_same_period_replica()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_ppa_revalidation_classifier_flags_post_pass_and_same_period_replica` |
| `test_ppa_persistence_summary_orders_threshold_groups` | function | 272 | `def test_ppa_persistence_summary_orders_threshold_groups()` | No docstring; inspect implementation before reuse. | `tests test_study_helpers py test_ppa_persistence_summary_orders_threshold_groups` |
