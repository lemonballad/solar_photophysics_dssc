"""
Tests for spectral fitting functions.
"""

import numpy as np
import pytest

from dssc.fitting import (
    gaussian,
    sum_of_gaussians,
    fit_spectrum_gaussians,
    fit_ta_gaussians,
    FitResult,
    GaussianParams,
    reconstruct_spectrum,
)
from dssc.io import TAData


class TestGaussian:
    """Tests for Gaussian function."""

    def test_peak_at_center(self):
        """Test that Gaussian peaks at center."""
        x = np.linspace(0, 100, 1000)
        y = gaussian(x, amplitude=10, center=50, width=5)

        peak_idx = np.argmax(y)
        assert x[peak_idx] == pytest.approx(50, abs=0.1)
        assert y[peak_idx] == pytest.approx(10, abs=0.01)

    def test_fwhm(self):
        """Test full width at half maximum."""
        x = np.linspace(0, 100, 1000)
        center = 50
        width = 5
        y = gaussian(x, amplitude=10, center=center, width=width)

        # FWHM = 2.355 * sigma
        expected_fwhm = 2.355 * width
        half_max = 5

        # Find width at half maximum
        above_half = x[y >= half_max]
        measured_fwhm = above_half[-1] - above_half[0]

        assert measured_fwhm == pytest.approx(expected_fwhm, rel=0.05)


class TestSumOfGaussians:
    """Tests for sum of Gaussians model."""

    def test_returns_correct_shape(self):
        """Test output shape matches input."""
        x = np.linspace(15000, 25000, 200)  # wavenumber
        params = (-100, 21000, 500, 50, 17000, 500, 30, 15000, 1000, 0)

        y = sum_of_gaussians(x, *params)

        assert y.shape == x.shape

    def test_offset_works(self):
        """Test that offset parameter works."""
        x = np.linspace(15000, 25000, 200)
        params = (0, 21000, 500, 0, 17000, 500, 0, 15000, 1000, 10)

        y = sum_of_gaussians(x, *params)

        # With zero amplitudes, should just be offset
        np.testing.assert_array_almost_equal(y, 10)


class TestFitSpectrumGaussians:
    """Tests for single spectrum fitting."""

    def test_fit_synthetic_data(self):
        """Test fitting synthetic Gaussian data."""
        wavelength = np.linspace(400, 800, 200)
        wavenumber = 1e7 / wavelength

        # Create synthetic spectrum with known parameters
        true_params = (-50, 1e7/461, 500, 20, 1e7/600, 600, 10, 1e7/680, 800, 0)
        signal = sum_of_gaussians(wavenumber, *true_params)

        # Fit
        params, covar = fit_spectrum_gaussians(wavelength, signal)

        # Check that fit recovered parameters (approximately)
        assert len(params) == 10
        assert params[0] < 0  # First Gaussian should be negative (bleach)

    def test_returns_covariance(self):
        """Test that covariance matrix is returned."""
        wavelength = np.linspace(400, 800, 200)
        signal = np.random.randn(200) * 0.1  # Noisy signal

        params, covar = fit_spectrum_gaussians(wavelength, signal)

        assert covar.shape == (10, 10)


class TestFitTAGaussians:
    """Tests for fitting Gaussians to full TA data."""

    def test_fit_result_shape(self, sample_ta_data):
        """Test FitResult has correct shape."""
        result = fit_ta_gaussians(sample_ta_data)

        assert isinstance(result, FitResult)
        assert result.parameters.shape == (10, sample_ta_data.ntime)
        assert result.covariance.shape == (10, 10, sample_ta_data.ntime)
        assert len(result.time) == sample_ta_data.ntime

    def test_skips_nan_signals(self):
        """Test that NaN signals are skipped."""
        wavelength = np.linspace(400, 800, 100)
        time = np.linspace(0, 10, 50)
        signal = np.random.randn(100, 50)

        # Add NaN to some time points
        signal[:, 10] = np.nan

        data = TAData(wavelength=wavelength, time=time, signal=signal)
        result = fit_ta_gaussians(data)

        # Parameters at NaN time should be zeros
        assert np.all(result.parameters[:, 10] == 0)


class TestGaussianParams:
    """Tests for GaussianParams dataclass."""

    def test_center_nm_conversion(self):
        """Test wavenumber to wavelength conversion."""
        params = GaussianParams(amplitude=10, center=1e7/500, width=500)

        assert params.center_nm == pytest.approx(500, rel=0.01)

    def test_fwhm_calculation(self):
        """Test FWHM calculation from width."""
        params = GaussianParams(amplitude=10, center=20000, width=500)

        expected_fwhm = 2.355 * 500
        assert params.fwhm == pytest.approx(expected_fwhm)


class TestReconstructSpectrum:
    """Tests for spectrum reconstruction."""

    def test_reconstruct_matches_original(self):
        """Test that reconstruction matches sum_of_gaussians."""
        wavelength = np.linspace(400, 800, 200)
        params = np.array([-50, 1e7/461, 500, 20, 1e7/600, 600, 10, 1e7/680, 800, 0])

        reconstructed = reconstruct_spectrum(wavelength, params)

        # Should match direct calculation
        wavenumber = 1e7 / wavelength
        expected = sum_of_gaussians(wavenumber, *params)

        np.testing.assert_array_almost_equal(reconstructed, expected)
