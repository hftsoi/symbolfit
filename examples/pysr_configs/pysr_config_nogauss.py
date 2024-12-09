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
    elementwise_loss='loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
