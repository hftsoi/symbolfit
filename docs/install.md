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

That's all!
