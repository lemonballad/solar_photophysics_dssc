Installation
============

Requirements
------------

- Python 3.9 or higher
- NumPy >= 1.20
- SciPy >= 1.7
- Matplotlib >= 3.5
- scikit-learn >= 1.0

Install from Source
-------------------

Clone the repository:

.. code-block:: bash

   git clone https://github.com/lemonballad/solar_photophysics_dssc.git
   cd solar_photophysics_dssc

Install in development mode:

.. code-block:: bash

   pip install -e .

Install with development dependencies:

.. code-block:: bash

   pip install -e .[dev]

Install with notebook support:

.. code-block:: bash

   pip install -e .[notebooks]

Verify Installation
-------------------

.. code-block:: python

   import dssc
   print(dssc.__version__)
   # Output: 2.0.0

Run Tests
---------

.. code-block:: bash

   pytest tests/ -v
