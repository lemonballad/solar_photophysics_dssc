"""
Tests for chirp correction functions.
"""

import numpy as np
import pytest

from dssc.chirp import (
    fit_chirp,
    calculate_chirp,
    calculate_time_zero,
    apply_chirp_correction,
    find_trust_bounds,
)
from dssc.io import TAData


class TestChirpCalculation:
    """Tests for chirp polynomial calculation."""

    def test_calculate_chirp(self, sample_wavelength, sample_chirp_params):
        """Test chirp calculation from parameters."""
        chirp = calculate_chirp(sample_wavelength, sample_chirp_params)

        assert len(chirp) == len(sample_wavelength)
        assert np.all(np.isfinite(chirp))

    def test_calculate_time_zero(self, sample_chirp_params):
        """Test time-zero calculation."""
        t0 = calculate_time_zero(sample_chirp_params)

        # Should be finite
        assert np.isfinite(t0)

        # Manual calculation: a0 - a1²/(4*a2)
        a2, a1, a0 = sample_chirp_params
        expected = a0 - a1**2 / (4 * a2)
        assert t0 == pytest.approx(expected)


class TestChirpCorrection:
    """Tests for chirp correction application."""

    def test_output_shape(self, sample_ta_data, sample_chirp_params):
        """Test that output has correct shape."""
        corrected = apply_chirp_correction(sample_ta_data, sample_chirp_params)

        assert corrected.shape == sample_ta_data.shape
        assert len(corrected.wavelength) == len(sample_ta_data.wavelength)

    def test_wavelength_unchanged(self, sample_ta_data, sample_chirp_params):
        """Test that wavelength axis is unchanged."""
        corrected = apply_chirp_correction(sample_ta_data, sample_chirp_params)

        np.testing.assert_array_equal(
            corrected.wavelength, sample_ta_data.wavelength
        )


class TestFindTrustBounds:
    """Tests for trust bounds finding."""

    def test_smooth_data(self):
        """Test finding bounds in smooth data."""
        # Create smooth polynomial data
        x = np.linspace(0, 10, 100)
        data = x**2

        first, last = find_trust_bounds(data, min_consecutive=10)

        # Should find valid bounds
        assert first >= 0
        assert last <= len(data)
        assert last > first


class TestChirpFitting:
    """Tests for chirp fitting from blank data."""

    def test_fit_returns_three_params(self):
        """Test that fit returns 3 polynomial coefficients."""
        # Create synthetic chirp data
        wavelength = np.linspace(400, 800, 200)
        time = np.linspace(480, 490, 100)

        # Create signal that peaks at chirp time
        signal = np.zeros((200, 100))
        for i, wvln in enumerate(wavelength):
            # Chirp: t0 = 0.00001*λ² - 0.01*λ + 485
            t0 = 0.00001 * wvln**2 - 0.01 * wvln + 485
            idx = np.argmin(np.abs(time - t0))
            if 0 <= idx < 100:
                signal[i, max(0, idx-5):min(100, idx+5)] = 10

        data = TAData(wavelength=wavelength, time=time, signal=signal)
        params = fit_chirp(data, wavelength_bounds=(450, 750))

        assert len(params) == 3
        assert np.all(np.isfinite(params))
