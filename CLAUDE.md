# CLAUDE.md - AI Assistant Guide for Solar Photophysics DSSC Repository

## Project Overview

This repository contains code for analyzing the **photophysics and charge injection mechanisms of ruthenium-based dyes** used in Dye-Sensitized Solar Cells (DSSCs). The project combines experimental spectroscopy data processing with kinetic modeling to understand excited state dynamics.

**Status**: Archived project (completed research)
**Domain**: Computational photophysics, spectroscopy data analysis
**Primary Technique**: Femtosecond Transient Absorption (fs-TA) Spectroscopy

## Repository Structure

```
solar_photophysics_dssc/
├── sub_task_1/              # Core fs-TA processing workflow (PRODUCTION)
│   ├── fsTA.py              # Main processing script with tkinter GUI
│   ├── Utility_Chirp.py     # Chirp correction utilities
│   ├── Utility_fsTA.py      # Core helper functions
│   └── sub_task_1_old/      # Archived previous versions
│
├── sub_task_2/              # Kinetiscope integration
│   ├── kinetiscope read TA.py                    # Reads simulation results
│   └── kinetiscope_ext_stimulus_profile_maker.py # Creates pulse sequences
│
├── sub_task_3/              # Experimental chirp GUI development
│   └── chirp.py             # GUI class for chirp parameters
│
├── sub_task_4/              # Advanced processing suite (MOST COMPREHENSIVE)
│   ├── Raw_TA_Proccessing.py            # Main GUI entry point
│   ├── utilities_raw_ta_processing.py   # Core processing functions
│   ├── utilities_chirp.py               # Enhanced chirp correction
│   ├── File Explorer and Plottter.py    # ML-based fitting
│   └── sub_task_4_1/                    # GUI component modules
│       ├── main_frame.py
│       ├── get_parameters.py
│       ├── get_ta_files.py
│       └── tc_buttons.py
│
├── kinetiscope_profiles/    # Input pulse sequences (july/october/november/trpl)
└── kinetiscope_results/     # Simulation output data
```

### Directory Purpose Summary

| Directory | Status | Purpose |
|-----------|--------|---------|
| `sub_task_1/` | Production | Basic fs-TA processing with chirp correction |
| `sub_task_2/` | Production | Kinetiscope kinetic modeling integration |
| `sub_task_3/` | Experimental | GUI development testbed |
| `sub_task_4/` | Most Advanced | Full-featured processing suite with ML |

**Key Insight**: `sub_task_4/` is the most mature implementation with the richest feature set.

## Core Scientific Concepts

### Femtosecond Transient Absorption (fs-TA)
- **What**: Pump-probe spectroscopy measuring excited state dynamics
- **Data Structure**: 2D matrices of `ΔAbsorption(wavelength, time)`
- **Timescales**: Femtoseconds (fs) to microseconds (μs)
- **Signal Components**:
  - **GSB**: Ground State Bleach (negative signal)
  - **ESE**: Excited State Absorption (positive signal)
  - **EMS**: Emission (negative signal)

### Chirp Correction
**Critical preprocessing step** to account for wavelength-dependent time-zero in ultrafast spectroscopy.

**Physical Cause**: Different wavelengths of the broadband probe pulse arrive at different times due to group velocity dispersion.

**Correction Method**:
1. Measure chirp using blank sample (water)
2. Fit polynomial to wavelength-dependent time-zero: `t₀(λ) = a₀ + a₁λ + a₂λ²`
3. Interpolate data to correct time axis for each wavelength

## Data Formats and Conventions

### Input Files (`.dat` format)

All data files are **space/tab-delimited ASCII** text files:

```
td1.dat                  # Delay stage positions (raw units)
wavelength_recal.dat     # Wavelength axis (nm)
wvlnCCS200.dat          # Alternative wavelength file
av1.dat                 # TA absorption matrix (averaged)
log1.dat                # Alternative TA data file
chirpfit.dat            # Chirp parameters [a₀, a₁, a₂]
```

### Data Structure Conventions

**Matrix Dimensions**:
- `ta[npix, nt]` - Absorption matrix indexed as `[wavelength, time]`
- `npix` - Number of wavelength pixels
- `nt` - Number of time points

**Axis Ordering**:
- Files may have ascending OR descending wavelength/time axes
- Code uses boolean flags (`flag_wvln_plus`, `flag_time_plus`) to track ordering
- Always validate axis monotonicity when loading data

**Units**:
- Wavelength: nanometers (nm)
- Wavenumber: cm⁻¹ (conversion: `ν = 10⁷/λ`)
- Time: picoseconds (ps) or femtoseconds (fs)
- Absorption: milli-Optical Density (mOD)
- Stage position: arbitrary units → converted to time delay

### Sign Conventions

⚠️ **CRITICAL**: Sign conventions differ between instruments and analysis steps.

```python
# Standard convention in this codebase:
# - Bleach (GSB) → NEGATIVE signal
# - Absorption (ESE) → POSITIVE signal
#
# Sign adjustment code pattern:
ibleach = np.max(np.argmax(np.abs(ta), axis=0))
for ipix, itime in enumerate:
    A2[ipix, itime] = -np.sign(ta[ibleach, itime]) * ta[ipix, itime] * 1000
    # Multiplier of 1000 converts OD → mOD
```

## Key Workflows

### Workflow A: Basic fs-TA Processing (`sub_task_1/`)

```
1. Launch GUI file dialog to select sample data
2. Load chirp parameters from water blank:
   - Read td1.dat, wavelength_recal.dat, av1.dat
   - Calculate expectation value ⟨t⟩ from TA signal
   - Find reliable fitting region via variance analysis
   - Fit 2nd-order polynomial to chirp
   - Save to chirpfit.dat
3. Load sample TA data (same file structure)
4. Apply chirp correction via interpolation
5. Adjust signal sign and convert to mOD
6. Generate visualizations:
   - 2D contour plots
   - Wavelength slices at fixed times
   - Time traces at fixed wavelengths
```

**Entry Point**: `sub_task_1/fsTA.py`

### Workflow B: Kinetiscope Modeling (`sub_task_2/`)

```
1. Create pump-probe pulse sequences (.prf files):
   - Define Gaussian pulse profiles (FWHM, center wavelength)
   - Generate delay series across fs/ps/ns timescales
   - Export time-intensity pairs for Kinetiscope
2. Run Kinetiscope simulations (external software):
   - Define reaction mechanisms (.rxn files)
   - Simulate excited state populations
3. Read Kinetiscope results:
   - Extract S₀, S₁, T₁ populations
   - Extract spectral features (GSB, ESE, EMS)
4. Calculate differential signals (pump-on vs pump-off)
5. Compare simulated vs experimental TA
```

**Entry Point**: `sub_task_2/kinetiscope_ext_stimulus_profile_maker.py` (write)
**Analysis**: `sub_task_2/kinetiscope read TA.py` (read)

### Workflow C: Advanced GUI Processing (`sub_task_4/`)

```
1. Launch main GUI application
2. Select chirp correction mode:
   a) Load existing chirp parameters from file
   b) Compute new parameters:
      - Browse for blank sample data
      - Process with Savitzky-Golay filtering
      - Save parameters for reuse
3. Load sample TA data via file dialog
4. Apply chirp correction with log-time interpolation
5. Optional: ML-based spectral fitting
   - Fit Gaussian components at each delay
   - Train KNN/RandomForest regressor
   - Predict fit parameters across time
6. Visualize and export processed data
```

**Entry Point**: `sub_task_4/Raw_TA_Proccessing.py`

## Core Utility Functions

### Shared Utilities (Present in Multiple sub_tasks)

#### `Utility_fsTA.py`
```python
constants(*args)
    # Returns physical constants: kb, c, hbar, eps0, pi, qe
    # Usage: kb, c, hbar = constants('kb', 'c', 'hbar')

find_index(array, query)
    # Returns index of nearest array element to query value
    # Usage: idx = find_index(wavelength_axis, 550)  # Find ~550nm
```

#### `Utility_Chirp.py` / `utilities_chirp.py`
```python
load_TA(path_wvln, path_time, path_abs, guess_flag)
    # Loads TA data from three separate files
    # Returns: wvln_axis, time_axis, ta_matrix, npix, nt
    # Validates dimensions and handles ascending/descending axes

chirp_fitter(npts, file_time, file_wvln, file_abs, path, plot_flag)
    # Determines chirp correction parameters from blank sample
    # Returns: [a0, a1, a2] polynomial coefficients

scorrect(ta_matrix, wvln_axis, time_axis, chirp_params)
    # Applies chirp correction via interpolation
    # Returns: corrected_time_axis, corrected_ta_matrix

find_trust_bounds(wvln, delay, ta)
    # Identifies reliable data region using 2nd derivative variance
    # Returns: wavelength bounds for chirp fitting
```

#### `utilities_raw_ta_processing.py` (sub_task_4)
```python
subtract_baseline(ta, time, delay_threshold=-0.5)
    # Removes baseline using median of negative delays
    # Critical for offset correction

fit_frequency_domain(wvln, delay, signal)
    # Fits sum of 3 Gaussians at each delay time
    # Uses scipy.optimize.curve_fit + sklearn ML
    # Returns: parameters[10, nt], covariance matrix
```

## Coding Conventions

### Naming Conventions

**Variables**:
```python
# Physics quantities - lowercase abbreviations
wvln        # wavelength
pm          # polynomial coefficients
kb, hbar    # physical constants
kT          # thermal energy

# Arrays - descriptive with _axis or _mat suffix
time_axis, wvln_axis
delay_mat, ta_matrix

# Indices - 'i' prefix
ipix, itime, idelay, ibleach

# Dimensions - 'n' prefix
npts, npix, nt, nw

# Flags - 'flag_' prefix
flag_time_plus, chirp_flag, plot_chirp_flag
```

**Functions**:
```python
# Snake_case with descriptive names
def chirp_fitter(...)
def load_TA(...)
def subtract_baseline(...)
def find_trust_bounds(...)
```

**Files**:
```python
# Spaces in filenames (Windows legacy)
"P Abs Gaussian Fit.py"
"fs-TA Processing.py"
"File Explorer and Plottter.py"  # Note: typo "Plottter" is intentional

# Utility modules end with underscore
"Utility_Code_.py"
```

### Import Patterns

```python
# Standard library
import os
import datetime
from pathlib import Path

# Scientific stack
import numpy as np
import matplotlib.pyplot as mplot  # Note: alias is "mplot" not "plt"
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d

# GUI
import tkinter as tk
from tkinter import filedialog, messagebox

# Machine learning (sub_task_4 only)
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
```

### Common Code Patterns

#### File Selection GUI
```python
root = tk.Tk()
root.withdraw()
filez = filedialog.askopenfilenames(parent=root, title='Choose a file')
lst = list(filez)
```

#### Hardcoded Windows Paths
```python
# ⚠️ WARNING: Many scripts contain hardcoded Windows paths
path = 'C:\\Users\\tpcheshire\\Documents\\TiCat3_TA\\1-29-16\\...'

# When modifying code, replace with:
from pathlib import Path
from tkinter import filedialog
path = filedialog.askdirectory()
```

#### Loop Over 2D Data
```python
index_pix = np.arange(0, npix)
index_time = np.arange(0, nt)
for ipix in index_pix:
    for itime in index_time:
        # Process ta[ipix, itime]
```

#### Date-Based File Organization
```python
# Kinetiscope results use datetime module
now = datetime.datetime.now()
today = now.strftime("%B") + " " + str(now.day) + " " + str(now.year)
today_folder = now.strftime("%B") + " " + str(now.year) + "\\" + today
```

## Development Guidelines for AI Assistants

### Before Making Changes

1. **Identify the correct sub_task directory**:
   - `sub_task_1/` - Simple, production workflows
   - `sub_task_4/` - Advanced features, ML integration
   - Avoid modifying `sub_task_3/` (experimental only)

2. **Understand the data flow**:
   - Always check file format expectations (`.dat` structure)
   - Verify wavelength/time axis ordering (ascending vs descending)
   - Confirm sign conventions for bleach vs absorption

3. **Check for code duplication**:
   - Utilities are duplicated across directories
   - Changes may need to propagate to multiple files
   - Consider creating a shared `utils/` directory for new code

### Code Modification Best Practices

#### When Adding Features

✅ **DO**:
- Use `pathlib.Path` for new file operations
- Add type hints for new functions
- Use `numpy` vectorization instead of nested loops when possible
- Test with both ascending/descending wavelength data
- Validate matrix dimensions with assertions
- Add docstrings explaining physics/math concepts

❌ **DON'T**:
- Hardcode file paths (use file dialogs)
- Assume wavelength/time axes are always ascending
- Mix different sign conventions without documentation
- Use `plt` alias (existing code uses `mplot`)
- Remove commented code without checking git history first

#### When Fixing Bugs

**Common Issues**:
1. **Axis ordering**: Always check `flag_wvln_plus` and `flag_time_plus`
2. **Index bounds**: Use `find_index()` utility instead of manual search
3. **Sign errors**: Double-check bleach vs absorption convention
4. **Unit conversion**: Verify nm ↔ cm⁻¹ conversions (`1e7/wavelength`)
5. **Chirp correction**: Ensure polynomial coefficients are applied correctly

**Debugging Strategy**:
```python
# Add validation checks
assert ta.shape == (npix, nt), f"Expected ({npix}, {nt}), got {ta.shape}"
assert np.all(np.isfinite(ta)), "TA matrix contains NaN or Inf"
assert np.all(np.diff(wvln_axis) > 0), "Wavelength axis not monotonically increasing"
```

### Working with GUIs

**tkinter Patterns in This Codebase**:
```python
# Parent-child window management
root = tk.Tk()
root.withdraw()  # Hide root window

# Multi-file selection
files = filedialog.askopenfilenames(...)
file_list = list(files)

# Error messages
from tkinter import messagebox
messagebox.showerror("Error", "Description")

# GUI classes (sub_task_4/sub_task_4_1/)
class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
```

### Physical Constants and Units

**Available via `constants()` function**:
```python
kb = 1.380649e-23      # Boltzmann constant (J/K)
c = 299792458          # Speed of light (m/s)
hbar = 1.054571e-34    # Reduced Planck constant (J·s)
eps0 = 8.854187e-12    # Vacuum permittivity (F/m)
pi = 3.141592653589793
qe = 1.602176634e-19   # Elementary charge (C)
```

**Common Conversions**:
```python
# Wavelength (nm) → Wavenumber (cm⁻¹)
wavenumber = 1e7 / wavelength_nm

# Energy (eV) → Wavelength (nm)
wavelength_nm = 1239.84 / energy_eV

# Stage position → Time delay (ps)
time_ps = (position - t_zero) * calibration_factor
```

### Machine Learning Integration (sub_task_4 only)

**Use Case**: Interpolate Gaussian fit parameters across noisy data

```python
# Training data: spectral features + delay time
X = np.append(signal[:, idelay], delay[idelay])

# Target: Gaussian parameters [A1, μ1, σ1, A2, μ2, σ2, A3, μ3, σ3, C]
y = fit_parameters.T

# Model
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsRegressor
regr = MultiOutputRegressor(KNeighborsRegressor(n_neighbors=5))
regr.fit(X_train, y_train)
```

**⚠️ Note**: ML code is experimental and not fully integrated into main workflow.

## Common Pitfalls and Solutions

### Pitfall 1: Hardcoded Paths
**Problem**: Scripts reference `C:\Users\tpcheshire\...`

**Solution**:
```python
# Replace hardcoded paths with file dialogs
from tkinter import filedialog
path = filedialog.askdirectory(title="Select data directory")
```

### Pitfall 2: Sign Convention Confusion
**Problem**: Bleach appears positive instead of negative

**Solution**:
```python
# Check sign at maximum bleach wavelength
ibleach = np.argmax(np.abs(ta), axis=0).max()
sign_correction = np.sign(ta[ibleach, :])

# Apply consistent sign convention
ta_corrected = -sign_correction * ta * 1000  # mOD units
```

### Pitfall 3: Axis Ordering Assumptions
**Problem**: Code assumes ascending wavelength, but data is descending

**Solution**:
```python
# Always check and sort
if np.diff(wvln_axis)[0] < 0:
    wvln_axis = wvln_axis[::-1]
    ta = ta[::-1, :]
    flag_wvln_plus = False
```

### Pitfall 4: Interpolation Errors
**Problem**: `scorrect()` fails with NaN values

**Solution**:
```python
# Check for monotonicity before interpolation
assert np.all(np.diff(time_axis) > 0) or np.all(np.diff(time_axis) < 0)

# Remove non-finite values
mask = np.isfinite(ta)
ta_clean = np.where(mask, ta, 0)
```

### Pitfall 5: Missing Dependencies
**Problem**: No `requirements.txt` file

**Solution**: Install manually:
```bash
pip install numpy scipy matplotlib scikit-learn
# tkinter typically included with Python
```

## Testing Strategy

### Minimal Test Cases

**Test Chirp Correction**:
```python
# Use water blank data from kinetiscope_profiles/
test_path = "./kinetiscope_profiles/july/"
wvln, time, ta, npix, nt = load_TA(
    test_path + "wavelength.dat",
    test_path + "delay.dat",
    test_path + "blank.dat",
    False
)
pm = chirp_fitter(500, "delay.dat", "wavelength.dat", "blank.dat", test_path, True)
assert len(pm) == 3, "Chirp fit should return 3 parameters"
assert np.all(np.isfinite(pm)), "Chirp parameters should be finite"
```

**Test Data Loading**:
```python
# Verify matrix dimensions
wvln, time, ta, npix, nt = load_TA(path_wvln, path_time, path_ta, False)
assert ta.shape == (npix, nt), f"Shape mismatch: {ta.shape} != ({npix}, {nt})"
assert len(wvln) == npix, f"Wavelength axis length {len(wvln)} != {npix}"
assert len(time) == nt, f"Time axis length {len(time)} != {nt}"
```

**Test Sign Convention**:
```python
# Bleach should be negative after correction
ta_corrected = process_ta(ta_raw)
bleach_indices = np.where(ta_corrected < 0)
assert len(bleach_indices[0]) > 0, "No negative (bleach) signal found"
```

## Git Workflow

### Branch Strategy
- Main development branch: `claude/claude-md-*` (auto-generated)
- Always push to feature branches, not main
- Use descriptive commit messages referencing the analysis type

### Commit Message Examples
```bash
git commit -m "Add chirp correction validation checks"
git commit -m "Fix wavelength axis ordering in load_TA()"
git commit -m "Refactor hardcoded paths to use file dialogs"
git commit -m "Add ML-based Gaussian fitting to sub_task_4"
```

## External Dependencies

### Kinetiscope
- **What**: Kinetic modeling software (external, proprietary)
- **Input**: `.prf` pulse profiles, `.rxn` reaction mechanisms
- **Output**: Time-resolved state populations and spectral features
- **Integration**: Scripts in `sub_task_2/` read/write Kinetiscope files

### Data Sources
- **Experimental**: fs-TA data from ultrafast laser system
- **Format**: ASCII `.dat` files (tab/space delimited)
- **Location**: Originally on Windows machine (see hardcoded paths)

## Troubleshooting

### Import Errors
```bash
# If tkinter is missing (Linux)
sudo apt-get install python3-tk

# If sklearn version mismatch
pip install --upgrade scikit-learn
```

### File Not Found Errors
```python
# Most scripts have hardcoded paths - update before running
# Search for: "C:\\Users\\tpcheshire"
# Replace with: file dialog or relative path
```

### GUI Not Appearing
```python
# Ensure X11 forwarding (if SSH) or local display
# Check that root.withdraw() is not preventing visibility
root.deiconify()  # Show window if hidden
```

## Future Improvements

### Suggested Refactoring
1. **Consolidate utilities**: Create `utils/` package to eliminate duplication
2. **Remove hardcoded paths**: Use config files or CLI arguments
3. **Add unit tests**: Use `pytest` for scientific validation
4. **Type hints**: Add annotations for better IDE support
5. **Documentation**: Add NumPy-style docstrings
6. **Requirements file**: Create `requirements.txt` with pinned versions
7. **CLI interface**: Add `argparse` for non-GUI operation
8. **Logging**: Replace print statements with `logging` module

### Modernization Opportunities
```python
# Current pattern
import matplotlib.pyplot as mplot
import numpy as np

# Modern alternative
import matplotlib.pyplot as plt  # Standard alias
import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class TAData:
    """Transient absorption dataset"""
    wavelength: np.ndarray
    time: np.ndarray
    signal: np.ndarray

    def __post_init__(self):
        assert self.signal.shape == (len(self.wavelength), len(self.time))
```

## Quick Reference Card

### Most Important Files
1. `sub_task_4/Raw_TA_Proccessing.py` - Start here for GUI workflow
2. `sub_task_1/fsTA.py` - Simpler processing script
3. `sub_task_4/utilities_chirp.py` - Core chirp correction
4. `sub_task_2/kinetiscope read TA.py` - Simulation analysis

### Key Functions to Understand
- `load_TA()` - Load experimental data
- `chirp_fitter()` - Determine chirp parameters
- `scorrect()` - Apply chirp correction
- `find_index()` - Array search utility
- `constants()` - Physical constants

### Critical Data Conventions
- Matrix indexing: `ta[wavelength, time]`
- Sign: Bleach = negative, Absorption = positive
- Units: wavelength (nm), time (ps), signal (mOD)
- Chirp polynomial: `t₀(λ) = a₀ + a₁λ + a₂λ²`

### Typical Workflow Summary
```
Water Blank → Chirp Fit → Save Parameters
    ↓
Sample Data → Load → Apply Chirp Correction
    ↓
Sign Adjustment → Unit Conversion (mOD)
    ↓
Visualization → Analysis → Export
```

---

**Document Version**: 1.0
**Last Updated**: 2025-11-19
**Maintained By**: AI Assistant Analysis
**Status**: Comprehensive guide for archived research code
