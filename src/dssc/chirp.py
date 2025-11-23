"""
Chirp correction for femtosecond transient absorption spectroscopy.

Chirp arises from group velocity dispersion in the broadband probe pulse,
causing different wavelengths to arrive at different times. This module
provides functions to measure and correct for this effect.

The chirp is modeled as a 2nd-order polynomial:
    t₀(λ) = a₂λ² + a₁λ + a₀

where t₀ is the effective time-zero at wavelength λ.
"""

import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

from .io import TAData
from .constants import find_index


def fit_chirp(
    ta_data: TAData,
    wavelength_bounds: tuple[float, float] | None = None,
    savgol_window: int = 101,
    savgol_order: int = 3,
) -> NDArray:
    """
    Fit chirp correction polynomial from blank (e.g., water) TA data.

    The chirp is determined by calculating the expectation value of time
    <t> weighted by signal² at each wavelength, then fitting a polynomial.

    Parameters
    ----------
    ta_data : TAData
        TA data from blank sample (e.g., water chirp).
    wavelength_bounds : tuple[float, float], optional
        (min_wvln, max_wvln) bounds for fitting region in nm.
        Default uses full range.
    savgol_window : int
        Window size for Savitzky-Golay smoothing filter.
    savgol_order : int
        Polynomial order for Savitzky-Golay filter.

    Returns
    -------
    NDArray
        Polynomial coefficients [a2, a1, a0] where t₀(λ) = a₂λ² + a₁λ + a₀.

    Examples
    --------
    >>> blank_data = load_ta_data("wavelength.dat", "delay.dat", "water.dat")
    >>> chirp_params = fit_chirp(blank_data, wavelength_bounds=(460, 700))
    >>> print(f"Chirp parameters: {chirp_params}")
    """
    wavelength = ta_data.wavelength
    time = ta_data.time
    signal = ta_data.signal

    # Clean signal - set NaN/Inf to 0
    signal_clean = signal.copy()
    signal_clean[~np.isfinite(signal_clean)] = 0

    # Create time matrix for integration
    time_mat = np.tile(time, (len(wavelength), 1))

    # Calculate expectation value <t> = ∫(t * S²)dt / ∫(S²)dt at each wavelength
    numerator = np.trapezoid(time_mat * signal_clean**2, x=time, axis=1)
    denominator = np.trapezoid(signal_clean**2, x=time, axis=1)

    # Avoid division by zero
    denominator[denominator == 0] = 1
    expectation_t = numerator / denominator

    # Smooth the expectation value
    expectation_t = savgol_filter(expectation_t, savgol_window, savgol_order)

    # Determine fitting region
    if wavelength_bounds is None:
        idx_first, idx_last = 0, len(wavelength)
    else:
        idx_first = find_index(wavelength, wavelength_bounds[0])
        idx_last = find_index(wavelength, wavelength_bounds[1])

    assert idx_last > idx_first, (
        f"Invalid wavelength bounds: {wavelength_bounds}"
    )

    # Fit polynomial to chirp
    params = np.polyfit(
        wavelength[idx_first:idx_last],
        expectation_t[idx_first:idx_last],
        2
    )

    assert np.all(np.isfinite(params)), "Chirp fit produced NaN/Inf parameters"

    return params


def calculate_chirp(wavelength: NDArray, params: NDArray) -> NDArray:
    """
    Calculate chirp (time-zero) at each wavelength.

    Parameters
    ----------
    wavelength : NDArray
        Wavelength axis in nm.
    params : NDArray
        Polynomial coefficients [a2, a1, a0].

    Returns
    -------
    NDArray
        Time-zero at each wavelength.
    """
    return params[0] * wavelength**2 + params[1] * wavelength + params[2]


def calculate_time_zero(params: NDArray) -> float:
    """
    Calculate the minimum time-zero (vertex of parabola).

    Parameters
    ----------
    params : NDArray
        Polynomial coefficients [a2, a1, a0].

    Returns
    -------
    float
        Minimum time-zero value.

    Notes
    -----
    For t₀(λ) = a₂λ² + a₁λ + a₀, the minimum is at:
        t₀_min = a₀ - a₁²/(4a₂)
    """
    a2, a1, a0 = params
    return a0 - a1**2 / (4 * a2)


def apply_chirp_correction(
    ta_data: TAData,
    params: NDArray,
    use_log_time: bool = True,
) -> TAData:
    """
    Apply chirp correction to TA data via interpolation.

    Parameters
    ----------
    ta_data : TAData
        Raw TA data to correct.
    params : NDArray
        Chirp polynomial coefficients [a2, a1, a0].
    use_log_time : bool
        If True, create logarithmically-spaced output time axis.

    Returns
    -------
    TAData
        Chirp-corrected TA data with new time axis.

    Examples
    --------
    >>> raw_data = load_ta_data("wavelength.dat", "delay.dat", "sample.dat")
    >>> chirp_params = load_chirp_params("chirpfit.dat")
    >>> corrected = apply_chirp_correction(raw_data, chirp_params)
    """
    wavelength = ta_data.wavelength
    time = ta_data.time
    signal = ta_data.signal

    nwvln = len(wavelength)
    ntime = len(time)

    # Calculate chirp at each wavelength
    t0 = calculate_chirp(wavelength, params)

    # Determine output time range
    time_shift = np.max(t0) - np.min(t0)
    t_low = np.min(time) - time_shift
    t_high = np.max(time) + time_shift

    # Create output time axis
    if use_log_time:
        dt = (t_high - t_low) / ntime
        rt = np.arange(ntime)
        new_time = (dt * ntime + 1) ** (rt / ntime) + t_low - np.min(t0) - 1
    else:
        new_time = np.linspace(t_low, t_high, ntime)

    # Interpolate each wavelength to new time axis
    new_signal = np.zeros((nwvln, ntime))

    for iwvln in range(nwvln):
        # Original delay axis for this wavelength
        delay = time - t0[iwvln]

        # Interpolate to new time axis
        interpolator = interp1d(
            delay,
            signal[iwvln, :],
            kind="cubic",
            bounds_error=False,
            fill_value=np.nan,
        )
        new_signal[iwvln, :] = interpolator(new_time)

    return TAData(
        wavelength=wavelength,
        time=new_time,
        signal=new_signal,
    )


def find_trust_bounds(data: NDArray, min_consecutive: int) -> tuple[int, int]:
    """
    Find reliable fitting region using 2nd derivative variance.

    Parameters
    ----------
    data : NDArray
        1D data array to analyze.
    min_consecutive : int
        Minimum number of consecutive "smooth" points required.

    Returns
    -------
    tuple[int, int]
        (first_index, last_index) of reliable region.

    Notes
    -----
    A point is considered "smooth" if its 2nd derivative magnitude
    is less than the overall variance of the 2nd derivative.
    """
    # Calculate 2nd derivative
    d2 = np.abs(np.diff(data, n=2))
    variance = np.var(d2)

    # Find consecutive smooth points
    smooth = d2 < variance
    count = 0
    mid_point = len(d2) // 2  # Default fallback

    for i in range(len(smooth) - 1):
        if smooth[i] and smooth[i + 1]:
            count += 1
            if count >= min_consecutive:
                mid_point = i - min_consecutive // 2
                break
        else:
            count = 0

    # Find bounds around midpoint
    # Search backward for first non-smooth point
    first_idx = 0
    for i in range(mid_point - 1, 0, -1):
        if d2[i] > variance:
            first_idx = i + 1
            break

    # Search forward for first non-smooth point
    last_idx = len(d2)
    for i in range(mid_point, len(d2)):
        if d2[i] > variance:
            last_idx = i
            break

    return first_idx, last_idx
