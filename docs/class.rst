SymbolFit Class
=================

Arguments
---------

Dataset
~~~~~~~

* ``x``: list | ndarray
   *Default: None*

   Independent variable x, or bin center values for histogram data.
   If provided as a python list, e.g., [1, 2, 3,...] for 1D, [[1, 1], [1, 2], [1, 3],...] for 2D, [[1, 1, 1], [1, 1, 2], [1, 1, 3],...] for 3D etc.
   If provided as ndarray, then shape is (num_examples, dim).

* ``y``: list | ndarray
   *Default: None*

   Dependent variable y, or bin content values for histogram data.
   Shape is (num_examples, 1).

* ``y_up``: list | ndarray
   *Default: None*

   Upper one standard deviation of y (+1 sigma).
   It should be the deviation value and non-negative.
   Shape is (num_examples, 1).

* ``y_down``: list | ndarray
   *Default: None*

   Lower one standard deviation of y (-1 sigma).
   It should be the deviation value and non-negative.
   Shape is (num_examples, 1).

If there is no uncertainty in the input data, one can set ones for both ``y_up`` and ``y_down``, with the same shape as ``y``.
See example section for a graphical illustration.

.. note::

   We will be adding support to more input formats (root, h5, ...) soon!

Fit configuration
~~~~~~~~~~~~~~~~~

* ``pysr_config``: pysr.PySRRegressor class
   *Default: None*

   Configuration file for PySR training, see https://github.com/MilesCranmer/PySR.
   The configuration can be stored in a python file like pysr_config.py:

   .. code-block:: python

      from pysr import PySRRegressor
      pysr_config = PySRRegressor(...)

   and source from there:

   .. code-block:: python

      pysr_config = importlib.import_module('directory.pysr_config').pysr_config
      model = SymbolFit(..., pysr_config = pysr_config,...)

* ``max_complexity``: int
   *Default: None*

   Maximum complexity of expression tree.
   Overwrite the maxsize parameter in PySRRegressor() if provided.

* ``input_rescale``: bool
   *Default: True*

   Rescale x to the range of (0, 1) for fitting, which could avoid fit instability or overflow.
   Fitted functions will be unscaled at outputs.

* ``scale_y_by``: str
   *Default: None*

   Normalize y for fitting: divide y by its 'max', 'mean', 'l2', or None.
   Fitted functions will be unscaled at outputs.
   Applicable when input_rescale is True.

* ``max_stderr``: float (%)
   *Default: 40*

   During refitting with LMFIT, fit is considered failed when any of the parameters has an uncertainty larger than max_stderr, then retry the fit by decreasing the ndf, keeping some parameters fixed to their initial values.
   It is to avoid bad fits when any parameters get unrealistically large.
   Note: setting max_uncertainty to O(10) suffices in most cases.

* ``fit_y_unc``: bool
   *Default: True*

   Consider y_up and y_down in the fits, i.e., take chi2 loss = (y_pred - y_true)^2 / y_unc^2.
   Here, for each bin, y_unc is taken as y_up when (fit - y) > 0, and taken as y_down when (fit - y) < 0.

* ``random_seed``: int
   *Default: None*

   Overwrite pysr_config:

   .. code-block:: python

      pysr_model.set_params(procs = 0,
                            multithreading = False,
                            random_state = self.random_seed,
                            deterministic = True)

   for reproducing the same batch of candidate functions.
   This will force to run PySR in single thread, so slower.

* ``loss_weights``: list | ndarray
   *Default: None*

   Scale loss by (y_model - y_label)^2 * loss_weights in fits.
   Will overwrite (y_model - y_label)^2 / y_unc^2 if provided.
   Shape is (num_examples, 1).


Methods
-------------

**fit()**
~~~~~~~~~~~~~~~
Performs a search for functional forms with PySR.
Parameterizes constants in all functions.
Creates a loop of re-optimization fit (ROF) to improve the constants and provide uncertainty estimation.

**save_to_csv()**
~~~~~~~~~~~~~~~~~

Saves the func_candidates dataframe (results) to a csv file.

1) Full info -> ``candidates.csv``.
2) Reduced info -> ``candidates_reduced.csv``.

* ``output_dir``: str
   *Default: './'*

   Output directory.

**plot_to_pdf()**
~~~~~~~~~~~~~~~~~

Plots all candidate functions to pdf files.

1) Candidate functions -> ``candidates.pdf``.
2) Candidate functions with unc. coverage -> ``candidates_sampling.pdf``.
3) Goodness-of-fit scores -> ``candidates_gof.pdf``.
4) Correlation matrices -> ``candidates_correlation.pdf``.

* ``output_dir``: str
   *Default: './'*

   Output directory.

*Options for 1D data*

* ``bin_widths_1d``: list | ndarray
   *Default: None*

   Bin widths for x for plotting 1D histogram data.
   Shape is (num_examples, 1).
   See example section for a graphical illustration.

* ``plot_logx``: bool
   *Default: False*

   Plot functions in log scale for x in candidates.pdf.

* ``plot_logy``: bool
   *Default: False*

   Plot functions in log scale for y in candidates.pdf.

* ``sampling_95quantile``: bool
   *Default: False*

   Whether to include 95% quantile range when plotting
   total uncertainty coverage from ensemble of functions
   generated by sampling parameters in candidates_sampling.pdf.
   If False, plot only the 68% quantile range.

*Options for 2D data*

* ``bin_edges_2d``: list
   *Default: None*

   Bin edges for x for plotting 2D histogram data,
   i.e., [[x0_0, x0_1,...], [x1_0, x1_1,...]],
   where the leftmost bin in x0 has edges x0_0 and x0_1.
   [x0_0, x0_1,...] has (num_x0_bins + 1) elements.
   [x1_0, x1_1,...] has (num_x1_bins + 1) elements.
   This should be a python list of two sub lists,
   since (num_x0_bins + 1) =/= (num_x1_bins + 1) is possible.

* ``plot_logx0``: bool
   *Default: False*

   Plot 2D functions in log scale for x0 in candidates.pdf.

* ``plot_logx1``: bool
   *Default: False*

   Plot 2D functions in log scale for x1 in candidates.pdf.

* ``plot_logy``: bool
   *Default: False*

   Plot functions in log scale for y in candidates.pdf.

* ``cbar_min``: float
   *Default: None*

   Plot 2D functions with min color bar value in candidates.pdf.

* ``cbar_max``: float
   *Default: None*

   Plot 2D functions with max color bar value in candidates.pdf.

* ``cmap``: str
   *Default: None*

   Plot color bar with matplotlib cmap style.

**print_candidate()**
~~~~~~~~~~~~~~~~~~~~~

Print candidate functions in prompt.

* ``candidate_number``: int
   *Default: 99*

   Print result for a particular candidate function by setting it to its #, or for all candidates by setting it to 99.

