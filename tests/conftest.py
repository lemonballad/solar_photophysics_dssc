"""
Pytest configuration and shared fixtures.
"""

import numpy as np
import pytest
from pathlib import Path


@pytest.fixture
def sample_data_dir():
    """Path to sample data directory."""
    return Path(__file__).parent / "fixtures" / "sample_data"


@pytest.fixture
def sample_wavelength():
    """Sample wavelength axis (nm)."""
    return np.linspace(400, 800, 200)


@pytest.fixture
def sample_time():
    """Sample time axis (ps)."""
    return np.linspace(-1, 10, 100)


@pytest.fixture
def sample_signal(sample_wavelength, sample_time):
    """
    Generate synthetic TA signal with realistic features.

    Features:
    - Ground state bleach at 460 nm (negative)
    - Excited state absorption at 600 nm (positive)
    - Exponential decay with 2 ps lifetime
    """
    nwvln = len(sample_wavelength)
    ntime = len(sample_time)

    # Create empty signal
    signal = np.zeros((nwvln, ntime))

    # Gaussian profiles for spectral features
    def gaussian(x, center, width):
        return np.exp(-((x - center) ** 2) / (2 * width ** 2))

    # Ground state bleach at 460 nm
    gsb_spectrum = -50 * gaussian(sample_wavelength, 460, 20)

    # Excited state absorption at 600 nm
    esa_spectrum = 30 * gaussian(sample_wavelength, 600, 40)

    # Total spectrum
    spectrum = gsb_spectrum + esa_spectrum

    # Time evolution: step function at t=0, exponential decay
    for itime, t in enumerate(sample_time):
        if t > 0:
            decay = np.exp(-t / 2.0)  # 2 ps lifetime
            signal[:, itime] = spectrum * decay
        else:
            signal[:, itime] = 0

    return signal


@pytest.fixture
def sample_ta_data(sample_wavelength, sample_time, sample_signal):
    """Complete TAData object for testing."""
    from dssc.io import TAData
    return TAData(
        wavelength=sample_wavelength,
        time=sample_time,
        signal=sample_signal,
    )


@pytest.fixture
def sample_chirp_params():
    """Sample chirp correction parameters."""
    # Typical values for water chirp
    # t0(λ) = a2*λ² + a1*λ + a0
    return np.array([1e-5, -0.01, 3.0])
