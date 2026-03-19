# SymbolFit Class

## Arguments

### Dataset

-   `x`: list | ndarray

    *Default: None*

    Independent variable x, or bin center values for histogram data. If provided as a python list, e.g., `[1, 2, 3,...]` for 1D, `[[1, 1], [1, 2], [1, 3],...]` for 2D, `[[1, 1, 1], [1, 1, 2], [1, 1, 3],...]` for 3D etc. If provided as ndarray, then shape is (num_examples, dim).

-   `y`: list | ndarray

    *Default: None*

    Dependent variable y, or bin content values for histogram data.
    Shape is (num_examples, 1).

-   `y_up`: list | ndarray

    *Default: 1*

    Upper one standard deviation of y (+1 sigma). It should be the
    absolute deviation value (not relative) and non-negative. Shape
    is (num_examples, 1).

    If your data has no uncertainty, set both `y_up` and `y_down`
    to `1` (the default) and set `fit_y_unc = False` so all data
    points are weighted equally in the fit.

-   `y_down`: list | ndarray

    *Default: 1*

    Lower one standard deviation of y (-1 sigma). It should be the
    absolute deviation value (not relative) and non-negative. Shape
    is (num_examples, 1).

    Asymmetric uncertainties are supported: the fit automatically
    uses `y_up` when the residual is positive and `y_down` when
    negative.

See [input data format](demo/input.md) for a graphical illustration of
how to prepare `x`, `y`, `y_up`, `y_down`, and bin widths/edges.


### Fit configuration

-   `pysr_config`: pysr.PySRRegressor class

    *Default: built-in config with +, \*, /, ^, exp, tanh, gauss, sin*

    Configuration for the PySR symbolic regression search. This
    controls which mathematical operators are available, how many
    iterations to run, population size, and other search
    hyperparameters. See
    [PySR documentation](https://github.com/MilesCranmer/PySR) for
    all available options.

    The configuration can be stored in a python file like
    pysr_config.py:

    ``` python
    from pysr import PySRRegressor
    pysr_config = PySRRegressor(
        model_selection = 'accuracy',
        niterations = 100,
        maxsize = 50,
        binary_operators = ['+', '*'],
        unary_operators = ['exp', 'tanh'],
        ...
    )
    ```

    and source from there:

    ``` python
    pysr_config = importlib.import_module('directory.pysr_config').pysr_config
    model = SymbolFit(..., pysr_config = pysr_config, ...)
    ```

    !!! tip
        The choice of operators is the most impactful setting. Start
        with operators that match the expected behavior of your data
        (e.g., `exp` for exponential decays, `gauss` for peaked
        distributions). See [PySR config examples](demo/pysr_configs.md)
        for common configurations.

-   `max_complexity`: int

    *Default: 60*

    Maximum complexity of the expression tree. Each operator and
    variable counts toward this budget (e.g., `a1 * exp(a2 * x0)`
    has complexity ~6). Higher values allow more complex functions
    but increase search time and risk overfitting.

    Overwrites the `maxsize` parameter in `PySRRegressor()` if
    provided.

    !!! tip
        Start with 40-60 for most cases. Increase if the search
        consistently returns functions that are too simple to capture
        the data shape. Decrease if functions are overfitting or the
        search is too slow.

-   `input_rescale`: bool

    *Default: True*

    Rescale x to the range (0, 1) before fitting. This prevents
    numerical instability or overflow when x values are very large
    or span many orders of magnitude. All fitted functions are
    automatically unscaled in the output, so the final expressions
    are in terms of the original x.

    !!! tip
        Keep this enabled (True) unless you have a specific reason
        not to. Disabling it can cause fits to fail when x values
        are large.

-   `scale_y_by`: str | None

    *Default: 'mean'*

    Normalize y before fitting.
    Options: `'mean'`, `'max'`, `'l2'`, or `None` (no
    normalization). Like `input_rescale`, the final output functions
    are unscaled back to original units. Only applies when
    `input_rescale` is True.

    !!! tip
        Use `'mean'` for most cases. Set to `None` if others don't
        work well.

-   `max_stderr`: float (%)

    *Default: 20*

    Maximum allowed relative uncertainty (in %) for any single
    parameter during the LMFIT re-optimization stage. If any
    parameter exceeds this threshold, the fit is considered
    unreliable and is retried with fewer free parameters (some are
    held fixed at their initial values from PySR).

    This acts as a quality gate by preventing the final results from
    containing parameters with meaninglessly large uncertainties.

    !!! tip
        Values of 10-40 work well in practice. Lower values are
        stricter (more parameters may be frozen), higher values are
        more permissive. If many of your candidates show frozen
        parameters, try increasing this.

-   `fit_y_unc`: bool

    *Default: True*

    Whether to use `y_up` / `y_down` as weights in the fit loss
    function. When True, the loss is chi2-weighted:
    `(y_pred - y_true)^2 / y_unc^2`, where `y_unc` is taken as
    `y_up` when the residual is positive and `y_down` when
    negative.

    Set to False for an unweighted (least-squares) fit where all
    data points contribute equally, regardless of their
    uncertainties. This is useful when uncertainties are not
    available or not meaningful.

-   `random_seed`: int | None

    *Default: None*

    Set to an integer to make the symbolic regression
    search reproducible. When set, PySR is forced to run in
    single-threaded mode, which makes runs
    slower but guarantees identical results across runs.

    Leave as `None` for the fastest search (multi-threaded, non-
    deterministic). Since the function space is vast, rerunning
    with `random_seed = None` naturally produces different
    candidates each time, which can be useful for exploring the
    solution space.

-   `loss_weights`: list | ndarray | None

    *Default: None*

    Custom per-bin weights for the fit loss. When provided, the
    loss becomes `(y_pred - y_true)^2 * loss_weights` and
    overrides the `y_up` / `y_down` uncertainty weighting.
    Shape is (num_examples, 1).

    This is useful when you want to emphasize certain regions of
    the data (e.g., assign higher weights to a signal region) or
    de-emphasize others.


## Methods

### **fit()**

Performs the full SymbolFit pipeline:

1.  Runs PySR to search for candidate functional forms.
2.  Parameterizes all numerical constants (replaces them with named
    parameters `a1`, `a2`, ...).
3.  Re-optimizes each candidate with LMFIT to refine parameter values
    and provide uncertainty estimation (re-optimization fit, or ROF).


### **save_to_csv()**

Saves all candidate functions and their evaluation metrics to CSV
files.

1.  `candidates.csv`: full results including intermediate fit details,
    parameterization, covariance matrices, and goodness-of-fit metrics.
2.  `candidates_compact.csv`: compact version with only the final
    functions, parameters, and key metrics for quick inspection.

-   `output_dir`: str

    *Default: './'*

    Output directory. Created automatically if it does not exist.

### **plot_to_pdf()**

Generates diagnostic plots for all candidate functions.

1.  `candidates.pdf`: each candidate plotted against the data with
    parameter-by-parameter uncertainty variations, plus residual and
    ratio panels.
2.  `candidates_sampling.pdf`: total uncertainty coverage bands
    generated by Monte Carlo sampling of parameters using their
    covariance matrix (1D only).
3.  `candidates_gof.pdf`: summary of goodness-of-fit metrics (Chi2/NDF,
    RMSE, R2, p-value) across all candidates for comparison.
4.  `candidates_correlation.pdf`: parameter correlation matrices for
    each candidate.

-   `output_dir`: str

    *Default: './'*

    Output directory. Created automatically if it does not exist.

*Options for 1D data*

-   `bin_widths_1d`: list | ndarray

    *Default: None*

    Bin widths corresponding to each x value. When provided, data
    points are plotted as histogram bars instead of scatter points.
    Shape is (num_examples, 1). See [input data format](demo/input.md)
    for a graphical illustration.

-   `plot_logx`: bool

    *Default: False*

    Use logarithmic scale for the x-axis in candidates.pdf.

-   `plot_logy`: bool

    *Default: False*

    Use logarithmic scale for the y-axis in candidates.pdf.

-   `sampling_95quantile`: bool

    *Default: False*

    Whether to include the 95% quantile range (in addition to the
    default 68% range) when plotting total uncertainty coverage in
    candidates_sampling.pdf. Enable this to visualize wider
    uncertainty bands.

*Options for 2D data*

-   `bin_edges_2d`: list

    *Default: None*

    Bin edges for plotting 2D histogram data, provided as a list of
    two sub-lists: `[[x0_0, x0_1, ...], [x1_0, x1_1, ...]]`. The
    leftmost bin in x0 has edges `x0_0` and `x0_1`. `[x0_0,
    x0_1, ...]` has `(num_x0_bins + 1)` elements and
    `[x1_0, x1_1, ...]` has `(num_x1_bins + 1)` elements. This
    must be a python list (not ndarray) since the two sub-lists can
    have different lengths.

-   `plot_logx0`: bool

    *Default: False*

    Use logarithmic scale for the x0-axis in 2D plots.

-   `plot_logx1`: bool

    *Default: False*

    Use logarithmic scale for the x1-axis in 2D plots.

-   `plot_logy`: bool

    *Default: False*

    Use logarithmic scale for the y-axis (color scale) in 2D plots.

-   `cbar_min`: float

    *Default: None*

    Minimum value for the color bar range in 2D plots. If None,
    determined automatically from the data.

-   `cbar_max`: float

    *Default: None*

    Maximum value for the color bar range in 2D plots. If None,
    determined automatically from the data.

-   `cmap`: str

    *Default: None*

    Matplotlib colormap name for 2D plots (e.g., `'viridis'`,
    `'coolwarm'`, `'RdBu_r'`). If None, uses the matplotlib
    default.

### **print_candidate()**

Print candidate functions with fully substituted parameter values
to the terminal.

-   `candidate_number`: int

    *Default: 99*

    Print a specific candidate by its number (as shown in the
    output CSV/PDF), or set to `99` to print all candidates.
