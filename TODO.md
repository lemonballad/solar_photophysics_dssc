# TODO: Future Development Roadmap

## Modernization Status: COMPLETE ✅

The initial modernization is complete. All phases from the original roadmap have been implemented:

- ✅ Phase 1: Project Setup & Dependencies
- ✅ Phase 2: Code Cleanup & Consolidation
- ✅ Phase 3: Core Library Development
- ✅ Phase 4: Jupyter Notebooks
- ✅ Phase 5: Testing
- ✅ Phase 6: Documentation
- ✅ Phase 7: Automation & CI
- ✅ Phase 8: Final Cleanup

---

## Current State Assessment

### Package Structure
- **7 modules** in `src/dssc/`
- **4 notebooks** demonstrating all workflows
- **5 test files** with comprehensive coverage
- **Sphinx docs** structure ready for build
- **CI/CD** with GitHub Actions

### Code Quality
- Type hints throughout
- NumPy-style docstrings
- Assertions for fail-fast behavior
- No hardcoded paths
- No GUI dependencies

### Test Coverage
- Core I/O functions tested
- Chirp correction tested
- Signal processing tested
- Fitting functions tested
- Kinetiscope integration tested

---

## Future Development TODO

### High Priority - Usability

#### 1. Real Data Validation
- [ ] Test with actual experimental .dat files
- [ ] Verify chirp correction accuracy
- [ ] Compare processed results with legacy code output
- [ ] Document any edge cases or data format issues

#### 2. Example Data
- [ ] Add sample data files to `data/examples/`
- [ ] Include water blank for chirp fitting
- [ ] Include sample TA data
- [ ] Update notebooks to use real data paths

#### 3. CLI Completion
- [ ] Implement `dssc chirp-fit` command fully
- [ ] Implement `dssc process` command fully
- [ ] Add `dssc plot` command for quick visualization
- [ ] Add progress bars for long operations

### Medium Priority - Features

#### 4. Kinetic Analysis
- [ ] Add exponential decay fitting
- [ ] Global analysis (SVD/MCR)
- [ ] Rate constant extraction
- [ ] Arrhenius analysis tools

#### 5. Advanced Fitting
- [ ] Support variable number of Gaussians
- [ ] Add Lorentzian/Voigt profiles
- [ ] Automatic peak detection
- [ ] Confidence intervals on parameters

#### 6. Data Export
- [ ] Export to HDF5 format
- [ ] Export to Origin/Igor Pro format
- [ ] Generate publication-ready figures
- [ ] LaTeX table generation for parameters

#### 7. Interactive Visualization
- [ ] Add plotly/bokeh interactive plots
- [ ] Jupyter widgets for parameter exploration
- [ ] Real-time fitting preview

### Lower Priority - Polish

#### 8. Documentation Enhancements
- [ ] Build and host Sphinx docs (ReadTheDocs)
- [ ] Add tutorial videos/animations
- [ ] Scientific background section
- [ ] Cite relevant papers

#### 9. Performance Optimization
- [ ] Profile slow operations
- [ ] Parallelize fitting across time points
- [ ] Optimize memory for large datasets
- [ ] Add caching for expensive calculations

#### 10. Additional Integrations
- [ ] TRPL (Time-Resolved PL) analysis
- [ ] TA-NIR (near-infrared) support
- [ ] TCSPC data import
- [ ] Other kinetic modeling software

#### 11. Code Quality Improvements
- [ ] Increase test coverage to >90%
- [ ] Add property-based testing (hypothesis)
- [ ] Benchmark tests for regression
- [ ] Mutation testing

#### 12. Release & Distribution
- [ ] Create v2.0.0 git tag
- [ ] Publish to PyPI
- [ ] Create conda-forge package
- [ ] Add badges to README

---

## Technical Debt

### Known Issues
- [ ] `np.int` deprecation warnings in legacy code
- [ ] Some fitting bounds are hardcoded for Ru complexes
- [ ] Savitzky-Golay window size should be adaptive
- [ ] Log-time axis in chirp correction may not suit all data

### Potential Improvements
- [ ] Replace `griddata` with faster interpolation in `scorrect`
- [ ] Add progress callbacks for long operations
- [ ] Better error messages for data format issues
- [ ] Configurable default parameters (YAML/TOML)

---

## Architecture Considerations

### Future Refactoring
1. **Plugin system** for custom fitting models
2. **Pipeline API** for chaining operations
3. **Async support** for web interfaces
4. **Database backend** for experiment management

### Scalability
- Current design handles typical TA datasets well
- For very large datasets (>1000 time points), consider:
  - Chunked processing
  - Dask integration
  - Memory-mapped arrays

---

## Contributing Guidelines

### For New Features
1. Create issue describing feature
2. Discuss approach in issue
3. Implement with tests
4. Update notebooks if needed
5. Update CLAUDE.md if API changes

### For Bug Fixes
1. Create issue with reproducible example
2. Add failing test
3. Fix bug
4. Verify all tests pass

### Code Standards
- Format with `black`
- Lint with `ruff`
- Type hints required
- Docstrings required (NumPy style)
- Tests required for new functions

---

## Estimated Effort

| Priority | Items | Est. Hours |
|----------|-------|------------|
| High | Real data validation, examples, CLI | 8-10 |
| Medium | Kinetics, advanced fitting, export | 15-20 |
| Lower | Docs, performance, integrations | 10-15 |
| Tech debt | Cleanup, improvements | 5-8 |
| **Total** | | **38-53 hours** |

---

## Quick Wins (< 1 hour each)

- [ ] Add example data files
- [ ] Create v2.0.0 git tag
- [ ] Add badges to README
- [ ] Fix deprecation warnings
- [ ] Add CONTRIBUTING.md

---

**Created**: 2025-11-20
**Status**: Active development roadmap
**Maintainer**: AI Assistant
