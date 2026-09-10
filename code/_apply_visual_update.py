from pathlib import Path
import re

# ---- code/run_paper.py ----
path = Path('code/run_paper.py')
text = path.read_text(encoding='utf-8')
text = text.replace(
    'import argparse\nimport json\nimport subprocess\n',
    'import argparse\nimport json\nimport os\nimport subprocess\n',
)
text = text.replace(
    'import matplotlib.pyplot as plt\nimport matplotlib.ticker as mtick\nimport pandas as pd\n',
    'import pandas as pd\n\nfrom figures import generate_paper_figures, validate_figure_inputs\n',
)
text, n = re.subn(
    r'\n\ndef _plot_persistence\(.*?\n\ndef _compare_retained',
    '\n\ndef _compare_retained',
    text,
    flags=re.S,
)
assert n == 1, f'expected to remove one _plot_persistence block, got {n}'

old_required = '''    required_paths = [\n        REPO_ROOT / "cmat_analysis" / "pyproject.toml",\n        PAPER_DIR / "main.tex",\n        PAPER_DIR / "references.bib",\n        RETAINED_TABLES_DIR / "102_ppa_persistence_by_mu_group.csv",\n    ]'''
new_required = '''    required_paths = [\n        REPO_ROOT / "cmat_analysis" / "pyproject.toml",\n        REPO_ROOT / "code" / "figures.py",\n        PAPER_DIR / "main.tex",\n        PAPER_DIR / "references.bib",\n        RETAINED_TABLES_DIR / "98_ppa_progression_cohort_flow.csv",\n        RETAINED_TABLES_DIR / "102_ppa_persistence_by_mu_group.csv",\n        RETAINED_TABLES_DIR / "105_ppa_persistence_logistic_models.csv",\n        RETAINED_TABLES_DIR / "106_ppa_piecewise_threshold_persistence.csv",\n    ]'''
assert old_required in text
text = text.replace(old_required, new_required)

old_missing = '''    if missing:\n        print("Paper 1 check failed; missing required repository paths:", file=sys.stderr)\n        for path in missing:\n            print(f"  - {path}", file=sys.stderr)\n        return 1\n\n    print("Paper 1 recipe check: OK")'''
new_missing = '''    if missing:\n        print("Paper 1 check failed; missing required repository paths:", file=sys.stderr)\n        for path in missing:\n            print(f"  - {path}", file=sys.stderr)\n        return 1\n\n    try:\n        validate_figure_inputs(RETAINED_TABLES_DIR)\n    except (FileNotFoundError, ValueError) as exc:\n        print(f"Paper 1 figure-input check failed: {exc}", file=sys.stderr)\n        return 1\n\n    print("Paper 1 recipe check: OK")'''
assert old_missing in text
text = text.replace(old_missing, new_missing)
text = text.replace(
    '    print("Primary outcome: any CMAT use in the eligible Calculus I period")\n    print("No private data were read.")',
    '    print("Primary outcome: any CMAT use in the eligible Calculus I period")\n    print("Figure inputs: retained aggregate snapshot is complete")\n    print("No private data were read.")',
)

old_plot = '''    figure_path = FIGURES_DIR / "ppa_persistence_by_mu_group.png"\n    _plot_persistence(persistence, figure_path)'''
new_plot = '''    figure_paths = generate_paper_figures(TABLES_DIR, FIGURES_DIR)'''
assert old_plot in text
text = text.replace(old_plot, new_plot)
text = text.replace(
    '        "figures": [str(figure_path.relative_to(REPO_ROOT))],',
    '        "figures": [str(path.relative_to(REPO_ROOT)) for path in figure_paths],',
)
text = text.replace(
    '    print(f"Generated figure: {figure_path}")',
    '    print("Generated figures:")\n    for path in figure_paths:\n        print(f"  - {path}")',
)
old_compile = '''    if args.compile:\n        subprocess.run([sys.executable, str(PAPER_DIR / "build.py")], check=True)'''
new_compile = '''    if args.compile:\n        build_env = os.environ.copy()\n        build_env["PAPER1_FIGURE_SOURCE"] = "generated"\n        subprocess.run(\n            [sys.executable, str(PAPER_DIR / "build.py")],\n            check=True,\n            env=build_env,\n        )'''
assert old_compile in text
text = text.replace(old_compile, new_compile)
path.write_text(text, encoding='utf-8')

# ---- paper/main.tex ----
path = Path('paper/main.tex')
text = path.read_text(encoding='utf-8')

flow_pattern = re.compile(
    r'Table~\\ref\{tab:flow\} summarizes the cohort construction\. The resulting primary cohort contains 3,241 students\.\n\n'
    r'\\begin\{table\}\[htbp\].*?\\end\{table\}\n',
    re.S,
)
flow_replacement = r'''Figure~\ref{fig:cohort-flow} summarizes the cohort construction. The resulting primary cohort contains 3,241 students.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.82\textwidth]{../results/figures/figure_01_cohort_flow.png}
\caption{Construction of the primary longitudinal cohort. Counts are reproduced from the retained aggregate cohort-flow table; the final analytic sample contains students who passed their first real observed MU attempt, subsequently had a numeric Calculus I grade, had CMAT coverage and valid classroom-relative performance measures in both courses, and progressed to Calculus I in the next regular term.}
\label{fig:cohort-flow}
\end{figure}
'''
text, n = flow_pattern.subn(lambda m: flow_replacement, text, count=1)
assert n == 1, f'flow replacement count={n}'

old_persistence = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.78\textwidth]{../brainstorm/methodology_report/figures/refined_longitudinal_persistence_3241.png}
\caption{Probability of any CMAT use during Calculus I by prior MU visit group in the primary longitudinal cohort ($N=3{,}241$). The underlying retained snapshot reports Wilson 95\% confidence intervals.}
\label{fig:persistence}
\end{figure}'''
new_persistence = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.78\textwidth]{../results/figures/figure_02_main_persistence.png}
\caption{Probability of any CMAT use during Calculus I by prior University Mathematics (MU) visit group in the primary longitudinal cohort ($N=3{,}241$). Points show observed group proportions and error bars show Wilson 95\% confidence intervals.}
\label{fig:persistence}
\end{figure}'''
assert old_persistence in text
text = text.replace(old_persistence, new_persistence)

anchor = '''The comparison is consistent with behavioural heterogeneity around the operational threshold: students who continued beyond three MU visits were more likely to use CMAT again later than students who stopped exactly at three. It does not establish that crossing three visits caused persistence, because the number of visits is student-controlled.\n\n\\subsection{Adjusted persistence models}'''
inserted = '''The comparison is consistent with behavioural heterogeneity around the operational threshold: students who continued beyond three MU visits were more likely to use CMAT again later than students who stopped exactly at three. It does not establish that crossing three visits caused persistence, because the number of visits is student-controlled.\n\n\\subsection{Visit-count shape around the threshold}\n\nA descriptive piecewise model shows a much steeper association between visit count and later use through three visits than after three. Up to the threshold, the estimated odds ratio per additional visit is 1.994 (95\\% CI [1.807, 2.200], $p<.001$). Beyond three visits, the corresponding odds ratio is 1.063 (95\\% CI [0.982, 1.150], $p=.131$). Figure~\\ref{fig:threshold-piecewise} summarizes this contrast. The flattening is descriptive; it does not identify a discontinuity caused by the institutional threshold.\n\n\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=0.72\\textwidth]{../results/figures/figure_03_threshold_piecewise.png}\n\\caption{Estimated per-visit odds ratios from the descriptive piecewise logistic model of later CMAT use, with cluster-robust 95\\% confidence intervals. The first slope applies through three MU visits and the second applies after three visits. The dashed reference line denotes an odds ratio of 1. Visit count is student-controlled, so the figure is not a regression-discontinuity estimate.}\n\\label{fig:threshold-piecewise}\n\\end{figure}\n\n\\subsection{Adjusted persistence models}'''
assert anchor in text
text = text.replace(anchor, inserted)

text = text.replace(
    'The persistence gradient remains after adjustment for prior classroom-relative MU performance, official degree programme, and MU period (Table~\\ref{tab:logit}).',
    'The persistence gradient remains after adjustment for prior classroom-relative MU performance, official degree programme, and MU period (Figure~\\ref{fig:adjusted-or}).',
)

logit_pattern = re.compile(
    r'\\begin\{table\}\[htbp\]\n\\centering\n\\caption\{Adjusted odds ratios for later CMAT use\}.*?\\end\{table\}\n',
    re.S,
)
logit_replacement = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.74\textwidth]{../results/figures/figure_04_adjusted_persistence_or.png}
\caption{Adjusted odds ratios for any CMAT use during Calculus I by prior MU visit group. The reference group is zero MU visits. The model adjusts for prior classroom-relative MU performance, official degree programme at the MU attempt, and MU academic period; error bars show cluster-robust 95\% confidence intervals with clustering by MU classroom.}
\label{fig:adjusted-or}
\end{figure}
'''
text, n = logit_pattern.subn(lambda m: logit_replacement, text, count=1)
assert n == 1, f'logit figure replacement count={n}'

duplicate_piecewise = '''\nA descriptive piecewise model shows a much steeper association between visit count and later use through three visits than after three. Up to the threshold, the estimated odds ratio per additional visit is 1.994 (95\\% CI [1.807, 2.200], $p<.001$). Beyond three visits, the corresponding odds ratio is 1.063 (95\\% CI [0.982, 1.150], $p=.131$). This flattening is descriptive; it does not identify a discontinuity caused by the institutional threshold.\n'''
assert duplicate_piecewise in text
text = text.replace(duplicate_piecewise, '\n', 1)
path.write_text(text, encoding='utf-8')
