# TODO: Modernization Roadmap

## Overview
Transform the Solar Photophysics DSSC codebase from GUI-based scripts to an automated, testable, notebook-driven workflow.

**Principles**:
- Fail fast and loud (no defensive error handling)
- Clean, readable code with solid documentation
- Jupyter notebooks replace tkinter GUIs
- Automated and reproducible

---

## Phase 1: Project Setup & Dependencies

### 1.1 Environment Setup
- [ ] Create `requirements.txt` with pinned versions:
  ```
  numpy>=1.20
  scipy>=1.7
  matplotlib>=3.5
  scikit-learn>=1.0
  jupyter>=1.0
  pytest>=7.0
  ```
- [ ] Create `pyproject.toml` for modern Python packaging
- [ ] Add `.python-version` file (recommend Python 3.9+)
- [ ] Create `setup.py` or use `pip install -e .` for development

### 1.2 Project Structure
- [ ] Create new directory structure:
  ```
  solar_photophysics_dssc/
  ├── src/
  │   └── dssc/
  │       ├── __init__.py
  │       ├── io.py           # Data loading functions
  │       ├── chirp.py        # Chirp correction
  │       ├── processing.py   # TA processing
  │       ├── fitting.py      # Gaussian/ML fitting
  │       ├── kinetiscope.py  # Kinetiscope integration
  │       ├── plotting.py     # Visualization functions
  │       └── constants.py    # Physical constants
  ├── notebooks/
  │   ├── 01_chirp_correction.ipynb
  │   ├── 02_ta_processing.ipynb
  │   ├── 03_kinetiscope_modeling.ipynb
  │   └── 04_spectral_fitting.ipynb
  ├── tests/
  │   ├── conftest.py
  │   ├── test_io.py
  │   ├── test_chirp.py
  │   ├── test_processing.py
  │   └── fixtures/
  │       └── sample_data/
  ├── data/
  │   └── examples/
  ├── legacy/                  # Archive old sub_task dirs
  └── docs/
  ```
- [ ] Move `sub_task_*` directories to `legacy/`
- [ ] Keep `kinetiscope_profiles/` and `kinetiscope_results/` in place

---

## Phase 2: Code Cleanup & Consolidation

### 2.1 Remove GUI Dependencies
- [ ] Identify all tkinter imports and file dialog usage
- [ ] Replace `filedialog.askopenfilenames()` with function parameters
- [ ] Remove `root.withdraw()` and window management code
- [ ] Delete `messagebox` error handling (fail with exceptions instead)

### 2.2 Eliminate Hardcoded Paths
- [ ] Search for all `C:\\Users\\tpcheshire\\` references
- [ ] Replace with `pathlib.Path` parameters
- [ ] Use relative paths for example data
- [ ] Add path validation with assertions (fail fast)

### 2.3 Consolidate Duplicate Code
Files to merge from `sub_task_1/`, `sub_task_4/`:
- [ ] `Utility_fsTA.py` → `src/dssc/constants.py`
- [ ] `Utility_Chirp.py` + `utilities_chirp.py` → `src/dssc/chirp.py`
- [ ] `utilities_raw_ta_processing.py` → `src/dssc/processing.py`
- [ ] Keep best implementation from each duplicate

### 2.4 Code Style Cleanup
- [ ] Standardize matplotlib alias: `mplot` → `plt`
- [ ] Remove all commented-out code blocks
- [ ] Remove unused imports
- [ ] Fix typos in filenames (`Plottter` → `Plotter`)
- [ ] Apply consistent formatting (use `black` or `ruff`)

### 2.5 Remove Defensive Error Handling
- [ ] Replace `try/except` blocks with assertions
- [ ] Remove `if ~my_file.is_file():` checks - just let it fail
- [ ] Remove `messagebox.showerror()` calls
- [ ] Use `assert` for preconditions:
  ```python
  assert ta.shape == (npix, nt), f"Shape mismatch: {ta.shape}"
  assert np.all(np.isfinite(ta)), "Data contains NaN/Inf"
  ```

---

## Phase 3: Core Library Development

### 3.1 Data I/O Module (`src/dssc/io.py`)
- [ ] `load_dat_file(path: Path) -> np.ndarray`
- [ ] `load_ta_data(wvln_path, time_path, abs_path) -> TAData`
- [ ] `save_chirp_params(path: Path, params: np.ndarray)`
- [ ] `load_chirp_params(path: Path) -> np.ndarray`
- [ ] Create `TAData` dataclass:
  ```python
  @dataclass
  class TAData:
      wavelength: np.ndarray  # nm
      time: np.ndarray        # ps
      signal: np.ndarray      # mOD, shape (nwvln, ntime)
  ```

### 3.2 Chirp Correction Module (`src/dssc/chirp.py`)
- [ ] `fit_chirp(ta_data: TAData, npts: int) -> np.ndarray`
- [ ] `apply_chirp_correction(ta_data: TAData, params: np.ndarray) -> TAData`
- [ ] `find_trust_bounds(ta_data: TAData) -> Tuple[float, float]`
- [ ] `calculate_time_zero(params: np.ndarray) -> float`

### 3.3 Processing Module (`src/dssc/processing.py`)
- [ ] `adjust_sign_convention(ta_data: TAData) -> TAData`
- [ ] `subtract_baseline(ta_data: TAData, threshold: float) -> TAData`
- [ ] `convert_to_mOD(ta_data: TAData) -> TAData`
- [ ] `block_pump_scatter(ta_data: TAData, center_wvln: float, fwhm: float) -> TAData`

### 3.4 Fitting Module (`src/dssc/fitting.py`)
- [ ] `fit_gaussians(ta_data: TAData) -> FitResult`
- [ ] `train_ml_model(fit_results: FitResult) -> sklearn.base.BaseEstimator`
- [ ] Remove hardcoded bounds - make them parameters

### 3.5 Kinetiscope Module (`src/dssc/kinetiscope.py`)
- [ ] `create_pulse_profile(delays: np.ndarray, fwhm: float) -> np.ndarray`
- [ ] `write_prf_file(path: Path, time: np.ndarray, intensity: np.ndarray)`
- [ ] `read_kinetiscope_results(path: Path) -> KinetisopeResult`
- [ ] `calculate_differential_signal(pump_on: np.ndarray, pump_off: np.ndarray) -> np.ndarray`

### 3.6 Plotting Module (`src/dssc/plotting.py`)
- [ ] `plot_ta_contour(ta_data: TAData, ax=None) -> plt.Axes`
- [ ] `plot_time_traces(ta_data: TAData, wavelengths: list) -> plt.Figure`
- [ ] `plot_spectra_at_delays(ta_data: TAData, delays: list) -> plt.Figure`
- [ ] `plot_chirp_fit(wvln: np.ndarray, params: np.ndarray) -> plt.Figure`

### 3.7 Add Type Hints Throughout
- [ ] All function signatures with type hints
- [ ] Use `numpy.typing` for array types
- [ ] Add `py.typed` marker for type checkers

---

## Phase 4: Jupyter Notebooks

### 4.1 Chirp Correction Notebook (`notebooks/01_chirp_correction.ipynb`)
- [ ] Introduction to chirp correction physics
- [ ] Load water blank data (path as variable at top)
- [ ] Calculate and visualize chirp parameters
- [ ] Save parameters for reuse
- [ ] Interactive plots with explanations

### 4.2 TA Processing Notebook (`notebooks/02_ta_processing.ipynb`)
- [ ] Load sample TA data
- [ ] Load or compute chirp parameters
- [ ] Apply chirp correction
- [ ] Sign adjustment and unit conversion
- [ ] Baseline subtraction
- [ ] Visualization: contours, slices, traces
- [ ] Export processed data

### 4.3 Kinetiscope Modeling Notebook (`notebooks/03_kinetiscope_modeling.ipynb`)
- [ ] Create pulse profiles
- [ ] Document Kinetiscope workflow (external step)
- [ ] Load and parse results
- [ ] Calculate differential signals
- [ ] Compare simulation vs experiment
- [ ] Multi-timescale visualization (fs/ps/ns)

### 4.4 Spectral Fitting Notebook (`notebooks/04_spectral_fitting.ipynb`)
- [ ] Gaussian fitting at each delay
- [ ] Visualize fit quality
- [ ] ML-based parameter interpolation
- [ ] Extract kinetic parameters

### 4.5 Notebook Best Practices
- [ ] All paths defined in first cell as variables
- [ ] Markdown explanations for each step
- [ ] Inline plots with proper labels
- [ ] Clear cell outputs before committing
- [ ] Add Table of Contents

---

## Phase 5: Testing

### 5.1 Create Test Fixtures
- [ ] Generate/copy small synthetic test data:
  - `tests/fixtures/sample_data/wavelength.dat`
  - `tests/fixtures/sample_data/delay.dat`
  - `tests/fixtures/sample_data/signal.dat`
  - `tests/fixtures/sample_data/chirp_params.dat`
- [ ] Create test data with known properties (ascending/descending axes)
- [ ] Include edge cases (NaN values, single point, etc.)

### 5.2 Unit Tests

#### `tests/test_io.py`
- [ ] Test loading valid .dat files
- [ ] Test assertion failure on missing files
- [ ] Test assertion failure on dimension mismatch
- [ ] Test TAData dataclass validation

#### `tests/test_chirp.py`
- [ ] Test chirp fitting returns 3 parameters
- [ ] Test chirp correction preserves data shape
- [ ] Test with ascending/descending wavelength axes
- [ ] Test trust bounds calculation

#### `tests/test_processing.py`
- [ ] Test sign convention adjustment
- [ ] Test baseline subtraction
- [ ] Test mOD conversion
- [ ] Test pump blocking

#### `tests/test_fitting.py`
- [ ] Test Gaussian fitting convergence
- [ ] Test parameter bounds

#### `tests/test_kinetiscope.py`
- [ ] Test PRF file format
- [ ] Test result parsing

### 5.3 Integration Tests
- [ ] Full chirp correction workflow
- [ ] Full TA processing pipeline
- [ ] Kinetiscope round-trip

### 5.4 Test Configuration
- [ ] Create `pytest.ini` or `pyproject.toml` [tool.pytest]
- [ ] Add test coverage with `pytest-cov`
- [ ] Create `tests/conftest.py` with shared fixtures

---

## Phase 6: Documentation

### 6.1 Docstrings
- [ ] NumPy-style docstrings for all public functions
- [ ] Include Parameters, Returns, Raises, Examples
- [ ] Document units in parameter descriptions
- [ ] Add equations in LaTeX format where relevant:
  ```python
  def fit_chirp(...):
      """
      Fit chirp correction polynomial.

      The chirp is modeled as:

      .. math::
          t_0(\lambda) = a_0 + a_1 \lambda + a_2 \lambda^2

      Parameters
      ----------
      ta_data : TAData
          Transient absorption data from blank sample
      ...
      """
  ```

### 6.2 API Documentation
- [ ] Set up Sphinx or MkDocs
- [ ] Generate API reference from docstrings
- [ ] Add installation instructions
- [ ] Add usage examples

### 6.3 Update README.md
- [ ] Project description and purpose
- [ ] Installation instructions
- [ ] Quick start guide
- [ ] Link to notebooks
- [ ] Contributing guidelines (even if archived)

### 6.4 Scientific Documentation
- [ ] Document physics background in notebooks
- [ ] Explain data conventions (sign, units, axes)
- [ ] Reference relevant papers
- [ ] Add Jablonski diagram explanation

---

## Phase 7: Automation & CI

### 7.1 Command-Line Interface
- [ ] Create `src/dssc/cli.py` using `argparse` or `click`
- [ ] Commands:
  - `dssc chirp-fit <blank_dir> <output_file>`
  - `dssc process <data_dir> <chirp_file> <output_dir>`
  - `dssc kinetiscope-profile <config_file>`
- [ ] Add entry point in `setup.py`/`pyproject.toml`

### 7.2 GitHub Actions CI
- [ ] Create `.github/workflows/test.yml`:
  ```yaml
  name: Tests
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-python@v4
          with:
            python-version: '3.9'
        - run: pip install -e .[dev]
        - run: pytest --cov=dssc
  ```
- [ ] Add linting workflow (ruff/black)
- [ ] Add type checking workflow (mypy)

### 7.3 Pre-commit Hooks
- [ ] Create `.pre-commit-config.yaml`
- [ ] Hooks: black, ruff, mypy, pytest (fast subset)

---

## Phase 8: Final Cleanup

### 8.1 Archive Legacy Code
- [ ] Move all `sub_task_*` to `legacy/` directory
- [ ] Add `legacy/README.md` explaining original structure
- [ ] Remove from active development

### 8.2 Version Control Cleanup
- [ ] Update `.gitignore`:
  ```
  __pycache__/
  *.pyc
  .pytest_cache/
  .coverage
  *.egg-info/
  dist/
  build/
  .ipynb_checkpoints/
  ```
- [ ] Remove any accidentally committed data files

### 8.3 Final Review
- [ ] Run full test suite
- [ ] Run notebooks end-to-end
- [ ] Review all docstrings
- [ ] Update CLAUDE.md with new structure
- [ ] Tag release v2.0.0

---

## Priority Order

**High Priority** (Do First):
1. Phase 1: Project Setup
2. Phase 2: Code Cleanup
3. Phase 3.1-3.3: Core modules (io, chirp, processing)
4. Phase 4.1-4.2: Main notebooks
5. Phase 5.1-5.2: Test fixtures and unit tests

**Medium Priority**:
6. Phase 3.4-3.6: Remaining modules
7. Phase 4.3-4.4: Additional notebooks
8. Phase 6: Documentation

**Lower Priority** (Nice to Have):
9. Phase 7: Automation & CI
10. Phase 8: Final cleanup

---

## Notes

### Design Decisions
- **No error handling**: Use assertions liberally. If data is wrong, crash immediately with a clear message.
- **Explicit over implicit**: All parameters passed explicitly, no hidden state.
- **Notebooks over GUIs**: Scientists prefer reproducible notebooks they can modify.
- **Fail fast**: `assert` statements at function entry points.

### Migration Strategy
- Keep legacy code in `legacy/` until new code is verified
- Test new functions against old implementations
- Notebooks should reproduce old GUI workflow results exactly

### Estimated Effort
- Phase 1-2: 2-3 hours
- Phase 3: 4-6 hours
- Phase 4: 3-4 hours
- Phase 5: 3-4 hours
- Phase 6-8: 2-3 hours
- **Total**: ~15-20 hours

---

**Created**: 2025-11-20
**Status**: Planning
