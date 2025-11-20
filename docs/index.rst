DSSC Documentation
==================

Tools for analyzing femtosecond transient absorption spectroscopy data
from dye-sensitized solar cell research.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index

Installation
------------

.. code-block:: bash

   pip install -e .

Quick Start
-----------

.. code-block:: python

   from dssc import (
       load_ta_data,
       fit_chirp,
       apply_chirp_correction,
       adjust_sign_convention,
       subtract_baseline,
       convert_to_mOD,
   )

   # Load data
   data = load_ta_data("wavelength.dat", "delay.dat", "signal.dat")

   # Process
   data = apply_chirp_correction(data, chirp_params)
   data = adjust_sign_convention(data)
   data = subtract_baseline(data)
   data = convert_to_mOD(data)

Features
--------

- **Data I/O**: Load and validate TA data files
- **Chirp Correction**: Fit and apply wavelength-dependent time-zero correction
- **Signal Processing**: Sign adjustment, baseline subtraction, unit conversion
- **Spectral Fitting**: Gaussian decomposition with ML interpolation
- **Kinetiscope Integration**: Create pulse profiles and analyze simulation results
- **Visualization**: Contour plots, kinetic traces, transient spectra

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
