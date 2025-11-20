Quick Start Guide
=================

This guide walks through a basic transient absorption processing workflow.

Loading Data
------------

TA data is stored in three separate ``.dat`` files:

.. code-block:: python

   from dssc import load_ta_data

   data = load_ta_data(
       "wavelength.dat",  # Wavelength axis (nm)
       "delay.dat",       # Time/delay axis (ps)
       "signal.dat",      # TA matrix
   )

   print(f"Shape: {data.shape}")
   print(f"Wavelength: {data.wavelength.min():.0f} - {data.wavelength.max():.0f} nm")
   print(f"Time: {data.time.min():.1f} - {data.time.max():.1f} ps")

Chirp Correction
----------------

Fit chirp parameters from a blank (e.g., water):

.. code-block:: python

   from dssc import fit_chirp, apply_chirp_correction
   from dssc.io import save_chirp_params

   # Fit from blank
   blank = load_ta_data("blank_wvln.dat", "blank_delay.dat", "blank_signal.dat")
   chirp_params = fit_chirp(blank, wavelength_bounds=(460, 700))

   # Save for reuse
   save_chirp_params("chirp_params.dat", chirp_params)

   # Apply to sample
   corrected = apply_chirp_correction(data, chirp_params)

Signal Processing
-----------------

Apply standard processing steps:

.. code-block:: python

   from dssc import adjust_sign_convention, subtract_baseline, convert_to_mOD

   # Ensure bleach is negative, absorption is positive
   data = adjust_sign_convention(data)

   # Remove baseline using negative delays
   data = subtract_baseline(data, time_threshold=-0.5)

   # Convert OD to mOD
   data = convert_to_mOD(data)

Visualization
-------------

Create standard plots:

.. code-block:: python

   from dssc.plotting import plot_summary
   import matplotlib.pyplot as plt

   fig = plot_summary(
       data,
       wavelengths=[450, 550, 650],
       times=[0.5, 2.0, 10.0],
   )
   plt.show()

Spectral Fitting
----------------

Fit Gaussians to extract kinetic parameters:

.. code-block:: python

   from dssc import fit_ta_gaussians

   result = fit_ta_gaussians(data)

   # Parameters: [A1, μ1, σ1, A2, μ2, σ2, A3, μ3, σ3, C]
   amplitudes = result.parameters[[0, 3, 6], :]  # Shape: (3, n_times)

Kinetiscope Integration
-----------------------

Create pulse profiles for kinetic modeling:

.. code-block:: python

   from dssc import create_pump_probe_sequence, write_prf_file

   # Create pump-probe sequence with 1 ps delay
   pump_probe, probe_only = create_pump_probe_sequence(
       delay=1e-12,
       pump_fwhm=40e-15,
       probe_fwhm=80e-15,
   )

   # Write to Kinetiscope format
   write_prf_file("pump_probe_1ps.prf", pump_probe)
