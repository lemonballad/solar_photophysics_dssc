"""
Spectral fitting functions for transient absorption data.

Provides Gaussian fitting with optional ML-based parameter interpolation.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import curve_fit
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor

from .io import TAData
from .constants import wavelength_to_wavenumber


@dataclass
class GaussianParams:
    """
    Parameters for a single Gaussian component.

    Attributes
    ----------
    amplitude : float
        Peak amplitude (mOD).
    center : float
        Peak center in wavenumber (cm^-1).
    width : float
        Standard deviation in wavenumber (cm^-1).
    """

    amplitude: float
    center: float  # cm^-1
    width: float  # cm^-1

    @property
    def center_nm(self) -> float:
        """Center wavelength in nm."""
        return 1e7 / self.center

    @property
    def fwhm(self) -> float:
        """Full width at half maximum in cm^-1."""
        return 2.355 * self.width


@dataclass
class FitResult:
    """
    Results from spectral fitting.

    Attributes
    ----------
    parameters : NDArray
        Fit parameters, shape (n_params, n_times).
    covariance : NDArray
        Covariance matrices, shape (n_params, n_params, n_times).
    time : NDArray
        Time axis.
    """

    parameters: NDArray
    covariance: NDArray
    time: NDArray

    @property
    def n_times(self) -> int:
        """Number of time points."""
        return len(self.time)


def gaussian(x: NDArray, amplitude: float, center: float, width: float) -> NDArray:
    """
    Single Gaussian function.

    Parameters
    ----------
    x : NDArray
        x-axis values.
    amplitude : float
        Peak amplitude.
    center : float
        Peak center.
    width : float
        Standard deviation.

    Returns
    -------
    NDArray
        Gaussian profile.
    """
    return amplitude * np.exp(-((x - center) ** 2) / (2 * width ** 2))


def sum_of_gaussians(
    x: NDArray,
    A1: float, mu1: float, sig1: float,
    A2: float, mu2: float, sig2: float,
    A3: float, mu3: float, sig3: float,
    C: float,
) -> NDArray:
    """
    Sum of three Gaussians plus constant offset.

    Parameters
    ----------
    x : NDArray
        x-axis values (wavenumber).
    A1, mu1, sig1 : float
        First Gaussian parameters.
    A2, mu2, sig2 : float
        Second Gaussian parameters.
    A3, mu3, sig3 : float
        Third Gaussian parameters.
    C : float
        Constant offset.

    Returns
    -------
    NDArray
        Sum of Gaussians.
    """
    g1 = gaussian(x, A1, mu1, sig1)
    g2 = gaussian(x, A2, mu2, sig2)
    g3 = gaussian(x, A3, mu3, sig3)
    return g1 + g2 + g3 + C


def fit_spectrum_gaussians(
    wavelength: NDArray,
    signal: NDArray,
    initial_guess: tuple | None = None,
    bounds: tuple | None = None,
) -> tuple[NDArray, NDArray]:
    """
    Fit spectrum with sum of three Gaussians.

    Parameters
    ----------
    wavelength : NDArray
        Wavelength axis (nm).
    signal : NDArray
        Signal to fit.
    initial_guess : tuple, optional
        Initial parameter guess (A1, mu1, sig1, A2, mu2, sig2, A3, mu3, sig3, C).
    bounds : tuple, optional
        Parameter bounds (lower, upper).

    Returns
    -------
    tuple[NDArray, NDArray]
        (parameters, covariance) from curve_fit.
    """
    # Convert to wavenumber
    wavenumber = wavelength_to_wavenumber(wavelength)

    # Default initial guess (typical for Ru complex)
    if initial_guess is None:
        initial_guess = (
            -300, 1e7 / 461, 600,   # GSB
            1, 1e7 / 608, 600,      # ESA 1
            1, 1e7 / 675, 1600,     # ESA 2
            0,                      # offset
        )

    # Default bounds
    if bounds is None:
        bounds = (
            (-500, 1e7 / 465, 100, -100, 1e7 / 620, 100, -100, 1e7 / 700, 100, -np.inf),
            (100, 1e7 / 455, 2000, 100, 1e7 / 580, 2000, 100, 1e7 / 650, 5000, np.inf),
        )

    # Fit
    params, covar = curve_fit(
        sum_of_gaussians,
        wavenumber,
        signal,
        p0=initial_guess,
        bounds=bounds,
        maxfev=2000,
    )

    return params, covar


def fit_ta_gaussians(
    ta_data: TAData,
    initial_guess: tuple | None = None,
    bounds: tuple | None = None,
) -> FitResult:
    """
    Fit Gaussians to TA spectra at each time point.

    Parameters
    ----------
    ta_data : TAData
        Transient absorption data.
    initial_guess : tuple, optional
        Initial parameter guess.
    bounds : tuple, optional
        Parameter bounds.

    Returns
    -------
    FitResult
        Fitted parameters and covariance at each time.

    Notes
    -----
    Skips time points where signal contains NaN/Inf.
    """
    n_params = 10  # 3 Gaussians × 3 params + offset
    n_times = ta_data.ntime

    parameters = np.zeros((n_params, n_times))
    covariance = np.zeros((n_params, n_params, n_times))

    for itime in range(n_times):
        signal = ta_data.signal[:, itime]

        # Skip if signal has NaN/Inf
        if not np.all(np.isfinite(signal)):
            continue

        try:
            params, covar = fit_spectrum_gaussians(
                ta_data.wavelength,
                signal,
                initial_guess=initial_guess,
                bounds=bounds,
            )
            parameters[:, itime] = params
            covariance[:, :, itime] = covar
        except RuntimeError:
            # Fit failed, leave as zeros
            pass

    return FitResult(
        parameters=parameters,
        covariance=covariance,
        time=ta_data.time,
    )


def train_parameter_model(
    fit_result: FitResult,
    ta_data: TAData,
    model_type: str = "knn",
    n_neighbors: int = 5,
) -> MultiOutputRegressor:
    """
    Train ML model to interpolate fit parameters.

    Parameters
    ----------
    fit_result : FitResult
        Results from Gaussian fitting.
    ta_data : TAData
        Original TA data.
    model_type : str
        Model type: "knn" or "rf" (random forest).
    n_neighbors : int
        Number of neighbors for KNN.

    Returns
    -------
    MultiOutputRegressor
        Trained model.

    Notes
    -----
    Features: signal at each wavelength + time
    Target: fit parameters
    """
    # Build feature matrix: signal + time
    X = np.zeros((ta_data.ntime, ta_data.nwvln + 1))
    for itime in range(ta_data.ntime):
        X[itime, :-1] = ta_data.signal[:, itime]
        X[itime, -1] = ta_data.time[itime]

    # Target: fit parameters
    y = fit_result.parameters.T

    # Handle NaN
    X = np.nan_to_num(X, nan=0)

    # Select model
    if model_type == "knn":
        base_model = KNeighborsRegressor(n_neighbors=n_neighbors)
    elif model_type == "rf":
        base_model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    # Train
    model = MultiOutputRegressor(base_model)
    model.fit(X, y)

    return model


def predict_parameters(
    model: MultiOutputRegressor,
    ta_data: TAData,
) -> NDArray:
    """
    Predict fit parameters using trained model.

    Parameters
    ----------
    model : MultiOutputRegressor
        Trained model from train_parameter_model.
    ta_data : TAData
        TA data to predict for.

    Returns
    -------
    NDArray
        Predicted parameters, shape (n_times, n_params).
    """
    # Build feature matrix
    X = np.zeros((ta_data.ntime, ta_data.nwvln + 1))
    for itime in range(ta_data.ntime):
        X[itime, :-1] = ta_data.signal[:, itime]
        X[itime, -1] = ta_data.time[itime]

    X = np.nan_to_num(X, nan=0)

    return model.predict(X)


def reconstruct_spectrum(
    wavelength: NDArray,
    parameters: NDArray,
) -> NDArray:
    """
    Reconstruct spectrum from Gaussian parameters.

    Parameters
    ----------
    wavelength : NDArray
        Wavelength axis (nm).
    parameters : NDArray
        Fit parameters (10 values).

    Returns
    -------
    NDArray
        Reconstructed spectrum.
    """
    wavenumber = wavelength_to_wavenumber(wavelength)
    return sum_of_gaussians(wavenumber, *parameters)
