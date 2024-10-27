import numpy as np
from .utils import *
import scipy


# compute the refitted function, with all parameters at their best fit values, or have one of them shifted +/-1sigma
def func_evaluate(
    func_candidate,
    x,
    dim,
    param_shifted = None,
    sigma_pm = None,
    evaluate_pysr = False
):
    '''
    Compute the function values corresponding to the input array x.
    
    Arguments
    ---------
    func_candidate (pd.dataframe):
        A particular function candidate (single row of the func_candidates dataframe).
        
    x0 (np.ndarray):
        Numpy array of the independent variable.
        
    param_shifted (str):
        Set to 'a3' to evaluate the function values shifting the 'a3' while keeping the rest parameters unshifted.
        If None, evaluate the function values with all parameters at their best-fit values.
        
    sigma_pm (str):
        Set to '+' ('-1') for +1 (-1) sigma of param_shifted.
        If None, evaluate the function values with all parameters at their best-fit values.
        
    evaluate_pysr (bool):
        True: evaluate with the original function from PySR.
        False: evaluate with the refitted function from LMFIT.
    
    
    Returns
    -------
    y_pred (np.ndarray):
        The predicted dependent variable y for the function candidate.
    '''
    
    if param_shifted is None:
        # Substitute with the parameters from LMFIT (second fit) or from PySR (first fit).
        if evaluate_pysr == False:
            func = re.sub(r'\b(a\d+)\b',
                        r"func_candidate['Parameters: (best-fit, +1, -1)']['\1'][0]",
                        func_candidate['Parameterized equation, unscaled'])
                        
        else:
            func = re.sub(r'\b(a\d+)\b',
                        r"func_candidate['Parameterization']['\1']",
                        func_candidate['Parameterized equation, unscaled'])
                        
    else:
        # First substitute with all best-fit parameters.
        func = re.sub(r'\b(a\d+)\b',
                      r"func_candidate['Parameters: (best-fit, +1, -1)']['\1'][0]",
                      func_candidate['Parameterized equation, unscaled'])
                      
        # Then replace the param_shifted with its +/-1 sigma value.
        if sigma_pm == '+':
            func = re.sub(r"func_candidate\['Parameters: \(best-fit, \+1, -1\)'\]\['" + re.escape(param_shifted) + r"'\]\[0\]",
                          r"(func_candidate['Parameters: (best-fit, +1, -1)']['" + param_shifted + r"'][0] + func_candidate['Parameters: (best-fit, +1, -1)']['" + param_shifted + r"'][1])",
                          func)
                          
        elif sigma_pm == '-':
            func = re.sub(r"func_candidate\['Parameters: \(best-fit, \+1, -1\)'\]\['" + re.escape(param_shifted) + r"'\]\[0\]",
                          r"(func_candidate['Parameters: (best-fit, +1, -1)']['" + param_shifted + r"'][0] + func_candidate['Parameters: (best-fit, +1, -1)']['" + param_shifted + r"'][2])",
                          func)
    
    if dim > 1:
        for i in range(dim):
            globals()[f'x{i}'] = np.reshape(x[:, i], (-1, 1))
            
    else:
        x0 = x
        
    if re.findall(r'x\d+', func_candidate['Parameterized equation, unscaled']):
        return eval(func)
        
    else:
        # For function not depending on x.
        return np.full((x.shape[0], 1), eval(func))
        
        
def add_gof(
    func_candidates,
    x,
    y,
    y_up,
    y_down,
    dim
):
    '''
    Compute goodness-of-fit metrics for all function candidates at once.
    
    Arguments
    ---------
    func_candidates (pd.dataframe):
        The full dataframe containing all function candidates.
        
    x (np.ndarray):
        Numpy array of the independent variable.
        
    y (np.ndarray):
        Numpy array of the dependent variable (input at central).
        
    y_up (np.ndarray):
        Numpy array of the dependent variable (input at +1 sigma).

    y_down (np.ndarray):
        Numpy array of the dependent variable (input at -1 sigma).
        
    dim (np.int):
        Dimension of the input data.
    
    
    Returns
    -------
    func_candidates (pd.dataframe):
        Add new columns to the dataframe:
            RMSE (before refit): root-mean-square-error of the PySR function before refit with LMFIT,
            RMSE: after refit with LMFIT,
            R2: coefficient of determination,
            NDF: number of degrees of freedom,
            Chi2 (before refit): Chi2 of the PySR function before refit with LMFIT,
            Chi2: after refit with LMFIT,
            Chi2/NDF (before refit): similar as above,
            Chi2/NDF: similar as above.
    '''
    # Functions after ROF.
    rmse_values = []
    r2_values = []
    chi2_values = []
    ndf_values = []
    chi2_ndf_values = []
    p_values = []
    
    # Functions before ROF.
    chi2_values_pysr = []
    chi2_ndf_values_pysr = []
    p_values_pysr = []
    rmse_values_pysr = []

    for i in range(len(func_candidates)):
        func_candidate = func_candidates.iloc[i]
        
        # Function evaluated with re-fitted parameters from LMFIT.
        y_pred = func_evaluate(func_candidate, x, dim)
        
        # Function evaluated with original parameters from PySR.
        y_pred_pysr = func_evaluate(func_candidate, x, dim, evaluate_pysr = True)
        
        rmse = np.sqrt(np.sum((y - y_pred)**2) / y.size)
        r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
            
        rmse_values.append(round_a_number(rmse, 4))
        r2_values.append(round_a_number(r2, 4))
        
        # The uncertainties of input y are required to compute Chi2.
        if y_up is not None and y_down is not None:
            residual = y_pred - y
            residual_pysr = y_pred_pysr - y
            
            # For each bin, take up/down uncertainty if the residual error is +/-ve.
            # If either uncertainty input is 0, take the other one.
            y_unc = np.where(residual > 0,
                             np.where(y_up != 0, y_up, y_down),
                             np.where(y_down != 0, y_down, y_up))
                             
            y_unc_pysr = np.where(residual_pysr > 0,
                                  np.where(y_up != 0, y_up, y_down),
                                  np.where(y_down != 0, y_down, y_up))
                                  
            chi2 = np.sum(residual**2 / y_unc**2)
            chi2_pysr = np.sum(residual_pysr**2 / y_unc_pysr**2)
            
            # NDF = number of independent data point - number of varying parameters in the function.
            num_free_param = 0
            if len(func_candidate['Parameters: (best-fit, +1, -1)']) > 0:
                for j in range(len(func_candidate['Parameters: (best-fit, +1, -1)'])):
                    if func_candidate['Parameters: (best-fit, +1, -1)'][f'a{j+1}'][1] > 0:
                        num_free_param += 1
                        
            if y.size - num_free_param > 0:
                ndf = y.size - num_free_param
                
            else:
                ndf = -1
                
            p_value = scipy.stats.chi2.sf(chi2, ndf)
            p_value_pysr = scipy.stats.chi2.sf(chi2_pysr, ndf)
                
            ndf_values.append(ndf)
            chi2_values.append(round_a_number(chi2, 4))
            chi2_ndf_values.append(round_a_number(chi2/ndf, 4))
            chi2_values_pysr.append(round_a_number(chi2_pysr, 4))
            chi2_ndf_values_pysr.append(round_a_number(chi2_pysr/ndf, 4))
            p_values.append(round_a_number(p_value, 4))
            p_values_pysr.append(round_a_number(p_value_pysr, 4))
            
        else:
            rmse_pysr = np.sqrt(np.sum((y - y_pred_pysr)**2) / y.size)
            rmse_values_pysr.append(round_a_number(rmse_pysr, 4))
        
    func_candidates['RMSE'] = rmse_values
    func_candidates['R2'] = r2_values
    
    if y_up is not None and y_down is not None:
        func_candidates['NDF'] = ndf_values
        
        func_candidates['Chi2 (before ROF)'] = chi2_values_pysr
        func_candidates['Chi2'] = chi2_values
        
        func_candidates['Chi2/NDF (before ROF)'] = chi2_ndf_values_pysr
        func_candidates['Chi2/NDF'] = chi2_ndf_values
        
        func_candidates['p-value (before ROF)'] = p_values_pysr
        func_candidates['p-value'] = p_values
        
    else:
        func_candidates['RMSE (before ROF)'] = rmse_values_pysr
    
    return func_candidates
    
