# Legacy Code

This directory contains the original codebase structure before modernization.

## Original Structure

- `sub_task_1/` - Core fs-TA processing workflow with tkinter GUI
- `sub_task_2/` - Kinetiscope integration scripts
- `sub_task_3/` - Experimental GUI development
- `sub_task_4/` - Advanced processing suite with ML

## Why Archived

The legacy code has been replaced with a clean, tested, and documented package in `src/dssc/`. Key improvements:

1. **No GUI dependencies** - Replaced with Jupyter notebooks
2. **No hardcoded paths** - All paths are parameters
3. **Type hints** - Full type annotations
4. **Tests** - Pytest suite with fixtures
5. **Fail fast** - Assertions instead of error handling
6. **Documentation** - NumPy-style docstrings

## Reference

This code is kept for reference only. Use the new `dssc` package for all work:

```python
from dssc import load_ta_data, fit_chirp, apply_chirp_correction
```
