from symbolfit.symbolfit import *
import importlib

dataset = importlib.import_module('examples.datasets.toy_dataset_1.dataset')
pysr_config = importlib.import_module('examples.pysr_configs.pysr_config_gauss').pysr_config

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

model.save_to_csv(output_dir = 'output_dir/')

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
