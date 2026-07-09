import os
import shutil
import warnings
from itertools import combinations

from lmfit import Minimizer, Parameters

from .evaluate import *
from .math_defs import *
from .plotting import *
from .processing import *
from .utils import *

warnings.filterwarnings("ignore")


class SymbolFit:
    """
    Fits a dataset with symbolic regression and provides parameter
    uncertainty estimation for the fitted functions.

    See [input data format](demo/input.md) for a graphical illustration of
    how to prepare `x`, `y`, `y_up`, `y_down`, and bin widths/edges.

    Parameters
    ----------
    x : list | ndarray
        Independent variable x, or bin center values for histogram data.
        If provided as a python list, e.g., `[1, 2, 3,...]` for 1D,
        `[[1, 1], [1, 2], [1, 3],...]` for 2D,
        `[[1, 1, 1], [1, 1, 2], [1, 1, 3],...]` for 3D etc.
        If provided as ndarray, then shape is (num_examples, dim).

    y : list | ndarray
        Dependent variable y, or bin content values for histogram data.
        Shape is (num_examples, 1).

    y_up : list | ndarray
        Upper one standard deviation of y (+1 sigma).
        It should be the absolute deviation value (not relative) and non-negative.
        Shape is (num_examples, 1).

        If your data has no uncertainty, set both `y_up` and `y_down` to `1`
        (the default) and set `fit_y_unc = False` so all data points are
        weighted equally in the fit.

    y_down : list | ndarray
        Lower one standard deviation of y (-1 sigma).
        It should be the absolute deviation value (not relative) and non-negative.
        Shape is (num_examples, 1).

        Asymmetric uncertainties are supported: the re-optimization fit
        (LMFIT stage) automatically uses `y_up` when the residual is positive
        and `y_down` when negative. The initial PySR search stage weights
        symmetrically by `1 / y_up^2` (using `y_down` where `y_up` is 0).

    pysr_config : pysr.PySRRegressor
        Configuration for the PySR symbolic regression search.
        This controls which mathematical operators are available, how many
        iterations to run, population size, and other search hyperparameters.
        See [PySR documentation](https://github.com/MilesCranmer/PySR) for
        all available options.

        The configuration can be stored in a python file like pysr_config.py:

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
        import importlib
        pysr_config = importlib.import_module('directory.pysr_config').pysr_config
        model = SymbolFit(..., pysr_config=pysr_config, ...)
        ```

        !!! tip
            The choice of operators is the most impactful setting. Start with
            operators that match the expected behavior of your data (e.g., `exp`
            for exponential decays, `gauss` for peaked distributions). See
            [PySR config examples](demo/pysr_configs.md) for common configurations.

    max_complexity : int | None
        Maximum complexity of the expression tree. Each operator and variable
        counts toward this budget (e.g., `a1 * exp(a2 * x0)` has complexity ~6).
        Higher values allow more complex functions but increase search time and
        risk overfitting.

        Overwrites the `maxsize` parameter in `PySRRegressor()`. Set to `None`
        to keep the `maxsize` from your own `pysr_config` instead.

        !!! tip
            Start with 40-60 for most cases. Increase if the search consistently
            returns functions that are too simple to capture the data shape.
            Decrease if functions are overfitting or the search is too slow.

    input_rescale : bool
        Rescale x to the range (0, 1) before fitting. This prevents numerical
        instability or overflow when x values are very large or span many orders
        of magnitude. All fitted functions are automatically unscaled in the
        output, so the final expressions are in terms of the original x.

        !!! tip
            Keep this enabled (True) unless you have a specific reason not to.
            Disabling it can cause fits to fail when x values are large.

    scale_y_by : str | None
        Normalize y before fitting. Options: `'mean'`, `'max'`, `'l2'`, or
        `None` (no normalization). Like `input_rescale`, the final output
        functions are unscaled back to original units.
        Only applies when `input_rescale` is True.

        !!! tip
            Use `'mean'` for most cases. Set to `None` if others don't work well.

    max_stderr : float
        Maximum allowed relative uncertainty (in %) for any single parameter
        during the LMFIT re-optimization stage. If any parameter exceeds this
        threshold, the fit is considered unreliable and is retried with fewer
        free parameters (some are held fixed at their initial values from PySR).

        This acts as a quality gate by preventing the final results from
        containing parameters with meaninglessly large uncertainties.

        !!! tip
            Values of 10-40 work well in practice. Lower values are stricter
            (more parameters may be frozen), higher values are more permissive.
            If many of your candidates show frozen parameters, try increasing this.

    fit_y_unc : bool
        Whether to use `y_up` / `y_down` as weights in the fit loss function.
        When True, the loss is chi2-weighted: `(y_pred - y_true)^2 / y_unc^2`.
        In the LMFIT re-optimization stage, `y_unc` is taken as `y_up` when
        the residual is positive and `y_down` when negative; the PySR search
        stage weights symmetrically by `1 / y_up^2`.

        Set to False for an unweighted (least-squares) fit where all data points
        contribute equally, regardless of their uncertainties. This is useful
        when uncertainties are not available or not meaningful.

    random_seed : int | None
        Set to an integer to make the symbolic regression search reproducible.
        When set, PySR is forced to run in single-threaded mode, which makes
        runs slower but guarantees identical results across runs.

        Leave as `None` for the fastest search (multi-threaded, non-deterministic).
        Since the function space is vast, rerunning with `random_seed = None`
        naturally produces different candidates each time, which can be useful
        for exploring the solution space.

    loss_weights : list | ndarray | None
        Custom per-bin weights for the fit loss. When provided, the loss becomes
        `(y_pred - y_true)^2 * loss_weights` and overrides the `y_up` / `y_down`
        uncertainty weighting. Shape is (num_examples, 1).

        This is useful when you want to emphasize certain regions of the data
        (e.g., assign higher weights to a signal region) or de-emphasize others.
    """

    def __init__(
        self,
        x=None,
        y=None,
        y_up=1,
        y_down=1,
        pysr_config=PySRRegressor(
            model_selection="accuracy",
            niterations=100,
            maxsize=40,
            binary_operators=["+", "*", "/", "^"],
            elementwise_loss="loss(y, y_pred, weights) = (y - y_pred)^2 * weights",
        ),
        max_complexity=40,
        input_rescale=True,
        scale_y_by="mean",
        max_stderr=20,
        fit_y_unc=True,
        random_seed=None,
        loss_weights=None,
        func_candidates=pd.DataFrame(),
    ):
        self.x = x
        self.y = y
        self.y_up = y_up
        self.y_down = y_down
        self.pysr_config = pysr_config
        self.max_complexity = max_complexity
        self.input_rescale = input_rescale
        self.scale_y_by = scale_y_by
        self.max_stderr = max_stderr
        self.fit_y_unc = fit_y_unc
        self.random_seed = random_seed
        self.loss_weights = loss_weights
        self.func_candidates = func_candidates

    def fit(self):
        """
        Performs the full SymbolFit pipeline:

        1. Runs PySR to search for candidate functional forms.
        2. Parameterizes all numerical constants
           (replaces them with named parameters `a1`, `a2`, ...).
        3. Re-optimizes each candidate with LMFIT to refine parameter values
           and provide uncertainty estimation (re-optimization fit, or ROF).
        """

        x = self.x
        y = self.y
        y_up = self.y_up
        y_down = self.y_down
        pysr_model = self.pysr_config
        max_complexity = self.max_complexity
        input_rescale = self.input_rescale
        scale_y_by = self.scale_y_by
        max_stderr = self.max_stderr
        fit_y_unc = self.fit_y_unc
        loss_weights = self.loss_weights

        x, y, y_up, y_down, fit_y_unc, dim = dataset_formatting(x=x, y=y, y_up=y_up, y_down=y_down, fit_y_unc=fit_y_unc)
        self.fit_y_unc = fit_y_unc

        # Rescale the input data before training to prevent overflows in the fits,
        # since say exp(x) would cause problem if x is large.
        # E.g., x -> [0,1] and norm -> 1.
        if self.input_rescale:
            X, Y, Y_up, Y_down, y_scale = histogram_scale(
                x=x, y=y, y_up=y_up, y_down=y_down, x_min=0, x_max=1, scale_y_by=scale_y_by
            )

        else:
            X, Y, Y_up, Y_down, y_scale = x, y, y_up, y_down, 1.0

        # Remove output files from previous PySR fits before starting new one below.
        # pklfiles = glob('hall*')
        # for f in pklfiles:
        #    os.remove(f)
        if os.path.exists("outputs_tmp"):
            shutil.rmtree("outputs_tmp")

        # In PySR, set weighted loss = (y_model - y_label)^2 * loss_weights.
        if loss_weights is not None:
            pysr_weights = np.reshape(np.array(loss_weights), (-1, 1))

        elif y_up is not None and y_down is not None:
            pysr_weights = np.where(Y_up != 0, Y_up, Y_down)
            pysr_weights = 1 / pysr_weights**2

        else:
            pysr_weights = np.ones(y.shape)

        # Run PySR fit.
        if self.random_seed is not None:
            pysr_model.set_params(parallelism="serial", random_state=self.random_seed, deterministic=True)

        if self.max_complexity is not None:
            pysr_model.set_params(maxsize=max_complexity)

        pysr_model.set_params(output_directory="outputs_tmp")

        pysr_model.fit(X, Y, weights=pysr_weights.flatten())

        print("\n")

        # Get essential info from the PySR output file (hall_.pkl),
        # and save to a df for later processing/refit.
        # os.rename(glob('hall*.pkl')[0],'pysr_model_temp.pkl')

        # func_candidates = parse_pysr_equ(pysr_pkl = 'pysr_model_temp.pkl', x = X)
        hash_subdir = [d for d in os.listdir("outputs_tmp") if os.path.isdir(os.path.join("outputs_tmp", d))]
        run_directory = os.path.join("outputs_tmp", hash_subdir[0])

        func_candidates = parse_pysr_equ(pysr_dir=run_directory, x=X)

        print("\n")

        # The constants in the fitted functions from PySR do not have uncert. estimation,
        # so we fix the functional forms, parameterize all constants, and refit them with LMFIT.
        # The first step is to parameterize the fitted functions from PySR.
        def parameterize_func_single(func_str, dim):
            """
            Parameterizing a function like: '1.2*x0 + exp(3.4*x0)' -> 'a1*x0 + exp(a2*x0)'.
            Set the constants as initial conditions for the parameters in the second fits:
                e.g., {'a1': 1.2, 'a2': 3.4}.

            Arguments
            ---------
            func_str (str):
                Function in str like '1.2*x0 + exp(3.4*x0)'.


            Returns
            -------
            function (str):
                E.g., '1.2*x0 + exp(3.4*x0)' same as input

            parameterized function (str):
                E.g., 'a1*x0 + exp(a2*x0)'

            parameterization (dict):
                E.g., {'a1': 1.2, 'a2': 3.4}
            """

            # Define the independent variable (x0, x1, x2,...),
            # parse the input function str into a SymPy equation.
            for i in range(dim):
                func = sympy.sympify(func_str, locals={f"x{i}": sympy.symbols(f"x{i}")})

            # Loop over all constants in the function using SymPy's tree traversal method.
            # If there are 3 constants (1.2, 3.4, 5.6), then create {1.2: 'a1', 3.4: 'a2', 5.6: 'a3'} for them.
            parameterization = {}
            variable_counter = 0

            for a in sympy.preorder_traversal(func):
                # Replace non-integer constants only,
                # as sometimes constants like 1 are trivial.
                if isinstance(a, sympy.Number) and not a.is_Integer:
                    variable_counter += 1
                    parameterization[a] = sympy.Symbol(f"a{variable_counter}")

            # In case there are constants belonging to more than one subtree,
            # the earlier variable_counter will be overriden,
            # creating {1.2: 'a1', 3.4: 'a3', 5.6: 'a4'} instead of {1.2: 'a1', 3.4: 'a2', 5.6: 'a3'}.
            # We don't want that since it will cause problem in later processing.
            # Here, we rename the variables with ascending subscripts {'a1', 'a2', 'a3',...}.
            def rename_ascending_variables(param_dict):
                # parameterization was created with float keys and sympy symbols as values.
                # First sort the items by the constants (keys).
                sorted_items = sorted(param_dict.items(), key=lambda x: x[0])

                # Loop over the sorted items, rename the variables,
                # and store to a new dictionary.
                param_dict_renamed = {}
                for i, (key, value) in enumerate(sorted_items, start=1):
                    renamed_variable = f"a{i}"

                    if value.name != renamed_variable:
                        value = sympy.symbols(renamed_variable)

                    param_dict_renamed[key] = value

                return param_dict_renamed

            parameterization = rename_ascending_variables(parameterization)

            # Replace constants by their corresponding parameters in the function.
            func_parameterized = func.subs(parameterization)

            return (
                str(func),
                str(func_parameterized),
                {str(value): float(key) for key, value in parameterization.items()},
            )

        def parameterize_func_all(func_candidates, dim):
            """
            Parameterize all candidate functions at once.

            Arguments
            ---------
            func_candidates (pd.dataframe):
                Contains all PySR functions to be parameterized.


            Returns
            -------
            func_candidates (pd.dataframe):
                Add new columns for the parameterized functions
                and the parameterization that stores the initial values.
            """

            # Loop over all candidate functions, parameterize them,
            # and store as new columns.
            func_param_all = []
            param_all = []

            for i in range(len(func_candidates)):
                _, func_param, param = parameterize_func_single(func_str=func_candidates["PySR equation"][i], dim=dim)

                func_param_all.append(func_param)
                param_all.append(param)

            func_candidates["Parameterized equation"] = func_param_all

            func_candidates["Parameterization"] = param_all

            try:
                func_candidates = func_candidates[
                    ["PySR template spec", "PySR equation", "Parameterized equation", "Parameterization", "Complexity"]
                ]
            except Exception:
                func_candidates = func_candidates[
                    ["PySR equation", "Parameterized equation", "Parameterization", "Complexity"]
                ]

            return func_candidates

        def get_rel_err(param):
            """
            Get relative error of a fitted parameter from the LMFIT result.

            Arguments
            ---------
            param (LMFIT.Param):
                Parameter instance of LMFIT after fit.


            Returns
            -------
            value (np.float):
                Best-fit.

            std_err (np.float):
                Standard error.

            ratio (np.float):
                (standard error / best-fit value) * 100, in absolute value.
            """

            # Get numbers of a fitted parameter from the LMFIT result
            numbers = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", str(param))
            numbers = np.array(numbers, dtype=float)

            value = None
            std_err = None
            ratio = 99999

            # If the fit succeeds, LMFIT parameter returns something like
            # "... a1 ... [best-fit] ... [standard error]...", 3 numbers in total,
            # we need the last two to calculate the relative error.
            # Otherwise the parameter has been held fixed or sent to inf,
            # which we assign 99999 for the relative error and ignore it for later.
            if len(numbers) == 3:
                value, std_err = numbers[1], numbers[2]
                ratio = std_err / np.abs(value) * 100

            return value, std_err, ratio

        def get_covariance_correlation(fit_result):
            """
            Get correlation of all fitted parameters from the LMFIT result.

            Arguments
            ---------
            fit_result:
                Fit result from LMFIT.


            Returns
            -------
            correlation (dict):
                Correlation matrix of fitted parameters {'a1, a2': 0.1, ...}.
            """

            # Get the number of fitted parameters that were not held fixed.
            num_param = len(fit_result.params)
            param_varied = []

            for i in range(num_param):
                if "fixed" not in str(fit_result.params[f"a{i + 1}"]):
                    param_varied.append(f"a{i + 1}")

            num_param_varied = len(param_varied)

            # Store diagonal and upper or lower triangular elements.
            covariance = {}

            # Calculate correlation as covariance(x, y) / (stderr_x * stderr_y).
            correlation = {}

            # Correlation only when at least one pair of parameters exist.
            if num_param_varied > 1:
                # All possible pairs.
                for i in range(num_param_varied - 1):
                    for j in range(i + 1, num_param_varied):
                        # Get a pair of parameters.
                        pair = f"{param_varied[i]}, {param_varied[j]}"

                        # Get standard errors from covariance matrix.
                        _, error_i, _ = get_rel_err(param=fit_result.params[param_varied[i]])
                        _, error_j, _ = get_rel_err(param=fit_result.params[param_varied[j]])

                        # Compute the correlation value.
                        corr = round_a_number(number=fit_result.covar[i][j] / (error_i * error_j), sig_fig=4)

                        # Numerical rounding causing correlation slightly > 1 or < 1.
                        if corr > 1:
                            corr = 1

                        elif corr < -1:
                            corr = -1

                        correlation[pair] = corr

                        # Off diagonal elements of the covariance matrix.
                        covariance[pair] = fit_result.covar[i][j]

                # Diagonal elements of the covariance matrix.
                for i in range(num_param_varied):
                    pair = f"{param_varied[i]}, {param_varied[i]}"
                    covariance[pair] = fit_result.covar[i][i]

            return covariance, correlation

        def refit_single(func_candidate, x, y, y_up, y_down, max_stderr, dim):
            """
            After parameterizing a PySR function, fit it with LMFIT.
            It contains a refit loop:
                First allow all parameters to vary in the fit,
                if the fit fails (no min found or any parameter returns a too high error)
                then loosen the ndf (keep some of parameters fixed in fits) and refit again.

            Arguments
            ---------
            func_candidate (pd.dataframe):
                Contains one candidate function (one row).

            x (np.ndarray):
                Independent variable of data after processing.

            y (np.ndarray):
                Dependent variable of data after processing.

            y_up (np.ndarray):
                +1 sigma for y.

            y_down (np.ndarray):
                -1 sigma for y.

            max_stderr (np.float):
                Maximum standard error (%) allowed for all parameters in a fit.
                If the fit returns any of the parameters with a stderr higher than that,
                the fit is re-tried by loosening the ndf by fixing some of the parameters.


            Returns
            -------
            result:
                Full fit result returned by the LMFIT Minimizer.

            covariance:
                Covariance matrix of the fitted parameters.

            correlation:
                Correlation matrix of the fitted parameters.

            ci:
                Confidence intervals for the fitted parameters
                (more robust than standard errors from Minimizer).
            """

            # Define the minimization objective for LMFIT (it takes residual^2).
            def residual(params, x, data, y_up, y_down, dim):
                if dim > 1:
                    for i in range(dim):
                        globals()[f"x{i}"] = np.reshape(x[:, i], (-1, 1))

                else:
                    x0 = x  # noqa: F841 -- used by eval(model) below

                # LMFIT uses Parameter object to represent a variable,
                # substitute a1, a2,... by their Parameter object defined in the input params.
                model = re.sub(r"\b(a\d+)\b", r"params['\1']", func_candidate["Parameterized equation"])
                residual = eval(model) - data

                # Scale residual by +/-1 sigma in the fit if they exist.
                # If the residual is +ve in a bin, scale by +1 sigma,
                # otherwise scale by -1 sigma.
                # Also replace with one another if either is zero in a bin.
                if loss_weights is not None:
                    residual = residual * np.sqrt(loss_weights)

                elif y_up is not None and y_down is not None:
                    y_unc = np.where(
                        residual > 0, np.where(y_up != 0, y_up, y_down), np.where(y_down != 0, y_down, y_up)
                    )

                    residual = residual / y_unc

                return residual

            # In principle, we want to have all parameters being varied in a fit,
            # but sometimes the fit fails due to instability or hitting infinities.
            # In these cases, we fit with less ndf by keeping some parameters fixed in next fits.
            # So start a fit with all parameters being variables.
            # If it fails or any parameters have too high relative errors (> max_stderr),
            # redo the fit by fixing one of more parameters until the fit succeeds.

            # Here, we create a list that contains all possible combinations of
            # varying/fixing parameters in a fit.
            # If there are two parameters in a function, then it will generate:
            # [[True, True], [True, False], [False, True], [False, False]].
            def vary_combinations(num_params):
                # Start from a list with all True's.
                vary_combo = [[True] * num_params]

                # Create new combinations by turning some into False's.
                for r in range(1, num_params + 1):
                    for combo in combinations(range(num_params), r):
                        temp_list = vary_combo[0].copy()

                        for index in combo:
                            temp_list[index] = False

                        vary_combo.append(temp_list)

                return vary_combo

            num_params = len(func_candidate["Parameterization"])

            # In case the function does not have any parameter to fit, e.g. y=1 or y=exp(x).
            if num_params == 0:
                return None

            vary_combo = vary_combinations(num_params)

            result = None
            rel_errors = []

            # Loop over the possible combinations of which parameters to vary/fixed in a fit.
            for vary_trial in range(len(vary_combo)):
                print(
                    "    >>> loop of re-parameterization with less NDF"
                    f" for bad fits {vary_trial + 1}/{len(vary_combo)}...",
                    end="\r",
                )

                params = Parameters()

                for i in range(num_params):
                    # Define the LMFIT Parameter for the current fit,
                    # setting which parameters to vary/fixed from the vary_combo,
                    # and their initial values from the parameterization.
                    init_value = func_candidate["Parameterization"][f"a{i + 1}"]

                    # LMFIT Parameter class method add().
                    params.add(name=f"a{i + 1}", value=init_value, vary=vary_combo[vary_trial][i])

                try:
                    # Fit the parameters with the LMFIT minimizer.
                    mini = Minimizer(userfcn=residual, params=params, fcn_args=(x, y, y_up, y_down, dim))
                    # ^ arguments for residual()

                    result = mini.minimize()

                except Exception:
                    # The fit might not converge due to complex phase space,
                    # in that case we give up the current vary_combo and
                    # retry another one (decreasing ndf by fixing more parameters).
                    continue

                # If the above fit converges, get the standard errors in %.
                rel_errors = []

                for i in range(num_params):
                    if vary_combo[vary_trial][i]:
                        _, _, ratio = get_rel_err(param=result.params[f"a{i + 1}"])

                        rel_errors.append(ratio)

                # Here, check if all relative errors are within the pre-set max_stderr,
                # if it does, then stop the refit loop and go to confidence interval calculations,
                # otherwise continue the loop (retry another vary_combo).
                # A finite/small max_stderr is to ensure bounded errors for the fitted parameters.
                # Also, we don't want a too small max_stderr, since it would lead to only
                # a small subset of parameters that float and survive the fit, and the
                # errors would be too small for a meaningful uncertainty model.
                if len(rel_errors) > 0 and all(rel_error < max_stderr for rel_error in rel_errors):
                    print(
                        "    >>> loop of re-parameterization with less NDF"
                        f" for bad fits {vary_trial + 1}/{len(vary_combo)}...\n"
                    )

                    break

            # All combinations exhausted without a successful fit.
            if result is None:
                print(
                    "    >>> all re-parameterization combinations exhausted,"
                    " no successful second-fit for this candidate.\n"
                )
                return None

            # Compute the correlation for fitted parameters from the standard error estimation.
            covariance, correlation = get_covariance_correlation(fit_result=result)

            # Compute the confidence intervals for the fitted parameters,
            # which are more robust estimation of the uncertainties than standard errors.
            if len(rel_errors) > 1:
                try:
                    # ci = lmfit.conf_interval(minimizer = mini,
                    #                         result = result
                    #                         )
                    ci = None

                except Exception:
                    ci = None

            else:
                ci = None

            return result, covariance, correlation, ci

        def refit_all(func_candidates, x, y, y_up, y_down, max_stderr, dim):
            """
            Fit all parameterized candidate functions at once, using the
            refit_single(func_candidate, x, y, y_up, y_down, max_stderr) defined above.

            Arguments
            ---------
            func_candidates (pd.dataframe):
                Contains all candidate functions.

            x (np.ndarray):
                Independent variable of data after processing.

            y (np.ndarray):
                Dependent variable of data after processing.

            y_up (np.ndarray):
                +1 sigma for y.

            y_down (np.ndarray):
                -1 sigma for y.

            max_stderr (np.float):
                Maximum standard error (%) allowed for all parameters in a fit.
                If the fit returns any of the parameters with a stderr higher than that,
                the fit is re-tried by loosening the ndf by fixing some of the parameters.


            Returns
            -------
            func_candidates (pd.dataframe):
                Update the dataframe by adding new columns:
                    1) 'Parameters: (best-fit, +1, -1)',
                    2) 'Covariance',
                    3) 'Correlation',
                    4) 'Confidence interval'.
            """

            def get_val_err(param_str):
                # Get relevant numbers from Parameter in string.
                numbers = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", param_str)
                numbers = np.array(numbers, dtype=float)

                # If fit returns, there will be 3 numbers.
                # First is best-fit, then up and down unc.
                if len(numbers) == 3:
                    value, error = numbers[1], numbers[2]

                else:
                    value = numbers[1]
                    error = 0

                return value, error

            refitted_params = []
            covariances = []
            correlations = []
            confidence_intervals = []

            for i in range(len(func_candidates)):
                print(f"Re-optimizing parameterized candidate function {i + 1}/{len(func_candidates)}...")

                # Do nothing for candidate without any parameter to fit.
                if func_candidates["Parameterization"][i] == {}:
                    refitted_params.append({})

                    covariances.append({})
                    correlations.append({})
                    confidence_intervals.append(None)

                else:
                    refitted_param = {}

                    # Run the refit.
                    refit_result = refit_single(
                        func_candidate=func_candidates.iloc[i],
                        x=x,
                        y=y,
                        y_up=y_up,
                        y_down=y_down,
                        max_stderr=max_stderr,
                        dim=dim,
                    )

                    # refit_single returns None when all parameter combinations
                    # fail to converge. Fall back to initial values with zero uncertainty.
                    if refit_result is None:
                        for j in range(len(func_candidates["Parameterization"][i])):
                            init_val = func_candidates["Parameterization"][i][f"a{j + 1}"]
                            refitted_param[f"a{j + 1}"] = (round_a_number(init_val), 0, 0)

                        refitted_params.append(refitted_param)
                        covariances.append({})
                        correlations.append({})
                        confidence_intervals.append(None)

                    else:
                        result, covariance, correlation, ci = refit_result

                        # Either all from standard least-square or all from ci.
                        for j in range(len(result.params)):
                            # value, error = get_val_err(str(result.params[f'a{j+1}']))
                            # refitted_param[f'a{j+1}'] = (
                            #     round_a_number(value, sig_fig=6), round_a_number(error, sig_fig=6)
                            # )
                            try:
                                # See LMFIT confidence intervals output format.
                                central = ci[f"a{j + 1}"][3][1]
                                up = ci[f"a{j + 1}"][4][1] - central
                                down = ci[f"a{j + 1}"][2][1] - central

                                refitted_param[f"a{j + 1}"] = (
                                    round_a_number(central),
                                    round_a_number(up),
                                    round_a_number(down),
                                )

                            except Exception:
                                central, std_err = get_val_err(param_str=str(result.params[f"a{j + 1}"]))

                                refitted_param[f"a{j + 1}"] = (
                                    round_a_number(central),
                                    round_a_number(std_err),
                                    round_a_number(-std_err),
                                )

                        refitted_params.append(refitted_param)
                        covariances.append(covariance)
                        correlations.append(correlation)
                        confidence_intervals.append(ci)

            func_candidates["Parameters: (best-fit, +1, -1)"] = refitted_params
            func_candidates["Covariance"] = covariances
            func_candidates["Correlation"] = correlations
            func_candidates["Confidence interval"] = confidence_intervals

            try:
                func_candidates = func_candidates[
                    [
                        "Complexity",
                        "PySR template spec",
                        "PySR equation",
                        "Parameterized equation",
                        "Parameterization",
                        "Parameters: (best-fit, +1, -1)",
                        "Covariance",
                        "Correlation",
                    ]
                ]
            except Exception:
                func_candidates = func_candidates[
                    [
                        "Complexity",
                        "PySR equation",
                        "Parameterized equation",
                        "Parameterization",
                        "Parameters: (best-fit, +1, -1)",
                        "Covariance",
                        "Correlation",
                    ]
                ]

            return func_candidates

        # Parameterize all functional forms from PySR outputs.
        func_candidates = parameterize_func_all(func_candidates=func_candidates, dim=dim)

        # Re-optimization loop (ROF) to improve constants and provide unc estimation.
        func_candidates = refit_all(
            func_candidates=func_candidates, x=X, y=Y, y_up=Y_up, y_down=Y_down, max_stderr=max_stderr, dim=dim
        )

        # Undo the input rescaling after all the fits.
        func_candidates = functions_unscale(
            func_candidates=func_candidates, x=x, X=X, y_scale=y_scale, input_scale=input_rescale, dim=dim
        )

        # Compute goodness-of-fit scores.
        func_candidates = add_gof(func_candidates=func_candidates, x=x, y=y, y_up=y_up, y_down=y_down, dim=dim)

        # Remove intermediate files.
        # intermediate_files = glob('hall*')
        # for f in intermediate_files:
        #    os.remove(f)

        # os.remove('pysr_model_temp.pkl')
        shutil.rmtree("outputs_tmp")

        # Update the full func_candidates dataframe containing all results.
        self.func_candidates = func_candidates

    def save_to_csv(
        self,
        output_dir="./",
    ):
        """
        Saves all candidate functions and their evaluation metrics to CSV files:

        1. `candidates.csv`: full results including intermediate fit details,
           parameterization, covariance matrices, and goodness-of-fit metrics.
        2. `candidates_compact.csv`: compact version with only the final
           functions, parameters, and key metrics for quick inspection.

        Parameters
        ----------
        output_dir : str
            Output directory. Created automatically if it does not exist.
        """

        func_candidates = self.func_candidates

        # Define output directory to store csv and pdf files.
        if output_dir.endswith("/"):
            output_dir = output_dir

        else:
            output_dir = output_dir + "/"

        os.makedirs(output_dir) if not os.path.exists(output_dir) else None

        # Save the full func_candidates dataframe to a csv file.
        print(f"Saving full results >>> {output_dir}candidates.csv")

        func_candidates.to_csv(output_dir + "candidates.csv")

        # Save the compact version removing intermediate info.
        print(f"Saving compact results >>> {output_dir}candidates_compact.csv")

        try:
            func_candidates[
                [
                    "Parameterized equation, unscaled",
                    "Parameters: (best-fit, +1, -1)",
                    "Covariance",
                    "Correlation",
                    "RMSE",
                    "R2",
                    "NDF",
                    "Chi2",
                    "Chi2/NDF",
                    "p-value",
                ]
            ].to_csv(output_dir + "candidates_compact.csv")

        except Exception:
            func_candidates[
                [
                    "Parameterized equation, unscaled",
                    "Parameters: (best-fit, +1, -1)",
                    "Covariance",
                    "Correlation",
                    "RMSE",
                    "R2",
                ]
            ].to_csv(output_dir + "candidates_compact.csv")

    def plot_to_pdf(
        self,
        output_dir="./",
        bin_widths_1d=None,
        bin_edges_2d=None,
        plot_logy=False,
        plot_logx=False,
        plot_logx0=False,
        plot_logx1=False,
        cbar_min=None,
        cbar_max=None,
        cmap=None,
        contour=None,
        sampling_95quantile=False,
    ):
        """
        Generates diagnostic plots for all candidate functions:

        1. `candidates.pdf`: each candidate plotted against the data with
           parameter-by-parameter uncertainty variations, plus residual and
           ratio panels.
        2. `candidates_sampling.pdf`: total uncertainty coverage bands generated
           by Monte Carlo sampling of parameters using their covariance matrix
           (1D only).
        3. `candidates_gof.pdf`: summary of goodness-of-fit metrics
           (Chi2/NDF, RMSE, R2, p-value) across all candidates for comparison.
        4. `candidates_correlation.pdf`: parameter correlation matrices for
           each candidate.

        Parameters
        ----------
        output_dir : str
            Output directory. Created automatically if it does not exist.

        bin_widths_1d : list | ndarray
            *(1D data)* Bin widths corresponding to each x value. When provided,
            each data point is drawn with a horizontal bar spanning its bin
            width (histogram style). Only takes effect when the data has y
            uncertainties. Shape is (num_examples, 1).
            See [input data format](demo/input.md) for a graphical illustration.

        bin_edges_2d : list
            *(2D data)* Bin edges for plotting 2D histogram data, provided as a
            list of two sub-lists: `[[x0_0, x0_1, ...], [x1_0, x1_1, ...]]`.
            The leftmost bin in x0 has edges `x0_0` and `x0_1`.
            `[x0_0, x0_1, ...]` has `(num_x0_bins + 1)` elements and
            `[x1_0, x1_1, ...]` has `(num_x1_bins + 1)` elements.
            This must be a python list (not ndarray) since the two sub-lists
            can have different lengths.

        plot_logy : bool
            Use logarithmic scale for the y-axis in candidates.pdf.
            For 2D data, this applies to the color scale.

        plot_logx : bool
            *(1D data)* Use logarithmic scale for the x-axis in candidates.pdf.

        plot_logx0 : bool
            *(2D data)* Use logarithmic scale for the x0-axis.

        plot_logx1 : bool
            *(2D data)* Use logarithmic scale for the x1-axis.

        cbar_min : float
            *(2D data)* Minimum value for the color bar range.
            If None, determined automatically from the data.

        cbar_max : float
            *(2D data)* Maximum value for the color bar range.
            If None, determined automatically from the data.

        cmap : str
            *(2D data)* Matplotlib colormap name for 2D plots
            (e.g., `'viridis'`, `'coolwarm'`, `'RdBu_r'`).
            If None, defaults to `'Greens'`.

        contour : float
            *(2D data)* If provided, draw a contour line (in red) at this
            value of the function on the 2D plots.

        sampling_95quantile : bool
            *(1D data)* Whether to include the 95% quantile range (in addition
            to the default 68% range) when plotting total uncertainty coverage
            in candidates_sampling.pdf. Enable this to visualize wider
            uncertainty bands.
        """

        x = self.x
        y = self.y
        y_up = self.y_up
        y_down = self.y_down
        fit_y_unc = self.fit_y_unc
        func_candidates = self.func_candidates

        x, y, y_up, y_down, _, dim = dataset_formatting(x=x, y=y, y_up=y_up, y_down=y_down, fit_y_unc=fit_y_unc)

        # Define output directory to store csv and pdf files.
        if output_dir.endswith("/"):
            output_dir = output_dir

        else:
            output_dir = output_dir + "/"

        os.makedirs(output_dir) if not os.path.exists(output_dir) else None

        # Plot results and write to output pdf files.
        if dim == 1:
            if bin_widths_1d is not None:
                if not isinstance(bin_widths_1d, (list, np.ndarray)):
                    raise TypeError("Input bin_widths_1d must be either a python list or a numpy array.")

                bin_widths_1d = np.reshape(np.array(bin_widths_1d), (-1, 1))
                if bin_widths_1d.shape[0] != x.shape[0]:
                    raise ValueError(
                        f"Input data mismatch: x has {x.shape[0]} data points, "
                        f"but there are {bin_widths_1d.shape[0]} bin widths in bin_widths_1d."
                    )

            plot_all_syst_all_func_1D(
                func_candidates=func_candidates,
                x=x,
                bin_widths_1d=bin_widths_1d,
                y=y,
                y_up=y_up,
                y_down=y_down,
                pdf_path=output_dir + "candidates.pdf",
                logy=plot_logy,
                logx=plot_logx,
            )

            plot_total_unc_coverage_all_func_1D(
                func_candidates=func_candidates,
                x=x,
                bin_widths_1d=bin_widths_1d,
                y=y,
                y_up=y_up,
                y_down=y_down,
                n_samples=2000,
                sampling_95quantile=sampling_95quantile,
                pdf_path=output_dir + "candidates_sampling.pdf",
                logy=plot_logy,
                logx=plot_logx,
            )

        elif dim == 2:
            if bin_edges_2d is not None:
                if not isinstance(bin_edges_2d, (list, np.ndarray)):
                    raise TypeError("Input bin_edges_2d must be either a python list or a numpy array.")

            plot_all_syst_all_func_2D(
                func_candidates=func_candidates,
                x=x,
                bin_edges_2d=bin_edges_2d,
                y=y,
                y_up=y_up,
                y_down=y_down,
                pdf_path=output_dir + "candidates.pdf",
                logx0=plot_logx0,
                logx1=plot_logx1,
                logy=plot_logy,
                cbar_min=cbar_min,
                cbar_max=cbar_max,
                cmap=cmap,
                contour=contour,
            )

        plot_all_corr(
            func_candidates=func_candidates,
            y_up=y_up,
            y_down=y_down,
            pdf_path=output_dir + "candidates_correlation.pdf",
        )

        plot_all_gof(
            func_candidates=func_candidates, y_up=y_up, y_down=y_down, pdf_path=output_dir + "candidates_gof.pdf"
        )

    def print_candidate(
        self,
        candidate_number=99,
    ):
        """
        Print candidate functions with fully substituted parameter values
        to the terminal.

        Parameters
        ----------
        candidate_number : int
            Print a specific candidate by its number (as shown in the output
            CSV/PDF), or set to `99` to print all candidates.
        """

        pd.set_option("display.max_colwidth", 30)

        # Whether to print relevant info or full info including all intermediate results.
        try:
            func_candidates = self.func_candidates[
                [
                    "Parameterized equation, unscaled",
                    "Parameters: (best-fit, +1, -1)",
                    "Covariance",
                    "Correlation",
                    "RMSE",
                    "R2",
                    "NDF",
                    "Chi2",
                    "Chi2/NDF",
                    "p-value",
                ]
            ]

        except Exception:
            # 'NDF', 'Chi2', 'Chi2/NDF' do not exist if y_up/y_down were not considered in fits.
            func_candidates = self.func_candidates[
                [
                    "Parameterized equation, unscaled",
                    "Parameters: (best-fit, +1, -1)",
                    "Covariance",
                    "Correlation",
                    "RMSE",
                    "R2",
                ]
            ]

        # A function to print a particular candidate.
        def print_cand(func_candidate):

            print(func_candidate)

            # Print candidate function separately with its best-fit parameters and +/-1 sigma substituted.
            # First print the parameterized function before substitution,
            # as well as the parameters and their correlation.
            func_unsub = func_candidate["Parameterized equation, unscaled"]

            print("\nFunction:\n" + func_unsub)

            print("\nParameters (best-fit, +1, -1):\n" + str(func_candidate["Parameters: (best-fit, +1, -1)"]))

            print("\nCovariance:\n" + str(func_candidate["Covariance"]))

            print("\nCorrelation:\n" + str(func_candidate["Correlation"]))

            # Then print the substituted function.
            if len(func_candidate["Parameters: (best-fit, +1, -1)"]) > 0:
                # Substitute all parameters with their best-fit values and print the function.
                func_sub = func_unsub

                for i in range(len(func_candidate["Parameters: (best-fit, +1, -1)"])):
                    func_sub = func_sub.replace(
                        f"a{i + 1}", str(func_candidate["Parameters: (best-fit, +1, -1)"][f"a{i + 1}"][0])
                    )

                print("\nBest-fit:\n" + func_sub + "\n")

                # Substitute with each parameter shifted by +/-1 sigma while keeping others in their best-fit values.
                for i in range(len(func_candidate["Parameters: (best-fit, +1, -1)"])):
                    func_sub = func_unsub

                    # Possible only if the parameter has +/-1 sigma values stored.
                    if func_candidate["Parameters: (best-fit, +1, -1)"][f"a{i + 1}"][1] > 0:
                        # Substitute with +/-1 sigma separately for the current parameter.
                        up = func_candidate["Parameters: (best-fit, +1, -1)"][f"a{i + 1}"][0]
                        up = up + func_candidate["Parameters: (best-fit, +1, -1)"][f"a{i + 1}"][1]

                        down = func_candidate["Parameters: (best-fit, +1, -1)"][f"a{i + 1}"][0]
                        down = down + func_candidate["Parameters: (best-fit, +1, -1)"][f"a{i + 1}"][2]

                        func_sub_up = func_sub.replace(f"a{i + 1}", str(round_a_number(up, 6)))

                        func_sub_down = func_sub.replace(f"a{i + 1}", str(round_a_number(down, 6)))

                        # Substitute the rest parameters with their best-fit values.
                        for j in range(len(func_candidate["Parameters: (best-fit, +1, -1)"])):
                            # The current parameter i is already substituted with its +/-1 sigma.
                            if j is not i:
                                func_sub_up = func_sub_up.replace(
                                    f"a{j + 1}", str(func_candidate["Parameters: (best-fit, +1, -1)"][f"a{j + 1}"][0])
                                )

                                func_sub_down = func_sub_down.replace(
                                    f"a{j + 1}", str(func_candidate["Parameters: (best-fit, +1, -1)"][f"a{j + 1}"][0])
                                )

                        print(f"a{str(i + 1)} (up):\n" + func_sub_up + "\n")

                        print(f"a{str(i + 1)} (down):\n" + func_sub_down + "\n")

        # Print result for all candidate functions (# = 99) or just for a particular one.
        if candidate_number == 99:
            for i in range(len(func_candidates)):
                print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

                print_cand(func_candidate=func_candidates.iloc[i])

                print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        else:
            if candidate_number < len(func_candidates):
                print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

                print_cand(func_candidate=func_candidates.iloc[candidate_number])

                print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
            else:
                print(f"Error: candidate_number must be 0-{str(len(func_candidates) - 1)}")
