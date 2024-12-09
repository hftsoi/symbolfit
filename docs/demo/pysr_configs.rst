Common PySR configurations
===========================

To define the function space being searched by PySR, one can check out the PySR documentation `here <https://astroautomata.com/PySR/#detailed-example>`_ for full descriptions of all options.

Since symbolic regression is highly flexible and PySR is highly configurable, a few common configurations can be used to fit many different distribution shapes.
An example is shown below:

.. code-block:: python

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
      elementwise_loss='loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
  )

This configuration works well in many cases where there is a peak in the distribution, as a custom-defined ``gauss`` operator is allowed to appear in the candidate functions.
For instance, this single configuration can be used to fit Toy Dataset 1 (1D) and Toy Datasets 3a, 3b, and 3c (2D).

If the distribution does not contain shape peaks, you can use the following example template:

.. code-block:: python

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
      elementwise_loss='loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
  )

For example, this single configuration is used to fit Toy Dataset 2a, 2b, and 2c, as well as all five LHC datasets (dijet, trijet, paired-dijet, diphoton, and dimuon), using different ``maxsize`` values.

In practice, these two configurations work for many distribution shapes due to the large function spaces they define.
However, users can still fine-tune and explore additional options as needed.

Additionally, the flexibility extends to cases where the current fit does not yield satisfactory functions.
In such scenarios, one can repeat the fit using the exact same configuration but with a different random seed to obtain new batches of candidate functions.
