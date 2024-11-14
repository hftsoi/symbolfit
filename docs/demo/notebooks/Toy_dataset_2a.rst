.. container:: cell markdown
   :name: 88b4c9b6-6e92-494e-ad97-bfe7aeaaf6c5

   .. rubric:: Toy Dataset 2a
      :name: toy-dataset-2a

.. container:: cell code
   :name: 95ae43f4-d947-4c53-a133-73b163369e3d

   .. code:: python

      x = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
      y = [3.0, 2.2, 2.1, 2.05, 2, 2.1, 2.2, 1.9, 1.6]
      y_up = [0.4, 0.3, 0.2, 0.2, 0.1, 0.05, 0.06, 0.1, 0.1]
      y_down = [0.4, 0.3, 0.2, 0.2, 0.1, 0.05, 0.06, 0.1, 0.1]
      bin_widths_1d = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

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
              max_complexity = 40,
              input_rescale = False,
              scale_y_by = None,
              max_stderr = 20,
              fit_y_unc = True,
              random_seed = seed,
              loss_weights = None
      )

      model.fit()

.. container:: cell code
   :name: 014cd1d2-0b50-431d-9a47-3b356de10d14

   .. code:: python

      model.save_to_csv(output_dir = 'toy_dataset_2a/')

.. container:: cell code
   :name: cd1b926b-6942-4e5c-8b32-1570be622800

   .. code:: python

      model.plot_to_pdf(
          	output_dir = 'toy_dataset_2a/',
          	bin_widths_1d = bin_widths_1d,
          	#bin_edges_2d = bin_edges_2d,
          	plot_logy = False,
          	plot_logx = False,
              sampling_95quantile = False
      )

.. container:: cell code
   :name: c243c219-799e-49f2-a6ce-812203375189

   .. code:: python

.. container:: cell markdown
   :name: 7e41691a-8945-4719-952a-6f35dabc68a8

   .. rubric:: Toy Dataset 2b
      :name: toy-dataset-2b

.. container:: cell code
   :name: f7bbb46c-6d88-4293-8d2a-bc11e2df5201

   .. code:: python

      x=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]

      y=[3, 2.8, 2.7, 2.7, 2.8, 2.6, 2.1, 1.7, 1]

      y_up=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05]

      y_down=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05]

      bin_widths_1d=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

.. container:: cell code
   :name: bd3537de-0f48-4c8c-b3e2-647cc41b0487

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

.. container:: cell code
   :name: 2cf77210-5932-4c6c-8866-1906ac721b43

   .. code:: python

      from symbolfit.symbolfit import *

      model = SymbolFit(
              x = x,
              y = y,
              y_up = y_up,
              y_down = y_down,
              pysr_config = pysr_config,
              max_complexity = 40,
              input_rescale = False,
              scale_y_by = None,
              max_stderr = 20,
              fit_y_unc = True,
              random_seed = seed,
              loss_weights = None
      )

      model.fit()

.. container:: cell code
   :name: 1c6291c9-9faa-439c-af79-eaf81c76b3fd

   .. code:: python

      model.save_to_csv(output_dir = 'toy_dataset_2b/')

.. container:: cell code
   :name: e3813c8b-77c1-4a5c-867d-d91a541568f3

   .. code:: python

      model.plot_to_pdf(
          	output_dir = 'toy_dataset_2b/',
          	bin_widths_1d = bin_widths_1d,
          	#bin_edges_2d = bin_edges_2d,
          	plot_logy = False,
          	plot_logx = False,
              sampling_95quantile = False
      )

.. container:: cell code
   :name: 28e85137-682d-4259-a58d-bcb512d79f94

   .. code:: python

.. container:: cell markdown
   :name: ee5ae7ad-c82d-483e-bf64-bd5b341178ea

   .. rubric:: Toy Dataset 2c
      :name: toy-dataset-2c

.. container:: cell code
   :name: 180f8ec1-4cb9-4014-9979-fa7a57173ca8

   .. code:: python

      x=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 10]

      y=[0.7, 0.95, 1.04, 1.07, 1.065, 1.06, 1.055, 1.04, 1.02, 1, 0.99, 0.98, 0.985, 0.99, 0.995, 0.997, 1, 1, 1]

      y_up=[0.05, 0.03, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.006, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]

      y_down=[0.05, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]

      bin_widths_1d=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.5]

.. container:: cell code
   :name: 6a009058-5384-4988-a12b-d6ac1bf7bd44

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

.. container:: cell code
   :name: 3fc09f89-45a9-43b3-b697-8bc7f642afb3

   .. code:: python

      from symbolfit.symbolfit import *

      model = SymbolFit(
              x = x,
              y = y,
              y_up = y_up,
              y_down = y_down,
              pysr_config = pysr_config,
              max_complexity = 40,
              input_rescale = False,
              scale_y_by = None,
              max_stderr = 20,
              fit_y_unc = True,
              random_seed = seed,
              loss_weights = None
      )

      model.fit()

.. container:: cell code
   :name: 308e679d-3e10-43a8-a018-3243abc4971a

   .. code:: python

      model.save_to_csv(output_dir = 'toy_dataset_2c/')

.. container:: cell code
   :name: f045a847-e5df-4f68-97b0-33e064eaf3bb

   .. code:: python

      model.plot_to_pdf(
          	output_dir = 'toy_dataset_2c/',
          	bin_widths_1d = bin_widths_1d,
          	#bin_edges_2d = bin_edges_2d,
          	plot_logy = False,
          	plot_logx = False,
              sampling_95quantile = False
      )

.. container:: cell code
   :name: 721ed6d7-5692-441d-ad87-d94b09e7f978

   .. code:: python
