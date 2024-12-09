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
