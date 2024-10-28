import pandas as pd
import sympy
import os
import re
from pysr import PySRRegressor
from glob import glob
from .math_defs import *

pd.set_option('display.max_colwidth', None)
pd.options.mode.chained_assignment = None
np.seterr(divide='ignore', invalid='ignore')


def round_a_number(number, sig_fig = 6):
    '''
    Round a numpy float number to a certain significant figure.
    '''
        
    try:
        return np.round(number, sig_fig - 1 - int(np.floor(log10(np.abs(number)))))
        
    except:
        return number


def round_numbers_in_sympy_expr(sympy_expr, sig_fig = 3):
    '''
    Round all numbers in a sympy expression to a certain significant figure.
    '''
    
    def rounding(x, sig = sig_fig):
        if x.is_Number and not x.is_Integer:
            return x.round(sig - 1 - int(sympy.floor(sympy.log(abs(x), 10))))
            
        else:
            return x
    
    rounded_expr = sympy_expr.replace(lambda x: x.is_Number,
                                      lambda x: rounding(x, sig_fig))
                                      
    return rounded_expr


def simplify_pkl(pysr_pkl, x):
    '''
    Extract the function candidates from the PySR output file (.pkl) and create a dataframe for them.
    
    Arguments
    ---------
    pysr_pkl (str):
        PySR output file.
    
    x (np.ndarray):
        Independent variable (scaled).
    
    
    Returns
    -------
    A dataframe containing the function candidates, complexity, and loss from the PySR fit.
    '''
    
    model = PySRRegressor.from_file(pysr_pkl)
    
    equation = []
    complexity = []
    loss = []
    
    for i in range(len(model.equations_['equation'])):
        # Simplify the pysr functions algebraically (e.g., (x0 + x0) -> 2 * x0).
        with sympy.evaluate(True):
            equ = model.sympy(i)
        
        # Round the float numbers to a certain significant figure.
        equ = round_numbers_in_sympy_expr(equ)
        
        # Store functions in strings for later manipulation.
        # Also replace custom sympy operators to those that can be treated with numpy.
        equ = str(equ).replace('^', '**').replace('Piecewise(', 'piecewise').replace(' > 0), (0.0, True))', ')')
        
        equation.append(equ)
        
        complexity.append(model.equations_['complexity'][i])
        
        loss.append(round_a_number(model.equations_['loss'][i] * len(x), sig_fig = 3))
        
    df = pd.DataFrame({'PySR equation': equation, 'Complexity': complexity, 'PySR loss': loss})
    
    return df

