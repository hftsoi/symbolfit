<p align="center">
  <img src="https://raw.githubusercontent.com/hftsoi/symbolfit/main/docs/logo.png" width="400"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/hftsoi/symbolfit/main/docs/thumbnail.png" width="1200"/>
</p>

<div align="center">
  
![Animation](docs/demo/animation.gif)

</div>

<div align="center">

Docs | Paper | Slides | Colab |
|:-:|:-:|:-:|:-:|
[![Read the Docs](https://img.shields.io/readthedocs/symbolfit?color=blue&style=flat-square)](https://symbolfit.readthedocs.io) | [![arXiv](https://img.shields.io/badge/arXiv-2411.09851-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2411.09851) <br /> [![doi](https://img.shields.io/badge/journal-doi-informational?style=flat-square&color=teal)](https://doi.org/10.1007/s41781-025-00140-9) | [![slides](https://img.shields.io/badge/talk-slides-informational?style=flat-square&color=purple)](https://github.com/hftsoi/symbolfit/blob/main/symbolfit.pdf) | [![Open in Colab](https://img.shields.io/badge/Colab-notebook-informational?style=flat-square&color=gold)](https://colab.research.google.com/github/hftsoi/symbolfit/blob/main/colab_demo/symbolfit_colab.ipynb) |

</div>

<div align="center">

GitHub | pip | conda |
|:-:|:-:|:-:|
[![GitHub Created At](https://img.shields.io/github/created-at/hftsoi/symbolfit?color=black&style=flat-square)](https://github.com/hftsoi/symbolfit) <br /> [![GitHub Release](https://img.shields.io/github/v/release/hftsoi/symbolfit?color=black&style=flat-square)](https://github.com/hftsoi/symbolfit/releases) <br /> [![GitHub Release Date](https://img.shields.io/github/release-date/hftsoi/symbolfit?color=black&style=flat-square)](https://github.com/hftsoi/symbolfit/releases) | [![PyPI - Version](https://img.shields.io/pypi/v/symbolfit?color=orange&style=flat-square)](https://pypi.org/project/symbolfit) <br /> [![Pepy Total Downloads](https://img.shields.io/pepy/dt/symbolfit?color=orange&style=flat-square)](https://www.pepy.tech/projects/symbolfit) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/symbolfit.svg?color=green&style=flat-square)](https://anaconda.org/conda-forge/symbolfit) <br /> [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/symbolfit.svg?color=green&style=flat-square)](https://anaconda.org/conda-forge/symbolfit) |

</div>

An API to automate parametric modeling with symbolic regression, originally developed for data analysis in the experimental high-energy physics community, but also applicable beyond.

SymbolFit takes binned data with measurement/systematic uncertainties (optional) as input, utilizes [PySR](https://github.com/MilesCranmer/PySR) to perform a machine-search for batches of functional forms that model the data, parameterizes these functions, and utilizes [LMFIT](https://github.com/lmfit/lmfit-py) to re-optimize the functions and provide uncertainty estimation, all in one go.
It is designed to maximize automation with minimal human input. Each run produces a batch of functions with uncertainty estimation, which are evaluated, saved, and plotted automatically into readable output files, ready for downstream tasks.

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Citation](#citation)

> **Note:** This API is actively being updated to accommodate more use cases, so any feedback and contributions are very much welcomed and appreciated! If you encounter any problems while using it, please don’t hesitate to:
> - Report bugs or suggest new features at [![Issues](https://img.shields.io/badge/issues-github-informational?style=flat-square)](https://github.com/hftsoi/symbolfit/issues)
> - Ask for specific help and recommendations for your dataset at [![Discussions](https://img.shields.io/badge/discussions-github-informational?style=flat-square)](https://github.com/hftsoi/symbolfit/discussions)
> 
> If you don't feel like sharing your data in public, please feel free to drop me a message or [![Email](https://img.shields.io/badge/email-ho.fung.tsoi@cern.ch-informational?style=flat-square&color=blue)](mailto:ho.fung.tsoi@cern.ch). We are happy to assist in getting it to work on your data!

## Installation
**Prerequisite (Julia)**

Install Julia (backend for PySR):
```
curl -fsSL https://install.julialang.org | sh
```
Then check if installed properly:
```
julia --version
```
If julia is not found, most probably it is not yet included in PATH. To include, do:
```
export PATH="$PATH:/path/to/<Julia directory>/bin"
```
Check out [here](https://julialang.org/downloads/platform) for platform-specific instructions.

Afterward, it is recommended to start from an empty virtual environment for installing and running SymbolFit.

**Installation via PyPI**

With python>=3.10 and pip:
```
pip install symbolfit
```

<details>
  <summary>Installation via conda</summary>
  
  (to be updated for >= v0.2.0, please use pip for now)
  ```
  conda create --name symbolfit_env python=3.10
  conda activate symbolfit_env
  conda install -c conda-forge symbolfit
  ```
</details>

<details>
  <summary>Editable installation for developers</summary>

  ```
  git clone https://github.com/hftsoi/symbolfit.git
  cd symbolfit
  pip install -e .
  ```
</details>

## Getting Started
To run an example fit, get the example datasets by cloning this repo:
```
git clone https://github.com/hftsoi/symbolfit.git
cd symbolfit
```
Then within a python session (or simply do ```python fit_example.py```):
```
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
```
After the fit, save results to csv files:
```
model.save_to_csv(output_dir = 'output_dir/')
```
and plot results to pdf files:
```
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
```
Candidate functions with full substitutions can be printed promptly:
```
model.print_candidate(candidate_number = 20)
```
When preparing for your own data, a graphical illustration of the input data format can be found [here](https://symbolfit.readthedocs.io/demo/input.html).

Each fit will produce a batch of candidate functions and will automatically save all results to six output files:
1) ```candidates.csv```: saves all candidate functions and evaluations in a csv table.
2) ```candidates_compact.csv```: saves a reduced version for essential information without intermediate results.
3) ```candidates.pdf```: plots all candidate functions (1D/2D only for now) with associated uncertainties one by one for fit quality evaluation.
4) ```candidates_sampling.pdf```: plots all candidate functions (1D only for now) with total uncertainty coverage generated by sampling parameters.
5) ```candidates_gof.pdf```: plots the goodness-of-fit scores.
6) ```candidates_correlation.pdf```: plots the correlation matrices for the parameters of the candidate functions.

Output files from an example fit can be found and downloaded [here](https://github.com/hftsoi/symbolfit/tree/main/docs/demo/output_dir/toy_dataset_1) for illustration.

> **Note:** The function space is usually huge, even when constrained by the pysr config. This means that if you are not satisfied with the results from a fit, you can simply rerun it with the exact same config and obtain a completely different set of candidate functions&mdash;the only difference being the random seed that initiates the seeding functions. Therefore, you can rerun the fit as many times as you want until you are satisfied with the results. If you use ```model = SymbolFit(..., random_seed = None, ...)```, nothing needs to be changed&mdash;just rerun the fit. If you set a specific ```random_seed```, change its value before rerunning. However, if you are still not satisfied with the results after many trials, it might indicate an issue with the config. Then you might want to try a different config, tune it, and start new runs.

For detailed instructions and more demonstrations, please check out the Colab notebook and the documentation.

## Documentation
The documentation can be found [here](https://symbolfit.readthedocs.io) for more information and demonstrations.

## Citation
If you find this useful in your research, please consider citing SymbolFit:
```
@article{Tsoi:2024pbn,
    author = "Tsoi, Ho Fung and Rankin, Dylan and Caillol, Cecile and Cranmer, Miles and Dasu, Sridhara and Duarte, Javier and Harris, Philip and Lipeles, Elliot and Loncar, Vladimir",
    title = "{SymbolFit: Automatic Parametric Modeling with Symbolic Regression}",
    eprint = "2411.09851",
    archivePrefix = "arXiv",
    primaryClass = "hep-ex",
    doi = "10.1007/s41781-025-00140-9",
    journal = "Comput. Softw. Big Sci.",
    volume = "9",
    pages = "12",
    year = "2025"
}
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

