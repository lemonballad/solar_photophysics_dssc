"""
Signal processing functions for transient absorption data.

Handles sign conventions, baseline correction, and unit conversion.

Sign Convention:
    - Ground State Bleach (GSB): NEGATIVE signal
    - Excited State Absorption (ESA): POSITIVE signal
    - Stimulated Emission (SE): NEGATIVE signal
"""

import numpy as np
from numpy.typing import NDArray

from .io import TAData
from .constants import find_index


def adjust_sign_convention(ta_data: TAData) -> TAData:
    """
    Adjust signal sign to match standard convention (bleach = negative).

    Determines sign by looking at the wavelength with maximum absolute signal,
    which is typically the ground state bleach.

    Parameters
    ----------
    ta_data : TAData
        Input TA data with potentially incorrect sign.

    Returns
    -------
    TAData
        TA data with corrected sign convention.

    Notes
    -----
    Convention: Bleach (GSB) should be negative, Absorption (ESA) positive.
    The correction assumes the strongest feature is the bleach.
    """
    signal = ta_data.signal.copy()

    # Find wavelength index with maximum absolute signal
    max_abs_per_time = np.argmax(np.abs(signal), axis=0)
    bleach_idx = int(np.bincount(max_abs_per_time).argmax())

    # Determine sign at bleach wavelength
    bleach_signal = signal[bleach_idx, :]

    # Correct sign for each time point
    for itime in range(ta_data.ntime):
        if bleach_signal[itime] > 0:
            signal[:, itime] = -signal[:, itime]

    return TAData(
        wavelength=ta_data.wavelength,
        time=ta_data.time,
        signal=signal,
    )


def convert_to_mOD(ta_data: TAData) -> TAData:
    """
    Convert signal from OD to milli-OD (mOD).

    Parameters
    ----------
    ta_data : TAData
        Input TA data in OD units.

    Returns
    -------
    TAData
        TA data in mOD units (×1000).
    """
    return TAData(
        wavelength=ta_data.wavelength,
        time=ta_data.time,
        signal=ta_data.signal * 1000,
    )


def subtract_baseline(
    ta_data: TAData,
    time_threshold: float = -0.5,
) -> TAData:
    """
    Subtract baseline using median of negative delay times.

    Parameters
    ----------
    ta_data : TAData
        Input TA data.
    time_threshold : float
        Times below this value (in ps) are used for baseline.
        Default is -0.5 ps.

    Returns
    -------
    TAData
        Baseline-corrected TA data.

    Notes
    -----
    Uses median rather than mean to be robust against outliers.
    """
    signal = ta_data.signal.copy()
    time = ta_data.time

    # Find indices for baseline region (negative delays)
    baseline_mask = time < time_threshold

    assert np.any(baseline_mask), (
        f"No time points below threshold {time_threshold} ps. "
        f"Time range: [{time.min():.2f}, {time.max():.2f}]"
    )

    # Calculate baseline at each wavelength
    baseline = np.median(signal[:, baseline_mask], axis=1, keepdims=True)

    # Subtract baseline
    signal_corrected = signal - baseline

    return TAData(
        wavelength=ta_data.wavelength,
        time=ta_data.time,
        signal=signal_corrected,
    )


def block_pump_scatter(
    ta_data: TAData,
    center_wavelength: float,
    fwhm_wavenumber: float,
) -> TAData:
    """
    Mask out pump scatter region by setting to NaN.

    Parameters
    ----------
    ta_data : TAData
        Input TA data.
    center_wavelength : float
        Pump center wavelength in nm.
    fwhm_wavenumber : float
        Full width at half maximum in wavenumber (cm^-1).

    Returns
    -------
    TAData
        TA data with pump region masked as NaN.
    """
    signal = ta_data.signal.copy()
    wavelength = ta_data.wavelength

    # Convert FWHM to wavelength bounds
    center_wn = 1e7 / center_wavelength  # cm^-1
    low_wvln = 1e7 / (center_wn + fwhm_wavenumber)
    high_wvln = 1e7 / (center_wn - fwhm_wavenumber)

    # Find indices
    low_idx = find_index(wavelength, low_wvln)
    high_idx = find_index(wavelength, high_wvln)

    # Mask pump region
    signal[low_idx:high_idx, :] = np.nan

    return TAData(
        wavelength=ta_data.wavelength,
        time=ta_data.time,
        signal=signal,
    )


def extract_time_trace(
    ta_data: TAData,
    wavelength: float,
) -> tuple[NDArray, NDArray]:
    """
    Extract kinetic trace at specific wavelength.

    Parameters
    ----------
    ta_data : TAData
        Input TA data.
    wavelength : float
        Wavelength in nm.

    Returns
    -------
    tuple[NDArray, NDArray]
        (time_axis, signal) arrays.
    """
    idx = find_index(ta_data.wavelength, wavelength)
    return ta_data.time, ta_data.signal[idx, :]


def extract_spectrum(
    ta_data: TAData,
    time: float,
) -> tuple[NDArray, NDArray]:
    """
    Extract spectrum at specific delay time.

    Parameters
    ----------
    ta_data : TAData
        Input TA data.
    time : float
        Delay time in ps.

    Returns
    -------
    tuple[NDArray, NDArray]
        (wavelength_axis, signal) arrays.
    """
    idx = find_index(ta_data.time, time)
    return ta_data.wavelength, ta_data.signal[:, idx]


def smooth_signal(
    ta_data: TAData,
    window_wvln: int = 5,
    window_time: int = 3,
) -> TAData:
    """
    Apply moving average smoothing to signal.

    Parameters
    ----------
    ta_data : TAData
        Input TA data.
    window_wvln : int
        Window size for wavelength axis smoothing.
    window_time : int
        Window size for time axis smoothing.

    Returns
    -------
    TAData
        Smoothed TA data.
    """
    from scipy.ndimage import uniform_filter

    signal_smooth = uniform_filter(
        ta_data.signal,
        size=(window_wvln, window_time),
        mode='nearest'
    )

    return TAData(
        wavelength=ta_data.wavelength,
        time=ta_data.time,
        signal=signal_smooth,
    )
