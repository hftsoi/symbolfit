from pysr import PySRRegressor, TemplateExpressionSpec

expression_spec = TemplateExpressionSpec(
    'p[1] * f(x/13000) ^ g(log(x/13000))',
    expressions = ['f', 'g'],
    variable_names = ['x'],
    parameters = {'p': 1}
)

pysr_config = PySRRegressor(
    expression_spec = expression_spec,
    model_selection = 'accuracy',
    niterations = 200,
    maxsize = 40,
    binary_operators = ['+', '*'],
    elementwise_loss='loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
