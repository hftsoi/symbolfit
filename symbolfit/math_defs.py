import numpy as np
from numpy import sin, cos, tan, exp, sinh, cosh, tanh, log10, log, where


def square(x):
    return x*x
def cond(x, y):
    return where(x > 0., y, 0.)
def piecewise(y, x):
    return where(x > 0., y, 0.)
def gauss(x):
    return exp(-x*x)
