# Methodology changelog — v5

## 2026-09-07

- Corrected official-career linkage description: career is read from academic records linked through student ID.
- Replaced primary adverse-outcome imputation description/implementation with within-classroom Gaussian KDE below 7.5; SciPy default `bw_method=None` (Scott), truncated by rejection below the pass threshold; empirical fallback for degenerate pools; uniform fallback only for empty sub-pass pools.
- Added audit fields for imputation method/pool/KDE factor.
- Added full 0/1/2/3/4+ performance analysis: Welch, Brown-Forsythe, ten Games-Howell comparisons, ten adjusted classroom-FE + official-career contrasts with classroom-clustered SE and Holm correction.
- Added exact 0-12 descriptive performance curve and trend diagnostics, with 1-7 stable-tail sensitivity.
- Added temporal peak and periodicity analyses for both all-CMAT records and first-MU students during their MU term.
- Documented peak detector parameters and independent ACF/periodogram recurrence diagnostics.
- Added career analyses for three distinct populations, including career mean Z plots and use-vs-Z ecological scatterplots.
- Added explicit list of first-MU career codes with n<30; they are excluded only from aggregated career inference, not from the dataset.
- Added N=4,211 future-Calculus progressor sensitivity for MU performance, with explicit future-conditioning warning.
- Expanded tests; 9 tests pass.

**Scientific source fingerprint:** `03dd3d4ddd31cc2263be54900e1b25749fab8a7beb2033fbe796bf240fd4c39f`.
