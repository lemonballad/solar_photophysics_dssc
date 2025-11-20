"""
DSSC - Solar Photophysics Analysis Package

Tools for analyzing femtosecond transient absorption spectroscopy data
from dye-sensitized solar cell research.
"""

__version__ = "2.0.0"

from .io import load_ta_data, TAData
from .chirp import fit_chirp, apply_chirp_correction
from .processing import adjust_sign_convention, subtract_baseline, convert_to_mOD
from .constants import constants
from .fitting import fit_ta_gaussians, FitResult, train_parameter_model
from .kinetiscope import (
    create_pump_probe_sequence,
    write_prf_file,
    read_kinetiscope_result,
    PulseProfile,
    KinetiscopeResult,
)

__all__ = [
    # Data structures
    "TAData",
    "FitResult",
    "PulseProfile",
    "KinetiscopeResult",
    # I/O
    "load_ta_data",
    # Chirp
    "fit_chirp",
    "apply_chirp_correction",
    # Processing
    "adjust_sign_convention",
    "subtract_baseline",
    "convert_to_mOD",
    # Fitting
    "fit_ta_gaussians",
    "train_parameter_model",
    # Kinetiscope
    "create_pump_probe_sequence",
    "write_prf_file",
    "read_kinetiscope_result",
    # Utilities
    "constants",
]
