# CLAUDE.md - AI Assistant Guide for Solar Photophysics DSSC Repository

## Project Overview

This repository contains code for analyzing the **photophysics and charge injection mechanisms of ruthenium-based dyes** used in Dye-Sensitized Solar Cells (DSSCs). The project combines experimental spectroscopy data processing with kinetic modeling to understand excited state dynamics.

**Status**: Modernized package (v2.0.0)
**Domain**: Computational photophysics, spectroscopy data analysis
**Primary Technique**: Femtosecond Transient Absorption (fs-TA) Spectroscopy

## Repository Structure

```
solar_photophysics_dssc/
├── src/dssc/                    # Main Python package
│   ├── __init__.py              # Package exports
│   ├── io.py                    # Data loading (TAData dataclass)
│   ├── chirp.py                 # Chirp fitting and correction
│   ├── processing.py            # Signal processing
│   ├── fitting.py               # Gaussian fitting + ML
│   ├── kinetiscope.py           # Kinetiscope integration
│   ├── plotting.py              # Visualization functions
│   ├── constants.py             # Physical constants
│   └── cli.py                   # Command-line interface
│
├── notebooks/                   # Jupyter notebooks (main workflows)
│   ├── 01_ta_processing_demo.ipynb
│   ├── 02_chirp_correction.ipynb
│   ├── 03_kinetiscope_modeling.ipynb
│   └── 04_spectral_fitting.ipynb
│
├── tests/                       # Pytest test suite
│   ├── conftest.py              # Shared fixtures
│   ├── test_io.py
│   ├── test_chirp.py
│   ├── test_processing.py
│   ├── test_fitting.py
│   └── test_kinetiscope.py
│
├── docs/                        # Sphinx documentation
│   ├── conf.py
│   ├── index.rst
│   └── api/
│
├── legacy/                      # Archived original code
│   └── sub_task_*/              # Original GUI-based scripts
│
├── kinetiscope_profiles/        # Kinetiscope pulse profiles
├── kinetiscope_results/         # Simulation output data
│
├── requirements.txt             # Dependencies
├── pyproject.toml               # Package configuration
├── .pre-commit-config.yaml      # Pre-commit hooks
└── .github/workflows/test.yml   # CI configuration
```

## Quick Start

### Installation

```bash
pip install -e .           # Basic install
pip install -e .[dev]      # With dev tools
pip install -e .[notebooks] # With Jupyter
```

### Basic Usage

```python
from dssc import (
    load_ta_data,
    fit_chirp,
    apply_chirp_correction,
    adjust_sign_convention,
    subtract_baseline,
    convert_to_mOD,
)

# Load and process data
data = load_ta_data("wavelength.dat", "delay.dat", "signal.dat")
data = apply_chirp_correction(data, chirp_params)
data = adjust_sign_convention(data)
data = subtract_baseline(data)
data = convert_to_mOD(data)
```

### Run Tests

```bash
pytest tests/ -v --cov=dssc
```

## Core Data Structure

```python
from dssc import TAData

@dataclass
class TAData:
    wavelength: NDArray  # nm, shape (nwvln,)
    time: NDArray        # ps, shape (ntime,)
    signal: NDArray      # mOD, shape (nwvln, ntime)
```

**Convention**: `signal[wavelength_index, time_index]`

## Module Reference

### `dssc.io` - Data I/O
- `load_ta_data()` - Load from .dat files
- `save_chirp_params()` / `load_chirp_params()` - Chirp parameter I/O
- `TAData` - Main data container

### `dssc.chirp` - Chirp Correction
- `fit_chirp()` - Determine chirp from blank
- `apply_chirp_correction()` - Apply to sample data
- `calculate_chirp()` - Evaluate polynomial
- `calculate_time_zero()` - Find minimum t₀

### `dssc.processing` - Signal Processing
- `adjust_sign_convention()` - Ensure bleach is negative
- `subtract_baseline()` - Remove DC offset
- `convert_to_mOD()` - OD to milli-OD
- `extract_time_trace()` / `extract_spectrum()` - Data slicing

### `dssc.fitting` - Spectral Fitting
- `fit_ta_gaussians()` - Fit 3-Gaussian model
- `train_parameter_model()` - ML interpolation
- `reconstruct_spectrum()` - Build from parameters

### `dssc.kinetiscope` - Kinetic Modeling
- `create_pump_probe_sequence()` - Generate pulses
- `write_prf_file()` - Kinetiscope format
- `read_kinetiscope_result()` - Parse output
- `calculate_differential_signal()` - Pump-on minus pump-off

### `dssc.plotting` - Visualization
- `plot_ta_contour()` - 2D contour map
- `plot_time_traces()` - Kinetic traces
- `plot_spectra()` - Transient spectra
- `plot_summary()` - Combined figure

### `dssc.constants` - Physical Constants
- `constants()` - Get kb, c, hbar, etc.
- `find_index()` - Array search
- `wavelength_to_wavenumber()` - Unit conversion

## Scientific Concepts

### Femtosecond Transient Absorption (fs-TA)
- **Pump-probe spectroscopy** measuring excited state dynamics
- **Data**: 2D matrix of ΔAbsorption(wavelength, time)
- **Timescales**: fs to μs

### Signal Components
- **GSB** (Ground State Bleach): Negative signal
- **ESA** (Excited State Absorption): Positive signal
- **SE** (Stimulated Emission): Negative signal

### Chirp Correction
Corrects for wavelength-dependent time-zero due to group velocity dispersion:

```
t₀(λ) = a₂λ² + a₁λ + a₀
```

## Data Conventions

### Units
- Wavelength: nanometers (nm)
- Wavenumber: cm⁻¹ (`1e7 / wavelength_nm`)
- Time: picoseconds (ps)
- Signal: milli-Optical Density (mOD)

### Sign Convention
- **Bleach = NEGATIVE** (ground state depletion)
- **Absorption = POSITIVE** (excited state)

### File Format
All `.dat` files are space/tab-delimited ASCII text.

## Development Guidelines

### Design Principles
1. **Fail fast**: Use assertions, not try/except
2. **Explicit parameters**: No hardcoded paths
3. **Type hints**: All functions annotated
4. **Notebooks over GUIs**: Reproducible workflows

### Code Style
- Format with `black`
- Lint with `ruff`
- Type check with `mypy`
- Test with `pytest`

### Adding Features

```python
# Good: explicit, typed, documented
def process_data(
    ta_data: TAData,
    threshold: float = 0.5,
) -> TAData:
    """
    Process TA data with threshold.

    Parameters
    ----------
    ta_data : TAData
        Input data.
    threshold : float
        Processing threshold in ps.

    Returns
    -------
    TAData
        Processed data.
    """
    assert threshold > 0, f"Threshold must be positive: {threshold}"
    # ... implementation
```

### Running CI Locally

```bash
# Format
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/dssc/

# Test
pytest tests/ -v
```

## Notebooks

| Notebook | Purpose |
|----------|---------|
| `01_ta_processing_demo.ipynb` | Complete processing workflow |
| `02_chirp_correction.ipynb` | Chirp fitting and correction |
| `03_kinetiscope_modeling.ipynb` | Pulse profiles and results |
| `04_spectral_fitting.ipynb` | Gaussian fitting with ML |

## Legacy Code

Original GUI-based code is archived in `legacy/sub_task_*/`. See `legacy/README.md` for details.

**Do not modify legacy code** - use the new `dssc` package instead.

## Common Tasks

### Load and Process Data
```python
from dssc import load_ta_data, apply_chirp_correction
from dssc.io import load_chirp_params

data = load_ta_data("wvln.dat", "delay.dat", "signal.dat")
params = load_chirp_params("chirp.dat")
data = apply_chirp_correction(data, params)
```

### Fit Chirp from Blank
```python
from dssc import load_ta_data, fit_chirp
from dssc.io import save_chirp_params

blank = load_ta_data("wvln.dat", "delay.dat", "water.dat")
params = fit_chirp(blank, wavelength_bounds=(460, 700))
save_chirp_params("chirp.dat", params)
```

### Create Kinetiscope Profiles
```python
from dssc import create_pump_probe_sequence, write_prf_file

pump_probe, probe = create_pump_probe_sequence(delay=1e-12)
write_prf_file("pulse.prf", pump_probe)
```

### Fit Spectra
```python
from dssc import fit_ta_gaussians, train_parameter_model

result = fit_ta_gaussians(data)
model = train_parameter_model(result, data, model_type="knn")
```

## Troubleshooting

### Import Errors
```bash
pip install -e .  # Reinstall package
```

### Test Failures
```bash
pytest tests/ -v -x  # Stop on first failure
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

---

**Version**: 2.0.0
**Last Updated**: 2025-11-20
**Python**: 3.9+
