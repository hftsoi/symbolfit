# Welcome to SymbolFit

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
[![Docs](https://img.shields.io/badge/docs-site-informational?color=blue&style=flat-square)](https://hftsoi.github.io/symbolfit) | [![arXiv](https://img.shields.io/badge/arXiv-2411.09851-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2411.09851) | [![slides](https://img.shields.io/badge/talk-slides-informational?style=flat-square&color=purple)](https://github.com/hftsoi/symbolfit/blob/main/symbolfit.pdf) | [![Open in Colab](https://img.shields.io/badge/Colab-notebook-informational?style=flat-square&color=gold)](https://colab.research.google.com/github/hftsoi/symbolfit/blob/main/colab_demo/symbolfit_colab.ipynb) | [![PyPI - Version](https://img.shields.io/pypi/v/symbolfit?color=orange&style=flat-square)](https://pypi.org/project/symbolfit) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/symbolfit.svg?color=green&style=flat-square)](https://anaconda.org/conda-forge/symbolfit) |

## What is SymbolFit?

**SymbolFit automatically finds closed-form functions that fit your data with uncertainty estimation, no manual guessing required.**

SymbolFit was originally developed for experimental high-energy physics (HEP) analyses, but it works on any 1D, 2D, or higher-dimensional dataset where you need an interpretable parametric model with uncertainty estimates. You provide data points and SymbolFit returns a batch of candidate functions ranked by goodness-of-fit, each with optimized parameters and uncertainty estimates. All results are saved to CSV tables and PDF plots, ready for downstream use such as hypothesis testing in HEP.

Under the hood, it chains three steps into a single pipeline:

1. **Function search**: [PySR](https://github.com/MilesCranmer/PySR) (symbolic regression) explores combinations of mathematical operators to discover functional forms that fit the data, without requiring a predefined template.
2. **Re-optimization**: [LMFIT](https://github.com/lmfit/lmfit-py) re-optimizes the numerical parameters in each candidate function and provides uncertainty estimates via covariance matrices.
3. **Evaluation**: every candidate is automatically scored (chi2/NDF, p-value, RMSE, R2), plotted with individual uncertainty variations and total uncertainty coverage, and saved to output files.

## Navigation

| I want to... | Go to |
|---|---|
| Install and set up | [Installation](install.md) |
| Run my first fit | [Quick Start](quick_start.md) |
| Understand all options | [API Reference](class.md) |
| See example fits on real data | [Demos](demo/input.md) |
| Configure the function search | [PySR Configs](demo/pysr_configs.md) |

!!! note

    This API is being actively updated to accommodate more use cases, so any feedback and contributions are very much welcomed and appreciated! If you encounter any problems while using it, please don't hesitate to raise questions or report bugs at [Issues](https://github.com/hftsoi/symbolfit/issues). If you need further help, also feel free to drop me a message as I am happy to assist in getting it to work on your data!
