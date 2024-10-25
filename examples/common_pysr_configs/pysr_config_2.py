from pysr import PySRRegressor
import sympy

pysr_config = PySRRegressor(
    model_selection = 'accuracy',
    timeout_in_seconds = 60*100,
    niterations = 200,
    maxsize = 80,
    binary_operators = [
        '+', '*', '/', '^'
                     ],
    unary_operators = [
        'exp',
        'tanh',
    ],
    constraints = {
        '*'    : (12, 12),
        '/'    : (12, 12),
        '^'    : (12, 12),
        'exp'  : 12,
        'tanh' : 12,
    },
    #complexity_of_operators={'exp': 5, 'gauss': 5, '/': 5, 'cond': 5, 'pow': 5},
    nested_constraints = {
        'exp':    {'exp': 0, 'tanh': 0, '*': 2, '/': 1, '^': 1},
        'tanh':   {'exp': 0, 'tanh': 0, '*': 2, '/': 1, '^': 1},
        '*':      {'exp': 1, 'tanh': 1, '*': 2, '/': 1, '^': 1},
        '^':      {'exp': 1, 'tanh': 1, '*': 2, '/': 1, '^': 0},
        '/':      {'exp': 1, 'tanh': 1, '*': 2, '/': 0, '^': 1},
    },
    loss='loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
