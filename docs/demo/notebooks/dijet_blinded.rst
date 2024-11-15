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

      '''
      CMS search for high-mass dijet resonances at sqrt(s) = 13 TeV
          https://arxiv.org/abs/1911.03947
          https://doi.org/10.1007/JHEP05(2020)033

      Differential dijet spectrum (Figure 5), public data taken from HEPDATA
          https://www.hepdata.net/record/ins1764471
      '''

      x=[1568.5, 1647.0, 1728.5, 1813.0, 1900.5, 1991.0, 2084.5, 2181.5, 2281.5, 2385.0, 2492.0, 2602.5,
      #2717.0, 2835.0, 2957.0, 3083.0, 3213.0, 3347.5, 3487.0,
      3631.0, 3779.0, 3932.0, 4090.5, 4254.0, 4423.0, 4597.5, 4777.5, 4963.5, 5155.5, 5354.0, 5559.0, 5770.0, 5988.0, 6213.5, 6446.0, 6686.0, 6934.0, 7190.0, 7454.5, 7727.5, 8009.0, 8452.0]

      y=[149.27999877929688, 109.44000244140625, 80.0770034790039, 58.715999603271484, 43.082000732421875, 31.559999465942383, 23.219999313354492, 16.982999801635742, 12.36400032043457, 9.121100425720215, 6.679200172424316, 4.889999866485596,
      #3.589400053024292, 2.5933001041412354, 1.902999997138977, 1.3653000593185425, 0.9902999997138977, 0.7092800140380859, 0.5142099857330322,
      0.3630400002002716, 0.26298001408576965, 0.18937000632286072, 0.12946000695228577, 0.08928799629211426, 0.06131099909543991, 0.04499199986457825, 0.03179299831390381, 0.021355999633669853, 0.013650000095367432, 0.009144900366663933, 0.005454500205814838, 0.0038403000216931105, 0.0025553000159561634, 0.0015561999753117561, 0.0010168999433517456, 0.0005365100223571062, 0.00023088000307325274, 0.00022378000721801072, 0.00021629000548273325, 0.0, 7.628699677297845e-05, 1.2120999599574134e-05]

      y_up=[0.11884000152349472, 0.09983699768781662, 0.08385500311851501, 0.07055199891328812, 0.0594169981777668, 0.05002899840474129, 0.042238999158144, 0.03539599850773811, 0.029911000281572342, 0.025085000321269035, 0.021276000887155533, 0.017805000767111778,
      #0.015064000152051449, 0.012597999535501003, 0.010623999871313572, 0.008864900097250938, 0.007441999856382608, 0.006189499981701374, 0.005183400120586157,
      0.004302599932998419, 0.003619600087404251, 0.0030181999318301678, 0.002463799901306629, 0.002022000029683113, 0.0016528000123798847, 0.001401199959218502, 0.001164300017990172, 0.0009455800172872841, 0.0007514799945056438, 0.0006105700158514082, 0.0004726200131699443, 0.0003963200142607093, 0.0003233299939893186, 0.0002555900136940181, 0.00020963999850209802, 0.00015859999984968454, 0.00011385999823687598, 0.00011036000068997964, 0.00010666000162018463, 4.726000042865053e-05, 7.420800102408975e-05, 2.787400080705993e-05]

      y_down=[0.11874999850988388, 0.09974599629640579, 0.08376699686050415, 0.07046700268983841, 0.059335000813007355, 0.049949999898672104, 0.042162999510765076, 0.035321999341249466, 0.02983899973332882, 0.02501700073480606, 0.02120799943804741, 0.017741000279784203,
      #0.015002000145614147, 0.012536999769508839, 0.010564999654889107, 0.008807900361716747, 0.0073866997845470905, 0.006136199925094843, 0.00513189984485507,
      0.0042524999007582664, 0.0035707999486476183, 0.0029712000396102667, 0.002418200019747019, 0.0019777000416070223, 0.0016099000349640846, 0.001359499990940094, 0.0011238999431952834, 0.0009062800090759993, 0.0007132000173442066, 0.0005734399892389774, 0.0004362500039860606, 0.0003607299877330661, 0.00028870999813079834, 0.00022154999896883965, 0.00017612999363336712, 0.00012527000217232853, 7.989699952304363e-05, 7.743899914203212e-05, 7.484800153179094e-05, -0.0, 4.151900066062808e-05, 1.0026999916590285e-05]
       
      bin_widths_1d=[77.0, 80.0, 83.0, 86.0, 89.0, 92.0, 95.0, 99.0, 101.0, 106.0, 108.0, 113.0,
      #116., 120., 124., 128., 132., 137., 142.,
      146.0, 150.0, 156.0, 161.0, 166.0, 172.0, 177.0, 183.0, 189.0, 195.0, 202.0, 208.0, 214.0, 222.0, 229.0, 236.0, 244.0, 252.0, 260.0, 269.0, 277.0, 286.0, 600.0]

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
      plt.savefig('img/dijet_blinded/dataset.png')

   .. container:: output display_data

      |image1|

.. container:: cell markdown
   :name: c86895b5-b140-4714-a3d5-742abf74f011

   This is a steeply falling shape, let's plot in log scale:

.. container:: cell code
   :name: 27b55452-5a5c-4255-8a89-90d556a8e838

   .. code:: python

      fig, axes = plt.subplots(figsize = (6, 4))
      plt.errorbar(np.array(x).flatten(),
                   np.array(y).flatten(),
                   yerr = [np.array(y_down).flatten(), np.array(y_up).flatten()],
                   xerr = np.array(bin_widths_1d)/2,
                   fmt = '.', c = 'black', ecolor = 'grey', capsize = 0,
                  )
      plt.xscale('log')
      plt.yscale('log')
      plt.savefig('img/dijet_blinded/dataset_log.png')

   .. container:: output display_data

      |image2|

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
          	max_complexity = 80,
          
              # Whether to scale input x to be within 0 and 1 for the fits for numerical stability,
              # as large x could lead to overflow when there is e.g. exp(x) -> exp(10000).
              # So set this to False when your x's are or close to O(1), otherwise recommended to set True.
              # After the fits, the functions will be unscaled to relect the original dataset.
          	input_rescale = True,
              # ^ scaling needed here since the input x is O(1000).
          
              # Whether to scale y for the fits for numerical stability,
              # options are (when input_rescale is True): None / 'mean' / 'max' / 'l2'.
              # This is useful to stabilize fits when your y's are very large or very small.
              # After the fits, the functions will be unscaled to relect the original dataset.
          	scale_y_by = None,
              # ^ scaling may or may not be needed here since the input y is widely spreading and not too extreme.
          
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


         Expressions evaluated per second: 6.970e+05
         Head worker occupation: 11.5%
         Progress: 1559 / 3000 total iterations (51.967%)
         ====================================================================================================
         Hall of Fame:
         ---------------------------------------------------------------------------------------------------
         Complexity  Loss       Score     Equation
         1           9.188e-03  1.594e+01  y = -0.079682
         2           2.795e-03  1.190e+00  y = tanh(0.00027823)
         3           2.708e-03  3.133e-02  y = 0.00051651 ^ x₀
         5           1.853e-03  1.899e-01  y = 3.1328e-05 ^ (x₀ + -0.26968)
         7           1.993e-05  2.266e+00  y = 0.00014414 ^ (-0.56768 + (x₀ / 0.35022))
         8           1.323e-05  4.097e-01  y = 0.00014414 ^ ((x₀ / 0.3711) + tanh(-0.63691))
         9           1.164e-05  1.280e-01  y = 0.00014414 ^ ((tanh(x₀) / 0.3711) + tanh(-0.63691))
         10          1.092e-05  6.419e-02  y = (-0.033238 * -0.021517) ^ ((tanh(x₀) / 0.30777) + -0.68422...
                                           )
         11          2.237e-06  1.585e+00  y = 0.00014414 ^ (-0.56768 + ((x₀ / (0.48726 + x₀)) + x₀))
         12          9.479e-07  8.588e-01  y = 0.00014414 ^ (tanh(-0.63691) + (x₀ + (x₀ / (0.49882 + x₀))...
                                           ))
         13          8.195e-07  1.455e-01  y = 0.00014414 ^ (tanh(-0.63691) + (x₀ + (x₀ / (tanh(0.53853) ...
                                           + x₀))))
         14          3.990e-07  7.197e-01  y = (-0.025128 * -0.025128) ^ (x₀ + ((x₀ / tanh(0.38277 + x₀))...
                                            + -0.67808))
         15          3.972e-07  4.649e-03  y = (-0.025128 * tanh(-0.025128)) ^ (x₀ + ((x₀ / tanh(0.38277 ...
                                           + x₀)) + -0.67808))
         16          1.345e-07  1.083e+00  y = (-0.025128 * -0.025128) ^ (x₀ + ((x₀ / tanh(0.38301 + (x₀ ...
                                           * 0.93211))) + -0.67808))
         17          1.306e-07  2.971e-02  y = (-0.025128 * tanh(-0.025128)) ^ (x₀ + ((x₀ / tanh((x₀ * 0....
                                           93211) + 0.38301)) + -0.67808))
         18          5.409e-08  8.812e-01  y = ((-0.025128 * -0.025128) ^ (x₀ + (-0.67808 + (x₀ / tanh(0....
                                           38301 + (0.91588 * x₀)))))) * 1.0085
         19          4.142e-08  2.670e-01  y = (-0.025128 * tanh(-0.025128 * 0.98769)) ^ (x₀ + ((x₀ / tan...
                                           h((x₀ * 0.93211) + 0.38301)) + -0.67808))
         20          3.950e-08  4.758e-02  y = (-0.025128 * (-0.025128 * 0.98769)) ^ (x₀ + ((x₀ / tanh((x...
                                           ₀ * (0.93211 + -0.0064717)) + 0.38301)) + -0.67808))
         22          3.750e-08  2.596e-02  y = (tanh(-0.025128 * -0.025128) ^ (x₀ + (-0.67808 + (x₀ / tan...
                                           h(0.38301 + x₀))))) * ((exp(-0.025128) + x₀) ^ -0.2704)
         47          2.960e-08  9.458e-03  y = tanh(((1.2673 + 1.0353) * x₀) ^ (x₀ * (-0.924 * x₀))) * ((...
                                           ((-0.029311 / exp(0.87704 + -0.039602)) * (exp(1.2637) + (0.67...
                                           826 + x₀))) * -0.035065) ^ ((x₀ / (tanh(0.38379) + tanh(x₀))) ...
                                           + (-0.79093 + ((1.7258 * -0.028759) + (x₀ / tanh(0.68257))))))
         48          2.673e-08  1.021e-01  y = tanh(((1.2673 + 1.0353) * x₀) ^ (x₀ * (-0.924 * x₀))) * ((...
                                           ((-0.029311 / exp(0.87704 + -0.039602)) * (exp(1.2637) + (0.67...
                                           826 + x₀))) * tanh(-0.035065)) ^ ((x₀ / (tanh(0.38379) + tanh(...
                                           x₀))) + (-0.79093 + ((1.7258 * -0.028759) + (x₀ / tanh(0.68257...
                                           ))))))
         ---------------------------------------------------------------------------------------------------
         ====================================================================================================
         Press 'q' and then <enter> to stop execution early.


         Checking if pysr_model_temp.pkl exists...
         Loading model from pysr_model_temp.pkl


         Re-optimizing parameterized candidate function 1/21...
         Re-optimizing parameterized candidate function 2/21...bad fits 2/2...
         Re-optimizing parameterized candidate function 3/21...bad fits 2/2...
         Re-optimizing parameterized candidate function 4/21...bad fits 2/2...
             >>> loop of re-parameterization with less NDF for bad fits 2/4...

         Re-optimizing parameterized candidate function 5/21...
             >>> loop of re-parameterization with less NDF for bad fits 3/4...

         Re-optimizing parameterized candidate function 6/21...
             >>> loop of re-parameterization with less NDF for bad fits 2/8...

         Re-optimizing parameterized candidate function 7/21...
             >>> loop of re-parameterization with less NDF for bad fits 2/8...

         Re-optimizing parameterized candidate function 8/21...
             >>> loop of re-parameterization with less NDF for bad fits 1/8...

         Re-optimizing parameterized candidate function 9/21...
             >>> loop of re-parameterization with less NDF for bad fits 1/8...

         Re-optimizing parameterized candidate function 10/21...
             >>> loop of re-parameterization with less NDF for bad fits 4/16...

         Re-optimizing parameterized candidate function 11/21...
             >>> loop of re-parameterization with less NDF for bad fits 1/8...

         Re-optimizing parameterized candidate function 12/21...
             >>> loop of re-parameterization with less NDF for bad fits 1/8...

         Re-optimizing parameterized candidate function 13/21...
             >>> loop of re-parameterization with less NDF for bad fits 1/16...

         Re-optimizing parameterized candidate function 14/21...
             >>> loop of re-parameterization with less NDF for bad fits 1/16...

         Re-optimizing parameterized candidate function 15/21...
             >>> loop of re-parameterization with less NDF for bad fits 1/16...

         Re-optimizing parameterized candidate function 16/21...
             >>> loop of re-parameterization with less NDF for bad fits 1/16...

         Re-optimizing parameterized candidate function 17/21...
             >>> loop of re-parameterization with less NDF for bad fits 2/16...

         Re-optimizing parameterized candidate function 18/21...
             >>> loop of re-parameterization with less NDF for bad fits 2/16...

         Re-optimizing parameterized candidate function 19/21...
             >>> loop of re-parameterization with less NDF for bad fits 2/16...

         Re-optimizing parameterized candidate function 20/21...
             >>> loop of re-parameterization with less NDF for bad fits 2/16...

         Re-optimizing parameterized candidate function 21/21...
             >>> loop of re-parameterization with less NDF for bad fits 7/32...

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

      model.save_to_csv(output_dir = 'output_dijet_blinded/')

   .. container:: output stream stdout

      ::

         Saving full results >>> output_dijet_blinded/candidates.csv
         Saving reduced results >>> output_dijet_blinded/candidates_reduced.csv

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
          	output_dir = 'output_dijet_blinded/',
          	bin_widths_1d = bin_widths_1d,
          	#bin_edges_2d = bin_edges_2d,
          	plot_logy = True,
          	plot_logx = True,
              sampling_95quantile = False
      )

   .. container:: output stream stdout

      ::

         Plotting candidate functions 21/21 >>> output_dijet_blinded/candidates.pdf
         Plotting candidate functions (sampling parameters) 21/21 >>> output_dijet_blinded/candidates_sampling.pdf
         Plotting correlation matrices 21/21 >>> output_dijet_blinded/candidates_correlation.pdf
         Plotting goodness-of-fit scores >>> output_dijet_blinded/candidates_gof.pdf

.. |image1| image:: 711d7f8bab4e3c71cbd05ce6fdd074aea11be9d9.png
.. |image2| image:: 7069de6c60d16b951623234898db18ed3b202a8e.png
