<p align="center">
  <img src="https://github.com/hftsoi/symbolfit/blob/main/display/logo.png" width="250"/>
</p>

# SymbolFit: An API to Automate Parametric Modeling with Symbolic Regression
Paper: coming soon...

## Contents
[Motivations](https://github.com/hftsoi/symbolfit/tree/main?tab=readme-ov-file#motivations)

[Installation](https://github.com/hftsoi/symbolfit/tree/main?tab=readme-ov-file#installation)

[Examples](https://github.com/hftsoi/symbolfit/tree/main?tab=readme-ov-file#examples)

[Troubleshooting](https://github.com/hftsoi/symbolfit/tree/main?tab=readme-ov-file#troubleshooting)

[Citation](https://github.com/hftsoi/symbolfit/tree/main?tab=readme-ov-file#citation)

## Motivations
coming soon...

## Installation
coming soon...

## Instructions
Two inputs are all needed to run:
1) An input dataset such as the python file at [examples/toy_dataset_1/dataset.py](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/dataset.py)
2) A PySR configuration such as the python file at [examples/toy_dataset_1/pysr_config.py](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/pysr_config.py)

The main function to run the fit is:
```
from symbolfit.symbolfit import *
model = SymbolFit()
model.fit(...)
```
Each single run will produce a batch of candidate functions and will automatically save all results to five output files:
1) ```candidates.csv```: saves all candidate functions and evaluations in a dataframe format, e.g., [examples/toy_dataset_1/candidates.csv](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/candidates.csv)
2) ```candidates_reduced.csv```: a reduced version for essential information without intermediate results, e.g., [examples/toy_dataset_1/candidates_reduced.csv](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/candidates_reduced.csv)
3) ```candidates.pdf```: plot all candidate functions with associated uncertainties one by one for fit quality evaluation, e.g., [examples/toy_dataset_1/candidates.pdf](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/candidates.df)
4) ```candidates_gof.pdf```: plot goodness-of-fit scores, e.g., [examples/toy_dataset_1/candidates_gof.pdf](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/candidates_gof.pdf)
5) ```candidates_correlation.pdf```: plot correlation matrices for parameters of each candidate function, e.g., [examples/toy_dataset_1/candidates_correlation.pdf](https://github.com/hftsoi/symbolfit/blob/main/examples/toy_dataset_1/candidates_correlation.pdf)

Example script to run on the toy dataset 1 (1D binned histogram):
```
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
          max_stderr = 40,
          loss_weights = None,
          fit_y_unc = True,
          plot_logy = False,
          plot_logx = False
         )
```

Example script to run on the toy dataset 3b (2D binned histogram):
```
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
          max_stderr = 40,
          fit_y_unc = True,
          plot_logy = False,
          plot_logx = False
         )
```

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

### CMS Run 2 dijet dataset (public data from [HEPDATA](https://www.hepdata.net/record/ins1764471), [1911.03947](https://arxiv.org/abs/1911.03947))
<details>
  <summary>Expand to see plots of a candidate function (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/dijet/dijet-candidate1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/dijet/dijet-candidate2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/dijet/dijet-candidate3.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/dijet/dijet-candidate4.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/dijet/dijet-candidate5.png" width="800"/>
    </p>
</details>

### CMS Run 2 diphoton dataset (public data from [HEPDATA](https://www.hepdata.net/record/ins2787227), [2405.09320](https://arxiv.org/abs/2405.09320))
<details>
  <summary>Expand to see plots of a candidate function (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/diphoton/diphoton-candidate1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/diphoton/diphoton-candidate2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/diphoton/diphoton-candidate3.png" width="800"/>
    </p>
</details>

### CMS Run 2 trijet dataset (public data from [HEPDATA](https://www.hepdata.net/record/ins2713513), [2310.14023](https://arxiv.org/abs/2310.14023))
<details>
  <summary>Expand to see plots of a candidate function (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/trijet/trijet-candidate1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/trijet/trijet-candidate2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/trijet/trijet-candidate3.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/trijet/trijet-candidate4.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/trijet/trijet-candidate5.png" width="800"/>
    </p>
</details>

### CMS Run 2 paired-dijet dataset (public data from [HEPDATA](https://www.hepdata.net/record/ins2098256), [2206.09997](https://arxiv.org/abs/2206.09997))
<details>
  <summary>Expand to see plots of a candidate function (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/fourjet/fourjet-candidate1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/fourjet/fourjet-candidate2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/fourjet/fourjet-candidate3.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/fourjet/fourjet-candidate4.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/fourjet/fourjet-candidate5.png" width="800"/>
    </p>
</details>

### CMS Run 2 dimuon dataset (public data from [HEPDATA](https://www.hepdata.net/record/ins2678141), [2307.08708](https://arxiv.org/abs/2307.08708))
<details>
  <summary>Expand to see plots of a candidate function (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/dimuon/dimuon-candidate1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/dimuon/dimuon-candidate2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/dimuon/dimuon-candidate3.png" width="800"/>
    </p>
</details>


### Toy dataset 2 (1D)
<details>
  <summary>Expand to see plots of a candidate function for sub-dataset 2a (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2a/toy_dataset_2a-candidate1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2a/toy_dataset_2a-candidate2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2a/toy_dataset_2a-candidate3.png" width="800"/>
    </p>
</details>

<details>
  <summary>Expand to see plots of a candidate function for sub-dataset 2b (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2b/toy_dataset_2b-candidates1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2b/toy_dataset_2b-candidates2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2b/toy_dataset_2b-candidates3.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2b/toy_dataset_2b-candidates4.png" width="800"/>
    </p>
</details>

<details>
  <summary>Expand to see plots of a candidate function for sub-dataset 2c (best-fits and uncertainties)</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2c/toy_dataset_2c-candidates1.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2c/toy_dataset_2c-candidates2.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2c/toy_dataset_2c-candidates3.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2c/toy_dataset_2c-candidates4.png" width="800"/>
    </p>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_2c/toy_dataset_2c-candidates5.png" width="800"/>
    </p>
</details>

### Toy dataset 3 (2D)

<details>
  <summary>Expand to see plots of a candidate function for sub-dataset 3a</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_3a/toy_dataset_3a-candidates1.png" width="800"/>
    </p>
</details>

<details>
  <summary>Expand to see plots of a candidate function for sub-dataset 3b</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_3b/toy_dataset_3b-candidates1.png" width="800"/>
    </p>
</details>

<details>
  <summary>Expand to see plots of a candidate function for sub-dataset 3c</summary>
    <p align="center">
      <img src="https://github.com/hftsoi/symbolfit/blob/main/display/toy_dataset_3c/toy_dataset_3c-candidates1.png" width="800"/>
    </p>
</details>

## Troubleshooting
coming soon...

## Citation
If this is useful for your research, please consider citing the Symbolfit (coming soon...) and PySR (https://arxiv.org/abs/2305.01582) papers.
