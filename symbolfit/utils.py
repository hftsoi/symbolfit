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


def parse_pysr_equ(pysr_dir, x):
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
    
    model = PySRRegressor.from_file(run_directory = pysr_dir)
    
    equation = []
    equation_spec = []
    complexity = []
    loss = []

    if model.expression_spec is None:
        for i in range(len(model.equations_['equation'])):
            # Simplify the pysr functions algebraically (e.g., (x0 + x0) -> 2 * x0).
            with sympy.evaluate(True):
                equ = model.sympy(i)
            
            # Round the float numbers to a certain significant figure.
            equ = round_numbers_in_sympy_expr(equ)
            
            # Store functions in strings for later manipulation.
            # Also replace custom sympy operators to those that can be treated with numpy.
            equ = str(equ).replace('^', '**')
            
            equation.append(equ)
            complexity.append(model.equations_['complexity'][i])
            loss.append(round_a_number(model.equations_['loss'][i] * len(x), sig_fig = 3))

        df = pd.DataFrame({'PySR equation': equation, 'Complexity': complexity, 'PySR loss': loss})

    else:
        '''
        E.g.:
        model.expression_spec.combine: 'f(x) * g(x) + p[1] + p[2]*x'
        model.expression_spec.expressions: ['f', 'g']
        model.expression_spec.variable_names: ['x']
        model.expression_spec.parameters: {'p': 2}'

        model.equations_['equation'][i]:
        'f = (#1 * -0.073103055) + -70.07095; g = log(#1 + -1387.8005); p = [-15.679159, 0.71771586]'

        or (>1d)

        model.expression_spec.combine: 'sin(f(qq)) + f(qq^2) * g(q,qq) + d[1]*q + d[2]*qq + d[3]'
        model.expression_spec.expressions: ['f', 'g'],
        model.expression_spec.variable_names: ['q', 'qq'],
        model.expression_spec.parameters: {'d': 3}

        model.equations_['equation'][i]:
        f = (#1 * 0.7463786) + 4.54765; g = ((#1 * ((#2 + -0.8933617) * (#1 + -1.0033985))) * -4.229166) + 0.6955875; d = [0.04280354, -0.62839013, 7.853348]
        '''
        template_combine = model.expression_spec.combine
        template_expressions = model.expression_spec.expressions
        template_variable_names = model.expression_spec.variable_names
        template_parameters = model.expression_spec.parameters

        def replace_function_calls(equ, func, result_container):
            # Substitute func(...) in the string equ with the candidate expression.
            new_equ = ""
            pos = 0
            target = f"{func}("
            while True:
                idx = equ.find(target, pos)
                if idx == -1:
                    # no more occurrences.
                    new_equ += equ[pos:]
                    break
                new_equ += equ[pos:idx]

                # The argument starts right after target.
                start = idx + len(target)
                count = 1  # count the opening parenthesis just passed
                end = start

                # Scan forward to find the matching closing parenthesis.
                while end < len(equ) and count:
                    if equ[end] == "(":
                        count += 1
                    elif equ[end] == ")":
                        count -= 1
                    end += 1

                # Now equ[idx:end] is the full function call,
                # and equ[start:end-1] is the argument content.
                arg_content = equ[start:end-1]

                # If there are multiple arguments separated by commas, split them.
                args = [a.strip() for a in arg_content.split(',')]

                candidate_expr = result_container[func]

                # Replace variables (#1, #2,...) with the arguments, wrapping each argument.
                for j, arg in enumerate(args, start=1):
                    candidate_expr = candidate_expr.replace(f"#{j}", f"({arg})")

                new_equ += f"({candidate_expr})"
                pos = end
                
            return new_equ
    
        for i in range(len(model.equations_['equation'])):
            equ_raw = model.equations_['equation'][i]
            equation_spec.append(equ_raw)

            result_container = {}
            for part in equ_raw.split(';'):
                part = part.strip()
                key, val = part.split('=', 1)
                key = key.strip()
                val = val.strip()
                result_container[key] = val

            equ = template_combine
            for func in template_expressions:
                equ = replace_function_calls(equ, func, result_container)

            if template_parameters is not None:
                for param, count in template_parameters.items():
                    param_val = [val.strip() for val in result_container[param].strip("[]").split(",")]
                    for j, val in enumerate(param_val, start=1):
                        equ = equ.replace(f"{param}[{j}]", val)

            for idx, var in enumerate(template_variable_names):
                new_var = f"x{idx}"
                equ = re.sub(rf'\b{var}\b', new_var, equ)

            equ = equ.replace('^', '**')
            #print(equ)
            sympy_symbols = {f"x{idx}": sympy.symbols(f"x{idx}") for idx in range(len(template_variable_names))}
            equ = sympy.parse_expr(equ, local_dict=sympy_symbols, evaluate=True)

            equ = round_numbers_in_sympy_expr(equ)
            equ = str(equ)

            equation.append(equ)
            complexity.append(model.equations_['complexity'][i])
            loss.append(round_a_number(model.equations_['loss'][i], sig_fig = 3))

        df = pd.DataFrame({'PySR template spec': equation_spec, 'PySR equation': equation, 'Complexity': complexity, 'PySR loss': loss})
    
    return df

