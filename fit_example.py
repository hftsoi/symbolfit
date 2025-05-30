from symbolfit.symbolfit import *

dataset = importlib.import_module('examples.datasets.toy_dataset_1.dataset')
pysr_config = importlib.import_module('examples.pysr_configs.pysr_config_gauss').pysr_config

model = SymbolFit(
    x = dataset.x,
    y = dataset.y,
    y_up = dataset.y_up,
    y_down = dataset.y_down,
    pysr_config = pysr_config,
    max_complexity = 60,
    input_rescale = True,
    scale_y_by = 'mean',
    max_stderr = 20,
    fit_y_unc = True,
    random_seed = None,
    loss_weights = None
)
                  
model.fit()

model.save_to_csv(output_dir = 'output_dir/')

model.plot_to_pdf(
    output_dir = 'output_dir/',
    bin_widths_1d = dataset.bin_widths_1d,
    plot_logy = False,
    plot_logx = False,
    sampling_95quantile = False,
    #bin_edges_2d = dataset.bin_edges_2d,
    #plot_logx0 = False,
    #plot_logx1 = False,
    #cbar_min = None,
    #cbar_max = None,
    #cmap = None,
    #contour = None,
    # ^ additional options for 2D plotting
)
