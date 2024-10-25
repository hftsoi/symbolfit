from pysr import PySRRegressor
import sympy

pysr_config = PySRRegressor(
    model_selection = 'accuracy',
    timeout_in_seconds = 60*100,
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
    constraints = {
        #'*'    : (6, 6),
        #'tanh' : 6,
        #'exp'  : 6,
        #'gauss': 6,
    },
    #complexity_of_operators={'exp': 5, 'gauss': 5, '/': 5, 'cond': 5, 'pow': 5},
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
