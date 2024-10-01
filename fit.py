from symbolfit.symbolfit import *
model = SymbolFit()

dataset = importlib.import_module('examples.toy_dataset_1.dataset')
pysr_config = importlib.import_module('examples.toy_dataset_1.pysr_config')

model.fit(dataset=(dataset.x, dataset.y, dataset.y_up, dataset.y_down),
          #bin_edges_2d = dataset.bin_edges_2d,
          bin_widths_1d = dataset.bin_widths_1d,
          pysr_config = pysr_config,
	      output_dir = 'examples/toy_dataset_1/run',
	      input_rescale = False,
          scale_y_by = None,
          max_stderr = 40,
	      #loss_weights = None,
	      fit_y_unc = True,
	      #plot_logy = True,
	      #plot_logx = True
	 )

