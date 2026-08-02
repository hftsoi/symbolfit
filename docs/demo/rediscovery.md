# CMS/ATLAS dijet function rediscovery

This page is the reference setup for the rediscovery study presented in [2607.19750](https://arxiv.org/abs/2607.19750) where SymbolFit rediscovers the "dijet function" and the "UA2 function" from the published CMS and ATLAS Run 2 dijet spectra, given only the data:

```
f_dijet(x) = p0 * (1 - x)^p1 / x^(p2 + p3*ln(x))

f_UA2(x) = p0 * exp(-p2*x - p3*x^2) / x^p1
```

with x = m_jj / sqrt(s), sqrt(s) = 13 TeV.

Below are the two datasets and the exact seven search configurations used, so the fits can be reproduced or adapted easily.

## Data

Both inputs are public spectra from HEPData, fed to SymbolFit as binned data `(x, y, y_up, y_down)`:

**CMS dijet spectrum** (Figure 5 of [1911.03947](https://arxiv.org/abs/1911.03947))

- <https://www.hepdata.net/record/ins1764471>
- Differential spectrum dsigma/dm_jj, 42 bins, m_jj = 1530-8752 GeV
- `y`, `y_up`, `y_down` are taken directly from the HEPData table
- This is the same dataset as in the [CMS dijet demo](dijet.md)

**ATLAS dijet spectrum** (Figure 3a of [1910.08447](https://arxiv.org/abs/1910.08447), inclusive |y*| < 0.6)

- <https://www.hepdata.net/record/ins1759712>
- Observed event counts per bin, 91 bins, m_jj = 1100-8208 GeV
- `y = counts / bin width` (the bin widths vary, so this keeps `y` a smooth function of `x` for the fit; the paper figures multiply back by bin width only for display, to match the event-count convention of the published Figure 3a)
- Since the table provides no uncertainties, `y_up`/`y_down` are assigned as the central 68.27% Poisson intervals of the counts

In both cases the input variable is fed directly as the dimensionless

``` python
x = m_jj / 13000
```

with `input_rescale = False` and `scale_y_by = None`, so that `x0` appearing in the discovered functions is literally x = m_jj / sqrt(s), the same variable the dijet and UA2 functions are written in.

## The seven search configurations

Four free-form configurations (operators combined freely) and three template configurations (a functional template is imposed and the sub-expressions are searched).
`maxsize` is set via SymbolFit's `max_complexity = 40` below.

``` python
from pysr import PySRRegressor, TemplateExpressionSpec
```

### ops-broad

Free-form, operators {+, -, *, /, ^, exp, log, tanh}, the broadest space.

``` python
pysr_config = PySRRegressor(
    model_selection = 'accuracy',
    niterations = 200,
    binary_operators = ['+', '-', '*', '/', '^'],
    unary_operators = ['exp', 'log', 'tanh'],
    nested_constraints = {
        'exp':  {'exp': 0, 'tanh': 0},
        'tanh': {'exp': 0, 'tanh': 0},
        'log':  {'log': 0},
        '^':    {'^': 0},
    },
    elementwise_loss = 'loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
```

### ops-log

Free-form, operators {+, -, *, /, ^, log}.

``` python
pysr_config = PySRRegressor(
    model_selection = 'accuracy',
    niterations = 200,
    binary_operators = ['+', '-', '*', '/', '^'],
    unary_operators = ['log'],
    elementwise_loss = 'loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
```

### ops-log-tight

Same as `ops-log`, with the sizes of the `^` subtrees limited (base subtree up to 5 nodes, exponent subtree up to 8).

``` python
pysr_config = PySRRegressor(
    model_selection = 'accuracy',
    niterations = 200,
    binary_operators = ['+', '-', '*', '/', '^'],
    unary_operators = ['log'],
    constraints = {'^': (5, 8)},
    nested_constraints = {'^': {'^': 0}, 'log': {'log': 0}},
    elementwise_loss = 'loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
```

### ops-minimal

Free-form, operators {-, *, /, ^}, the smallest grammar containing the dijet function.

``` python
pysr_config = PySRRegressor(
    model_selection = 'accuracy',
    niterations = 200,
    binary_operators = ['-', '*', '/', '^'],
    nested_constraints = {'^': {'^': 0}},
    elementwise_loss = 'loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
```

### tpl-exp-x

Template f = exp(h(x)), with the sub-expression `h` built from {+, -, *, log}.

``` python
expression_spec = TemplateExpressionSpec(
    'exp(h(x))',
    expressions = ['h'],
    variable_names = ['x'],
)

pysr_config = PySRRegressor(
    expression_spec = expression_spec,
    model_selection = 'accuracy',
    niterations = 100,
    binary_operators = ['+', '-', '*'],
    unary_operators = ['log'],
    nested_constraints = {'log': {'log': 0}},
    elementwise_loss = 'loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
```

### tpl-pow-log

Template f = f1(x) ^ h(log x), with `f1` and `h` built from {+, -, *}.

``` python
expression_spec = TemplateExpressionSpec(
    'f1(x) ^ h(log(x))',
    expressions = ['f1', 'h'],
    variable_names = ['x'],
)

pysr_config = PySRRegressor(
    expression_spec = expression_spec,
    model_selection = 'accuracy',
    niterations = 100,
    binary_operators = ['+', '-', '*'],
    elementwise_loss = 'loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
```

!!! note
    The template sub-expressions are named `f1`/`h` rather than `f`/`g` to avoid name clashes in expression parsing.

### tpl-exp-log

Template f = exp(h(log x, log(1-x))), with `h` built from {+, -, *}. In these variables the dijet function is a low-order polynomial.

``` python
expression_spec = TemplateExpressionSpec(
    'exp(h(log(x), log(1 - x)))',
    expressions = ['h'],
    variable_names = ['x'],
)

pysr_config = PySRRegressor(
    expression_spec = expression_spec,
    model_selection = 'accuracy',
    niterations = 100,
    binary_operators = ['+', '-', '*'],
    elementwise_loss = 'loss(y, y_pred, weights) = (y - y_pred)^2 * weights',
)
```

## The SymbolFit call

Every configuration uses the same SymbolFit settings, and each is run 40 times per dataset with random seeds 0-39 (7 x 40 x 2 = 560 independent seeded runs in total):

``` python
from symbolfit.symbolfit import SymbolFit

model = SymbolFit(
    x = x,                    # m_jj / 13000
    y = y,
    y_up = y_up,              # central 68.27% Poisson intervals
    y_down = y_down,
    pysr_config = pysr_config,
    max_complexity = 40,
    input_rescale = False,
    scale_y_by = None,
    fit_y_unc = True,
    loss_weights = None,
    max_stderr = 20,
    random_seed = seed,       # 0, 1, ..., 39
)

model.fit()

model.save_to_csv(output_dir = 'output/')

model.plot_to_pdf(
    output_dir = 'output/',
    bin_widths_1d = bin_widths,   # in the same convention as x, i.e., width in GeV / 13000
    plot_logy = True,
    plot_logx = True,
)
```

Each seeded run is an independent, reproducible draw from the function space and returns tens of candidate functions, and rerunning with a new seed is the intended way to obtain fresh candidates.
See the paper for how candidates are checked for algebraic equivalence to the dijet/UA2 function families and for all results.
