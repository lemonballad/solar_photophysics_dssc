"""
Kinetiscope integration for kinetic modeling.

Functions for creating pulse profiles and reading simulation results.
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


@dataclass
class PulseProfile:
    """
    Pulse profile for Kinetiscope simulation.

    Attributes
    ----------
    time : NDArray
        Time axis in seconds.
    intensity : NDArray
        Pulse intensity (normalized).
    """

    time: NDArray  # seconds
    intensity: NDArray

    def __post_init__(self):
        assert len(self.time) == len(self.intensity), (
            f"Time and intensity must have same length"
        )


@dataclass
class KinetiscopeResult:
    """
    Results from Kinetiscope simulation.

    Attributes
    ----------
    time : NDArray
        Time axis in seconds.
    s0 : NDArray
        Ground state (S0) population.
    s1 : NDArray
        Singlet excited state (S1) population.
    t1 : NDArray
        Triplet state (T1) population.
    gsb : NDArray
        Ground state bleach signal.
    esa : NDArray
        Excited state absorption signal.
    ems : NDArray
        Emission signal.
    """

    time: NDArray
    s0: NDArray
    s1: NDArray
    t1: NDArray
    gsb: NDArray
    esa: NDArray
    ems: NDArray


def gaussian_pulse(
    time: NDArray,
    center: float,
    fwhm: float,
    amplitude: float = 1.0,
) -> NDArray:
    """
    Generate Gaussian pulse profile.

    Parameters
    ----------
    time : NDArray
        Time axis in seconds.
    center : float
        Pulse center time in seconds.
    fwhm : float
        Full width at half maximum in seconds.
    amplitude : float
        Peak amplitude.

    Returns
    -------
    NDArray
        Pulse intensity profile.
    """
    sigma = fwhm / 2.355
    return amplitude * np.exp(-((time - center) ** 2) / (2 * sigma ** 2))


def create_pump_probe_sequence(
    delay: float,
    pump_fwhm: float = 40e-15,
    probe_fwhm: float = 80e-15,
    pump_amplitude: float = 1.0,
    probe_amplitude: float = 0.1,
    time_resolution: float = 0.5e-15,
    time_end: float = 1.1e-9,
    tolerance: float = 0.001,
) -> tuple[PulseProfile, PulseProfile]:
    """
    Create pump-probe pulse sequence for Kinetiscope.

    Parameters
    ----------
    delay : float
        Pump-probe delay in seconds.
    pump_fwhm : float
        Pump pulse FWHM in seconds.
    probe_fwhm : float
        Probe pulse FWHM in seconds.
    pump_amplitude : float
        Pump pulse amplitude.
    probe_amplitude : float
        Probe pulse amplitude.
    time_resolution : float
        Time step in seconds.
    time_end : float
        End time in seconds.
    tolerance : float
        Intensity threshold for trimming.

    Returns
    -------
    tuple[PulseProfile, PulseProfile]
        (pump_probe_combined, probe_only) pulse profiles.
    """
    # Time axis
    time = np.arange(0, time_end, time_resolution)

    # Calculate pulse centers
    pump_sigma = pump_fwhm / 2.355
    probe_sigma = probe_fwhm / 2.355

    pump_center = 3 * pump_sigma  # Start pump early enough
    probe_center = pump_center + delay

    # Generate pulses
    pump = gaussian_pulse(time, pump_center, pump_fwhm, pump_amplitude)
    probe = gaussian_pulse(time, probe_center, probe_fwhm, probe_amplitude)

    # Combined sequence
    combined = pump + probe

    # Trim to significant values
    mask = combined >= tolerance
    time_trimmed = time[mask]
    combined_trimmed = combined[mask]
    probe_trimmed = probe[mask]

    # Ensure starts at t=0
    if time_trimmed[0] != 0:
        time_trimmed = np.insert(time_trimmed, 0, 0)
        combined_trimmed = np.insert(combined_trimmed, 0, 1e-20)
        probe_trimmed = np.insert(probe_trimmed, 0, 1e-20)

    # Add end point
    time_trimmed = np.append(time_trimmed, time_end)
    combined_trimmed = np.append(combined_trimmed, 0)
    probe_trimmed = np.append(probe_trimmed, 0)

    pump_probe = PulseProfile(time=time_trimmed, intensity=combined_trimmed)
    probe_only = PulseProfile(time=time_trimmed, intensity=probe_trimmed)

    return pump_probe, probe_only


def write_prf_file(path: Path, profile: PulseProfile) -> None:
    """
    Write pulse profile to Kinetiscope .prf format.

    Parameters
    ----------
    path : Path
        Output file path.
    profile : PulseProfile
        Pulse profile to write.
    """
    path = Path(path)
    data = np.column_stack([profile.time, profile.intensity])
    np.savetxt(path, data)


def create_delay_series(
    delays: NDArray,
    output_dir: Path,
    **pulse_kwargs,
) -> None:
    """
    Create pulse profiles for a series of delays.

    Parameters
    ----------
    delays : NDArray
        Array of delays in seconds.
    output_dir : Path
        Output directory for .prf files.
    **pulse_kwargs
        Additional arguments for create_pump_probe_sequence.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for delay in delays:
        pump_probe, probe_only = create_pump_probe_sequence(delay, **pulse_kwargs)

        # Determine filename based on timescale
        if abs(delay) < 1e-12:
            delay_str = f"{delay * 1e15:.0f}fs"
        elif abs(delay) < 1e-9:
            delay_str = f"{delay * 1e12:.0f}ps"
        else:
            delay_str = f"{delay * 1e9:.0f}ns"

        write_prf_file(output_dir / f"pump_probe_{delay_str}.prf", pump_probe)
        write_prf_file(output_dir / f"probe_{delay_str}.prf", probe_only)


def read_kinetiscope_result(path: Path) -> KinetiscopeResult:
    """
    Read Kinetiscope simulation output.

    Parameters
    ----------
    path : Path
        Path to result file.

    Returns
    -------
    KinetiscopeResult
        Parsed simulation results.

    Notes
    -----
    Assumes Kinetiscope output format with columns:
    time, ems, esa, gsb, s0, s1, t1
    """
    path = Path(path)
    assert path.exists(), f"Result file not found: {path}"

    data = np.genfromtxt(
        path,
        skip_header=11,
        skip_footer=1,
        unpack=True,
        usecols=(1, 2, 3, 4, 5, 6, 7),
    )

    time, ems, esa, gsb, s0, s1, t1 = data

    return KinetiscopeResult(
        time=time,
        s0=s0,
        s1=s1,
        t1=t1,
        gsb=gsb,
        esa=esa,
        ems=ems,
    )


def calculate_differential_signal(
    pump_on: KinetiscopeResult,
    pump_off: KinetiscopeResult,
) -> dict[str, NDArray]:
    """
    Calculate differential (pump-on minus pump-off) signals.

    Parameters
    ----------
    pump_on : KinetiscopeResult
        Results with pump.
    pump_off : KinetiscopeResult
        Results without pump.

    Returns
    -------
    dict[str, NDArray]
        Differential signals: 'gsb', 'esa', 'ems', 's0', 's1', 't1'.
    """
    return {
        "gsb": pump_on.gsb - pump_off.gsb,
        "esa": pump_on.esa - pump_off.esa,
        "ems": pump_on.ems - pump_off.ems,
        "s0": pump_on.s0 - pump_off.s0,
        "s1": pump_on.s1 - pump_off.s1,
        "t1": pump_on.t1 - pump_off.t1,
    }


def standard_delay_series() -> NDArray:
    """
    Generate standard delay series spanning fs to μs.

    Returns
    -------
    NDArray
        Delays in seconds: [-500fs to 1μs].
    """
    delays = np.array([-500, -400, -300, -200, -100, 0])

    # fs to μs range
    for magnitude in range(1, 6):
        delays = np.append(delays, np.arange(1, 10) * 10 ** magnitude)

    delays = np.append(delays, 1e6)

    return delays * 1e-15  # Convert to seconds
