# Welcome to SymbolFit documentation!

<p align="center">
  <img src="logo.png" width="400">
</p>

<p align="center">
  <img src="thumbnail.png" width="1200">
</p>

<p align="center">
  <img src="demo/animation.gif" width="900">
</p>

Docs | Paper | Slides | Colab | pip | conda |
|:-:|:-:|:-:|:-:|:-:|:-:|
[![Read the Docs](https://img.shields.io/readthedocs/symbolfit?color=blue&style=flat-square)](https://hftsoi.github.io/symbolfit) | [![arXiv](https://img.shields.io/badge/arXiv-2411.09851-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2411.09851) | [![slides](https://img.shields.io/badge/talk-slides-informational?style=flat-square&color=purple)](https://github.com/hftsoi/symbolfit/blob/main/symbolfit.pdf) | [![Open in Colab](https://img.shields.io/badge/Colab-notebook-informational?style=flat-square&color=gold)](https://colab.research.google.com/github/hftsoi/symbolfit/blob/main/colab_demo/symbolfit_colab.ipynb) | [![PyPI - Version](https://img.shields.io/pypi/v/symbolfit?color=orange&style=flat-square)](https://pypi.org/project/symbolfit) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/symbolfit.svg?color=green&style=flat-square)](https://anaconda.org/conda-forge/symbolfit) |

An API to automate parametric modeling with symbolic regression, originally developed for data analysis in the experimental high-energy physics community, but also applicable beyond.

SymbolFit takes binned data with measurement/systematic uncertainties (optional) as input, utilizes [PySR](https://github.com/MilesCranmer/PySR) to perform a machine-search for batches of functional forms that model the data, parameterizes these functions, and utilizes [LMFIT](https://github.com/lmfit/lmfit-py) to re-optimize the functions and provide uncertainty estimation, all in one go.
It is designed to maximize automation with minimal human input. Each run produces a batch of functions with uncertainty estimation, which are evaluated, saved, and plotted automatically into readable output files, ready for downstream tasks.

In short, `symbolfit` = `pysr (symbolic regression to generate functional forms)` + `lmfit (re-optimization & uncertainty modeling)` + `auto-evaluation tools (parameter correlation, uncertainty variation and coverage, statistical tests, etc.)`.


!!! note

    This API is being actively updated to accommodate more use cases, so any feedback and contributions are very much welcomed and appreciated! If you encounter any problems while using it, please don't hesitate to raise questions or report bugs at [Issues](https://github.com/hftsoi/symbolfit/issues). If you need further help, also feel free to drop me a message as I am happy to assist in getting it to work on your data!
