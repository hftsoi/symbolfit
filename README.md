<p align="center">
  <img src="https://github.com/hftsoi/symbolfit/blob/main/docs/logo.png" width="300"/>
</p>

[![Documentation Status](https://readthedocs.org/projects/symbolfit/badge/?version=latest)](https://symbolfit.readthedocs.io/?badge=latest)

An API to automate parametric modeling with symbolic regression.

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Citation](#citation)

## Overview


## Installation


## Getting Started
To run an example fit:
```
from symbolfit.symbolfit import *

dataset = importlib.import_module('examples.datasets.toy_dataset_1.dataset')
pysr_config = importlib.import_module('examples.pysr_configs.pysr_config_1')

model = SymbolFit(
    	x = dataset.x,
    	y = dataset.y,
    	y_up = dataset.y_up,
    	y_down = dataset.y_down,
    	pysr_config = pysr_config,
    	max_complexity = 60,
    	input_rescale = True,
    	scale_y_by = 'mean',
    	max_stderr = 40,
    	fit_y_unc = True,
    	random_seed = 42,
    	loss_weights = None
)

model.fit()
```
After the fit, save results to csv:
```
model.save_to_csv(output_dir = 'output_dir/')
```
and plot results to pdf:
```
model.plot_to_pdf(
    	output_dir = 'output_dir/',
    	bin_widths_1d = dataset.bin_widths_1d,
    	#bin_edges_2d = dataset.bin_edges_2d,
    	plot_logy = False,
    	plot_logx = False
)
```
Candidate functions with full substitutions can be printed in prompt:
```
model.print_candidate(candidate_number = 10)
```

Each run will produce a batch of candidate functions and will automatically save all results to five output files:
1) ```candidates.csv```: saves all candidate functions and evaluations in a csv table.
2) ```candidates_reduced.csv```: saves a reduced version for essential information without intermediate results.
3) ```candidates.pdf```: plots all candidate functions with associated uncertainties one by one for fit quality evaluation.
4) ```candidates_gof.pdf```: plots the goodness-of-fit scores.
5) ```candidates_correlation.pdf```: plots the correlation matrices for the parameters of each candidate function.

## Documentation
The documentation can be found [here](https://symbolfit.readthedocs.io/) for more info and demonstrations.

## Citation
If you find this useful in your research, please consider citing Symbolfit:
```
Coming soon!
```
and PySR:
```
@misc{cranmerInterpretableMachineLearning2023,
    title = {Interpretable {Machine} {Learning} for {Science} with {PySR} and {SymbolicRegression}.jl},
    url = {http://arxiv.org/abs/2305.01582},
    doi = {10.48550/arXiv.2305.01582},
    urldate = {2023-07-17},
    publisher = {arXiv},
    author = {Cranmer, Miles},
    month = may,
    year = {2023},
    note = {arXiv:2305.01582 [astro-ph, physics:physics]},
    keywords = {Astrophysics - Instrumentation and Methods for Astrophysics, Computer Science - Machine Learning, Computer Science - Neural and Evolutionary Computing, Computer Science - Symbolic Computation, Physics - Data Analysis, Statistics and Probability},
}
```

