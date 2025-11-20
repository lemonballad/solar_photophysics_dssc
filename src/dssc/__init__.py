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

__all__ = [
    "TAData",
    "load_ta_data",
    "fit_chirp",
    "apply_chirp_correction",
    "adjust_sign_convention",
    "subtract_baseline",
    "convert_to_mOD",
    "constants",
]
