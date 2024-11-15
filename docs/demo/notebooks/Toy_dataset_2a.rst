.. container:: cell code
   :name: 2eb555c2-8163-4fe3-8546-3454b651e865

   .. code:: python

      from symbolfit.symbolfit import *

   .. container:: output stream stdout

      ::

         Detected IPython. Loading juliacall extension. See https://juliapy.github.io/PythonCall.jl/stable/compat/#IPython

.. container:: cell markdown
   :name: 66906c16-9eb8-43ff-aa4d-29a5ea50d033

   .. rubric:: Dataset
      :name: dataset

.. container:: cell markdown
   :name: 1bbc1b76-6d40-48d4-9dde-6cb56052d1e0

   Five inputs are needed, which can be python lists or numpy arrays
   (more options will be added in future!):

   #. ``x``: independent variable (bin center location).
   #. ``y``: dependent variable.
   #. ``y_up``: upward uncertainty in y per bin.
   #. ``y_down``: downward uncertainty in y per bin.
   #. ``bin_widths_1d`` bin widths in x.

   - Elements in both y_up and y_down should be non-negative values.
   - These values are the "delta" in y,

     - y + y_up = y shifted up by one standard deviation.
     - y - y_down = y shifted down by one standard deviation.

   - If no uncertainty in the dataset, one can set both y_up and y_down
     to ones with the same shape as x.

.. container:: cell code
   :name: 95ae43f4-d947-4c53-a133-73b163369e3d

   .. code:: python

      x = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
      y = [3.0, 2.2, 2.1, 2.05, 2, 2.1, 2.2, 1.9, 1.6]
      y_up = [0.4, 0.3, 0.2, 0.2, 0.1, 0.05, 0.06, 0.1, 0.1]
      y_down = [0.4, 0.3, 0.2, 0.2, 0.1, 0.05, 0.06, 0.1, 0.1]
      bin_widths_1d = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

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
      plt.savefig('img/toy2a/dataset.png')

   .. container:: output display_data

      |image1|

.. container:: cell markdown
   :name: 8c27af64-6c06-40b7-97ca-8b55d8fab279

   .. rubric:: Configure the fit
      :name: configure-the-fit

.. container:: cell markdown
   :name: 28c4e18d-adc4-4f41-bace-96138f09a128

   Configure PySR to define the function space being searched for with
   symbolic regression:

.. container:: cell code
   :name: f3415459-b989-4cbe-8472-3fe2ae77f9be

   .. code:: python

      from pysr import PySRRegressor

      pysr_config = PySRRegressor(
          model_selection = 'accuracy',
          niterations = 200,
          maxsize = 80,
          binary_operators = [
              '+', '*', '/', '^'
                           ],
          unary_operators = [
              'exp',
              'tanh',
          ],
          nested_constraints = {
              'exp':    {'exp': 0, 'tanh': 0, '*': 2, '/': 1, '^': 1},
              'tanh':   {'exp': 0, 'tanh': 0, '*': 2, '/': 1, '^': 1},
              '*':      {'exp': 1, 'tanh': 1, '*': 2, '/': 1, '^': 1},
              '^':      {'exp': 1, 'tanh': 1, '*': 2, '/': 1, '^': 0},
              '/':      {'exp': 1, 'tanh': 1, '*': 2, '/': 0, '^': 1},
          },
          loss='loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
      )

.. container:: cell markdown
   :name: ed837443-a0fc-4227-9ea9-350c898a96b2

   Here, we allow four binary operators (+, \*, /, pow) and two unary
   operators (exp, tanh) when searching for functional forms. The
   custom-defined gauss in the previous example may not be needed here
   since it this dataset is not obvious with a peak.

   Nested constraints are imposed to prohibit, e.g., exp(exp(x))...

   Loss function is a weighted MSE, where the weight is the sqaured
   uncertainty by default in SymbolFit.

   For PySR options, please see:

   - https://github.com/MilesCranmer/PySR
   - https://astroautomata.com/PySR/

.. container:: cell markdown
   :name: c904493f-a36c-4b84-bc09-5fdad6e0f6d3

   Configure SymbolFit with the PySR config and for the re-optimization
   process:

.. container:: cell code
   :name: a61d9307-8b17-42dc-9915-3a4d0f7d1c51

   .. code:: python

      model = SymbolFit(
              # Dataset: x, y, y_up, y_down.
          	x = x,
          	y = y,
          	y_up = y_up,
          	y_down = y_down,
          
              # PySR configuration of the function space.
          	pysr_config = pysr_config,
          
              # Constrain the maximum function size and over-write maxsize in pysr_config.
              # Set a higher value for more complex shape, or when the lower one does not fit well.
          	max_complexity = 30,
          
              # Whether to scale input x to be within 0 and 1 for the fits for numerical stability,
              # as large x could lead to overflow when there is e.g. exp(x) -> exp(10000).
              # So set this to False when your x's are or close to O(1), otherwise recommended to set True.
              # After the fits, the functions will be unscaled to relect the original dataset.
          	input_rescale = False,
              # ^ no scaling needed here since the input x is O(1).
          
              # Whether to scale y for the fits for numerical stability,
              # options are (when input_rescale is True): None / 'mean' / 'max' / 'l2'.
              # This is useful to stabilize fits when your y's are very large or very small.
              # After the fits, the functions will be unscaled to relect the original dataset.
          	scale_y_by = None,
              # ^ no scaling needed here since the input y is O(1).
          
              # Set a maximum standard error (%) for all parameters to avoid bad fits during re-optimization.
              # In the refit loop, when any of the parameters returns a standard error larger than max_stderr,
              # the fit is considered failed, and the fit will retry itself for fewer or other combination of varying parameters,
              # by freezing some of the parameters to their initial values and kept fixed during re-optimization.
              # This is to avoid bad fits when the objective is too complex to minimize, which could cause some parameters
              # to have unrealistically large standard errors.
              # In most cases 10 < max_stderr < 100 suffices.
          	max_stderr = 20,
          
              # Consider y_up and y_down to weight the MSE loss during SR search and re-optimization.
          	fit_y_unc = True,
          
              # Set a random seed for returning the same batch of functional forms every time (single-threaded),
              # otherwise set None to explore more functions every time (multi-threaded and faster).
              # In most cases the function space is huge, one can retry the fits with the exact same fit configuration
              # and get completely different sets of candidate functions, merely by using different random seeds.
              # So if the candidate functions are not satisfactory this time, rerun it few times more with
              # random_seed = None or a different seed each time.
          	random_seed = None,
          
              # Custome loss weight to set "(y - y_pred)^2 * loss_weights", overwriting that with y_up and y_down.
          	loss_weights = None
      )

.. container:: cell markdown
   :name: 150c9085-9eea-4fe4-9b3c-3ab1b2d727f9

   .. rubric:: Symbol Fit it!
      :name: symbol-fit-it

.. container:: cell markdown
   :name: 31867aec-575b-40fe-aa4f-7e4b6ebeffc3

   Run the fits: SR fit for functional form searching ->
   parameterization -> re-optimization fit for improved best-fits and
   uncertainty estimation -> evaluation.

.. container:: cell code
   :name: 473996da-005b-451c-a452-c1449fa8ca04

   .. code:: python

      model.fit()

   .. container:: output stream stdout

      ::

         Compiling Julia backend...

   .. container:: output stream stderr

      ::

         [ Info: Started!

   .. container:: output stream stdout

      ::


         Expressions evaluated per second: 7.180e+05
         Head worker occupation: 16.4%
         Progress: 1457 / 3000 total iterations (48.567%)
         ====================================================================================================
         Hall of Fame:
         ---------------------------------------------------------------------------------------------------
         Complexity  Loss       Score     Equation
         1           1.752e-01  1.594e+01  y = 1.68
         2           3.437e-02  1.629e+00  y = exp(0.72041)
         5           2.267e-02  1.387e-01  y = (-0.15192 * x₀) + 2.5457
         6           1.478e-02  4.280e-01  y = 2.2524 + (exp(x₀) * -0.0061958)
         7           1.043e-02  3.484e-01  y = (-0.00062681 * (x₀ ^ x₀)) + 2.1433
         8           1.021e-02  2.138e-02  y = (-5.2253e-07 * (exp(x₀) ^ 3.0764)) + 2.1265
         10          1.016e-02  2.503e-03  y = tanh(-2.9879e-05 * ((x₀ + x₀) ^ x₀)) + 2.1267
         11          7.875e-03  2.548e-01  y = (2.1336 + (-0.00061524 * (x₀ ^ x₀))) + (0.13061 ^ x₀)
         12          7.452e-03  5.516e-02  y = (2.1165 + (-5.0177e-07 * (exp(x₀) ^ 3.0805))) + (0.15228 ^...
                                            x₀)
         13          6.008e-03  2.153e-01  y = (2.1336 + (-0.00061524 * (x₀ ^ x₀))) + ((0.013848 ^ x₀) / ...
                                           0.13724)
         14          5.845e-03  2.759e-02  y = ((-5.0177e-07 * (exp(x₀) ^ 3.0805)) + 2.1165) + ((0.14706 ...
                                           ^ x₀) / x₀)
         15          5.702e-03  2.468e-02  y = ((0.47413 / x₀) ^ 3.1654) + ((-3.4388e-07 * (exp(x₀) ^ 3.1...
                                           654)) + exp(0.74782))
         16          5.567e-03  2.404e-02  y = ((0.45735 / x₀) ^ exp(x₀)) + ((-3.445e-07 * (exp(x₀) ^ 3.1...
                                           654)) + exp(0.75035))
         17          5.551e-03  2.948e-03  y = ((0.45735 / x₀) ^ (3.172 * x₀)) + (((exp(x₀) ^ 3.172) * -3...
                                           .3335e-07) + exp(0.75035))
         18          5.549e-03  3.421e-04  y = ((0.42627 / x₀) ^ (exp(x₀) * x₀)) + (exp(0.75035) + (-3.44...
                                           5e-07 * (exp(x₀) ^ 3.1654)))
         19          3.413e-03  4.859e-01  y = ((x₀ ^ 0.40686) + (exp((0.47803 / x₀) ^ x₀) + ((exp(x₀) ^ ...
                                           1.8685) * -0.00019322))) + -0.39961
         21          3.393e-03  2.935e-03  y = (-0.045569 + ((x₀ ^ 0.38808) + (exp((0.46993 / x₀) ^ x₀) +...
                                            ((exp(x₀) ^ 1.8773) * -0.00017942)))) + -0.32154
         22          3.382e-03  3.239e-03  y = ((x₀ ^ 0.40686) + (exp((0.47803 / (x₀ * 0.95372)) ^ x₀) + ...
                                           ((exp(x₀) ^ 1.8685) * tanh(-0.00019322)))) + -0.39961
         23          3.249e-03  4.024e-02  y = -0.33587 + ((x₀ ^ 0.37768) + (((exp(x₀) ^ 1.7986) * -0.000...
                                           25789) + exp(0.95391 / (x₀ + (x₀ ^ (x₀ + x₀))))))
         24          2.757e-03  1.643e-01  y = (-0.33118 + (((exp(0.41338 ^ x₀) + (exp(x₀) * -0.029169)) ...
                                           + (x₀ ^ tanh(-0.54561))) + (x₀ * (0.14758 * x₀)))) + 0.045004
         26          2.748e-03  1.661e-03  y = (-0.33118 + (((x₀ ^ tanh(-0.54561)) + (exp(0.41338 ^ x₀) +...
                                            (exp(x₀) * -0.029169))) + (x₀ * (0.14758 * x₀)))) + (0.045004...
                                            * 1.1576)
         28          2.735e-03  2.299e-03  y = ((((exp(x₀) * -0.029169) + (exp(0.41338 ^ x₀) + 0.20771)) ...
                                           + ((x₀ ^ -0.54561) + (-0.12587 / tanh(x₀)))) + (x₀ * (x₀ * 0.1...
                                           4758))) + -0.33118
         29          2.725e-03  3.784e-03  y = -0.40398 + (((exp((0.39274 + 0.36498) / (x₀ + (x₀ ^ -0.497...
                                           47))) + (exp(x₀) * -0.029507)) + ((x₀ * 0.84467) ^ -0.75566)) ...
                                           + ((x₀ * 0.15314) * x₀))
         30          2.622e-03  3.847e-02  y = -0.3954 + ((((exp(x₀) * -0.028641) + exp(0.38721 / (x₀ ^ x...
                                           ₀))) + ((tanh(x₀ ^ x₀) / x₀) + 0.36897)) + ((x₀ * (x₀ * 0.1544...
                                           )) ^ 0.94872))
         ---------------------------------------------------------------------------------------------------
         ====================================================================================================
         Press 'q' and then <enter> to stop execution early.


         Checking if pysr_model_temp.pkl exists...
         Loading model from pysr_model_temp.pkl


         Re-optimizing parameterized candidate function 1/22...
             >>> loop of re-parameterization with less NDF for bad fits 1/2...

         Re-optimizing parameterized candidate function 2/22...
             >>> loop of re-parameterization with less NDF for bad fits 1/2...

         Re-optimizing parameterized candidate function 3/22...
             >>> loop of re-parameterization with less NDF for bad fits 1/2...

         Re-optimizing parameterized candidate function 4/22...
             >>> loop of re-parameterization with less NDF for bad fits 2/4...

         Re-optimizing parameterized candidate function 5/22...
             >>> loop of re-parameterization with less NDF for bad fits 2/4...

         Re-optimizing parameterized candidate function 6/22...
             >>> loop of re-parameterization with less NDF for bad fits 2/4...

         Re-optimizing parameterized candidate function 7/22...
             >>> loop of re-parameterization with less NDF for bad fits 2/8...

         Re-optimizing parameterized candidate function 8/22...
             >>> loop of re-parameterization with less NDF for bad fits 4/8...

         Re-optimizing parameterized candidate function 9/22...
             >>> loop of re-parameterization with less NDF for bad fits 5/8...

         Re-optimizing parameterized candidate function 10/22...
             >>> loop of re-parameterization with less NDF for bad fits 5/8...

         Re-optimizing parameterized candidate function 11/22...
             >>> loop of re-parameterization with less NDF for bad fits 10/16...

         Re-optimizing parameterized candidate function 12/22...
             >>> loop of re-parameterization with less NDF for bad fits 6/16...

         Re-optimizing parameterized candidate function 13/22...
             >>> loop of re-parameterization with less NDF for bad fits 6/16...

         Re-optimizing parameterized candidate function 14/22...
             >>> loop of re-parameterization with less NDF for bad fits 6/16...

         Re-optimizing parameterized candidate function 15/22...
             >>> loop of re-parameterization with less NDF for bad fits 1/8...

         Re-optimizing parameterized candidate function 16/22...
             >>> loop of re-parameterization with less NDF for bad fits 1/8...

         Re-optimizing parameterized candidate function 17/22...
             >>> loop of re-parameterization with less NDF for bad fits 5/16...

         Re-optimizing parameterized candidate function 18/22...
             >>> loop of re-parameterization with less NDF for bad fits 4/16...

         Re-optimizing parameterized candidate function 19/22...
             >>> loop of re-parameterization with less NDF for bad fits 7/32...

         Re-optimizing parameterized candidate function 20/22...
             >>> loop of re-parameterization with less NDF for bad fits 2/32...

         Re-optimizing parameterized candidate function 21/22...
             >>> loop of re-parameterization with less NDF for bad fits 3/32...

         Re-optimizing parameterized candidate function 22/22...
             >>> loop of re-parameterization with less NDF for bad fits 2/32...

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

      model.save_to_csv(output_dir = 'output_Toy_dataset_2a/')

   .. container:: output stream stdout

      ::

         Saving full results >>> output_Toy_dataset_2a/candidates.csv
         Saving reduced results >>> output_Toy_dataset_2a/candidates_reduced.csv

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
          	output_dir = 'output_Toy_dataset_2a/',
          	bin_widths_1d = bin_widths_1d,
          	#bin_edges_2d = bin_edges_2d,
          	plot_logy = False,
          	plot_logx = False,
              sampling_95quantile = False
      )

   .. container:: output stream stdout

      ::

         Plotting candidate functions 22/22 >>> output_Toy_dataset_2a/candidates.pdf
         Plotting candidate functions (sampling parameters) 22/22 >>> output_Toy_dataset_2a/candidates_sampling.pdf
         Plotting correlation matrices 22/22 >>> output_Toy_dataset_2a/candidates_correlation.pdf
         Plotting goodness-of-fit scores >>> output_Toy_dataset_2a/candidates_gof.pdf

   .. container:: output display_data

      |image2|

   .. container:: output display_data

      |image3|

.. |image1| image:: e6e56eda00bda12cab731ff0e596d902fa356e93.png
.. |image2| image:: 8a12a1a1aea33d523e912e1e5283638af776e72e.png
.. |image3| image:: 8a12a1a1aea33d523e912e1e5283638af776e72e.png
