# Installation

**Installation via PyPI** (recommended), with Python>=3.10:

```
pip install symbolfit
```

<details>
  <summary>Installation via conda</summary>
  
  ```
  conda create --name symbolfit_env python=3.10
  conda activate symbolfit_env
  conda install -c conda-forge symbolfit
  ```
</details>

Julia (the backend for PySR) is installed automatically the first time you import PySR (one-time setup):
```python
import pysr
```

## Verifying the installation

After installing, you can verify everything is working:

```python
from symbolfit.symbolfit import *

model = SymbolFit(
    x = [1, 2, 3, 4, 5],
    y = [2.1, 4.0, 5.9, 6.5, 6.9],
    y_up=[0.5, 0.5, 0.5, 0.5, 0.5],
    y_down=[0.5, 0.5, 0.5, 0.5, 0.5],
    max_complexity=15,
)
model.fit()

model.save_to_csv(output_dir = 'results/')
model.plot_to_pdf(output_dir = 'results/')
```
