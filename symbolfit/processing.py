import numpy as np
from .utils import round_a_number
    

def dataset_formatting(
    x,
    y,
    y_up,
    y_down,
    fit_y_unc
):

    dim = 0
    
    # Input dataset is in python lists.
    if isinstance(x, list):
        # dataset[0] is the independent variable x that takes the form:
        # [1, 2, 3,...] of 1D;
        # [[1, 1], [1, 2], [1, 3],...] for 2D;
        # [[1, 1, 1], [1, 1, 2], [1, 1, 3],...] for 3D etc.
        if isinstance(x[0], list):
            dim = len(x[0])
            
        else:
            dim = 1
            
    elif isinstance(x, np.ndarray):
        # dataset[0] is the independent variable in np.ndarray with shape (n, dim).
        dim = np.shape(x)[1]
        
    else:
        raise TypeError('Input x should be either lists or numpy arrays.')
            
    # Get x and y.
    x = np.reshape(np.array(x), (-1, dim))
    y = np.reshape(np.array(y), (-1, 1))
    
    assert(x.shape[0] == y.shape[0])
        
    # Get uncertainties for y.
    if y_up is not None and y_down is not None:
        #if isinstance(dataset[2], list) and isinstance(dataset[3], list):
        #    pass
        #elif isinstance(dataset[2], np.ndarray) and isinstance(dataset[3], np.ndarray):
        #    pass
        #else:
        #    raise TypeError('Input dataset should be either python lists or numpy arrays.')
        
        y_up = np.reshape(np.array(y_up), (-1, 1))
        y_down = np.reshape(np.array(y_down), (-1, 1))
        
        assert(x.shape[0] == y.shape[0] == y_up.shape[0] == y_down.shape[0])

        if fit_y_unc:
            # Do not fit with y uncert. if any of these is zero,
            # since loss = (y_pred - y_true)^2/y_unc^2 would become undefined.
            if np.any(np.logical_and(y_up == 0, y_down == 0)):
                y_up = None
                y_down = None
                fit_y_unc = False
                
        else:
            y_up = None
            y_down = None
            fit_y_unc = False
            
    else:
        y_up = None
        y_down = None
        fit_y_unc = False
        
    return x, y, y_up, y_down, fit_y_unc, dim
        

def histogram_scale(
    x,
    y,
    y_up,
    y_down,
    x_min = 0,
    x_max = 1,
    scale_y_by = None
):
    '''
    Pre-process the input data by scaling both x and y:
        1) scale x to [x_min, x_max],
        2) scale y s.t. the normalization = norm (computed with np.trapz).
    This is to stablize the fits and avoid numerical overflow etc.
    
    Arguments
    ---------
    x (np.ndarray):
        Numpy array of the independent variable.
        
    y (np.ndarray):
        Numpy array of the dependent variable (input at central).
        
    y_up (np.ndarray):
        Numpy array of the dependent variable (input at +1 sigma).

    y_down (np.ndarray):
        Numpy array of the dependent variable (input at -1 sigma).
        
    x_min (np.float):
        Minimum of x after scaling.
    
    x_max (np.float):
        Maximum of x after scaling.
    
    norm (np.float):
        Normalization of (x, y) after scaling.
    
    
    Returns
    -------
    X (np.ndarray):
        Scaled x with the range [x_min, x_max].
    
    Y (np.ndarray):
        Scaled y with normalization.
    
    Y_up (np.ndarray):
        Scaled y_up by the same norm as applied to y.
    
    Y_down (np.ndarray):
        Scaled y_down by the same norm as applied to y.
    
    y_scale (np.float):
        The scale number multiplied to y's,
        it will be used to unscale the functions after fitting.
    '''
    
    # Scale the x axis to a range from x_min to x_max.
    X = (x - np.min(x, axis = 0)) * (x_max - x_min) / (np.max(x, axis = 0) - np.min(x, axis = 0)) + x_min
    
    # Scale y.
    if scale_y_by == 'max':
        y_scale = 1 / np.abs(np.max(y))
        
    elif scale_y_by == 'mean':
        y_scale = 1 / np.abs(np.mean(y))
        
    elif scale_y_by == 'l2':
        y_scale = 1 / np.linalg.norm(y)
        
    else:
        y_scale = 1
        
    Y = y * y_scale
    
    if y_up is not None and y_down is not None:
        Y_up = y_up * y_scale
        Y_down = y_down * y_scale
        
    else:
        Y_up = None
        Y_down = None
    
    return X, Y, Y_up, Y_down, y_scale
    

def functions_unscale(
    func_candidates,
    x,
    X,
    y_scale,
    input_scale,
    dim
):
    '''
    The PySR/LMFIT fits were done on the scaled data,
    these fitted functions need to be unscaled to described the original data.
    
    Arguments
    ---------
    func_candidates (pd.dataframe):
        Dataframe containing all function candidates after fits.
        
    x (np.ndarray):
        The independent variable before scaling.
        
    X (np.ndarray):
        The independent variable after scaling.
    
    y_scale (np.float):
        The scale number multiplied to y's,
        it will be used to unscale the functions after fitting.
        
    input_rescale (bool):
        True: scaling enabled.
        False: scaling not enabled, so just return the same functions after fits.
    
    
    Returns
    -------
    func_candidates (pd.dataframe):
        Add a new column for the unscaled parameterized functions.
    '''
    
    # Scaled.
    X_min = np.min(X, axis = 0)
    X_max = np.max(X, axis = 0)
    
    # Original.
    x_min = np.min(x, axis = 0)
    x_max = np.max(x, axis = 0)
    
    X_range = X_max - X_min
    x_range = x_max - x_min
    
    func_unscaled = []
    
    for i in range(len(func_candidates)):
        func = func_candidates['Parameterized equation'][i]
        
        if input_scale == True:
            # Scale X back to the original range:
            # substitute X by (x - x_min) * (x_range_scaled / x_range_original) + X_min.
            for j in range(dim):
                var = f'x{j}'
                if X_min[j] == 0:
                    func = func.replace(var, '(({0} - {1}) * {2})'.format(var, x_min[j], round_a_number(X_range[j]/x_range[j], 6)))
                    
                else:
                    func = func.replace(var, '(({0} - {1}) * {3} + {2})'.format(var, x_min[j], X_min[j], round_a_number(X_range[j]/x_range[j], 6)))
                    
            # Scale Y back to the original scale by multiplying by 1/y_scale.
            func_unscaled.append('{0}*({1})'.format(round_a_number(1/y_scale, 6), func))
            
        else:
            func_unscaled.append(func)
            
    func_candidates['Parameterized equation, unscaled'] = func_unscaled
    
    return func_candidates
    


