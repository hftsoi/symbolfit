.. container:: cell code
   :name: 95ae43f4-d947-4c53-a133-73b163369e3d

   .. code:: python

      '''
      CMS search for high-mass dimuon resonance produced in association with b quark jets at sqrt(s) = 13 TeV
          https://arxiv.org/abs/2307.08708
          https://doi.org/10.1007/JHEP10(2023)043

      Invariant mass spectra of dimuon events in the N_b = 1 category (Figure 4 left), public data taken from HEPDATA
          https://www.hepdata.net/record/ins2678141
      '''

      x=[397.4, 408.2, 419.0, 429.8, 440.6, 451.4, 462.2, 473.0, 483.8, 494.6, 505.4, 516.2, 527.0, 537.8, 548.6, 559.4, 570.2, 581.0, 591.8, 602.6]

      y=[10.0, 7.0, 8.0, 10.0, 9.0, 7.0, 3.0, 1.0, 8.0, 5.0, 7.0, 3.0, 2.0, 1.0, 6.0, 2.0, 6.0, 2.0, 4.0, 3.0]

      y_up=[4.267, 3.7704, 3.9452, 4.267, 4.1103, 3.7704, 2.9182, 2.2996, 3.9452, 3.3825, 3.7704, 2.9182, 2.6379, 2.2996, 3.5837, 2.6379, 3.5837, 2.6379, 3.1628, 2.9182]

      y_down=[3.1087, 2.5815, 2.7684, 3.1087, 2.9435, 2.5815, 1.6327, 0.82725, 2.7684, 2.1597, 2.5815, 1.6327, 1.2918, 0.82725, 2.38, 1.2918, 2.38, 1.2918, 1.9144, 1.6327]
       
      bin_widths_1d=[10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8]

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
              max_complexity = 10,
              input_rescale = True,
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

      model.save_to_csv(output_dir = 'dimuon/')

.. container:: cell code
   :name: cd1b926b-6942-4e5c-8b32-1570be622800

   .. code:: python

      model.plot_to_pdf(
          	output_dir = 'dimuon/',
          	bin_widths_1d = bin_widths_1d,
          	#bin_edges_2d = bin_edges_2d,
          	plot_logy = False,
          	plot_logx = False,
              sampling_95quantile = False
      )

.. container:: cell code
   :name: c243c219-799e-49f2-a6ce-812203375189

   .. code:: python
