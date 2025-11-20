"""
Physical constants and utility functions for spectroscopy calculations.
"""

import numpy as np
from numpy.typing import NDArray


# Physical constants
KB = 1.38064852e-23  # Boltzmann constant (J/K)
C = 2.99792458e8  # Speed of light (m/s)
HBAR = 1.0545718e-34  # Reduced Planck's constant (J·s)
EPS0 = 8.85418782e-12  # Permittivity of free space (F/m)
QE = 1.6021765e-19  # Elementary charge (C)
PI = np.pi


def constants(*args: str) -> tuple:
    """
    Retrieve physical constants by name.

    Parameters
    ----------
    *args : str
        Names of constants to retrieve. Valid names:
        - 'kb': Boltzmann constant (J/K)
        - 'c': Speed of light (m/s)
        - 'hbar': Reduced Planck's constant (J·s)
        - 'eps0': Permittivity of free space (F/m)
        - 'pi': Pi
        - 'qe': Elementary charge (C)

    Returns
    -------
    tuple
        Values of requested constants in order requested.

    Examples
    --------
    >>> kb, c = constants('kb', 'c')
    >>> print(f"kT at 300K = {kb * 300:.4e} J")
    kT at 300K = 4.1419e-21 J
    """
    const_dict = {
        "kb": KB,
        "c": C,
        "hbar": HBAR,
        "eps0": EPS0,
        "pi": PI,
        "qe": QE,
    }

    values = tuple(const_dict[query] for query in args if query in const_dict)
    return values


def find_index(array: NDArray, query: float) -> int:
    """
    Find index of array element nearest to query value.

    Parameters
    ----------
    array : NDArray
        1D array to search.
    query : float
        Value to find.

    Returns
    -------
    int
        Index of nearest element.

    Examples
    --------
    >>> wvln = np.array([400, 450, 500, 550, 600])
    >>> find_index(wvln, 523)
    2
    """
    return int(np.abs(array - query).argmin())


def wavelength_to_wavenumber(wavelength_nm: NDArray) -> NDArray:
    """
    Convert wavelength (nm) to wavenumber (cm^-1).

    Parameters
    ----------
    wavelength_nm : NDArray
        Wavelength in nanometers.

    Returns
    -------
    NDArray
        Wavenumber in cm^-1.

    Examples
    --------
    >>> wavelength_to_wavenumber(np.array([500, 600]))
    array([20000.        , 16666.66666667])
    """
    return 1e7 / wavelength_nm


def wavenumber_to_wavelength(wavenumber_cm: NDArray) -> NDArray:
    """
    Convert wavenumber (cm^-1) to wavelength (nm).

    Parameters
    ----------
    wavenumber_cm : NDArray
        Wavenumber in cm^-1.

    Returns
    -------
    NDArray
        Wavelength in nanometers.
    """
    return 1e7 / wavenumber_cm


def energy_to_wavelength(energy_ev: float) -> float:
    """
    Convert photon energy (eV) to wavelength (nm).

    Parameters
    ----------
    energy_ev : float
        Energy in electron volts.

    Returns
    -------
    float
        Wavelength in nanometers.

    Examples
    --------
    >>> energy_to_wavelength(2.0)
    619.92
    """
    return 1239.84 / energy_ev


def wavelength_to_energy(wavelength_nm: float) -> float:
    """
    Convert wavelength (nm) to photon energy (eV).

    Parameters
    ----------
    wavelength_nm : float
        Wavelength in nanometers.

    Returns
    -------
    float
        Energy in electron volts.
    """
    return 1239.84 / wavelength_nm
