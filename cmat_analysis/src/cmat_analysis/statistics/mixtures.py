"""Univariate mixture and skew-normal tools for distributional heterogeneity.

These helpers fit and compare one-dimensional Gaussian mixture models using
expectation-maximization through scikit-learn. Components are ordered by their
estimated means so labels remain stable across groups and runs.

Mixture components are statistical features of a distribution; they should not
be interpreted automatically as latent student types or causal subpopulations.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np
import pandas as pd
from scipy.stats import skewnorm
from sklearn.mixture import GaussianMixture


def _clean_values(values: Iterable[float]) -> np.ndarray:
    array = pd.to_numeric(pd.Series(values), errors="coerce").dropna().to_numpy(float)
    if len(array) < 3:
        raise ValueError("At least three finite observations are required.")
    return array.reshape(-1, 1)


def skew_normal_fit_summary(values: Iterable[float]) -> pd.DataFrame:
    """Fit a single univariate skew-normal distribution and summarize its fit.

    Parameters
    ----------
    values : iterable of float
        One-dimensional observations. Non-numeric and missing values are
        removed before estimation.

    Returns
    -------
    pandas.DataFrame
        One-row summary containing sample size, parameter count, fitted
        skew-normal shape, location and scale parameters, log-likelihood, AIC,
        and BIC.

    Notes
    -----
    A skew-normal is a single continuous component with one shape parameter.
    Comparing it with a one-component Gaussian and a two-component Gaussian
    mixture helps distinguish simple asymmetry from distributional structure
    that still requires a finite mixture. A preferred mixture remains a density
    result and does not by itself identify substantive latent classes.
    """
    x = _clean_values(values).ravel()
    shape, loc, scale = (float(value) for value in skewnorm.fit(x))
    if not np.isfinite([shape, loc, scale]).all() or scale <= 0:
        raise RuntimeError("Skew-normal fit returned invalid parameters.")

    log_likelihood = float(np.sum(skewnorm.logpdf(x, shape, loc=loc, scale=scale)))
    n = int(len(x))
    n_parameters = 3
    aic = float(2 * n_parameters - 2 * log_likelihood)
    bic = float(np.log(n) * n_parameters - 2 * log_likelihood)
    return pd.DataFrame([{
        "n": n,
        "n_parameters": n_parameters,
        "shape": shape,
        "loc": loc,
        "scale": scale,
        "log_likelihood": log_likelihood,
        "aic": aic,
        "bic": bic,
    }])


def _candidate_model(
    x: np.ndarray,
    *,
    n_components: int,
    random_state: int,
    n_init: int,
    reg_covar: float,
    means_init: Sequence[float] | None = None,
) -> GaussianMixture:
    kwargs: dict[str, object] = {
        "n_components": int(n_components),
        "covariance_type": "full",
        "random_state": int(random_state),
        "n_init": int(n_init),
        "reg_covar": float(reg_covar),
        "max_iter": 1000,
        "tol": 1e-6,
    }
    if means_init is not None:
        means = np.asarray(means_init, dtype=float).reshape(-1, 1)
        if len(means) != n_components:
            raise ValueError("means_init length must match n_components")
        kwargs["means_init"] = means
    return GaussianMixture(**kwargs).fit(x)


def fit_univariate_gaussian_mixture(
    values: Iterable[float],
    *,
    n_components: int,
    random_state: int = 42,
    n_init: int = 20,
    reg_covar: float = 1e-6,
    custom_mean_starts: Sequence[Sequence[float]] = (),
) -> GaussianMixture:
    """Fit a one-dimensional Gaussian mixture using multiple EM starts.

    Parameters
    ----------
    values : iterable of float
        One-dimensional observations.
    n_components : int
        Number of Gaussian components.
    random_state : int, default=42
        Reproducibility seed.
    n_init : int, default=20
        Number of default scikit-learn EM initializations.
    reg_covar : float, default=1e-6
        Non-negative covariance regularization.
    custom_mean_starts : sequence of sequences, default=()
        Additional mean initializations. Each sequence must contain exactly
        n_components means. The final model is the converged candidate with the
        largest log-likelihood.

    Returns
    -------
    sklearn.mixture.GaussianMixture
        Best fitted model among the default and supplied custom starts.

    Notes
    -----
    Scientifically motivated initial means should be additional starts rather
    than the unique starting condition.
    """
    if n_components < 1:
        raise ValueError("n_components must be at least 1")
    if n_init < 1:
        raise ValueError("n_init must be at least 1")
    if reg_covar < 0:
        raise ValueError("reg_covar must be non-negative")

    x = _clean_values(values)
    candidates = [
        _candidate_model(
            x,
            n_components=n_components,
            random_state=random_state,
            n_init=n_init,
            reg_covar=reg_covar,
        )
    ]
    for start in custom_mean_starts:
        candidates.append(
            _candidate_model(
                x,
                n_components=n_components,
                random_state=random_state,
                n_init=1,
                reg_covar=reg_covar,
                means_init=start,
            )
        )
    return max(candidates, key=lambda model: float(model.score(x) * len(x)))


def gaussian_mixture_model_selection(
    values: Iterable[float],
    *,
    component_counts: Sequence[int] = (1, 2, 3),
    random_state: int = 42,
    n_init: int = 20,
    reg_covar: float = 1e-6,
    two_component_mean_starts: Sequence[Sequence[float]] = (),
) -> tuple[pd.DataFrame, dict[int, GaussianMixture]]:
    """Fit candidate univariate GMMs and summarize model-selection diagnostics.

    Parameters
    ----------
    values : iterable of float
        One-dimensional observations.
    component_counts : sequence of int, default=(1, 2, 3)
        Candidate numbers of Gaussian components.
    random_state : int, default=42
        Reproducibility seed.
    n_init : int, default=20
        Number of default EM initializations for each candidate.
    reg_covar : float, default=1e-6
        Covariance regularization passed to scikit-learn.
    two_component_mean_starts : sequence of sequences, default=()
        Additional mean starts used only for the two-component candidate.

    Returns
    -------
    tuple
        A model-selection table and a mapping from component count to fitted
        model.

    Notes
    -----
    Lower BIC and ICL are preferred. ICL is computed as BIC plus twice the
    posterior classification entropy.
    """
    counts = [int(value) for value in component_counts]
    if not counts or min(counts) < 1 or len(set(counts)) != len(counts):
        raise ValueError("component_counts must contain unique positive integers")

    x = _clean_values(values)
    models: dict[int, GaussianMixture] = {}
    rows: list[dict[str, object]] = []
    for count in counts:
        starts = two_component_mean_starts if count == 2 else ()
        model = fit_univariate_gaussian_mixture(
            x.ravel(),
            n_components=count,
            random_state=random_state,
            n_init=n_init,
            reg_covar=reg_covar,
            custom_mean_starts=starts,
        )
        responsibilities = model.predict_proba(x)
        clipped = np.clip(responsibilities, 1e-15, 1.0)
        entropy = float(-np.sum(clipped * np.log(clipped)))
        log_likelihood = float(model.score(x) * len(x))
        bic = float(model.bic(x))
        rows.append(
            {
                "n_components": count,
                "n": int(len(x)),
                "log_likelihood": log_likelihood,
                "aic": float(model.aic(x)),
                "bic": bic,
                "icl": bic + 2.0 * entropy,
                "posterior_entropy": entropy,
                "mean_max_responsibility": float(
                    np.mean(np.max(responsibilities, axis=1))
                ),
                "converged": bool(model.converged_),
                "n_iter": int(model.n_iter_),
            }
        )
        models[count] = model
    return pd.DataFrame(rows).sort_values("n_components").reset_index(drop=True), models


def compare_univariate_shape_models(
    values: Iterable[float],
    *,
    random_state: int = 42,
    n_init: int = 20,
    reg_covar: float = 1e-6,
    two_component_mean_starts: Sequence[Sequence[float]] = (),
) -> pd.DataFrame:
    """Compare one Gaussian, one skew-normal, and a two-Gaussian mixture.

    Parameters
    ----------
    values : iterable of float
        One-dimensional observations scored under all three candidate models.
    random_state : int, default=42
        Reproducibility seed passed to Gaussian-mixture fitting.
    n_init : int, default=20
        Number of default EM initializations for Gaussian-mixture candidates.
    reg_covar : float, default=1e-6
        Covariance regularization passed to Gaussian-mixture candidates.
    two_component_mean_starts : sequence of sequences, default=()
        Additional mean starts for the two-Gaussian candidate.

    Returns
    -------
    pandas.DataFrame
        One-row comparison with log-likelihood, AIC, and BIC for the
        one-Gaussian, one-skew-normal, and two-Gaussian candidates; fitted
        skew-normal parameters; criterion advantages; and the preferred model
        under AIC and BIC.

    Notes
    -----
    All candidates are fit to exactly the same finite observations. A positive
    bic_advantage_gmm_k2_over_skew_normal value means the two-Gaussian mixture
    has lower BIC than the single skew-normal. This is a density specification
    check and does not establish substantive latent classes.
    """
    selection, _ = gaussian_mixture_model_selection(
        values,
        component_counts=(1, 2),
        random_state=random_state,
        n_init=n_init,
        reg_covar=reg_covar,
        two_component_mean_starts=two_component_mean_starts,
    )
    normal = selection.loc[selection["n_components"].eq(1)].iloc[0]
    gmm2 = selection.loc[selection["n_components"].eq(2)].iloc[0]
    skew = skew_normal_fit_summary(values).iloc[0]

    bic_candidates = {
        "gaussian_k1": float(normal["bic"]),
        "skew_normal_k1": float(skew["bic"]),
        "gaussian_mixture_k2": float(gmm2["bic"]),
    }
    aic_candidates = {
        "gaussian_k1": float(normal["aic"]),
        "skew_normal_k1": float(skew["aic"]),
        "gaussian_mixture_k2": float(gmm2["aic"]),
    }

    return pd.DataFrame([{
        "n": int(normal["n"]),
        "gaussian_k1_log_likelihood": float(normal["log_likelihood"]),
        "gaussian_k1_aic": float(normal["aic"]),
        "gaussian_k1_bic": float(normal["bic"]),
        "skew_normal_k1_shape": float(skew["shape"]),
        "skew_normal_k1_loc": float(skew["loc"]),
        "skew_normal_k1_scale": float(skew["scale"]),
        "skew_normal_k1_log_likelihood": float(skew["log_likelihood"]),
        "skew_normal_k1_aic": float(skew["aic"]),
        "skew_normal_k1_bic": float(skew["bic"]),
        "gaussian_mixture_k2_log_likelihood": float(gmm2["log_likelihood"]),
        "gaussian_mixture_k2_aic": float(gmm2["aic"]),
        "gaussian_mixture_k2_bic": float(gmm2["bic"]),
        "bic_advantage_skew_normal_over_gaussian_k1": (
            float(normal["bic"]) - float(skew["bic"])
        ),
        "bic_advantage_gmm_k2_over_skew_normal": (
            float(skew["bic"]) - float(gmm2["bic"])
        ),
        "aic_advantage_skew_normal_over_gaussian_k1": (
            float(normal["aic"]) - float(skew["aic"])
        ),
        "aic_advantage_gmm_k2_over_skew_normal": (
            float(skew["aic"]) - float(gmm2["aic"])
        ),
        "bic_preferred_model": min(bic_candidates, key=bic_candidates.get),
        "aic_preferred_model": min(aic_candidates, key=aic_candidates.get),
    }])


def gaussian_mixture_component_summary(
    model: GaussianMixture,
) -> pd.DataFrame:
    """Summarize Gaussian components ordered from lower to higher mean.

    Parameters
    ----------
    model : sklearn.mixture.GaussianMixture
        Fitted one-dimensional Gaussian mixture.

    Returns
    -------
    pandas.DataFrame
        Component label, original model index, weight, mean, standard deviation,
        and, for two-component models, Ashman's separation statistic.

    Notes
    -----
    Component labels describe relative performance only; they do not establish
    behavioural or psychological student types.
    """
    means = model.means_.reshape(-1).astype(float)
    variances = model.covariances_.reshape(-1).astype(float)
    weights = model.weights_.reshape(-1).astype(float)
    order = np.argsort(means)
    ashman_d = np.nan
    if len(order) == 2:
        first, second = order
        ashman_d = float(
            np.sqrt(2.0)
            * abs(means[second] - means[first])
            / np.sqrt(variances[first] + variances[second])
        )

    rows = []
    for rank, original in enumerate(order):
        if len(order) == 2:
            label = "lower_performance" if rank == 0 else "higher_performance"
        else:
            label = f"component_{rank + 1}"
        rows.append(
            {
                "component": label,
                "ordered_component": rank + 1,
                "model_component_index": int(original),
                "weight": float(weights[original]),
                "mean": float(means[original]),
                "sd": float(np.sqrt(variances[original])),
                "ashman_d_two_component_model": ashman_d,
            }
        )
    return pd.DataFrame(rows)


def gaussian_mixture_responsibilities(
    model: GaussianMixture,
    values: Iterable[float],
) -> pd.DataFrame:
    """Return posterior component responsibilities ordered by component mean.

    Parameters
    ----------
    model : sklearn.mixture.GaussianMixture
        Fitted one-dimensional Gaussian mixture.
    values : iterable of float
        Observations to score.

    Returns
    -------
    pandas.DataFrame
        One posterior-responsibility column per ordered component plus the
        maximum responsibility for each observation.
    """
    x = _clean_values(values)
    responsibilities = model.predict_proba(x)
    order = np.argsort(model.means_.reshape(-1))
    columns = []
    for rank in range(len(order)):
        if len(order) == 2:
            columns.append(
                "responsibility_lower_performance"
                if rank == 0
                else "responsibility_higher_performance"
            )
        else:
            columns.append(f"responsibility_component_{rank + 1}")
    ordered = responsibilities[:, order]
    out = pd.DataFrame(ordered, columns=columns)
    out["max_responsibility"] = np.max(ordered, axis=1)
    return out


def soft_component_composition(
    states: Iterable[object],
    responsibilities: pd.DataFrame,
    *,
    state_order: Sequence[str],
) -> pd.DataFrame:
    """Aggregate categorical-state composition using posterior responsibilities.

    Parameters
    ----------
    states : iterable of object
        State label for each observation used to calculate responsibilities.
    responsibilities : pandas.DataFrame
        Responsibility table with one responsibility column per component.
    state_order : sequence of str
        State labels to report.

    Returns
    -------
    pandas.DataFrame
        Soft expected counts and within-component state shares.

    Notes
    -----
    Expected counts are sums of posterior membership probabilities, avoiding a
    hard maximum-posterior classification.
    """
    state_series = pd.Series(list(states), dtype="string").reset_index(drop=True)
    resp = responsibilities.reset_index(drop=True)
    if len(state_series) != len(resp):
        raise ValueError("states and responsibilities must have equal length")
    component_columns = [
        column
        for column in resp.columns
        if column.startswith("responsibility_") and column != "max_responsibility"
    ]
    rows = []
    for column in component_columns:
        total = float(resp[column].sum())
        for state in [str(value) for value in state_order]:
            mask = state_series.eq(state).to_numpy()
            expected = float(resp.loc[mask, column].sum())
            rows.append(
                {
                    "component": column.removeprefix("responsibility_"),
                    "state": state,
                    "soft_expected_n": expected,
                    "component_expected_n": total,
                    "share_within_component": expected / total if total else np.nan,
                }
            )
    return pd.DataFrame(rows)


def parametric_bootstrap_gmm_lrt(
    values: Iterable[float],
    *,
    n_bootstrap: int = 199,
    random_state: int = 42,
    n_init: int = 20,
    reg_covar: float = 1e-6,
    two_component_mean_starts: Sequence[Sequence[float]] = (),
) -> pd.DataFrame:
    """Bootstrap the one- versus two-component GMM likelihood-ratio statistic.

    Parameters
    ----------
    values : iterable of float
        One-dimensional observations.
    n_bootstrap : int, default=199
        Number of samples generated from the fitted one-component null.
    random_state : int, default=42
        Seed controlling simulation and model starts.
    n_init : int, default=20
        Default EM initializations for each fit.
    reg_covar : float, default=1e-6
        Covariance regularization.
    two_component_mean_starts : sequence of sequences, default=()
        Additional two-component mean initializations.

    Returns
    -------
    pandas.DataFrame
        Observed likelihood-ratio statistic, empirical bootstrap p-value, number
        of bootstrap replicates, and null/alternative log-likelihoods.

    Notes
    -----
    The usual chi-square likelihood-ratio reference distribution is invalid for
    mixture-component tests because regularity conditions fail at the boundary.
    """
    if n_bootstrap < 19:
        raise ValueError("n_bootstrap must be at least 19")
    x = _clean_values(values)
    null_model = fit_univariate_gaussian_mixture(
        x.ravel(),
        n_components=1,
        random_state=random_state,
        n_init=n_init,
        reg_covar=reg_covar,
    )
    alt_model = fit_univariate_gaussian_mixture(
        x.ravel(),
        n_components=2,
        random_state=random_state,
        n_init=n_init,
        reg_covar=reg_covar,
        custom_mean_starts=two_component_mean_starts,
    )
    ll1 = float(null_model.score(x) * len(x))
    ll2 = float(alt_model.score(x) * len(x))
    observed = 2.0 * (ll2 - ll1)

    rng = np.random.default_rng(random_state)
    null_mean = float(null_model.means_[0, 0])
    null_sd = float(np.sqrt(null_model.covariances_.reshape(-1)[0]))
    simulated_statistics = []
    for index in range(n_bootstrap):
        sample = rng.normal(null_mean, null_sd, size=len(x))
        model1 = fit_univariate_gaussian_mixture(
            sample,
            n_components=1,
            random_state=random_state + index + 1,
            n_init=max(3, n_init // 2),
            reg_covar=reg_covar,
        )
        model2 = fit_univariate_gaussian_mixture(
            sample,
            n_components=2,
            random_state=random_state + index + 1,
            n_init=max(5, n_init // 2),
            reg_covar=reg_covar,
            custom_mean_starts=two_component_mean_starts,
        )
        sample_x = np.asarray(sample).reshape(-1, 1)
        simulated_statistics.append(
            2.0
            * (
                float(model2.score(sample_x) * len(sample_x))
                - float(model1.score(sample_x) * len(sample_x))
            )
        )

    exceedances = int(np.sum(np.asarray(simulated_statistics) >= observed))
    p_value = (exceedances + 1.0) / (n_bootstrap + 1.0)
    return pd.DataFrame(
        [
            {
                "null_components": 1,
                "alternative_components": 2,
                "n": int(len(x)),
                "log_likelihood_null": ll1,
                "log_likelihood_alternative": ll2,
                "likelihood_ratio": observed,
                "bootstrap_replicates": int(n_bootstrap),
                "bootstrap_exceedances": exceedances,
                "bootstrap_p_value": float(p_value),
            }
        ]
    )
