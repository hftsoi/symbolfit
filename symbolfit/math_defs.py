from numpy import exp, where


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
