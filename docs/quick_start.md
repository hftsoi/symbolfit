# Quick Start

This page walks through a complete fit from start to finish: loading data, running the fit, and inspecting the results.

## Minimal fit

A minimal fit to verify the installation works:

``` python
from symbolfit.symbolfit import *

model = SymbolFit(
    x = [1, 2, 3, 4, 5],
    y = [2.1, 4.0, 5.9, 6.5, 6.9],
    y_up = [0.5, 0.5, 0.5, 0.5, 0.5],
    y_down = [0.5, 0.5, 0.5, 0.5, 0.5],
    max_complexity = 15,
)
model.fit()

model.save_to_csv(output_dir = 'results/')
model.plot_to_pdf(output_dir = 'results/')
```

## Full example with more options

For a more realistic fit, clone the repo to get the example datasets and configs:

``` bash
git clone https://github.com/hftsoi/symbolfit.git
cd symbolfit
```

Then run the example (or simply do `python fit_example.py`):

``` python
from symbolfit.symbolfit import *
import importlib

# Load an example dataset and PySR configuration
dataset = importlib.import_module('examples.datasets.toy_dataset_1.dataset')
pysr_config = importlib.import_module('examples.pysr_configs.pysr_config_gauss').pysr_config

# Set up and run the fit
model = SymbolFit(
    x = dataset.x,              # Independent variable (bin centers for histograms)
    y = dataset.y,              # Dependent variable (bin contents for histograms)
    y_up = dataset.y_up,        # +1 sigma uncertainty on y (set to 1 if no uncertainty)
    y_down = dataset.y_down,    # -1 sigma uncertainty on y (set to 1 if no uncertainty)
    pysr_config = pysr_config,  # PySR search config (operators, iterations, etc.)
    max_complexity = 60,        # Max expression tree size; higher = more complex functions
    input_rescale = True,       # Rescale x to (0, 1) to avoid numerical instability
    scale_y_by = 'mean',        # Normalize y by its 'mean', 'max', 'l2', or None
    max_stderr = 20,            # Max parameter uncertainty (%); refit if exceeded
    fit_y_unc = True,           # Use uncertainties as weights in chi2 loss
    random_seed = None,         # Set int for reproducibility (forces single-thread)
    loss_weights = None         # Per-bin loss weights; overrides y_up/y_down if set
)
model.fit()
```

The `fit()` call runs the full pipeline: PySR search, parameterization, and LMFIT re-optimization.

After the fit, save results to CSV files:

``` python
model.save_to_csv(output_dir = 'output_dir/')
```

and generate diagnostic plots as PDF files:

``` python
model.plot_to_pdf(
    output_dir = 'output_dir/',
    bin_widths_1d = dataset.bin_widths_1d, # Bin widths for 1D histogram-style plots
    plot_logy = False,                     # Log scale for y-axis
    plot_logx = False,                     # Log scale for x-axis
    sampling_95quantile = False,           # Show 95% uncertainty band (default: 68% only)
    #bin_edges_2d = dataset.bin_edges_2d,  # Bin edges for 2D histogram plots
    #plot_logx0 = False,                   # Log scale for x0-axis (2D)
    #plot_logx1 = False,                   # Log scale for x1-axis (2D)
    #cbar_min = None,                      # Min value for 2D color bar
    #cbar_max = None,                      # Max value for 2D color bar
    #cmap = None,                          # Matplotlib colormap for 2D plots
    #contour = None,                       # Contour style for 2D plots
)
```

When it finishes, six output files are produced:

| File | What it contains |
|------|-----------------|
| `candidates.csv` | All candidate functions with parameters, uncertainties, covariance matrices, and goodness-of-fit scores |
| `candidates_compact.csv` | Compact version with only final functions, parameters, and key metrics |
| `candidates.pdf` | Each candidate plotted against data, with per-parameter uncertainty variations and residual panels |
| `candidates_sampling.pdf` | Total uncertainty bands from Monte Carlo parameter sampling (1D only) |
| `candidates_gof.pdf` | Summary of goodness-of-fit metrics (chi2/NDF, p-value, RMSE, R2) across all candidates |
| `candidates_correlation.pdf` | Parameter correlation matrices for each candidate |

You can browse the output files from this example fit [here](https://github.com/hftsoi/symbolfit/tree/main/docs/demo/output_dir/toy_dataset_1).

The options are explained in the API reference page [here](class.md).

You can also try SymbolFit directly in the browser with the [Colab notebook](https://colab.research.google.com/github/hftsoi/symbolfit/blob/main/colab_demo/symbolfit_colab.ipynb) (no local installation needed).

## Fit Your Own Data

To fit your own data, replace the `x`, `y`, `y_up`, `y_down` with your own Python lists or NumPy arrays, as shown in the minimal example above. For details on input data format (1D histograms, 2D histograms, etc.), see the [input format guide](demo/input.md).

**No input uncertainties?** Simply omit `y_up` and `y_down` (they default to 1), and set `fit_y_unc = False` for an unweighted least-squares fit.

**Custom PySR config:** The default PySR config includes simple operators (`+`, `*`, `/`, `^`). For your data, you may want to customize this and put some equation constraints. See the [PySR config examples](demo/pysr_configs.md) in the docs.

## Rerunning fits

!!! tip
    The function space is vast. Each run with `random_seed = None` explores different regions and returns a different batch of candidates. If the first run doesn't produce a satisfactory fit, simply rerun with the same config. After several runs, if results are still unsatisfactory, try adjusting the PySR config (e.g., different operators or higher `max_complexity`) and the various fit options.
