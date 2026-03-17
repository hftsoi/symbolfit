# Common PySR configurations

To define the function space being searched by PySR, check out the PySR documentation [here](https://ai.damtp.cam.ac.uk/pysr) for full descriptions of all options.
Since symbolic regression is highly flexible and PySR is highly configurable, a few common configurations can be used to fit many different distribution shapes.
An example is shown below:

``` python
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
```

This example configuration is used to fit Toy Dataset 2a, 2b, and 2c, as well as all five LHC datasets (dijet, trijet, paired-dijet, diphoton, and dimuon), using different `maxsize` values.

## Custom operators

To define custom operators such as a gaussian, sympy mappings can be used:

``` python
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
```

This configuration works well in many cases where there is a peak in the distribution, as a custom-defined `gauss` operator is allowed to appear in the candidate functions.
For instance, this example configuration can be used to fit Toy Dataset 1 (1D) and Toy Datasets 3a, 3b, and 3c (2D).

Additionally, one can repeat the fit using the exact same configuration but with a different random seed to obtain new batches of candidate functions if the current one is not satisfactory.

## User-defined functional templates

A functional form can be fixed by using the PySR's TemplateExpressionSpec API (supported in symbolfit since [v0.2.0](https://github.com/hftsoi/symbolfit/releases/tag/v0.2.0)), like forcing a form `p * f(x) ^ g(log(x))` and searching for the sub-expressions `f` and `g` and the parameter `p`. 
If the allowed operators are `+` and `*`, then `f(x)` will be a polynomial in `x` and `g(log(x))` will be a polynomial in `log(x)`.

```python
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
```

See `CMS dijet dataset (template spec)` for an example fit.

## Lower level constraints

One can further constrain the function space at a lower level by defining a more custom loss function in Julia (use these with caution as it may slow down the fit or even break some of the PySR functionalities, see [here](https://ai.damtp.cam.ac.uk/pysr/v1.5.9/examples#_9-custom-objectives) for PySR docs).
Also note that these constraints apply to the stage of PySR's equation search and is before the LMFIT re-optimization stage which can later correct the constrained behaviors if they were set not so compatible to the data (e.g., if all data points are positive and you added a penalty to encourage negative functions, then LMFIT can correct those by flipping the signs of multiplicative constants etc.).

### Monotonicity

For example, a penalty term can be added for positive derivative so that monotonically decreasing functions are more preferred. 

```python
from pysr import PySRRegressor
from pysr import jl

jl.seval('import Pkg; Pkg.add("Zygote")')
jl.seval('import Zygote')

pysr_config = PySRRegressor(
    model_selection='accuracy',
    niterations=80,
    maxsize=60,
    binary_operators=[
        '+', '*', '/', '^'
    ],
    nested_constraints={
        '*':    {'*': 2, '/': 1, '^': 1},
        '^':    {'*': 2, '/': 1, '^': 0},
        '/':    {'*': 2, '/': 0, '^': 1},
    },
    loss_function="""
    function eval_loss(tree, dataset::Dataset{T,L}, options)::L where {T,L}
        prediction, gradient, flag = eval_grad_tree_array(tree, dataset.X, options; variable=true)
        if !flag
            return L(Inf)
        end

        # Monotonicity penalty: penalize positive df/dx1
        mono_penalty = sum(
            gi -> gi > zero(gi) ? abs2(gi) : zero(L),
            view(gradient, 1, :);
            init=L(0)
        )

        # Weighted MSE
        mse = sum(
            i -> abs2(prediction[i] - dataset.y[i]) * dataset.weights[i],
            eachindex(prediction);
            init=L(0)
        )

        return mse / dataset.n + L(10000) * mono_penalty / dataset.n
    end
    """,
)
```

### Asymptotic behavior

Likewise, the asymptotic behavior of the functions can be constrained, such as sending `f->0` at large `x`, via a penalty term.

```python
from pysr import PySRRegressor

pysr_config = PySRRegressor(
    model_selection='accuracy',
    niterations=80,
    maxsize=60,
    binary_operators=[
        '+', '*', '/', '^'
    ],
    nested_constraints={
        '*':    {'*': 2, '/': 1, '^': 1},
        '^':    {'*': 2, '/': 1, '^': 0},
        '/':    {'*': 2, '/': 0, '^': 1},
    },
    loss_function="""
    function eval_loss(tree, dataset::Dataset{T,L}, options)::L where {T,L}
        prediction, flag = eval_tree_array(tree, dataset.X, options)
        if !flag
            return L(Inf)
        end

        # Weighted MSE
        mse = sum(
            i -> abs2(prediction[i] - dataset.y[i]) * dataset.weights[i],
            eachindex(prediction);
            init=L(0)
        ) / dataset.n

        # Evaluate at large x values to check asymptotic behavior
        n_features = size(dataset.X, 1)
        x_test = zeros(T, n_features, 2)
        x_test[1, :] .= T[10000.0, 20000.0]

        pred_asym, flag2 = eval_tree_array(tree, x_test, options)
        if !flag2
            return L(Inf)
        end

        # Penalize non-zero predictions at large x
        asym_penalty = sum(
            gi -> abs2(gi),
            pred_asym;
            init=L(0)
        ) / 2

        return mse + L(10000) * asym_penalty
    end
    """,
)
```

### Positive/Negative definite

One can also penalize negative/positive function values so that `f(x)>0`/`f(x)<0` is more preferred.

```python
from pysr import PySRRegressor

pysr_config = PySRRegressor(
    model_selection='accuracy',
    niterations=80,
    maxsize=60,
    binary_operators=[
        '+', '*', '/', '^'
    ],
    nested_constraints={
        '*':    {'*': 2, '/': 1, '^': 1},
        '^':    {'*': 2, '/': 1, '^': 0},
        '/':    {'*': 2, '/': 0, '^': 1},
    },
    loss_function="""
    function eval_loss(tree, dataset::Dataset{T,L}, options)::L where {T,L}
        prediction, flag = eval_tree_array(tree, dataset.X, options)
        if !flag
            return L(Inf)
        end

        # Weighted MSE
        mse = sum(
            i -> abs2(prediction[i] - dataset.y[i]) * dataset.weights[i],
            eachindex(prediction);
            init=L(0)
        ) / dataset.n

        # Penalize negative predictions: squared negative part
        neg_penalty = sum(
            pi -> pi < zero(pi) ? abs2(pi) : zero(L),
            prediction;
            init=L(0)
        ) / dataset.n

        return mse + L(10000) * neg_penalty
    end
    """,
)
```
