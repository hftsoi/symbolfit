Welcome to SymbolFit documentation!
===================================

.. image:: logo.png
   :width: 400px
   :align: center

.. list-table::
   :header-rows: 1
   :widths: 30 30 30
   :align: center

   * - Docs
     - Paper
     - Colab
   * - .. image:: https://img.shields.io/readthedocs/symbolfit?color=gold
          :target: https://symbolfit.readthedocs.io
          :width: 150
     - .. image:: https://img.shields.io/badge/arXiv-2411.09851-b31b1b.svg
          :target: https://arxiv.org/abs/2411.09851
          :width: 150
     - .. image:: https://colab.research.google.com/assets/colab-badge.svg
          :target: https://colab.research.google.com/github/hftsoi/symbolfit/blob/main/colab_demo/symbolfit_colab.ipynb
          :width: 150

.. list-table::
   :header-rows: 1
   :widths: 30 30 30
   :align: center

   * - GitHub
     - pip
     - conda
   * - .. image:: https://img.shields.io/github/created-at/hftsoi/symbolfit?color=black
          :target: https://github.com/hftsoi/symbolfit
          :width: 150
        \n
        .. image:: https://img.shields.io/github/v/release/hftsoi/symbolfit?color=black
          :target: https://github.com/hftsoi/symbolfit/releases
          :width: 150
        \n
        .. image:: https://img.shields.io/github/release-date/hftsoi/symbolfit?color=black
          :target: https://github.com/hftsoi/symbolfit/releases
          :width: 150
     - .. image:: https://img.shields.io/pypi/v/symbolfit?color=orange
          :target: https://pypi.org/project/symbolfit
          :width: 150
        \n
        .. image:: https://img.shields.io/pepy/dt/symbolfit?color=orange
          :target: https://www.pepy.tech/projects/symbolfit
          :width: 150
     - .. image:: https://img.shields.io/conda/vn/conda-forge/symbolfit.svg?color=green
          :target: https://anaconda.org/conda-forge/symbolfit
          :width: 150
        \n
        .. image:: https://img.shields.io/conda/dn/conda-forge/symbolfit.svg?color=green
          :target: https://anaconda.org/conda-forge/symbolfit
          :width: 150


An API to automate parametric modeling with symbolic regression, originally developed for data analysis in the experimental high-energy physics community, but also applicable beyond.

SymbolFit takes binned data with measurement/systematic uncertainties (optional) as input, utilizes `PySR <https://github.com/MilesCranmer/PySR>`_ to perform a machine-search for batches of functional forms that model the data, parameterizes these functions, and utilizes `LMFIT <https://github.com/lmfit/lmfit-py>`_ to re-optimize the functions and provide uncertainty estimation, all in one go.
It is designed to maximize automation with minimal human input. Each run produces a batch of functions with uncertainty estimation, which are evaluated, saved, and plotted automatically into readable output files, ready for downstream tasks.


.. note::

   Under active construction!

.. note::

   This API is actively being updated to accommodate more use cases, so any feedback and contributions are very much welcomed and appreciated! If you encounter any problems while using it, please don’t hesitate to:

   - Report bugs or suggest new features at |issue_badge|

   .. |issue_badge| image:: https://img.shields.io/badge/issues-github-informational
      :target: https://github.com/hftsoi/symbolfit/issues

   - Ask for specific help and recommendations for your dataset at |discussion_badge|
   .. |discussion_badge| image:: https://img.shields.io/badge/discussions-github-informational
      :target: https://github.com/hftsoi/symbolfit/discussions

   If you don't feel like sharing your data in public, please feel free to drop me a msg or email at ho.fung.tsoi@cern.ch. We are happy to assist in getting it to work on your data!

.. toctree::
   :hidden:

   overview.rst
   install.rst
   quick_start.rst
   class.rst 
   demo.rst
   tuning.rst
   citation.rst
