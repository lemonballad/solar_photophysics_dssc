"""
Tests for data I/O functions.
"""

import numpy as np
import pytest
from pathlib import Path

from dssc.io import TAData, load_dat_file, save_chirp_params, load_chirp_params


class TestTAData:
    """Tests for TAData dataclass."""

    def test_valid_creation(self, sample_wavelength, sample_time, sample_signal):
        """Test creating valid TAData."""
        data = TAData(
            wavelength=sample_wavelength,
            time=sample_time,
            signal=sample_signal,
        )
        assert data.nwvln == len(sample_wavelength)
        assert data.ntime == len(sample_time)
        assert data.shape == (len(sample_wavelength), len(sample_time))

    def test_shape_mismatch_fails(self, sample_wavelength, sample_time):
        """Test that mismatched dimensions fail."""
        wrong_signal = np.zeros((10, 10))  # Wrong shape

        with pytest.raises(AssertionError, match="Signal shape"):
            TAData(
                wavelength=sample_wavelength,
                time=sample_time,
                signal=wrong_signal,
            )

    def test_nan_in_wavelength_fails(self, sample_time, sample_signal):
        """Test that NaN in wavelength fails."""
        bad_wavelength = np.linspace(400, 800, 200)
        bad_wavelength[50] = np.nan

        with pytest.raises(AssertionError, match="Wavelength contains"):
            TAData(
                wavelength=bad_wavelength,
                time=sample_time,
                signal=sample_signal,
            )


class TestChirpParams:
    """Tests for chirp parameter I/O."""

    def test_save_and_load(self, tmp_path, sample_chirp_params):
        """Test saving and loading chirp parameters."""
        path = tmp_path / "chirp.dat"

        save_chirp_params(path, sample_chirp_params)
        loaded = load_chirp_params(path)

        np.testing.assert_array_almost_equal(loaded, sample_chirp_params)

    def test_wrong_param_count_fails(self, tmp_path):
        """Test that wrong number of parameters fails."""
        path = tmp_path / "bad_chirp.dat"
        bad_params = np.array([1.0, 2.0])  # Only 2 params

        with pytest.raises(AssertionError, match="Expected 3"):
            save_chirp_params(path, bad_params)

    def test_missing_file_fails(self, tmp_path):
        """Test that missing file fails."""
        path = tmp_path / "nonexistent.dat"

        with pytest.raises(AssertionError, match="not found"):
            load_chirp_params(path)
