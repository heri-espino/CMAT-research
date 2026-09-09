# Python function index — methodology update v5

Use this file before adding new analysis code. Search by task or symbol, then open only the referenced module. Any code change must update this file and `.ai_handoff.md`.

## Fast task map

| Task | Existing implementation |
|---|---|
| Primary adverse-grade imputation + Z outcomes | `src/visitas_analysis/study/outcomes.py` → `add_primary_outcomes`, `_scipy_default_kde_draws` |
| Exact 0/1/2/3/4+ performance analysis | `study/extended_methodology.py` → `exact_visit_group_summary`, `welch_anova_exact_groups`, `games_howell_exact_groups`, `fixed_effect_pairwise_exact_groups` |
| Exact 0-12 visit curve / dose diagnostics | `study/extended_methodology.py` → `exact_visit_count_summary`, `exact_visit_count_trend_diagnostics` |
| All-CMAT temporal peaks | `study/temporal.py` → `detect_period_peaks` called on all advisories in `study/pipeline.py` |
| First-MU temporal peaks | `study/temporal.py` → `primary_period_visit_events` then `detect_period_peaks` |
| Monthly recurrence ACF/periodogram | `study/temporal.py` → `monthly_periodicity_diagnostics` |
| Career plots and ecological associations | `study/extended_methodology.py` → `career_summary`, `career_ecological_association`; plots in `study/extended_plots.py` |
| Future-progressor N=4211 MU sensitivity | `study/extended_methodology.py` → `calc_progressor_mu_cohort` + same exact-group inference |
| Longitudinal MU→Calculus risk set | `study/cohort.py` cohort construction + `study/statistics.py` longitudinal summaries |
| Run all current analyses | `src/run_study.py` → `study/pipeline.py` |

## Complete static inventory (320 symbols)

### `config/settings.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `VisitAnalysisSettings` | class | 8 | VisitAnalysisSettings |
| `get_settings` | function | 20 | get settings |

### `config/study_config.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `CMATStudyConfig` | class | 8 | Pre-specified choices for the redesigned CMAT study. |
| `get_study_config` | function | 66 | get study config |

### `src/create_anonymized_release.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_load_key` | function | 24 |  load key |
| `_term_anchor` | function | 39 |  term anchor |
| `_make_anonymized_data` | function | 45 |  make anonymized data |
| `_copy_public_code` | function | 105 |  copy public code |
| `create_release` | function | 120 | create release |
| `main` | function | 154 | main |

### `src/generador_figuras_cli.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `UserFacingError` | class | 48 | UserFacingError |
| `get_base_dir` | function | 52 | get base dir |
| `validate_excel_path` | function | 58 | validate excel path |
| `validate_required_columns` | function | 68 | validate required columns |
| `validate_inputs` | function | 78 | validate inputs |
| `generate_descriptive_figures` | function | 106 | generate descriptive figures |
| `generate_all_figures` | function | 131 | generate all figures |
| `main` | function | 170 | main |

### `src/prepare_release_latex.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `should_copy_latex_file` | function | 23 | should copy latex file |
| `copy_tree_filtered` | function | 28 | copy tree filtered |
| `prepare_release_latex` | function | 38 | prepare release latex |
| `main` | function | 65 | main |

### `src/run_analysis.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `parse_args` | function | 21 | parse args |
| `main` | function | 38 | main |

### `src/run_study.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `main` | function | 17 | main |

### `src/visitas_analysis/analysis/cleaning.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `clean_materias_df` | function | 14 | clean materias df |
| `_silverman_bandwidth` | function | 31 |  silverman bandwidth |
| `_sample_kde_truncated` | function | 44 |  sample kde truncated |
| `_sample_empirical` | function | 63 |  sample empirical |
| `impute_nans_from_pre75_kde_df` | function | 69 | impute nans from pre75 kde df |
| `get_salones_with_imputations` | function | 149 | get salones with imputations |
| `limpieza_datos` | function | 210 | limpieza datos |

### `src/visitas_analysis/analysis/grade_analysis.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_output_path` | function | 7 |  output path |
| `salon` | function | 11 | salon |
| `estudiante_ultramerge_means` | function | 62 | estudiante ultramerge means |

### `src/visitas_analysis/analysis/nonparametric_tests.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_output_path` | function | 9 |  output path |
| `pruebas_no_parametricas` | function | 13 | pruebas no parametricas |

### `src/visitas_analysis/analysis/parametric_tests.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_output_path` | function | 9 |  output path |
| `pruebas_parametricas` | function | 13 | pruebas parametricas |

### `src/visitas_analysis/analysis/raw_report_figures.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `ProfessorColorScale` | class | 61 | ProfessorColorScale |
| `ReportContext` | class | 69 | ReportContext |
| `ClusterContext` | class | 85 | ClusterContext |
| `ParametricSummary` | class | 96 | ParametricSummary |
| `NonParametricSummary` | class | 107 | NonParametricSummary |
| `parse_args` | function | 123 | parse args |
| `main` | function | 151 | main |
| `resolve_path` | function | 206 | resolve path |
| `load_report_context` | function | 210 | load report context |
| `build_professor_color_scale` | function | 282 | build professor color scale |
| `compute_zscore` | function | 303 | compute zscore |
| `summarize_salones` | function | 315 | summarize salones |
| `pick_comparison_salon_key` | function | 339 | pick comparison salon key |
| `pick_outlier_salon_key` | function | 350 | pick outlier salon key |
| `format_salon_key` | function | 364 | format salon key |
| `numeric_array` | function | 369 | numeric array |
| `ensure_parent_dirs` | function | 373 | ensure parent dirs |
| `save_figure` | function | 378 | save figure |
| `save_cluster_grid` | function | 385 | save cluster grid |
| `add_relative_colorbar` | function | 392 | add relative colorbar |
| `_density_bandwidth` | function | 400 |  density bandwidth |
| `_gaussian_kernel_density` | function | 411 |  gaussian kernel density |
| `extract_kde_curve` | function | 416 | extract kde curve |
| `add_split_density` | function | 439 | add split density |
| `add_filled_density` | function | 470 | add filled density |
| `average_professor_pass_rates` | function | 494 | average professor pass rates |
| `global_pass_rates` | function | 513 | global pass rates |
| `add_pass_rate_legend` | function | 521 | add pass rate legend |
| `compute_parametric_summary` | function | 533 | compute parametric summary |
| `cliffs_delta` | function | 546 | cliffs delta |
| `bootstrap_diff_median` | function | 569 | bootstrap diff median |
| `bootstrap_ci_two_sample` | function | 587 | bootstrap ci two sample |
| `compute_non_parametric_summary` | function | 608 | compute non parametric summary |
| `plot_professor_mean_trends` | function | 683 | plot professor mean trends |
| `plot_all_professors_raw` | function | 718 | plot all professors raw |
| `plot_split_professor_densities` | function | 739 | plot split professor densities |
| `plot_imputation_comparison` | function | 779 | plot imputation comparison |
| `generate_professor_figures` | function | 799 | generate professor figures |
| `generate_imputation_figures` | function | 829 | generate imputation figures |
| `plot_visits_histograms` | function | 907 | plot visits histograms |
| `plot_visit_scatter` | function | 943 | plot visit scatter |
| `plot_parametric_comparison` | function | 978 | plot parametric comparison |
| `plot_non_parametric_comparison` | function | 1017 | plot non parametric comparison |
| `plot_mean_z_by_visits` | function | 1059 | plot mean z by visits |
| `generate_visit_figures` | function | 1083 | generate visit figures |
| `build_cluster_context` | function | 1143 | build cluster context |
| `plot_cluster_heatmap` | function | 1225 | plot cluster heatmap |
| `plot_cluster_selection` | function | 1252 | plot cluster selection |
| `silverman_bandwidth` | function | 1278 | silverman bandwidth |
| `kde_gaussian_grid` | function | 1289 | kde gaussian grid |
| `kde_bootstrap_ci` | function | 1294 | kde bootstrap ci |
| `plot_cluster_distributions` | function | 1310 | plot cluster distributions |
| `generate_cluster_figures` | function | 1387 | generate cluster figures |

### `src/visitas_analysis/analysis/report_compatible/context.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `BaseContext` | class | 19 | BaseContext |
| `VisitsContext` | class | 32 | VisitsContext |
| `load_base_context` | function | 37 | load base context |
| `load_visits_context` | function | 91 | load visits context |

### `src/visitas_analysis/analysis/report_compatible/figures_clusters.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `ClusterContext` | class | 23 | ClusterContext |
| `_initial_medoids` | function | 34 |  initial medoids |
| `_assign_to_medoids` | function | 45 |  assign to medoids |
| `_kmedoids_inertia` | function | 49 |  kmedoids inertia |
| `_fit_kmedoids` | function | 53 |  fit kmedoids |
| `build_cluster_context` | function | 81 | build cluster context |
| `plot_cluster_heatmap` | function | 122 | plot cluster heatmap |
| `plot_cluster_selection` | function | 150 | plot cluster selection |
| `assign_notebook_clusters` | function | 171 | assign notebook clusters |
| `_cluster_legend` | function | 177 |  cluster legend |
| `_add_shared_cluster_colorbar` | function | 187 |  add shared cluster colorbar |
| `_plot_cluster_distribution_axis` | function | 195 |  plot cluster distribution axis |
| `plot_cluster_distributions` | function | 262 | plot cluster distributions |
| `plot_cluster_distributions_with_ci` | function | 278 | plot cluster distributions with ci |

### `src/visitas_analysis/analysis/report_compatible/figures_imputation.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `plot_single_classroom_comparison` | function | 14 | plot single classroom comparison |
| `plot_global_imputation_phase1` | function | 33 | plot global imputation phase1 |
| `plot_outlier_phase1` | function | 51 | plot outlier phase1 |
| `plot_outlier_phase2` | function | 64 | plot outlier phase2 |
| `plot_global_imputation_phase2` | function | 77 | plot global imputation phase2 |

### `src/visitas_analysis/analysis/report_compatible/figures_professors.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `plot_yearly_professor_variance` | function | 14 | plot yearly professor variance |
| `plot_all_professors_png` | function | 45 | plot all professors png |
| `plot_reported_professors_split` | function | 70 | plot reported professors split |
| `plot_imputed_professors_split` | function | 108 | plot imputed professors split |

### `src/visitas_analysis/analysis/report_compatible/figures_tests.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_plot_ecdf` | function | 13 |  plot ecdf |
| `_plot_ecdf_comparison` | function | 21 |  plot ecdf comparison |
| `_bootstrap_diff_median` | function | 34 |  bootstrap diff median |
| `_bootstrap_ci_two_sample` | function | 46 |  bootstrap ci two sample |
| `_cliffs_delta` | function | 60 |  cliffs delta |
| `plot_parametric_student` | function | 77 | plot parametric student |
| `plot_ecdf_student` | function | 102 | plot ecdf student |
| `plot_parametric_salon` | function | 115 | plot parametric salon |
| `plot_ecdf_salon` | function | 131 | plot ecdf salon |
| `plot_nonparametric_student` | function | 144 | plot nonparametric student |
| `plot_nonparametric_salon` | function | 211 | plot nonparametric salon |

### `src/visitas_analysis/analysis/report_compatible/figures_visits.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `plot_visit_histograms` | function | 12 | plot visit histograms |
| `plot_salon_scatter` | function | 60 | plot salon scatter |
| `plot_student_scatter` | function | 74 | plot student scatter |
| `plot_mean_z_by_visits` | function | 101 | plot mean z by visits |

### `src/visitas_analysis/analysis/report_compatible/imputation.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `StageContext` | class | 13 | StageContext |
| `_add_mean_imputation` | function | 19 |  add mean imputation |
| `_silverman_bandwidth` | function | 30 |  silverman bandwidth |
| `_sample_kde_truncated` | function | 43 |  sample kde truncated |
| `_sample_empirical` | function | 64 |  sample empirical |
| `legacy_impute_nans_from_pre75_kde_df` | function | 71 | legacy impute nans from pre75 kde df |
| `corrected_impute_nans_from_pre75_kde_df` | function | 104 | corrected impute nans from pre75 kde df |
| `build_salones_mean_only` | function | 174 | build salones mean only |
| `build_salones_with_imputer` | function | 188 | build salones with imputer |
| `concat_salones` | function | 219 | concat salones |
| `compute_ultramerge_means` | function | 225 | compute ultramerge means |

### `src/visitas_analysis/analysis/report_compatible/kde_safe.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `numeric_values` | function | 11 | numeric values |
| `scott_bandwidth` | function | 15 | scott bandwidth |
| `silverman_bandwidth` | function | 25 | silverman bandwidth |
| `gaussian_kde_grid` | function | 37 | gaussian kde grid |
| `kde_curve` | function | 42 | kde curve |
| `_next_color` | function | 68 |  next color |
| `plot_filled_kde` | function | 72 | plot filled kde |
| `plot_split_kde` | function | 92 | plot split kde |
| `plot_hist_with_kde` | function | 126 | plot hist with kde |
| `kde_bootstrap_ci` | function | 146 | kde bootstrap ci |

### `src/visitas_analysis/analysis/report_compatible/main.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `parse_args` | function | 65 | parse args |
| `run_raw_report_figures` | function | 73 | run raw report figures |
| `main` | function | 152 | main |

### `src/visitas_analysis/analysis/report_compatible/plot_helpers.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `OutputLayout` | class | 13 | OutputLayout |
| `build_output_layout` | function | 20 | build output layout |
| `ensure_output_dirs` | function | 30 | ensure output dirs |
| `save_figure` | function | 36 | save figure |
| `save_cluster_grid` | function | 43 | save cluster grid |
| `add_half_blues_colorbar` | function | 50 | add half blues colorbar |
| `pass_rate_handles` | function | 58 | pass rate handles |

### `src/visitas_analysis/io/concentrado_reader.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `read_concentrado` | function | 9 | read concentrado |

### `src/visitas_analysis/pipeline/main_pipeline.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `run_visitas_pipeline` | function | 10 | Regenerate project outputs from the canonical raw Excel inputs. |

### `src/visitas_analysis/privacy.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `canonical_identifier` | function | 9 | Canonicalize identifiers so numeric Excel representations link reliably. |
| `hmac_pseudonym` | function | 20 | Return a deterministic keyed pseudonym. |

### `src/visitas_analysis/release_figures.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `figure_name` | function | 75 | figure name |
| `figure_path` | function | 79 | figure path |
| `figure_stem` | function | 83 | figure stem |
| `report_figure_names` | function | 87 | report figure names |

### `src/visitas_analysis/reporting/descriptive_pipeline.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `AnalyticalBundle` | class | 72 | AnalyticalBundle |
| `make_classroom_unit_id` | function | 88 | make classroom unit id |
| `clean_materias_with_tracking` | function | 93 | clean materias with tracking |
| `enrich_materias_with_visits` | function | 185 | enrich materias with visits |
| `build_analytical_bundle` | function | 233 | build analytical bundle |

### `src/visitas_analysis/reporting/metrics.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_safe_prop` | function | 44 |  safe prop |
| `_safe_number` | function | 50 |  safe number |
| `_series_to_numeric` | function | 64 |  series to numeric |
| `_describe_numeric` | function | 68 |  describe numeric |
| `_summary_metric_row` | function | 102 |  summary metric row |
| `_top_share` | function | 111 |  top share |
| `gini_coefficient` | function | 121 | gini coefficient |
| `compute_source_data_overview` | function | 135 | compute source data overview |
| `compute_student_visit_distribution` | function | 235 | compute student visit distribution |
| `compute_year_summary` | function | 358 | compute year summary |
| `compute_classroom_unit_summary` | function | 404 | compute classroom unit summary |
| `compute_classroom_size_distribution` | function | 433 | compute classroom size distribution |
| `compute_professor_summary` | function | 445 | compute professor summary |
| `compute_subject_summary` | function | 473 | compute subject summary |
| `compute_student_summary` | function | 502 | compute student summary |
| `compute_grade_variable_summary` | function | 521 | compute grade variable summary |
| `compute_non_numeric_grade_tokens` | function | 563 | compute non numeric grade tokens |
| `compute_threshold_summaries` | function | 579 | compute threshold summaries |
| `compute_top_students_by_visits` | function | 625 | compute top students by visits |
| `compute_concentration_outputs` | function | 636 | compute concentration outputs |
| `compute_summary_json` | function | 755 | compute summary json |

### `src/visitas_analysis/reporting/plots.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `save_figure_pdf` | function | 19 | save figure pdf |
| `plot_visits_histogram` | function | 27 | plot visits histogram |
| `plot_visits_histogram_low_counts` | function | 39 | plot visits histogram low counts |
| `plot_visits_ecdf` | function | 56 | plot visits ecdf |
| `plot_visits_tail_curve` | function | 68 | plot visits tail curve |
| `plot_visits_continuation_curve` | function | 83 | plot visits continuation curve |
| `plot_visits_by_year` | function | 98 | plot visits by year |
| `plot_classroom_size_distribution` | function | 115 | plot classroom size distribution |
| `plot_visits_lorenz_curve` | function | 126 | plot visits lorenz curve |
| `generate_figures` | function | 141 | generate figures |

### `src/visitas_analysis/reporting/render.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_format_value` | function | 11 |  format value |
| `_format_pct` | function | 19 |  format pct |
| `_format_tex_pct` | function | 25 |  format tex pct |
| `_markdown_table` | function | 31 |  markdown table |
| `_latex_table` | function | 47 |  latex table |
| `write_csv_tables` | function | 58 | write csv tables |
| `write_json_summary` | function | 68 | write json summary |
| `write_tex_snippets` | function | 73 | write tex snippets |
| `write_readme` | function | 292 | write readme |

### `src/visitas_analysis/reporting/report_assets.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_reset_output_dir` | function | 53 |  reset output dir |
| `_reset_descriptive_figures` | function | 60 |  reset descriptive figures |
| `_log_paths` | function | 81 |  log paths |
| `generate_report_assets` | function | 87 | generate report assets |
| `main` | function | 209 | main |

### `src/visitas_analysis/reporting/run_log.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_file_info` | function | 9 |  file info |
| `write_run_log` | function | 28 | write run log |

### `src/visitas_analysis/study/cohort.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `normalize_text` | function | 26 | normalize text |
| `normalize_session` | function | 37 | normalize session |
| `period_index` | function | 42 | period index |
| `period_label` | function | 49 | period label |
| `visit_group` | function | 53 | visit group |
| `StudyData` | class | 65 | StudyData |
| `normalize_identifier` | function | 71 | Normalize numeric or pseudonymized identifiers without requiring numbers. |
| `_read_table` | function | 83 |  read table |
| `_classify_grade` | function | 92 |  classify grade |
| `load_and_clean_inputs` | function | 104 | load and clean inputs |
| `_subject_mask` | function | 212 |  subject mask |
| `_eligible_attempts` | function | 216 |  eligible attempts |
| `first_attempts` | function | 222 | first attempts |
| `_visit_counts` | function | 228 |  visit counts |
| `attach_visits` | function | 244 | attach visits |
| `build_study_cohorts` | function | 268 | build study cohorts |

### `src/visitas_analysis/study/extended_methodology.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `exact_visit_group` | function | 20 | Map visit count to 0, 1, 2, 3, or 4+ without pooling 1 and 2. |
| `add_exact_visit_group` | function | 33 | add exact visit group |
| `exact_visit_group_summary` | function | 41 | Summarize n, mean Z, SD, SE and 95% CI for exact 0/1/2/3/4+ groups. |
| `exact_visit_count_summary` | function | 69 | Summarize classroom-relative performance for every exact count 0-12. |
| `exact_visit_count_trend_diagnostics` | function | 105 | Spearman and cluster-robust linear trend for 1-12 and stable 1-7 visit ranges. |
| `welch_anova_exact_groups` | function | 148 | Welch one-way ANOVA plus Brown-Forsythe variance diagnostic across 0/1/2/3/4+. |
| `games_howell_exact_groups` | function | 201 | All ten Games-Howell pairwise contrasts for unequal variances/sample sizes. |
| `fixed_effect_pairwise_exact_groups` | function | 260 | Single classroom-FE + official-career model; extracts all ten adjusted pairs with cluster-robust SE and Holm correction. |
| `_coverage_set` | function | 349 |  coverage set |
| `build_all_math_attempts_with_outcomes` | function | 354 | Build broad covered mathematics-attempt population across courses for career-level sensitivity. |
| `career_summary` | function | 375 | Aggregate official-career use rate and mean classroom Z for a specified population. |
| `career_ecological_association` | function | 402 | Compute career-level Pearson, Spearman and n-weighted ecological regression. |
| `calc_progressor_mu_cohort` | function | 434 | Select first-MU students who later have an eligible Calculus observation; future-conditioned sensitivity cohort. |
| `calc_progressor_followup_cohort` | function | 445 | Return linked later-Calculus attempts for the longitudinal risk set. |

### `src/visitas_analysis/study/extended_plots.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_save` | function | 9 |  save |
| `plot_pairwise_exact_group_means` | function | 16 | plot pairwise exact group means |
| `plot_career_mean_z` | function | 35 | plot career mean z |
| `plot_career_use_vs_z` | function | 49 | plot career use vs z |
| `plot_periodicity_acf_by_population` | function | 65 | plot periodicity acf by population |
| `plot_peak_spacing_by_population` | function | 83 | plot peak spacing by population |
| `plot_exact_visit_count_curve` | function | 99 | plot exact visit count curve |

### `src/visitas_analysis/study/outcomes.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_scipy_default_kde_draws` | function | 8 | Draw adverse grades from within-classroom Gaussian KDE using SciPy default Scott bandwidth, truncated below 7.5; empirical fallback if degenerate. |
| `_uniform_draws` | function | 72 | Random U(low, high) draws; high is exclusive for NumPy's Generator. |
| `_uniform_quantiles` | function | 79 | Deterministic interior points from a uniform distribution. |
| `add_primary_outcomes` | function | 91 | Construct primary KDE-based Z, uniform sensitivity Z, complete-case Z and pass/fail outcome. |

### `src/visitas_analysis/study/pipeline.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_json_default` | function | 72 |  json default |
| `_save_csv` | function | 84 |  save csv |
| `_merge_extra_covariates` | function | 89 |  merge extra covariates |
| `run_study_pipeline` | function | 104 | run study pipeline |

### `src/visitas_analysis/study/plots.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_save` | function | 13 |  save |
| `plot_visit_distribution` | function | 20 | plot visit distribution |
| `plot_continuation` | function | 37 | plot continuation |
| `plot_primary_group_means` | function | 50 | plot primary group means |
| `plot_longitudinal_persistence` | function | 63 | plot longitudinal persistence |
| `plot_daily_cmat_timeline` | function | 74 | Calendar-day service load with a 7-day rolling mean of unique students. |
| `plot_term_peak_profiles` | function | 92 | Small multiples of smoothed within-period attendance with detected peaks. |
| `plot_same_day_ppa_behavior` | function | 128 | Maximum number of same-day visits among students who reached the PPA threshold. |
| `plot_peak_spacing` | function | 144 | plot peak spacing |
| `plot_monthly_periodicity_acf` | function | 161 | plot monthly periodicity acf |
| `plot_exact3_regularity_performance` | function | 178 | plot exact3 regularity performance |

### `src/visitas_analysis/study/selection.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_weighted_mean` | function | 12 |  weighted mean |
| `_smd_binary` | function | 16 |  smd binary |
| `propensity_att_sensitivity` | function | 29 | Observed-covariate ATT weighting sensitivity analysis. |

### `src/visitas_analysis/study/statistics.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `group_summary` | function | 15 | group summary |
| `_cliffs_delta` | function | 37 |  cliffs delta |
| `robust_two_group_tests` | function | 43 | robust two group tests |
| `_coef_table` | function | 93 |  coef table |
| `primary_fixed_effect_models` | function | 112 | primary fixed effect models |
| `dose_group_fixed_effect_model` | function | 130 | dose group fixed effect model |
| `secondary_pass_model` | function | 140 | Secondary pass/fail sensitivity using a linear probability model. |
| `visit_distribution` | function | 158 | visit distribution |
| `continuation_curve` | function | 180 | continuation curve |
| `bunching_metrics` | function | 199 | bunching metrics |
| `longitudinal_summary` | function | 220 | longitudinal summary |
| `temporal_regularity_performance_models` | function | 238 | RQ2b: regularity-performance association conditional on visit intensity. |
| `exact_visit_count_regularity_summary` | function | 271 | Descriptive regularity-performance comparison at exactly V=3. |

### `src/visitas_analysis/study/temporal.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `TemporalPeakConfig` | class | 11 | TemporalPeakConfig |
| `primary_period_visit_events` | function | 20 | Restrict CMAT events to each first-MU student’s own MU academic period. |
| `daily_service_counts` | function | 38 | daily service counts |
| `same_day_ppa_behavior` | function | 55 | Describe same-day concentration among visitors and students reaching the three-visit threshold. |
| `top_daily_dates` | function | 184 | top daily dates |
| `detect_period_peaks` | function | 192 | Detect recurrent service-load peaks per term using 7-day centered rolling unique-student counts, 21-day separation and prominence threshold. |
| `peak_spacing_summary` | function | 302 | Summarize detected peak counts and inter-peak gaps, including 24-38-day monthly-like window. |
| `student_temporal_regularity` | function | 341 | Compute active-month/effective-week distribution of visits for temporal regularity analyses. |
| `monthly_periodicity_diagnostics` | function | 450 | Compute weekday-adjusted/detrended daily ACF (lags 14-45) and 21-42-day periodogram diagnostics. |

### `src/visitas_analysis/visualization/style.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `_candidate_font_roots` | function | 10 |  candidate font roots |
| `_register_local_eb_garamond` | function | 19 |  register local eb garamond |
| `mpl_apply` | function | 36 | Aplica un estilo personalizado a las gráficas de Matplotlib y Seaborn. |
| `set_style` | function | 104 | set style |
| `plotly_apply` | function | 110 | Aplica un estilo personalizado a las gráficas de Plotly, poner: |

### `tests/test_study_helpers.py`

| Symbol | Kind | Line | Purpose |
|---|---|---:|---|
| `test_normalization_and_period_order` | function | 4 | test normalization and period order |
| `test_visit_groups` | function | 14 | test visit groups |
| `test_hmac_pseudonym_is_stable_across_excel_numeric_types` | function | 22 | test hmac pseudonym is stable across excel numeric types |
| `test_same_day_ppa_behavior_identifies_first_three_same_day` | function | 29 | test same day ppa behavior identifies first three same day |
| `test_detect_period_peaks_finds_monthly_pattern` | function | 58 | test detect period peaks finds monthly pattern |
| `test_temporal_regularity_distinguishes_concentrated_and_distributed_use` | function | 92 | test temporal regularity distinguishes concentrated and distributed use |
| `test_monthly_periodicity_diagnostics_recovers_30_day_cycle` | function | 120 | test monthly periodicity diagnostics recovers 30 day cycle |
| `test_primary_outcome_uses_kde_and_uniform_fallback_as_documented` | function | 143 | test primary outcome uses kde and uniform fallback as documented |
| `test_exact_visit_grouping_and_all_pairwise_count` | function | 170 | test exact visit grouping and all pairwise count |

