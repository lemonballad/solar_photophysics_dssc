"""
Tests for Kinetiscope integration functions.
"""

import numpy as np
import pytest
from pathlib import Path

from dssc.kinetiscope import (
    gaussian_pulse,
    create_pump_probe_sequence,
    write_prf_file,
    standard_delay_series,
    calculate_differential_signal,
    PulseProfile,
    KinetiscopeResult,
)


class TestGaussianPulse:
    """Tests for Gaussian pulse generation."""

    def test_peak_at_center(self):
        """Test that pulse peaks at center time."""
        time = np.linspace(0, 1e-12, 1000)
        center = 500e-15
        pulse = gaussian_pulse(time, center=center, fwhm=50e-15)

        peak_idx = np.argmax(pulse)
        assert time[peak_idx] == pytest.approx(center, rel=0.01)

    def test_amplitude(self):
        """Test that amplitude is correct."""
        time = np.linspace(0, 1e-12, 1000)
        amplitude = 0.5
        pulse = gaussian_pulse(time, center=500e-15, fwhm=50e-15, amplitude=amplitude)

        assert np.max(pulse) == pytest.approx(amplitude, rel=0.01)

    def test_fwhm(self):
        """Test full width at half maximum."""
        time = np.linspace(0, 1e-12, 10000)
        fwhm = 50e-15
        pulse = gaussian_pulse(time, center=500e-15, fwhm=fwhm, amplitude=1.0)

        # Find width at half maximum
        half_max = 0.5
        above_half = time[pulse >= half_max]
        measured_fwhm = above_half[-1] - above_half[0]

        assert measured_fwhm == pytest.approx(fwhm, rel=0.1)


class TestPumpProbeSequence:
    """Tests for pump-probe pulse sequence creation."""

    def test_returns_two_profiles(self):
        """Test that function returns two PulseProfile objects."""
        pump_probe, probe_only = create_pump_probe_sequence(delay=1e-12)

        assert isinstance(pump_probe, PulseProfile)
        assert isinstance(probe_only, PulseProfile)

    def test_same_time_axis(self):
        """Test that both profiles have same time axis."""
        pump_probe, probe_only = create_pump_probe_sequence(delay=1e-12)

        np.testing.assert_array_equal(pump_probe.time, probe_only.time)

    def test_probe_less_than_combined(self):
        """Test that probe intensity is less than combined."""
        pump_probe, probe_only = create_pump_probe_sequence(
            delay=1e-12,
            pump_amplitude=1.0,
            probe_amplitude=0.1,
        )

        # Probe max should be less than combined max
        assert np.max(probe_only.intensity) < np.max(pump_probe.intensity)

    def test_starts_at_zero(self):
        """Test that time axis starts at zero."""
        pump_probe, _ = create_pump_probe_sequence(delay=1e-12)

        assert pump_probe.time[0] == 0

    def test_ends_with_zero_intensity(self):
        """Test that intensity ends at zero."""
        pump_probe, _ = create_pump_probe_sequence(delay=1e-12)

        assert pump_probe.intensity[-1] == 0


class TestWritePRFFile:
    """Tests for PRF file writing."""

    def test_write_creates_file(self, tmp_path):
        """Test that file is created."""
        profile = PulseProfile(
            time=np.array([0, 1e-12, 2e-12]),
            intensity=np.array([0, 1, 0]),
        )
        path = tmp_path / "test.prf"

        write_prf_file(path, profile)

        assert path.exists()

    def test_write_correct_format(self, tmp_path):
        """Test that file has correct format."""
        profile = PulseProfile(
            time=np.array([0, 1e-12, 2e-12]),
            intensity=np.array([0, 1, 0]),
        )
        path = tmp_path / "test.prf"

        write_prf_file(path, profile)

        # Load and verify
        data = np.loadtxt(path)
        assert data.shape == (3, 2)
        np.testing.assert_array_equal(data[:, 0], profile.time)
        np.testing.assert_array_equal(data[:, 1], profile.intensity)


class TestStandardDelaySeries:
    """Tests for standard delay series generation."""

    def test_returns_array(self):
        """Test that delays are returned as array."""
        delays = standard_delay_series()

        assert isinstance(delays, np.ndarray)

    def test_includes_negative_delays(self):
        """Test that negative delays are included."""
        delays = standard_delay_series()

        assert np.any(delays < 0)

    def test_includes_positive_delays(self):
        """Test that positive delays are included."""
        delays = standard_delay_series()

        assert np.any(delays > 0)

    def test_spans_fs_to_us(self):
        """Test that delays span femtoseconds to microseconds."""
        delays = standard_delay_series()

        # Should include fs range
        assert np.any((delays > 0) & (delays < 1e-12))

        # Should include ps range
        assert np.any((delays >= 1e-12) & (delays < 1e-9))

        # Should include ns/μs range
        assert np.any(delays >= 1e-9)


class TestDifferentialSignal:
    """Tests for differential signal calculation."""

    def test_calculates_difference(self):
        """Test that difference is calculated correctly."""
        time = np.linspace(0, 1e-9, 100)

        pump_on = KinetiscopeResult(
            time=time,
            s0=np.ones(100) * 0.5,
            s1=np.ones(100) * 0.3,
            t1=np.ones(100) * 0.2,
            gsb=np.ones(100) * -0.5,
            esa=np.ones(100) * 0.3,
            ems=np.ones(100) * 0.1,
        )

        pump_off = KinetiscopeResult(
            time=time,
            s0=np.ones(100),
            s1=np.zeros(100),
            t1=np.zeros(100),
            gsb=np.zeros(100),
            esa=np.zeros(100),
            ems=np.zeros(100),
        )

        diff = calculate_differential_signal(pump_on, pump_off)

        # Check differences
        np.testing.assert_array_almost_equal(diff['s0'], pump_on.s0 - pump_off.s0)
        np.testing.assert_array_almost_equal(diff['s1'], pump_on.s1 - pump_off.s1)
        np.testing.assert_array_almost_equal(diff['gsb'], pump_on.gsb - pump_off.gsb)

    def test_returns_all_signals(self):
        """Test that all signal types are returned."""
        time = np.linspace(0, 1e-9, 100)
        zeros = np.zeros(100)

        result = KinetiscopeResult(
            time=time, s0=zeros, s1=zeros, t1=zeros,
            gsb=zeros, esa=zeros, ems=zeros
        )

        diff = calculate_differential_signal(result, result)

        expected_keys = {'gsb', 'esa', 'ems', 's0', 's1', 't1'}
        assert set(diff.keys()) == expected_keys


class TestPulseProfile:
    """Tests for PulseProfile dataclass."""

    def test_valid_creation(self):
        """Test creating valid PulseProfile."""
        profile = PulseProfile(
            time=np.array([0, 1, 2]),
            intensity=np.array([0, 1, 0]),
        )

        assert len(profile.time) == 3
        assert len(profile.intensity) == 3

    def test_mismatched_lengths_fails(self):
        """Test that mismatched lengths fail."""
        with pytest.raises(AssertionError):
            PulseProfile(
                time=np.array([0, 1, 2]),
                intensity=np.array([0, 1]),  # Wrong length
            )
