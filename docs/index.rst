Welcome to SymbolFit documentation!
===================================

.. image:: logo.png
   :width: 400px
   :align: center


An API to automate parametric modeling with symbolic regression, originally developed for data analysis in the experimental high-energy physics community, but also applicable beyond.

Symbolfit takes binned data with measurement/systematic uncertainties as input, utilizes PySR to perform a machine-search for batches of functional forms that model the data, parameterizes these functions, and utilizes LMFIT to re-optimize the functions and provide uncertainty estimation, all in one go. It is designed to maximize automatation with minimal human input. Each run produces a batch of functions with uncertainty estimation, which are evaluated, saved, and plotted automatically into readable output files, ready for downstream tasks.

.. note::

   Under active construction!

.. toctree::
   :hidden:

   overview.rst
   install.rst
   quick_start.rst
   class.rst 
   demo.rst
   tuning.rst
   citation.rst
