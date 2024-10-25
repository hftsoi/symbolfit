from symbolfit.symbolfit import *
model = SymbolFit()

dataset = importlib.import_module('examples.toy_dataset_1.dataset')
pysr_config = importlib.import_module('examples.toy_dataset_1.pysr_config')

model.fit(dataset=(dataset.x, dataset.y, dataset.y_up, dataset.y_down),
          bin_widths_1d = dataset.bin_widths_1d,
          pysr_config = pysr_config,
          output_dir = 'examples/toy_dataset_1/run',
          input_rescale = True,
          scale_y_by = 'mean',
          random_seed  = 123,
          max_stderr = 40,
          loss_weights = None,
          fit_y_unc = True,
          plot_logy = False,
          plot_logx = False
         )

