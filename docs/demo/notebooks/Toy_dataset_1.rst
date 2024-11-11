.. container:: cell code
   :name: 95ae43f4-d947-4c53-a133-73b163369e3d

   .. code:: python

      x = [12.5, 37.5, 62.5, 87.5, 112.5, 137.5, 162.5, 187.5, 212.5, 237.5, 262.5, 287.5, 312.5, 337.5, 362.5, 387.5, 412.5, 437.5, 462.5, 487.5]
      y = [10.234884262084961, 122.1119384765625, 338.9125061035156, 810.2549438476562, 649.0571899414062, 351.8170166015625, 248.619873046875, 186.88763427734375, 141.754150390625, 103.42931365966797, 78.36450958251953, 60.3994255065918, 49.005863189697266, 33.54744338989258, 27.76025390625, 25.299283981323242, 19.729631423950195, 14.033162117004395, 15.06820011138916, 9.641764640808105]
      y_up = [3.199200566092248, 11.050427072134475, 18.409576478113657, 28.464977495997715, 25.476600831771226, 18.756785881423355, 15.767684454189048, 13.670685216087149, 11.906055198537633, 10.170020337229811, 8.852373104570296, 7.771706730608908, 7.000418786736781, 5.7920154859852175, 5.268800044246317, 5.029839359395411, 4.441804973650936, 3.746086239931536, 3.8817779575072504, 3.105119102515732]
      y_down = [3.199200566092248, 11.050427072134475, 18.409576478113657, 28.464977495997715, 25.476600831771226, 18.756785881423355, 15.767684454189048, 13.670685216087149, 11.906055198537633, 10.170020337229811, 8.852373104570296, 7.771706730608908, 7.000418786736781, 5.7920154859852175, 5.268800044246317, 5.029839359395411, 4.441804973650936, 3.746086239931536, 3.8817779575072504, 3.105119102515732]
      bin_widths_1d = [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]

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

.. container:: cell code
   :name: a61d9307-8b17-42dc-9915-3a4d0f7d1c51

   .. code:: python

      from symbolfit.symbolfit import *

      model = SymbolFit(
          	x = x,
          	y = y,
          	y_up = y_up,
          	y_down = y_down,
          	pysr_config = pysr_config,
          	max_complexity = 60,
          	input_rescale = True,
          	scale_y_by = 'mean',
          	max_stderr = 20,
          	fit_y_unc = True,
          	random_seed = None,
          	loss_weights = None
      )

      model.fit()

.. container:: cell code
   :name: 014cd1d2-0b50-431d-9a47-3b356de10d14

   .. code:: python

      model.save_to_csv(output_dir = 'toy_dataset_1/')

.. container:: cell code
   :name: cd1b926b-6942-4e5c-8b32-1570be622800

   .. code:: python

      model.plot_to_pdf(
          	output_dir = 'toy_dataset_1/',
          	bin_widths_1d = bin_widths_1d,
          	#bin_edges_2d = bin_edges_2d,
          	plot_logy = False,
          	plot_logx = False,
              sampling_95quantile = False
      )

.. container:: cell code
   :name: c243c219-799e-49f2-a6ce-812203375189

   .. code:: python
