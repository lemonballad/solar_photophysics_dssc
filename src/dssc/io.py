"""
Data I/O functions for loading and saving transient absorption data.
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


@dataclass
class TAData:
    """
    Container for transient absorption spectroscopy data.

    Attributes
    ----------
    wavelength : NDArray
        Wavelength axis in nanometers, shape (nwvln,).
    time : NDArray
        Time/delay axis in picoseconds, shape (ntime,).
    signal : NDArray
        TA signal matrix in mOD, shape (nwvln, ntime).

    Notes
    -----
    Matrix convention: signal[wavelength_index, time_index]
    Sign convention: Bleach = negative, Absorption = positive
    """

    wavelength: NDArray  # nm
    time: NDArray  # ps
    signal: NDArray  # mOD, shape (nwvln, ntime)

    def __post_init__(self):
        """Validate data dimensions on creation."""
        nwvln = len(self.wavelength)
        ntime = len(self.time)

        assert self.signal.shape == (nwvln, ntime), (
            f"Signal shape {self.signal.shape} != expected ({nwvln}, {ntime})"
        )
        assert np.all(np.isfinite(self.wavelength)), "Wavelength contains NaN/Inf"
        assert np.all(np.isfinite(self.time)), "Time contains NaN/Inf"

    @property
    def nwvln(self) -> int:
        """Number of wavelength points."""
        return len(self.wavelength)

    @property
    def ntime(self) -> int:
        """Number of time points."""
        return len(self.time)

    @property
    def shape(self) -> tuple[int, int]:
        """Shape of signal matrix (nwvln, ntime)."""
        return self.signal.shape


def load_dat_file(path: Path) -> NDArray:
    """
    Load data from ASCII .dat file.

    Parameters
    ----------
    path : Path
        Path to .dat file.

    Returns
    -------
    NDArray
        Loaded data array.
    """
    path = Path(path)
    assert path.exists(), f"File not found: {path}"
    return np.loadtxt(path)


def load_ta_data(
    wavelength_path: Path,
    time_path: Path,
    signal_path: Path,
) -> TAData:
    """
    Load transient absorption data from separate .dat files.

    Parameters
    ----------
    wavelength_path : Path
        Path to wavelength axis file (nm).
    time_path : Path
        Path to time/delay axis file (ps or stage position).
    signal_path : Path
        Path to TA signal matrix file.

    Returns
    -------
    TAData
        Loaded and validated TA data.

    Notes
    -----
    Automatically corrects for:
    - Transposed matrices (ensures signal[wavelength, time])
    - Descending axes (converts to ascending)

    Examples
    --------
    >>> data = load_ta_data(
    ...     "wavelength_recal.dat",
    ...     "td1.dat",
    ...     "av1.dat"
    ... )
    >>> print(f"Data shape: {data.shape}")
    """
    # Load raw data
    wavelength = load_dat_file(wavelength_path)
    time = load_dat_file(time_path)
    signal = load_dat_file(signal_path)

    # Ensure 1D axes
    wavelength = np.atleast_1d(wavelength).flatten()
    time = np.atleast_1d(time).flatten()

    nwvln = len(wavelength)
    ntime = len(time)

    # Handle 2D signal matrix - transpose if needed
    assert signal.ndim == 2, f"Signal must be 2D, got {signal.ndim}D"

    dim1, dim2 = signal.shape
    if dim1 == ntime and dim2 == nwvln:
        signal = signal.T

    assert signal.shape == (nwvln, ntime), (
        f"Signal shape {signal.shape} doesn't match axes ({nwvln}, {ntime})"
    )

    # Ensure ascending wavelength axis
    if wavelength[0] > wavelength[-1]:
        wavelength = wavelength[::-1]
        signal = signal[::-1, :]

    # Ensure ascending time axis
    if time[0] > time[-1]:
        time = time[::-1]
        signal = signal[:, ::-1]

    # Verify monotonicity
    assert np.all(np.diff(wavelength) > 0), "Wavelength axis not monotonically increasing"
    assert np.all(np.diff(time) > 0), "Time axis not monotonically increasing"

    return TAData(wavelength=wavelength, time=time, signal=signal)


def save_chirp_params(path: Path, params: NDArray) -> None:
    """
    Save chirp correction parameters to file.

    Parameters
    ----------
    path : Path
        Output file path.
    params : NDArray
        Polynomial coefficients [a2, a1, a0] for t0(λ) = a2*λ² + a1*λ + a0.
    """
    path = Path(path)
    assert len(params) == 3, f"Expected 3 chirp parameters, got {len(params)}"
    np.savetxt(path, params)


def load_chirp_params(path: Path) -> NDArray:
    """
    Load chirp correction parameters from file.

    Parameters
    ----------
    path : Path
        Path to chirp parameters file.

    Returns
    -------
    NDArray
        Polynomial coefficients [a2, a1, a0].
    """
    path = Path(path)
    assert path.exists(), f"Chirp params file not found: {path}"

    params = np.loadtxt(path)
    assert len(params) == 3, f"Expected 3 chirp parameters, got {len(params)}"

    return params
