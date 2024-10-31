Quick Start
===========

To run an example fit:

.. code-block:: python

   from symbolfit.symbolfit import *

   dataset = importlib.import_module('examples.datasets.toy_dataset_1.dataset')
   pysr_config = importlib.import_module('examples.pysr_configs.pysr_config_1').pysr_config

   model = SymbolFit(
    	   x = dataset.x,
    	   y = dataset.y,
    	   y_up = dataset.y_up,
    	   y_down = dataset.y_down,
    	   pysr_config = pysr_config,
    	   max_complexity = 60,
    	   input_rescale = True,
    	   scale_y_by = 'mean',
    	   max_stderr = 40,
    	   fit_y_unc = True,
    	   random_seed = None,
    	   loss_weights = None
   )

   model.fit()

After the fit, save results to csv:

.. code-block:: python

   model.save_to_csv(output_dir = 'output_dir/')

and plot results to pdf:

.. code-block:: python

   model.plot_to_pdf(
    	   output_dir = 'output_dir/',
    	   bin_widths_1d = dataset.bin_widths_1d,
    	   #bin_edges_2d = dataset.bin_edges_2d,
    	   plot_logy = False,
    	   plot_logx = False
   )

Candidate functions with full substitutions can be printed in prompt:

.. code-block:: python

   model.print_candidate(candidate_number = 10)

Each run will produce a batch of candidate functions and will automatically save all results to five output files:

* ``candidates.csv``: saves all candidate functions and evaluations in a csv table.
* ``candidates_reduced.csv``: saves a reduced version for essential information without intermediate results.
* ``candidates.pdf``: plots all candidate functions with associated uncertainties one by one for fit quality evaluation.
* ``candidates_gof.pdf``: plots the goodness-of-fit scores.
* ``candidates_correlation.pdf``: plots the correlation matrices for the parameters of each candidate function.
