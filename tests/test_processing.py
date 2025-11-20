"""
Tests for signal processing functions.
"""

import numpy as np
import pytest

from dssc.processing import (
    adjust_sign_convention,
    convert_to_mOD,
    subtract_baseline,
    extract_time_trace,
    extract_spectrum,
)
from dssc.io import TAData


class TestSignConvention:
    """Tests for sign convention adjustment."""

    def test_bleach_becomes_negative(self):
        """Test that positive bleach becomes negative."""
        # Create data with positive bleach (wrong convention)
        wavelength = np.linspace(400, 800, 100)
        time = np.linspace(-1, 10, 50)
        signal = np.zeros((100, 50))

        # Add positive "bleach" at 460 nm
        idx = 15  # ~460 nm
        signal[idx, 25:] = 50  # Positive (wrong)

        data = TAData(wavelength=wavelength, time=time, signal=signal)
        corrected = adjust_sign_convention(data)

        # Bleach should now be negative
        assert corrected.signal[idx, 30] < 0


class TestUnitConversion:
    """Tests for unit conversion."""

    def test_convert_to_mOD(self, sample_ta_data):
        """Test OD to mOD conversion."""
        converted = convert_to_mOD(sample_ta_data)
        expected = sample_ta_data.signal * 1000

        np.testing.assert_array_equal(converted.signal, expected)


class TestBaselineSubtraction:
    """Tests for baseline subtraction."""

    def test_baseline_removed(self, sample_wavelength, sample_time):
        """Test that baseline is properly removed."""
        # Create signal with constant baseline
        signal = np.ones((len(sample_wavelength), len(sample_time))) * 5.0

        data = TAData(
            wavelength=sample_wavelength,
            time=sample_time,
            signal=signal,
        )

        corrected = subtract_baseline(data, time_threshold=0)

        # After baseline subtraction, negative times should be ~0
        neg_time_mask = sample_time < 0
        neg_time_signal = corrected.signal[:, neg_time_mask]

        np.testing.assert_array_almost_equal(
            neg_time_signal, 0, decimal=10
        )

    def test_no_negative_times_fails(self, sample_wavelength):
        """Test that missing negative times fails."""
        # Create time axis with no negative values
        time_positive = np.linspace(0.1, 10, 50)
        signal = np.zeros((len(sample_wavelength), 50))

        data = TAData(
            wavelength=sample_wavelength,
            time=time_positive,
            signal=signal,
        )

        with pytest.raises(AssertionError, match="No time points"):
            subtract_baseline(data, time_threshold=0)


class TestExtraction:
    """Tests for trace/spectrum extraction."""

    def test_extract_time_trace(self, sample_ta_data):
        """Test extracting kinetic trace."""
        time, signal = extract_time_trace(sample_ta_data, wavelength=460)

        assert len(time) == sample_ta_data.ntime
        assert len(signal) == sample_ta_data.ntime

    def test_extract_spectrum(self, sample_ta_data):
        """Test extracting spectrum."""
        wavelength, signal = extract_spectrum(sample_ta_data, time=1.0)

        assert len(wavelength) == sample_ta_data.nwvln
        assert len(signal) == sample_ta_data.nwvln
