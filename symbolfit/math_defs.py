import numpy as np  # noqa: F401 -- re-exported via star imports to other modules
from numpy import (  # noqa: F401
    arccos,
    arccosh,
    arcsin,
    arcsinh,
    arctan,
    arctanh,
    cos,
    cosh,
    exp,
    log,
    log10,
    sin,
    sinh,
    tan,
    tanh,
    where,
)


def square(x):
    return x * x


def cond(x, y):
    return where(x > 0.0, y, 0.0)


def piecewise(y, x):
    return where(x > 0.0, y, 0.0)


def gauss(x):
    return exp(-x * x)


def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))
