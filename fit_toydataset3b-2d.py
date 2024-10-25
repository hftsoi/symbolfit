from symbolfit.symbolfit import *
model = SymbolFit()

dataset = importlib.import_module('examples.toy_dataset_3.dataset_3b')
pysr_config = importlib.import_module('examples.toy_dataset_3.pysr_config')

model.fit(dataset=(dataset.x, dataset.y, dataset.y_up, dataset.y_down),
          bin_edges_2d = dataset.bin_edges_2d,
          pysr_config = pysr_config,
          output_dir = 'examples/toy_dataset_3/run_b',
          input_rescale = False,
          scale_y_by = None,
          random_seed  = 123,
          max_stderr = 40,
          fit_y_unc = True,
          plot_logy = False,
          plot_logx = False
         )

