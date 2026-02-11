# Installation

**Installation via PyPI**

With python>=3.10 and pip:
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

Julia (backend for PySR) will be automatically installed at first import of PySR:
```
import pysr
```
