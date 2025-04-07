Installation
============

Prerequisite
------------

Install Julia (backend for PySR):

.. code-block:: bash

   curl -fsSL https://install.julialang.org | sh

Then check if installed properly:

.. code-block:: bash

   julia --version

If julia is not found, most probably it is not yet included in PATH. To include, do:

.. code-block:: bash

   export PATH="$PATH:/path/to/<Julia directory>/bin"

Check out `here <https://julialang.org/downloads/platform/>`_ for platform-specific instructions.

Afterward, it is recommended to start from an empty virtual environment for installing and running SymbolFit.

Installation via PyPI
---------------------

With python>=3.10 and pip:

.. code-block:: bash

   pip install symbolfit

Installation via conda (to be updated for >= v0.2.0, please use pip for now)
----------------------

.. code-block:: bash

   conda create --name symbolfit_env python=3.10
   conda activate symbolfit_env
   conda install -c conda-forge symbolfit

Editable installation for developers
------------------------------------

.. code-block:: bash

   git clone https://github.com/hftsoi/symbolfit.git
   cd symbolfit
   pip install -e .

Requirements
~~~~~~~~~~~~

.. code-block:: text

   python>=3.10
   pysr>=1.4.0,<=1.5.2
   lmfit>=1.2.0,<1.4.0
   matplotlib>=3.8.0,<4.0.0
   seaborn>=0.13.0,<0.14.0
   numpy<2.0.0

