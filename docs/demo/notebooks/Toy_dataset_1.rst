.. container:: cell code
   :name: 2eb555c2-8163-4fe3-8546-3454b651e865

   .. code:: python

      from symbolfit.symbolfit import *

.. container:: cell markdown
   :name: 66906c16-9eb8-43ff-aa4d-29a5ea50d033

   .. rubric:: Dataset
      :name: dataset

.. container:: cell markdown
   :name: 1bbc1b76-6d40-48d4-9dde-6cb56052d1e0

   Five inputs are needed, which can be python lists or numpy arrays:

   #. ``x``: independent variable (bin center values).
   #. ``y``: dependent variable.
   #. ``y_up``: upward uncertainty in y per bin.
   #. ``y_down``: downward uncertainty in y per bin.
   #. ``bin_widths_1d`` bin widths for x.

   - Elements in both y_up and y_down should be non-negative values.
   - These values are the "delta" in y,

     - y + y_up = y shifted up by one standard deviation.
     - y - y_down = y shifted down by one standard deviation.

   - If no uncertainty in the dataset, one can set y_up and y_down to
     ones with the same shape as x.

.. container:: cell code
   :name: 95ae43f4-d947-4c53-a133-73b163369e3d

   .. code:: python

      x = [12.5, 37.5, 62.5, 87.5, 112.5, 137.5, 162.5, 187.5, 212.5, 237.5, 262.5, 287.5, 312.5, 337.5, 362.5, 387.5, 412.5, 437.5, 462.5, 487.5]
      y = [10.234884262084961, 122.1119384765625, 338.9125061035156, 810.2549438476562, 649.0571899414062, 351.8170166015625, 248.619873046875, 186.88763427734375, 141.754150390625, 103.42931365966797, 78.36450958251953, 60.3994255065918, 49.005863189697266, 33.54744338989258, 27.76025390625, 25.299283981323242, 19.729631423950195, 14.033162117004395, 15.06820011138916, 9.641764640808105]
      y_up = [3.199200566092248, 11.050427072134475, 18.409576478113657, 28.464977495997715, 25.476600831771226, 18.756785881423355, 15.767684454189048, 13.670685216087149, 11.906055198537633, 10.170020337229811, 8.852373104570296, 7.771706730608908, 7.000418786736781, 5.7920154859852175, 5.268800044246317, 5.029839359395411, 4.441804973650936, 3.746086239931536, 3.8817779575072504, 3.105119102515732]
      y_down = [3.199200566092248, 11.050427072134475, 18.409576478113657, 28.464977495997715, 25.476600831771226, 18.756785881423355, 15.767684454189048, 13.670685216087149, 11.906055198537633, 10.170020337229811, 8.852373104570296, 7.771706730608908, 7.000418786736781, 5.7920154859852175, 5.268800044246317, 5.029839359395411, 4.441804973650936, 3.746086239931536, 3.8817779575072504, 3.105119102515732]
      bin_widths_1d = [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]

.. container:: cell markdown
   :name: 2c819ddd-a45e-4bb9-915e-19718576b0eb

   Plot the dataset to see what we will be fitting to:

.. container:: cell code
   :name: ee24eb08-6d27-49ec-8221-383219ae5229

   .. code:: python

      fig, axes = plt.subplots(figsize = (6, 4))
      plt.errorbar(np.array(x).flatten(),
                   np.array(y).flatten(),
                   yerr = [np.array(y_down).flatten(), np.array(y_up).flatten()],
                   xerr = np.array(bin_widths_1d)/2,
                   fmt = '.', c = 'black', ecolor = 'grey', capsize = 0,
                  )

.. container:: cell markdown
   :name: 8c27af64-6c06-40b7-97ca-8b55d8fab279

   .. rubric:: Configure the fit
      :name: configure-the-fit

.. container:: cell markdown
   :name: 28c4e18d-adc4-4f41-bace-96138f09a128

   .. rubric:: Configure PySR to define the function space being
      searched for with symbolic regression
      :name: configure-pysr-to-define-the-function-space-being-searched-for-with-symbolic-regression

.. container:: cell code
   :name: f3415459-b989-4cbe-8472-3fe2ae77f9be

   .. code:: python

      from pysr import PySRRegressor
      import sympy

      pysr_config = PySRRegressor(
          model_selection = 'accuracy',
          niterations = 200,
          maxsize = 60,
          binary_operators = [
              '+', '*'
                           ],
          unary_operators = [
              'exp',
              'gauss(x) = exp(-x*x)',
              'tanh',
          ],
          nested_constraints = {
              'tanh':   {'tanh': 0, 'exp': 0, 'gauss': 0, '*': 2},
              'exp':    {'tanh': 0, 'exp': 0, 'gauss': 0, '*': 2},
              'gauss':  {'tanh': 0, 'exp': 0, 'gauss': 0, '*': 2},
              '*':      {'tanh': 1, 'exp': 1, 'gauss': 1, '*': 2},
          },
          extra_sympy_mappings={
              'gauss': lambda x: sympy.exp(-x*x),
                               },
          loss='loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
      )

.. container:: cell markdown
   :name: ed837443-a0fc-4227-9ea9-350c898a96b2

   Here, we allow two binary operators (+, \*) and three unary operators
   (exp, gauss, tanh) when searching for functional forms.

   Nested constraints are imposed to prohibit, e.g., exp(exp(x))...

   Loss function is a weighted MSE, where the weight is the sqaured
   uncertainty by default in SymbolFit.

   For PySR options, please see:

   - https://github.com/MilesCranmer/PySR
   - https://astroautomata.com/PySR/

.. container:: cell markdown
   :name: c904493f-a36c-4b84-bc09-5fdad6e0f6d3

   .. rubric:: Configure SymbolFit with the PySR config and for the
      re-optimization process
      :name: configure-symbolfit-with-the-pysr-config-and-for-the-re-optimization-process

.. container:: cell code
   :name: a61d9307-8b17-42dc-9915-3a4d0f7d1c51

   .. code:: python

      model = SymbolFit(
              # Dataset: x, y, y_up, y_down.
          	x = x,
          	y = y,
          	y_up = y_up,
          	y_down = y_down,
              # PySR configuration of function space.
          	pysr_config = pysr_config,
              # Constrain the maximum function size and over-write maxsize in pysr_config.
          	max_complexity = 60,
              # Whether to scale input x to be within 0 and 1 during fits for stability, as large x could lead to overflow.
          	input_rescale = True,
              # Whether to scale y during fits for stability (when input_rescale is True): None / 'mean' / 'max' / 'l2'.
          	scale_y_by = 'mean',
              # Set a maximum standard error (%) for all parameters to avoid bad fits during re-optimization (will re-parameterize and re-fit with fewer parameters when too large errors).
          	max_stderr = 20,
              # Consider y_up and y_down to weight the MSE loss during SR search and re-optimization.
          	fit_y_unc = True,
              # Set a random seed for returning the same batch of functional forms every time (single-threaded), otherwise set None to explore more functions every time.
          	random_seed = None,
              # Custome loss weight to replace y_up and y_down.
          	loss_weights = None
      )

.. container:: cell markdown
   :name: 150c9085-9eea-4fe4-9b3c-3ab1b2d727f9

   .. rubric:: Symbol Fit it!
      :name: symbol-fit-it

.. container:: cell markdown
   :name: 31867aec-575b-40fe-aa4f-7e4b6ebeffc3

   Run the fit: SR fit for functional forms -> parameterization ->
   re-optimization fit for improved best-fits and uncertainty estimation
   -> evaluation.

.. container:: cell code
   :name: 473996da-005b-451c-a452-c1449fa8ca04

   .. code:: python

      model.fit()

.. container:: cell markdown
   :name: b23a91aa-2272-4b6d-8862-f0fa8fc96ae4

   .. rubric:: Save results to output files
      :name: save-results-to-output-files

.. container:: cell markdown
   :name: 75b09236-4174-4e45-812d-5646ee872729

   Save results to csv tables:

   - ``candidates.csv``: saves all candidate functions and evaluations
     in a csv table.
   - ``candidates_reduced.csv``: saves a reduced version for essential
     information without intermediate results.

.. container:: cell code
   :name: 014cd1d2-0b50-431d-9a47-3b356de10d14

   .. code:: python

      model.save_to_csv(output_dir = 'output_dir/')

.. container:: cell markdown
   :name: 645acdb2-bee0-4394-98a5-5bc0d008baba

   Plot results to pdf files:

   - ``candidates.pdf``: plots all candidate functions with associated
     uncertainties one by one for fit quality evaluation.
   - ``candidates_sampling.pdf``: plots all candidate functions with
     total uncertainty coverage generated by sampling parameters.
   - ``candidates_gof.pdf``: plots the goodness-of-fit scores.
   - ``candidates_correlation.pdf``: plots the correlation matrices for
     the parameters of the candidate functions.

.. container:: cell code
   :name: cd1b926b-6942-4e5c-8b32-1570be622800

   .. code:: python

      model.plot_to_pdf(
          	output_dir = 'output_dir/',
          	bin_widths_1d = bin_widths_1d,
          	#bin_edges_2d = bin_edges_2d,
          	plot_logy = False,
          	plot_logx = False,
              sampling_95quantile = False
      )
