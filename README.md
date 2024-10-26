<p align="center">
  <img src="https://github.com/hftsoi/symbolfit/blob/main/display/logo.png" width="300"/>
</p>

An API to automate parametric modeling with symbolic regression

Paper: coming soon...

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Examples](#examples)
	- [Toy Dataset 1 (1D)](#toy-dataset-1-1d)
- [Troubleshooting](#troubleshooting)
- [Citation](#citation)

## Overview
coming soon...

## Installation
coming soon...

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
	max_complexity = 40,
	input_rescale = True,
	scale_y_by = 'mean',
	max_stderr = 40,
	fit_y_unc = True,
	random_seed = 12345,
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
	bin_widths_1d = dataset.bin_widths_1d,
	#bin_edges_2d = dataset.bin_edges_2d,
	output_dir = 'output_dir/',
	plot_logy = False,
	plot_logx = False
)
```
Each single run will produce a batch of candidate functions and will automatically save all results to five output files:
1) ```candidates.csv```: saves all candidate functions and evaluations in a dataframe format, e.g., [examples/toy_dataset_1/candidates.csv](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/run1/candidates.csv)
2) ```candidates_reduced.csv```: a reduced version for essential information without intermediate results, e.g., [examples/toy_dataset_1/candidates_reduced.csv](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/run1/candidates_reduced.csv)
3) ```candidates.pdf```: plot all candidate functions with associated uncertainties one by one for fit quality evaluation, e.g., [examples/toy_dataset_1/candidates.pdf](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/run1/candidates.pdf)
4) ```candidates_gof.pdf```: plot goodness-of-fit scores, e.g., [examples/toy_dataset_1/candidates_gof.pdf](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/run1/candidates_gof.pdf)
5) ```candidates_correlation.pdf```: plot correlation matrices for parameters of each candidate function, e.g., [examples/toy_dataset_1/candidates_correlation.pdf](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/run1/candidates_correlation.pdf)

Candidate functions with full substitutions can be printed in prompt:
```
model.print_candidate(candidate_number = 10)
```

## Documentation
coming soon...

## Examples

### Toy dataset 1 (1D)
<details>
  <summary>Expand to see goodness-of-fit scores for candidate functions obtained from a single run</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-gof_chi2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-gof_rmse.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-gof_r2.png" width="800"/>
    </p>
</details>

<details>
  <summary>Expand to see plots of candidate function #36 (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-candidates1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-candidates2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-candidates3.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-candidates4.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-candidates5.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-candidates6.png" width="800"/>
    </p>
</details>

<details>
  <summary>Expand to see correlation matrix for the parameters of candidate function #36</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_1/toy_dataset_1-corr.png" width="800"/>
    </p>
</details>

More demonstrations in

## Troubleshooting
coming soon...

## Citation
If you find this useful in your research, please consider citing Symbolfit:
```
coming soon...
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

