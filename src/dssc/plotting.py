"""
Visualization functions for transient absorption data.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from numpy.typing import NDArray

from .io import TAData
from .constants import find_index


def plot_ta_contour(
    ta_data: TAData,
    ax: Axes | None = None,
    levels: int = 20,
    cmap: str = "RdBu_r",
    symmetric: bool = True,
) -> Axes:
    """
    Plot 2D contour map of TA data.

    Parameters
    ----------
    ta_data : TAData
        TA data to plot.
    ax : Axes, optional
        Matplotlib axes. If None, creates new figure.
    levels : int
        Number of contour levels.
    cmap : str
        Colormap name.
    symmetric : bool
        If True, center colormap at zero.

    Returns
    -------
    Axes
        Matplotlib axes with contour plot.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    signal = ta_data.signal

    # Handle NaN values for plotting
    signal_plot = np.nan_to_num(signal, nan=0)

    # Set symmetric color limits
    if symmetric:
        vmax = np.nanmax(np.abs(signal))
        vmin = -vmax
    else:
        vmin, vmax = np.nanmin(signal), np.nanmax(signal)

    contour = ax.contourf(
        ta_data.time,
        ta_data.wavelength,
        signal_plot,
        levels=levels,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
    )

    plt.colorbar(contour, ax=ax, label="ΔA (mOD)")
    ax.set_xlabel("Delay (ps)")
    ax.set_ylabel("Wavelength (nm)")

    return ax


def plot_time_traces(
    ta_data: TAData,
    wavelengths: list[float],
    ax: Axes | None = None,
    log_time: bool = False,
) -> Axes:
    """
    Plot kinetic traces at multiple wavelengths.

    Parameters
    ----------
    ta_data : TAData
        TA data to plot.
    wavelengths : list[float]
        Wavelengths (nm) to plot traces for.
    ax : Axes, optional
        Matplotlib axes.
    log_time : bool
        If True, use logarithmic time scale.

    Returns
    -------
    Axes
        Matplotlib axes with kinetic traces.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    for wvln in wavelengths:
        idx = find_index(ta_data.wavelength, wvln)
        actual_wvln = ta_data.wavelength[idx]
        signal = ta_data.signal[idx, :]

        ax.plot(ta_data.time, signal, label=f"{actual_wvln:.0f} nm")

    if log_time:
        ax.set_xscale("log")

    ax.axhline(y=0, color="k", linestyle="--", linewidth=0.5)
    ax.set_xlabel("Delay (ps)")
    ax.set_ylabel("ΔA (mOD)")
    ax.legend()

    return ax


def plot_spectra(
    ta_data: TAData,
    times: list[float],
    ax: Axes | None = None,
) -> Axes:
    """
    Plot spectra at multiple delay times.

    Parameters
    ----------
    ta_data : TAData
        TA data to plot.
    times : list[float]
        Delay times (ps) to plot spectra for.
    ax : Axes, optional
        Matplotlib axes.

    Returns
    -------
    Axes
        Matplotlib axes with spectra.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    for t in times:
        idx = find_index(ta_data.time, t)
        actual_time = ta_data.time[idx]
        signal = ta_data.signal[:, idx]

        ax.plot(ta_data.wavelength, signal, label=f"{actual_time:.2f} ps")

    ax.axhline(y=0, color="k", linestyle="--", linewidth=0.5)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("ΔA (mOD)")
    ax.legend()

    return ax


def plot_chirp_fit(
    wavelength: NDArray,
    expectation_t: NDArray,
    params: NDArray,
    ax: Axes | None = None,
) -> Axes:
    """
    Plot chirp data and polynomial fit.

    Parameters
    ----------
    wavelength : NDArray
        Wavelength axis (nm).
    expectation_t : NDArray
        Measured expectation value <t> at each wavelength.
    params : NDArray
        Fitted polynomial coefficients [a2, a1, a0].
    ax : Axes, optional
        Matplotlib axes.

    Returns
    -------
    Axes
        Matplotlib axes with chirp plot.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    # Calculate fitted chirp
    fit_chirp = params[0] * wavelength**2 + params[1] * wavelength + params[2]

    # Calculate time-zero offset
    t_zero = params[2] - params[1]**2 / (4 * params[0])

    ax.plot(wavelength, expectation_t - t_zero, "b-", label="Measured")
    ax.plot(wavelength, fit_chirp - t_zero, "r--", label="Polynomial fit")

    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Chirp (ps)")
    ax.legend()

    return ax


def plot_summary(
    ta_data: TAData,
    wavelengths: list[float] | None = None,
    times: list[float] | None = None,
) -> Figure:
    """
    Create summary figure with contour, time traces, and spectra.

    Parameters
    ----------
    ta_data : TAData
        TA data to plot.
    wavelengths : list[float], optional
        Wavelengths for kinetic traces. Default: [450, 550, 700] nm.
    times : list[float], optional
        Times for spectra. Default: [0.2, 1.0, 5.0] ps.

    Returns
    -------
    Figure
        Matplotlib figure with 3 subplots.
    """
    if wavelengths is None:
        wavelengths = [450, 550, 700]
    if times is None:
        times = [0.2, 1.0, 5.0]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    plot_ta_contour(ta_data, ax=axes[0])
    axes[0].set_title("TA Contour")

    plot_time_traces(ta_data, wavelengths, ax=axes[1])
    axes[1].set_title("Kinetic Traces")

    plot_spectra(ta_data, times, ax=axes[2])
    axes[2].set_title("Transient Spectra")

    plt.tight_layout()
    return fig
