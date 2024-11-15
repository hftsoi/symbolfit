import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
import matplotlib.colors as mcolors
import seaborn as sns
import textwrap
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="seaborn")
from .utils import *
from .math_defs import *
from .evaluate import *
import scipy
from scipy.interpolate import griddata
from importlib import resources


'''
1D candidate plots
'''

def plot_single_syst_single_func_1D(
    func_candidate,
    candidate_idx,
    x,
    bin_widths_1d,
    y,
    y_up,
    y_down,
    param_shifted,
    logy,
    logx
):
    '''
    Plot a particular candidate function with all parameters at their best-fit values,
    or with one of the parameters in +1 or -1 sigma.
    
    Arguments
    ---------
    func_candidate (pd.dataframe):
        A particular candidate function (one row of the full func_candidates).
        
    candidate_idx (np.int):
        Candidate function # (ranked by function complexity).
    
    x (np.ndarray):
        The independent variable.
        
    y (np.ndarray):
        The dependent variable.
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
        
    param_shifted (str):
        Plot the function with a particular parameter shifted (e.g., 'a3').
    
    logy (bool):
        Plot y in log scale.
    
    logx (bool):
        Plot x in log scale.
    '''
    
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(9,8), gridspec_kw={'height_ratios': [3,1,1]})
    fig.subplots_adjust(hspace = 0.1)
    
    linewidth = 1
    alpha = 0.8
    
    x0 = np.arange(np.min(x), np.max(x), np.abs(np.max(x)-np.min(x))/200)
    
    # Function evaluated with all parameters in their best-fit values (with finer x0).
    central = func_evaluate(func_candidate = func_candidate,
                            x = x0,
                            dim = 1,
                            param_shifted = None,
                            sigma_pm = None
                            )
    
    # Evaluated with one of the parameters shifted up and down separately.
    if param_shifted is not None:
        if func_candidate['Parameters: (best-fit, +1, -1)'][param_shifted][1] > 0:
            up = func_evaluate(func_candidate = func_candidate,
                               x = x0,
                               dim = 1,
                               param_shifted = param_shifted,
                               sigma_pm = '+'
                               )
            
            down = func_evaluate(func_candidate = func_candidate,
                                 x = x0,
                                 dim = 1,
                                 param_shifted = param_shifted,
                                 sigma_pm = '-'
                                 )
    
    # Function evaluated with all parameters in their best-fit values (with the same input x grid).
    # For computing the errors comparing with the input data points directly.
    central_hist = func_evaluate(func_candidate = func_candidate,
                                 x = x,
                                 dim = 1,
                                 param_shifted = None,
                                 sigma_pm = None
                                 )
    
    # Function evaluated with one of the parameters shifted up and down separately (with the same input x grid).
    if param_shifted is not None:
        if func_candidate['Parameters: (best-fit, +1, -1)'][param_shifted][1] > 0:
            up_hist = func_evaluate(func_candidate = func_candidate,
                                    x = x,
                                    dim = 1,
                                    param_shifted = param_shifted,
                                    sigma_pm = '+'
                                    )
            
            down_hist = func_evaluate(func_candidate = func_candidate,
                                      x = x,
                                      dim = 1,
                                      param_shifted = param_shifted,
                                      sigma_pm = '-'
                                      )
    
    
    # Plot the input data in errorbar style if there are uncertainties in y provided,
    # otherwise plot in scatter style.
    if bin_widths_1d is not None:
        bin_widths_1d = np.reshape(np.array(bin_widths_1d), (-1, 1))
        
    if y_up is not None and y_down is not None:
        if bin_widths_1d is not None:
            axes[0].errorbar(x.flatten(),
                             y.flatten(),
                             yerr = [y_down.flatten(), y_up.flatten()],
                             xerr = bin_widths_1d.flatten() / 2,
                             fmt = '.',
                             c = 'black',
                             ecolor = 'grey',
                             capsize = 0,
                             label = 'Data'
                             )
            
        else:
            axes[0].errorbar(x.flatten(),
                             y.flatten(),
                             yerr = [y_down.flatten(), y_up.flatten()],
                             fmt = '.',
                             c = 'black',
                             ecolor = 'grey',
                             capsize = 0,
                             label = 'Data'
                             )
    else:
        axes[0].scatter(x,
                        y,
                        marker = 'o',
                        c = 'black',
                        alpha = 1,
                        label = 'Data'
                        )
                        
    # Plot the candidate function with all parameters in their best-fit values.
    axes[0].plot(x0,
                 central,
                 color = 'r',
                 label = 'Best-fit',
                 linewidth = linewidth,
                 alpha = alpha
                 )
    
    # Plot the candidate function with one of the parameters shifted up and down separately.
    if param_shifted is not None:
        if func_candidate['Parameters: (best-fit, +1, -1)'][param_shifted][1] > 0:
            axes[0].plot(x0,
                         up,
                         color = 'g',
                         label = '{0} Up'.format(param_shifted),
                         linewidth = linewidth,
                         alpha = alpha,
                         linestyle = 'dashed'
                         )
            
            axes[0].plot(x0,
                         down,
                         color = 'b',
                         label = '{0} Down'.format(param_shifted),
                         linewidth = linewidth,
                         alpha = alpha,
                         linestyle = 'dashed'
                         )
            
    axes[0].legend()
    
    # Define a string containing all the parameters in the function with each one in the form of
    # best-fit^{+1 sigma}_{-1 sigma}, with relative % error next to the +/-1 sigma values.
    # Highlight the one that is being shifted.
    parameters_string = ""
    parameters = func_candidate['Parameters: (best-fit, +1, -1)']
    
    for i in range(len(parameters)):
        # If the parameter is held fixed in the fit, it does not have +/-1 sigma values.
        if parameters[f'a{i+1}'][1] == 0:
            if f'a{i+1}' == param_shifted:
                parameters_string += r"$\bf{{{0} = {1}}}$".format(
                    f'a{i+1}',
                    round_a_number(parameters[f'a{i+1}'][0], 6),
                    )
                    
            else:
                parameters_string += r"${0} = {1}$".format(
                    f'a{i+1}',
                    round_a_number(parameters[f'a{i+1}'][0], 6),
                    )
        else:
            if f'a{i+1}' == param_shifted:
                parameters_string += r"$\bf{{{0} = {1}^{{+ {2} ({4}\%) }}_{{- {3} ({5}\%)}}}}$".format(
                    f'a{i+1}',
                    round_a_number(parameters[f'a{i+1}'][0], 6),
                    round_a_number(parameters[f'a{i+1}'][1], 4),
                    round_a_number(np.abs(parameters[f'a{i+1}'][2]), 4),
                    round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][1]) / float(parameters[f'a{i+1}'][0])), 3),
                    round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][2]) / float(parameters[f'a{i+1}'][0])), 3)
                    )
                    
            else:
                parameters_string += r"$\text{{{0}}} = {1}^{{+ {2} ({4}\%) }}_{{- {3} ({5}\%)}}$".format(
                f'a{i+1}',
                round_a_number(parameters[f'a{i+1}'][0], 6),
                round_a_number(parameters[f'a{i+1}'][1], 4),
                round_a_number(np.abs(parameters[f'a{i+1}'][2]), 4),
                round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][1]) / float(parameters[f'a{i+1}'][0])), 3),
                round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][2]) / float(parameters[f'a{i+1}'][0])), 3)
                )
        
        if i < len(parameters) - 1:
            parameters_string += ",  "
            
        if np.mod(i + 1, 2) == 0:
            parameters_string += "\n"
            
    # Print parameter string defined above as title.
    title = textwrap.fill(func_candidate['Parameterized equation, unscaled'], width = 95) + "\n\n" + parameters_string
    axes[0].set_title(title, loc = 'left', size = 9.5)
    
    # Show the candidate # being plotted and some of the gof metrics.
    if y_up is not None and y_down is not None:
        axes[0].set_title(r"$\bfit{{Candidate\,\#{}}}$".format(candidate_idx) + "\n$\\chi^2$/NDF = {0}/{1}, p-value = {3}, RMSE = {2}".format(func_candidate['Chi2'], func_candidate['NDF'], func_candidate['RMSE'], round_a_number(func_candidate['p-value'], 4)), loc = 'right', size = 9.5)
        
    else:
        axes[0].set_title(r"$\bfit{{Candidate\,\#{}}}$".format(candidate_idx) + "\nRMSE = {0}, R2 = {1}".format(func_candidate['RMSE'], func_candidate['R2']), loc = 'right', size = 9.5)

    formatter = ticker.FormatStrFormatter('%.3g')
    
    # Plot a panel showing the difference between the prediction and the input data point, essentially (y_pred - y_label) in sigmas.
    axes[1].plot(x0,
                 np.zeros(central.shape),
                 c = 'black',
                 linestyle = 'dashed',
                 linewidth = linewidth,
                 alpha = 0.5
                 )
    
    if y_up is not None and y_down is not None:
        residual_central = y - central_hist
        
        # Plot the residual error in terms of the input y uncertainties.
        y_unc_central =  np.where(residual_central < 0,
                                  np.where(y_up != 0, y_up, y_down),
                                  np.where(y_down != 0, y_down, y_up)
                                  )
                                  
        if bin_widths_1d is not None:
            axes[1].bar(x.flatten(),
                        (residual_central/y_unc_central).flatten(),
                        width=bin_widths_1d.flatten(),
                        edgecolor='none',
                        color='red',
                        alpha=alpha
                        )
        else:
            axes[1].scatter(x,
                            residual_central/y_unc_central,
                            marker='.',
                            c='r',
                            alpha=alpha
                            )
        
        axes[1].set_ylim(-1.3*max(np.abs(residual_central/y_unc_central)),
                         1.3*max(np.abs(residual_central/y_unc_central))
                         )
        
        # Draw reference lines showing +/-1 sigma.
        #axes[1].plot(x0, np.ones(central.shape).flatten(), c='grey', marker='none', alpha=0.7)
        #axes[1].plot(x0, -np.ones(central.shape).flatten(), c='grey', marker='none', alpha=0.7)
        #axes[1].fill_between(x0.flatten(), np.ones(central.shape).flatten(), -np.ones(central.shape).flatten(), color='grey', alpha=0.15, rasterized=True)
    else:
        if bin_widths_1d is not None:
            axes[1].bar(x.flatten(),
                        (y - central_hist).flatten(),
                        width=bin_widths_1d.flatten(),
                        edgecolor='none',
                        color='red',
                        alpha=alpha
                        )
        
        else:
            axes[1].scatter(x,
                            y - central_hist,
                            marker='.',
                            c='r',
                            alpha=alpha)
                            
            
        axes[1].set_ylim(-1.3*max(np.abs(y - central_hist)),
                         1.3*max(np.abs(y - central_hist))
                         )
    
    # Same residual plot as above but for the function evaluated with one of the parameters shifted.
    if param_shifted is not None:
        if func_candidate['Parameters: (best-fit, +1, -1)'][param_shifted][1] > 0:
            if y_up is not None and y_down is not None:
                residual_up = y - up_hist
                
                y_unc_up =  np.where(residual_up < 0,
                                     np.where(y_up != 0, y_up, y_down),
                                     np.where(y_down != 0, y_down, y_up))
                                     
                residual_down = y - down_hist
                
                y_unc_down =  np.where(residual_down < 0,
                                       np.where(y_up != 0, y_up, y_down),
                                       np.where(y_down != 0, y_down, y_up))
                                       
                #axes[1].scatter(x, residual_up/y_unc_up, marker='.', c='g', alpha=alpha)
                #axes[1].scatter(x, residual_down/y_unc_down, marker='.', c='b', alpha=alpha)
            #else:
                #axes[1].scatter(x, y - up_hist, marker='.', c='g', alpha=alpha)
                #axes[1].scatter(x, y - down_hist, marker='.', c='b', alpha=alpha)
                
    if y_up is not None and y_down is not None:
        #axes[1].plot(x, y_up, marker='none', c='grey', alpha=0.3)
        #axes[1].plot(x, -y_down, marker='none', c='grey', alpha=0.3)
        #axes[1].fill_between(x.flatten(), y_up.flatten(), -y_down.flatten(), color='grey', alpha=0.15)
    #axes[1].legend(loc='upper right', bbox_to_anchor=(1.26, 1))
        axes[1].set_ylabel('$\\frac{\\text{Data}-\\text{Fit}}{\\text{Data unc.}}$', fontsize=15)
        
    else:
        axes[1].set_ylabel('Data$-$Fit')
        
    axes[1].yaxis.set_label_position("right")
    axes[1].yaxis.set_major_formatter(formatter)
    
    # Ratio plot: (function evaluated with one of the parameters shifted) / (function evaluated with all parameters in best-fit).
    # This is to show the uncertainty variations comparing with the central best-fit.
    axes[2].plot(x0, np.ones(central.shape), color='black', linestyle='dashed', linewidth=linewidth, alpha=0.5)
    
    if param_shifted is not None:
        if func_candidate['Parameters: (best-fit, +1, -1)'][param_shifted][1] > 0:
            axes[2].plot(x0,
                         up/central,
                         color = 'g',
                         linewidth = linewidth,
                         alpha = alpha
                         )
                         
            axes[2].plot(x0,
                         down/central,
                         color = 'b',
                         linewidth = linewidth,
                         alpha = alpha
                         )
                         
    #axes[2].legend(loc='upper right', bbox_to_anchor=(1.25, 1))
    axes[2].set_ylabel('$\\frac{\\text{Up or Down}}{\\text{Best-fit}}$', fontsize=15)
    
    axes[2].yaxis.set_label_position("right")
    axes[2].yaxis.set_major_formatter(formatter)
    
    #axes[2].set_ylim(0.5,1.5)
    
    if logy:
        axes[0].set_yscale('log')
        #axes[1].set_yscale('symlog')
        
    if logx:
        axes[0].set_xscale('log')
    
    # Add logo to every plot.
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'img/logo.png'
                             )
    logo_img = mpimg.imread(logo_path)
    
    bbox = axes[0].get_position()
    
    logo_width = 0.13
    logo_height = logo_width * (logo_img.shape[0] / logo_img.shape[1])

    ax_inset = fig.add_axes([bbox.x0 +0.73,
                            bbox.y1 + 0.085,
                            logo_width,
                            logo_height]
                            )

    ax_inset.imshow(logo_img)
    ax_inset.axis('off')
    
    plt.tight_layout()
                

def plot_all_syst_all_func_1D(
    func_candidates,
    x,
    bin_widths_1d,
    y,
    y_up,
    y_down,
    pdf_path,
    logy,
    logx
):
    '''
    Plot all candidate functions, each with all possible parameter variations.
    
    Arguments
    ---------
    func_candidates (pd.dataframe):
        Full dataframe containing all candidate functions after fits.
    
    x (np.ndarray):
        The independent variable.
        
    y (np.ndarray):
        The dependent variable.
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
        
    pdf_path (str):
        Save the output files to this directory.
    
    logy (bool):
        Plot y in log scale.
    
    logx (bool):
        Plot x in log scale.
    
    
    Returns
    -------
    Plot all candidate functions with all parameter variations and write to an output file.
    '''
    
    with PdfPages(pdf_path) as pdf:
        for i in range(len(func_candidates)):
            # Print candidate # page.
            fig, axes = plt.subplots(figsize = (9, 7))
            axes.axis('off')
            plt.text(0.5,
                     0.5,
                     'Candidate function #{}'.format(len(func_candidates) - 1 - i),
                     fontsize = 20,
                     ha = 'center',
                     va = 'center'
                     )
                     
            plt.tight_layout()
            
            plt.savefig(pdf, format = 'pdf')
            
            plt.close()
            
            if i < len(func_candidates) - 1:
                print('Plotting candidate functions {0}/{1} >>> {2}'.format(i+1, len(func_candidates), pdf_path), end='\r')
                
            else:
                print('Plotting candidate functions {0}/{1} >>> {2}'.format(i+1, len(func_candidates), pdf_path))
                
            func_candidate = func_candidates.iloc[len(func_candidates) - 1 - i]
            
            if len(func_candidate['Parameters: (best-fit, +1, -1)']) > 0:
                # Check if the function has any parameter that has variations.
                has_uncert = False
                
                for j in range(len(func_candidate['Parameters: (best-fit, +1, -1)'])):
                    if func_candidate['Parameters: (best-fit, +1, -1)'][f'a{j+1}'][1] > 0:
                        has_uncert = True

                # Plot central, up, and down in the same plot, otherwise plot only the central.
                if has_uncert:
                    for j in range(len(func_candidate['Parameters: (best-fit, +1, -1)'])):
                        if func_candidate['Parameters: (best-fit, +1, -1)'][f'a{j+1}'][1] > 0:
                            plot_single_syst_single_func_1D(func_candidate = func_candidate,
                                                            candidate_idx = len(func_candidates) - 1 - i,
                                                            x = x,
                                                            bin_widths_1d = bin_widths_1d,
                                                            y = y,
                                                            y_up = y_up,
                                                            y_down = y_down,
                                                            param_shifted = f'a{j+1}',
                                                            logy = logy,
                                                            logx = logx
                                                            )
                            
                            plt.savefig(pdf, format='pdf')
                            plt.close()
                            
                else:
                    plot_single_syst_single_func_1D(func_candidate = func_candidate,
                                                    candidate_idx = len(func_candidates) - 1 - i,
                                                    x = x,
                                                    bin_widths_1d = bin_widths_1d,
                                                    y = y,
                                                    y_up = y_up,
                                                    y_down = y_down,
                                                    param_shifted = None,
                                                    logy = logy,
                                                    logx = logx
                                                    )
                    
                    plt.savefig(pdf, format='pdf')
                    plt.close()
                    
            else:
                plot_single_syst_single_func_1D(func_candidate = func_candidate,
                                                candidate_idx = len(func_candidates) - 1 - i,
                                                x = x,
                                                bin_widths_1d = bin_widths_1d,
                                                y = y,
                                                y_up = y_up,
                                                y_down = y_down,
                                                param_shifted = None,
                                                logy = logy,
                                                logx = logx
                                                )
                
                plt.savefig(pdf, format='pdf')
                plt.close()
                
                
'''
Monte Carlo sampling
'''

def plot_total_unc_coverage_single_func_1D(
    func_candidate,
    candidate_idx,
    x,
    bin_widths_1d,
    y,
    y_up,
    y_down,
    n_samples,
    sampling_95quantile,
    logy,
    logx
):
    '''
    Plot a particular candidate function with total uncertainty coverage.
    The coverage is computed from an ensemble of functions where the parameters
    are sampled from the multivariate normal distribution according to the
    best-fit parameter values and the covariance matrix.
    
    Arguments
    ---------
    func_candidate (pd.dataframe):
        A particular candidate function (one row of the full func_candidates).
        
    candidate_idx (np.int):
        Candidate function # (ranked by function complexity).
    
    x (np.ndarray):
        The independent variable.
        
    y (np.ndarray):
        The dependent variable.
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
        
    n_samples (int):
        Number of samples to be drawn from the multivariate normal distribution.
    
    logy (bool):
        Plot y in log scale.
    
    logx (bool):
        Plot x in log scale.
    '''
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(9,8), gridspec_kw={'height_ratios': [3,1,1]})
    fig.subplots_adjust(hspace = 0.1)
    
    linewidth = 1
    alpha = 0.8
    
    x0 = np.arange(np.min(x), np.max(x), np.abs(np.max(x)-np.min(x))/200)
    
    if n_samples is not None:
        func_bands, func_bands_finer = func_sampling_1d(func_str = func_candidate['Parameterized equation, unscaled'],
                                                                 param = func_candidate['Parameters: (best-fit, +1, -1)'],
                                                                 cov = func_candidate['Covariance'],
                                                                 x = x,
                                                                 x_finer = x0,
                                                                 n_samples = n_samples
                                                                 )
                                                                 
        (mean_func, lower_2sigma, lower_1sigma, upper_1sigma, upper_2sigma) = func_bands
        (mean_func_finer, lower_2sigma_finer, lower_1sigma_finer, upper_1sigma_finer, upper_2sigma_finer) = func_bands_finer
        
        axes[0].plot(x0, mean_func_finer, label = 'Sample mean', color = 'red')
        
        axes[0].fill_between(x0,
                             lower_1sigma_finer,
                             upper_1sigma_finer,
                             color = 'limegreen',
                             alpha = 0.5,
                             label = '68% quantile range'
                             )
        
        if sampling_95quantile:
            axes[0].fill_between(x0,
                                 lower_2sigma_finer,
                                 lower_1sigma_finer,
                                 color = 'gold',
                                 alpha = 0.5
                                 )
                             
            axes[0].fill_between(x0,
                                 upper_1sigma_finer,
                                 upper_2sigma_finer,
                                 color = 'gold',
                                 alpha = 0.5,
                                 label = '95% quantile range'
                                 )
                             
    else:
        # Function evaluated with all parameters in their best-fit values (with finer x0).
        central = func_evaluate(func_candidate = func_candidate,
                                x = x0,
                                dim = 1,
                                param_shifted = None,
                                sigma_pm = None
                                )
                                
        # Function evaluated with all parameters in their best-fit values (with the same input x grid).
        # For computing the errors comparing with the input data points directly.
        central_hist = func_evaluate(func_candidate = func_candidate,
                                    x = x,
                                    dim = 1,
                                    param_shifted = None,
                                    sigma_pm = None
                                    )
                                    
        axes[0].plot(x0,
                    central,
                    color = 'r',
                    label = 'Best-fit',
                    linewidth = linewidth,
                    alpha = alpha
                    )
    
    # Plot the input data in errorbar style if there are uncertainties in y provided,
    # otherwise plot in scatter style.
    if bin_widths_1d is not None:
        bin_widths_1d = np.reshape(np.array(bin_widths_1d), (-1, 1))
        
    if y_up is not None and y_down is not None:
        if bin_widths_1d is not None:
            axes[0].errorbar(x.flatten(),
                             y.flatten(),
                             yerr = [y_down.flatten(), y_up.flatten()],
                             xerr = bin_widths_1d.flatten() / 2,
                             fmt = '.',
                             c = 'black',
                             ecolor = 'grey',
                             capsize = 0,
                             label = 'Data'
                             )
            
        else:
            axes[0].errorbar(x.flatten(),
                             y.flatten(),
                             yerr = [y_down.flatten(), y_up.flatten()],
                             fmt = '.',
                             c = 'black',
                             ecolor = 'grey',
                             capsize = 0,
                             label = 'Data'
                             )
    else:
        axes[0].scatter(x,
                        y,
                        marker = 'o',
                        c = 'black',
                        alpha = 1,
                        label = 'Data'
                        )
                        
            
    axes[0].legend()
    
    # Define a string containing all the parameters in the function with each one in the form of
    # best-fit^{+1 sigma}_{-1 sigma}, with relative % error next to the +/-1 sigma values.
    # Highlight the one that is being shifted.
    parameters_string = ""
    parameters = func_candidate['Parameters: (best-fit, +1, -1)']
    
    for i in range(len(parameters)):
        # If the parameter is held fixed in the fit, it does not have +/-1 sigma values.
        if parameters[f'a{i+1}'][1] == 0:
            parameters_string += r"${0} = {1}$".format(
                f'a{i+1}',
                round_a_number(parameters[f'a{i+1}'][0], 6),
                )
                
        else:
            parameters_string += r"$\text{{{0}}} = {1}^{{+ {2} ({4}\%) }}_{{- {3} ({5}\%)}}$".format(
            f'a{i+1}',
            round_a_number(parameters[f'a{i+1}'][0], 6),
            round_a_number(parameters[f'a{i+1}'][1], 4),
            round_a_number(np.abs(parameters[f'a{i+1}'][2]), 4),
            round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][1]) / float(parameters[f'a{i+1}'][0])), 3),
            round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][2]) / float(parameters[f'a{i+1}'][0])), 3)
            )
        
        if i < len(parameters) - 1:
            parameters_string += ",  "
            
        if np.mod(i + 1, 2) == 0:
            parameters_string += "\n"
            
    # Print parameter string defined above as title.
    title = textwrap.fill(func_candidate['Parameterized equation, unscaled'], width = 95) + "\n\n" + parameters_string
    axes[0].set_title(title, loc = 'left', size = 9.5)
    
    # Show the candidate # being plotted and some of the gof metrics.
    if n_samples is not None:
        axes[0].set_title(r"$\bfit{{Candidate\,\#{}}}$".format(candidate_idx) + "\nEnsemble of functions generated by sampling parameters", loc = 'right', size = 9.5)
    else:
        axes[0].set_title(r"$\bfit{{Candidate\,\#{}}}$".format(candidate_idx) + "\n", loc = 'right', size = 9.5)

    formatter = ticker.FormatStrFormatter('%.3g')
    
    # Plot a panel showing the difference between the prediction and the input data point, essentially (y_pred - y_label) in sigmas.
    axes[1].plot(x0,
                 np.zeros(x0.shape),
                 c = 'black',
                 linestyle = 'dashed',
                 linewidth = linewidth,
                 alpha = 0.5
                 )
    
    if y_up is not None and y_down is not None:
        if n_samples is not None:
            residual_mean = y - mean_func
            residual_upper_1sigma = y - upper_1sigma
            residual_lower_1sigma = y - lower_1sigma
            
            if sampling_95quantile:
                residual_upper_2sigma = y - upper_2sigma
                residual_lower_2sigma = y - lower_2sigma
            
        else:
            residual_mean = y - central_hist
        
        # Plot the residual error in terms of the input y uncertainties.
        y_unc_mean =  np.where(residual_mean < 0,
                               np.where(y_up != 0, y_up, y_down),
                               np.where(y_down != 0, y_down, y_up)
                               )
                               
        if n_samples is not None:
            y_unc_upper_1sigma = np.where(residual_upper_1sigma < 0,
                                          np.where(y_up != 0, y_up, y_down),
                                          np.where(y_down != 0, y_down, y_up)
                                          )
                                          
            y_unc_lower_1sigma = np.where(residual_lower_1sigma < 0,
                                          np.where(y_up != 0, y_up, y_down),
                                          np.where(y_down != 0, y_down, y_up)
                                          )
                                          
            if sampling_95quantile:
                y_unc_upper_2sigma = np.where(residual_upper_2sigma < 0,
                                              np.where(y_up != 0, y_up, y_down),
                                              np.where(y_down != 0, y_down, y_up)
                                              )
                                              
                y_unc_lower_2sigma = np.where(residual_lower_2sigma < 0,
                                              np.where(y_up != 0, y_up, y_down),
                                              np.where(y_down != 0, y_down, y_up)
                                              )
                                  
        if bin_widths_1d is not None:
            if n_samples is not None:
                for i in range(x.size):
                    axes[1].hlines((residual_mean/y_unc_mean).flatten()[i],
                                   xmin=x[i] - bin_widths_1d[i] / 2,
                                   xmax=x[i] + bin_widths_1d[i] / 2,
                                   color='red',
                                   linewidth=1.5
                                   )
                
                axes[1].bar(x.flatten(),
                            (residual_lower_1sigma/y_unc_lower_1sigma - residual_mean/y_unc_mean).flatten(),
                            width = bin_widths_1d.flatten(),
                            bottom = (residual_mean/y_unc_mean).flatten(),
                            color = 'limegreen',
                            edgecolor = 'none',
                            alpha = 0.5,
                            )
                            
                axes[1].bar(x.flatten(),
                            (residual_upper_1sigma/y_unc_upper_1sigma - residual_mean/y_unc_mean).flatten(),
                            width = bin_widths_1d.flatten(),
                            bottom = (residual_mean/y_unc_mean).flatten(),
                            color = 'limegreen',
                            edgecolor = 'none',
                            alpha = 0.5,
                            )
                            
                if sampling_95quantile:
                    axes[1].bar(x.flatten(),
                                (- residual_lower_1sigma/y_unc_lower_1sigma + residual_lower_2sigma/y_unc_lower_2sigma).flatten(),
                                width = bin_widths_1d.flatten(),
                                bottom = (residual_lower_1sigma/y_unc_lower_1sigma).flatten(),
                                color = 'gold',
                                edgecolor = 'none',
                                alpha = 0.5,
                                )
                                
                    axes[1].bar(x.flatten(),
                                (residual_upper_2sigma/y_unc_upper_2sigma - residual_upper_1sigma/y_unc_upper_1sigma).flatten(),
                                width = bin_widths_1d.flatten(),
                                bottom = (residual_upper_1sigma/y_unc_upper_1sigma).flatten(),
                                color = 'gold',
                                edgecolor = 'none',
                                alpha = 0.5,
                                )
            
            else:
                axes[1].bar(x.flatten(),
                            (residual_mean/y_unc_mean).flatten(),
                            width=bin_widths_1d.flatten(),
                            edgecolor='none',
                            color='red',
                            alpha=alpha
                            )
            
                        
        else:
            axes[1].scatter(x,
                            residual_mean/y_unc_mean,
                            marker='.',
                            c='r',
                            alpha=alpha
                            )
        
        if n_samples is not None:
            if sampling_95quantile:
                axes[1].set_ylim(-1.1*np.max(np.maximum(np.abs(residual_lower_2sigma/y_unc_lower_2sigma),
                                                         np.abs(residual_upper_2sigma/y_unc_upper_2sigma))
                                             ),
                                 1.1*np.max(np.maximum(np.abs(residual_lower_2sigma/y_unc_lower_2sigma),
                                                        np.abs(residual_upper_2sigma/y_unc_upper_2sigma))
                                            )
                                )
                                
            else:
                axes[1].set_ylim(-1.1*np.max(np.maximum(np.abs(residual_lower_1sigma/y_unc_lower_1sigma),
                                                         np.abs(residual_upper_1sigma/y_unc_upper_1sigma))
                                             ),
                                 1.1*np.max(np.maximum(np.abs(residual_lower_1sigma/y_unc_lower_1sigma),
                                                        np.abs(residual_upper_1sigma/y_unc_upper_1sigma))
                                            )
                                )
                            
        else:
            axes[1].set_ylim(-1.3*max(np.abs(residual_mean/y_unc_mean)),
                             1.3*max(np.abs(residual_mean/y_unc_mean))
                             )
        
        
    else:
        if n_samples is not None:
            residual_mean = y - mean_func
            
        else:
            residual_mean = y - central_hist
            
        if bin_widths_1d is not None:
            axes[1].bar(x.flatten(),
                        residual_mean.flatten(),
                        width=bin_widths_1d.flatten(),
                        edgecolor='none',
                        color='red',
                        alpha=alpha
                        )
        
        else:
            axes[1].scatter(x,
                            residual_mean,
                            marker='.',
                            c='r',
                            alpha=alpha)
                            
            
        axes[1].set_ylim(-1.3*max(np.abs(residual_mean)),
                         1.3*max(np.abs(residual_mean))
                         )
                
    if y_up is not None and y_down is not None:
        axes[1].set_ylabel('$\\frac{\\text{Data}-\\text{Mean}}{\\text{Data unc.}}$', fontsize=15)
        
    else:
        axes[1].set_ylabel('Data$-$Fit')
        
    axes[1].yaxis.set_label_position("right")
    axes[1].yaxis.set_major_formatter(formatter)
    
    # Ratio plot: (function evaluated with one of the parameters shifted) / (function evaluated with all parameters in best-fit).
    # This is to show the uncertainty variations comparing with the central best-fit.
    axes[2].plot(x0, np.ones(x0.shape), color='black', linestyle='dashed', linewidth=linewidth, alpha=0.5)
    
    if n_samples is not None:
        axes[2].plot(x0,
                     upper_1sigma_finer/mean_func_finer,
                     color = 'limegreen',
                     linewidth = linewidth,
                     alpha = 1
                     )
                     
        axes[2].plot(x0,
                     lower_1sigma_finer/mean_func_finer,
                     color = 'limegreen',
                     linewidth = linewidth,
                     alpha = 1
                     )
                     
        if sampling_95quantile:
            axes[2].plot(x0,
                         upper_2sigma_finer/mean_func_finer,
                         color = 'gold',
                         linewidth = linewidth,
                         alpha = 1
                         )
                         
            axes[2].plot(x0,
                         lower_2sigma_finer/mean_func_finer,
                         color = 'gold',
                         linewidth = linewidth,
                         alpha = 1
                         )
                         
    #axes[2].legend(loc='upper right', bbox_to_anchor=(1.25, 1))
    axes[2].set_ylabel('$\\frac{\\text{Quantile range}}{\\text{Mean}}$', fontsize=15)
    
    axes[2].yaxis.set_label_position("right")
    axes[2].yaxis.set_major_formatter(formatter)
    
    #axes[2].set_ylim(0.5,1.5)
    
    if logy:
        axes[0].set_yscale('log')
        #axes[1].set_yscale('symlog')
        
    if logx:
        axes[0].set_xscale('log')
    
    # Add logo to every plot.
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'img/logo.png'
                             )
    logo_img = mpimg.imread(logo_path)
    
    bbox = axes[0].get_position()
    
    logo_width = 0.13
    logo_height = logo_width * (logo_img.shape[0] / logo_img.shape[1])

    ax_inset = fig.add_axes([bbox.x0 +0.73,
                            bbox.y1 + 0.085,
                            logo_width,
                            logo_height]
                            )

    ax_inset.imshow(logo_img)
    ax_inset.axis('off')
    
    plt.tight_layout()
                

def plot_total_unc_coverage_all_func_1D(
    func_candidates,
    x,
    bin_widths_1d,
    y,
    y_up,
    y_down,
    n_samples,
    sampling_95quantile,
    pdf_path,
    logy,
    logx
):
    '''
    Plot all candidate functions with total uncertainty coverage.
    The coverage is computed from an ensemble of functions where the parameters
    are sampled from the multivariate normal distribution according to the
    best-fit parameter values and the covariance matrix.
    
    Arguments
    ---------
    func_candidates (pd.dataframe):
        Full dataframe containing all candidate functions after fits.
    
    x (np.ndarray):
        The independent variable.
        
    y (np.ndarray):
        The dependent variable.
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
        
    n_samples (int):
        Number of samples to be drawn from the multivariate normal distribution.
        
    pdf_path (str):
        Save the output files to this directory.
    
    logy (bool):
        Plot y in log scale.
    
    logx (bool):
        Plot x in log scale.
    
    
    Returns
    -------
    Plot all candidate functions with total unc coverage and write to an output file.
    '''
    
    with PdfPages(pdf_path) as pdf:
        for i in range(len(func_candidates)):
            # Print candidate # page.
            fig, axes = plt.subplots(figsize = (9, 7))
            axes.axis('off')
            plt.text(0.5,
                     0.5,
                     'Candidate function #{}'.format(len(func_candidates) - 1 - i),
                     fontsize = 20,
                     ha = 'center',
                     va = 'center'
                     )
                     
            plt.tight_layout()
            
            plt.savefig(pdf, format = 'pdf')
            
            plt.close()
            
            if i < len(func_candidates) - 1:
                print('Plotting candidate functions (sampling parameters) {0}/{1} >>> {2}'.format(i+1, len(func_candidates), pdf_path), end='\r')
                
            else:
                print('Plotting candidate functions (sampling parameters) {0}/{1} >>> {2}'.format(i+1, len(func_candidates), pdf_path))
                
            func_candidate = func_candidates.iloc[len(func_candidates) - 1 - i]
            
            if len(func_candidate['Parameters: (best-fit, +1, -1)']) > 0:
                # Check if the function has any parameter that has variations.
                has_uncert = False
                
                for j in range(len(func_candidate['Parameters: (best-fit, +1, -1)'])):
                    if func_candidate['Parameters: (best-fit, +1, -1)'][f'a{j+1}'][1] > 0:
                        has_uncert = True

                if has_uncert:
                    try:
                        plot_total_unc_coverage_single_func_1D(func_candidate = func_candidate,
                                                               candidate_idx = len(func_candidates) - 1 - i,
                                                               x = x,
                                                               bin_widths_1d = bin_widths_1d,
                                                               y = y,
                                                               y_up = y_up,
                                                               y_down = y_down,
                                                               n_samples = n_samples,
                                                               sampling_95quantile = sampling_95quantile,
                                                               logy = logy,
                                                               logx = logx
                                                               )
                                                               
                    except:
                        plot_total_unc_coverage_single_func_1D(func_candidate = func_candidate,
                                                               candidate_idx = len(func_candidates) - 1 - i,
                                                               x = x,
                                                               bin_widths_1d = bin_widths_1d,
                                                               y = y,
                                                               y_up = y_up,
                                                               y_down = y_down,
                                                               n_samples = None,
                                                               sampling_95quantile = False,
                                                               logy = logy,
                                                               logx = logx
                                                               )
                    
                    plt.savefig(pdf, format='pdf')
                    plt.close()
                        
                else:
                    plot_total_unc_coverage_single_func_1D(func_candidate = func_candidate,
                                                           candidate_idx = len(func_candidates) - 1 - i,
                                                           x = x,
                                                           bin_widths_1d = bin_widths_1d,
                                                           y = y,
                                                           y_up = y_up,
                                                           y_down = y_down,
                                                           n_samples = None,
                                                           sampling_95quantile = False,
                                                           logy = logy,
                                                           logx = logx
                                                           )
                    
                    plt.savefig(pdf, format='pdf')
                    plt.close()
                
            else:
                plot_total_unc_coverage_single_func_1D(func_candidate = func_candidate,
                                                       candidate_idx = len(func_candidates) - 1 - i,
                                                       x = x,
                                                       bin_widths_1d = bin_widths_1d,
                                                       y = y,
                                                       y_up = y_up,
                                                       y_down = y_down,
                                                       n_samples = None,
                                                       sampling_95quantile = False,
                                                       logy = logy,
                                                       logx = logx
                                                       )
                
                plt.savefig(pdf, format='pdf')
                plt.close()


'''
2D candidate plots
'''

def plot_single_syst_single_func_2D(
    func_candidate,
    candidate_idx,
    x,
    bin_edges_2d,
    y,
    y_up,
    y_down,
    param_shifted,
    logx0,
    logx1,
    logy,
    cbar_min,
    cbar_max,
    cmap,
    contour,
):
    '''
    Plot a particular candidate function with all parameters at their best-fit values,
    or with one of the parameters in +1 or -1 sigma.
    
    Arguments
    ---------
    func_candidate (pd.dataframe):
        A particular candidate function (one row of the full func_candidates).
        
    candidate_idx (np.int):
        Candidate function # (ranked by function complexity).
    
    x (np.ndarray):
        The independent variable.
        
    y (np.ndarray):
        The dependent variable.
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
        
    param_shifted (str):
        Plot the function with a particular parameter shifted (e.g., 'a3').
    
    logx0 (bool):
        Plot x0 in log scale.
    
    logx1 (bool):
        Plot x1 in log scale.
        
    logy (bool):
        Plot y in log scale.
        
    cbar_min (float):
        Plot color bar with min value.
        
    cbar_max (float):
        Plot color bar with max value.
        
    cmap (str):
        Plot color bar with matplotlib cmap style.
        
    contour (float):
        Plot contour line to 2D plots.
    
    
    Returns
    -------
    Plot the candidate function.
    '''
    
    fig, axes = plt.subplots(2, 2, sharex = True, sharey = True, figsize = (9, 7),
                             gridspec_kw = {'width_ratios': [1, 1], 'height_ratios': [1, 1]}
                             )
    #fig.subplots_adjust(hspace = 0.1)
    alpha = 1
    cbar_fontsize = 14
    label_fontsize = 12
    
    x0_bins = np.reshape(np.array(bin_edges_2d[0]), (-1))
    x1_bins = np.reshape(np.array(bin_edges_2d[1]), (-1))
    
    if cbar_min is None:
        cbar_min = min(y)
    if cbar_max is None:
        cbar_max = max(y)
    
    if cmap is None:
        cmap = 'Greens'
    
    '''
    # Plot input.
    fig_data = axes[0,0].hist2d(x[:,0],
                                x[:,1],
                                bins = [x0_bins, x1_bins],
                                weights = np.squeeze(y),
                                cmap = cmap,
                                edgecolor = 'none',
                                rasterized = True,
                                vmin = cbar_min,
                                vmax = cbar_max
                                )
                                
    cbar_data = plt.colorbar(fig_data[3], ax=axes[0,0], pad=0, label='Data')
    '''
    
    hist, x_edges, y_edges = np.histogram2d(
    np.array(x)[:, 0], np.array(x)[:, 1],
    bins=[x0_bins, x1_bins], weights=np.squeeze(y))

    # Mask bins with no data points
    #bin_has_data = hist > 0
    #hist_masked = np.ma.masked_where(~bin_has_data, hist)
    
    hist_masked = np.ma.masked_where(hist == 0, hist)

    cmap = plt.get_cmap(cmap).copy()
    cmap.set_bad(color='white')

    # Plot using pcolormesh
    if logy:
        mesh = axes[0,0].pcolormesh(
            x_edges, y_edges, hist_masked.T,
            cmap=cmap, rasterized=True, edgecolor = 'grey', linewidth = 0.5,
            norm=mcolors.LogNorm(vmin=cbar_min, vmax=cbar_max)
        )
    else:
        mesh = axes[0,0].pcolormesh(
            x_edges, y_edges, hist_masked.T,
            cmap=cmap, rasterized=True, edgecolor = 'grey', linewidth = 0.5,
            vmin=cbar_min, vmax=cbar_max
        )
                                
    cbar_data = plt.colorbar(mesh, ax=axes[0,0], pad=0, label='Data')
    
    
    cbar_data.ax.yaxis.label.set_size(cbar_fontsize)
    
    if contour is not None:
        X, Y = np.meshgrid(x_edges, y_edges)
        axes[0,0].contour(
            X[:-1, :-1], Y[:-1, :-1], hist_masked.T,
            levels=[contour], colors='red'
        )
    
    axes[0,0].set_xlabel('x0', fontsize = label_fontsize)
    axes[0,0].set_ylabel('x1', fontsize = label_fontsize)
    
    if logx0:
        axes[0,0].set_xscale('log')
    if logx1:
        axes[0,0].set_yscale('log')
    if logy:
        cbar_data.set_ticks(ticker.LogLocator())
        cbar_data.update_ticks()

    
    # Evaluate the candidate function in finer bins
    x0_nbins = 200
    x1_nbins = 200
    
    x0_range = np.linspace(min(x0_bins), max(x0_bins), x0_nbins)
    x1_range = np.linspace(min(x1_bins), max(x1_bins), x1_nbins)
    
    x0_smooth, x1_smooth = np.meshgrid(x0_range, x1_range)
    
    x_smooth = np.column_stack((x0_smooth.flatten(), x1_smooth.flatten()))
    
    central_smooth = func_evaluate(func_candidate = func_candidate,
                                   x = x_smooth,
                                   dim = 2,
                                   param_shifted = None,
                                   sigma_pm = None
                                   )
    
    # Plot the candidate function (smooth)
    if logy:
        fig_fitted_smooth = axes[0,1].hist2d(x_smooth[:,0],
                                             x_smooth[:,1],
                                             bins = (x0_nbins, x1_nbins),
                                             weights = np.squeeze(central_smooth),
                                             cmap = cmap,
                                             edgecolor = 'none',
                                             rasterized = True,
                                             norm = mcolors.LogNorm(vmin=cbar_min, vmax=cbar_max)
                                             )
    else:
        fig_fitted_smooth = axes[0,1].hist2d(x_smooth[:,0],
                                             x_smooth[:,1],
                                             bins = (x0_nbins, x1_nbins),
                                             weights = np.squeeze(central_smooth),
                                             cmap = cmap,
                                             edgecolor = 'none',
                                             rasterized = True,
                                             vmin = cbar_min,
                                             vmax = cbar_max
                                             )
    
    cbar_fitted_smooth = plt.colorbar(fig_fitted_smooth[3], ax=axes[0,1], pad=0, label='Fit (finer binning)')
    
    cbar_fitted_smooth.ax.yaxis.label.set_size(cbar_fontsize)
    
    if contour is not None:
        axes[0,1].contour(
            x0_smooth, x1_smooth, central_smooth.reshape(x0_nbins, x1_nbins),
            levels=[contour], colors='red'
        )
    
    axes[0,1].set_xlabel('x0', fontsize = label_fontsize)
    axes[0,1].set_ylabel('x1', fontsize = label_fontsize)
    
    if logx0:
        axes[0,1].set_xscale('log')
    if logx1:
        axes[0,1].set_yscale('log')
    if logy:
        cbar_fitted_smooth.set_ticks(ticker.LogLocator())
        cbar_fitted_smooth.update_ticks()
    
    # Compute the candidate function and the error in original bins
    central_hist = func_evaluate(func_candidate = func_candidate,
                                 x = x,
                                 dim = 2,
                                 param_shifted = None,
                                 sigma_pm = None
                                 )
    
    central_error = y - central_hist
    
    if y_up is not None and y_down is not None:
        y_unc =  np.where(central_error < 0,
                          np.where(y_up != 0, y_up, y_down),
                          np.where(y_down != 0, y_down, y_up)
                          )
                          
        central_error = central_error / y_unc

    x0_centers = (x0_bins[:-1] + x0_bins[1:]) / 2
    x1_centers = (x1_bins[:-1] + x1_bins[1:]) / 2

    # Create a meshgrid of all possible bin centers.
    x0_mesh, x1_mesh = np.meshgrid(x0_centers, x1_centers)

    # Flatten the meshgrid to create a full set of bin centers.
    x_full = np.column_stack((x0_mesh.flatten(), x1_mesh.flatten()))
    
    central_hist_full = func_evaluate(func_candidate = func_candidate,
                                      x = x_full,
                                      dim = 2,
                                      param_shifted = None,
                                      sigma_pm = None
                                      )
    
    
    # Plot the candidate function in original bins
    if logy:
        fig_fitted_hist = axes[1,0].hist2d(x_full[:,0],
                                           x_full[:,1],
                                           bins = [x0_bins, x1_bins],
                                           weights = np.squeeze(central_hist_full),
                                           cmap = cmap,
                                           edgecolor = 'grey',
                                           linewidth = 0.5,
                                           rasterized = True,
                                           norm=mcolors.LogNorm(vmin=cbar_min, vmax=cbar_max)
                                           )
    else:
        fig_fitted_hist = axes[1,0].hist2d(x_full[:,0],
                                           x_full[:,1],
                                           bins = [x0_bins, x1_bins],
                                           weights = np.squeeze(central_hist_full),
                                           cmap = cmap,
                                           edgecolor = 'grey',
                                           linewidth = 0.5,
                                           rasterized = True,
                                           vmin = cbar_min,
                                           vmax = cbar_max
                                           )
    
    cbar_fitted_hist = plt.colorbar(fig_fitted_hist[3], ax=axes[1,0], pad=0, label='Fit (same binning as Data)')
    
    cbar_fitted_hist.ax.yaxis.label.set_size(cbar_fontsize)
    
    if contour is not None:
        axes[1,0].contour(
            x0_mesh, x1_mesh, central_hist_full.reshape(x1_bins.size-1, x0_bins.size-1),
            levels=[contour], colors='red'
        )

    axes[1,0].set_xlabel('x0', fontsize = label_fontsize)
    axes[1,0].set_ylabel('x1', fontsize = label_fontsize)
    
    if logx0:
        axes[1,0].set_xscale('log')
    if logx1:
        axes[1,0].set_yscale('log')
    if logy:
        cbar_fitted_hist.set_ticks(ticker.LogLocator())
        cbar_fitted_hist.update_ticks()

    # Plot the error in sigmas in original bins.
    fig_error = axes[1,1].hist2d(x[:,0],
                                 x[:,1],
                                 bins = [x0_bins, x1_bins],
                                 weights = np.squeeze(central_error),
                                 cmap = 'bwr',
                                 vmin = -max(np.abs(central_error)),
                                 vmax = max(np.abs(central_error)),
                                 edgecolor = 'none',
                                 rasterized = True
                                 )
    
    if y_up is not None and y_down is not None:
        cbar_error = plt.colorbar(fig_error[3],
                                  ax = axes[1,1],
                                  pad = 0,
                                  label = '$\\frac{\\text{Data}-\\text{Fit}}{\\text{Data unc.}}$'
                                  )
        
    else:
        cbar_error = plt.colorbar(fig_error[3],
                                  ax = axes[1,1],
                                  pad = 0,
                                  label = '$\\text{Data}-\\text{Fit}$'
                                  )
                                  
    cbar_error.ax.yaxis.label.set_size(cbar_fontsize)
    
    axes[1,1].set_xlabel('x0', fontsize = label_fontsize)
    axes[1,1].set_ylabel('x1', fontsize = label_fontsize)
    
    if logx0:
        axes[1,1].set_xscale('log')
    if logx1:
        axes[1,1].set_yscale('log')
    
    
    # Define a string containing all the parameters in the function with each one in the form of
    # best-fit^{+1 sigma}_{-1 sigma}, with relative % error next to the +/-1 sigma values.
    # Highlight the one that is being shifted.
    parameters_string = ""
    
    parameters = func_candidate['Parameters: (best-fit, +1, -1)']
    
    for i in range(len(parameters)):
        # If the parameter is held fixed in the fit, it does not have +/-1 sigma values.
        if parameters[f'a{i+1}'][1] == 0:
            if f'a{i+1}' == param_shifted:
                parameters_string += r"$\bf{{{0} = {1}}}$".format(
                    f'a{i+1}',
                    round_a_number(parameters[f'a{i+1}'][0], 6),
                    )
                    
            else:
                parameters_string += r"${0} = {1}$".format(
                    f'a{i+1}',
                    round_a_number(parameters[f'a{i+1}'][0], 6),
                    )
                    
        else:
            if f'a{i+1}' == param_shifted:
                parameters_string += r"$\bf{{{0} = {1}^{{+ {2} ({4}\%) }}_{{- {3} ({5}\%)}}}}$".format(
                    f'a{i+1}',
                    round_a_number(parameters[f'a{i+1}'][0], 6),
                    round_a_number(parameters[f'a{i+1}'][1], 4),
                    round_a_number(np.abs(parameters[f'a{i+1}'][2]), 4),
                    round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][1]) / float(parameters[f'a{i+1}'][0])), 3),
                    round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][2]) / float(parameters[f'a{i+1}'][0])), 3)
                    )
                    
            else:
                parameters_string += r"$\text{{{0}}} = {1}^{{+ {2} ({4}\%) }}_{{- {3} ({5}\%)}}$".format(
                f'a{i+1}',
                round_a_number(parameters[f'a{i+1}'][0], 6),
                round_a_number(parameters[f'a{i+1}'][1], 4),
                round_a_number(np.abs(parameters[f'a{i+1}'][2]), 4),
                round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][1]) / float(parameters[f'a{i+1}'][0])), 3),
                round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][2]) / float(parameters[f'a{i+1}'][0])), 3)
                )
        
        if i < len(parameters) - 1:
            parameters_string += ",  "
            
        if np.mod(i + 1, 2) == 0:
            parameters_string += "\n"
            
    # Print parameter string defined above as title.
    title = textwrap.fill(func_candidate['Parameterized equation, unscaled'], width = 95) + "\n\n" + parameters_string
    
    axes[0,0].set_title(title, loc = 'left', size = 9.5)
    
    # Show the candidate # being plotted and some of the gof metrics.
    if y_up is not None and y_down is not None:
        axes[0,1].set_title(r"$\bfit{{Candidate\,\#{}}}$".format(candidate_idx) + "\n$\\chi^2$/NDF = {0}/{1}, p-value = {3}, RMSE = {2}".format(func_candidate['Chi2'], func_candidate['NDF'], func_candidate['RMSE'], round_a_number(func_candidate['p-value'], 4)), loc = 'right', size = 9.5)
        
    else:
        axes[0,1].set_title(r"$\bfit{{Candidate\,\#{}}}$".format(candidate_idx) + "\nRMSE = {0}, R2 = {1}".format(func_candidate['RMSE'], func_candidate['R2']), loc = 'right', size = 9.5)

    formatter = ticker.FormatStrFormatter('%.3g')

    
    # Add logo to every plot.
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'img/logo.png'
                             )
    logo_img = mpimg.imread(logo_path)
        
    bbox = axes[0,0].get_position()
    
    logo_width = 0.13
    logo_height = logo_width * (logo_img.shape[0] / logo_img.shape[1])

    ax_inset = fig.add_axes([bbox.x0 +0.73,
                            bbox.y1 + 0.085,
                            logo_width,
                            logo_height])

    ax_inset.imshow(logo_img)
    ax_inset.axis('off')
    
    plt.tight_layout()
    
    
def plot_all_syst_all_func_2D(
    func_candidates,
    x,
    bin_edges_2d,
    y,
    y_up,
    y_down,
    pdf_path,
    logx0,
    logx1,
    logy,
    cbar_min,
    cbar_max,
    cmap,
    contour
):
    '''
    Plot all candidate functions, each with all possible parameter variations.
    
    Arguments
    ---------
    func_candidates (pd.dataframe):
        Full dataframe containing all candidate functions after fits.
    
    x (np.ndarray):
        The independent variable.
        
    y (np.ndarray):
        The dependent variable.
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
        
    pdf_path (str):
        Save the output files to this directory.
    
    logx0 (bool):
        Plot x0 in log scale.
    
    logx1 (bool):
        Plot x1 in log scale.
        
    logy (bool):
        Plot y in log scale.
        
    cbar_min (float):
        Plot color bar with min value.
        
    cbar_max (float):
        Plot color bar with max value.
        
    cmap (str):
        Plot color bar with matplotlib cmap style.
        
    contour (float):
        Plot contour line to 2D plots.
    '''
    
    with PdfPages(pdf_path) as pdf:
        for i in range(len(func_candidates)):
            # Print candidate # page.
            fig, axes = plt.subplots(figsize = (9, 7))
            axes.axis('off')
            
            plt.text(0.5,
                     0.5,
                     'Candidate function #{}'.format(len(func_candidates) - 1 - i),
                     fontsize = 20,
                     ha = 'center',
                     va = 'center'
                     )
                     
            plt.tight_layout()
            
            plt.savefig(pdf, format = 'pdf')
            
            plt.close()
            
            if i < len(func_candidates) - 1:
                print('Plotting candidate functions {0}/{1} >>> {2}'.format(i+1, len(func_candidates), pdf_path), end='\r')
                
            else:
                print('Plotting candidate functions {0}/{1} >>> {2}'.format(i+1, len(func_candidates), pdf_path))
                
            func_candidate = func_candidates.iloc[len(func_candidates) - 1 - i]
            
            #if len(func_candidate['Parameters: (best-fit, +1, -1)']) > 0:
            if False: # fix later
                # Check if the function has any parameter that has variations.
                has_uncert = False
                for j in range(len(func_candidate['Parameters: (best-fit, +1, -1)'])):
                    if func_candidate['Parameters: (best-fit, +1, -1)'][f'a{j+1}'][1] > 0:
                        has_uncert = True
                
                # Plot central, up, and down in the same plot, otherwise plot only the central.
                if has_uncert:
                    for j in range(len(func_candidate['Parameters: (best-fit, +1, -1)'])):
                        if func_candidate['Parameters: (best-fit, +1, -1)'][f'a{j+1}'][1] > 0:
                            plot_single_syst_single_func_2D(func_candidate = func_candidate,
                                                            candidate_idx = len(func_candidates) - 1 - i,
                                                            x = x,
                                                            bin_edges_2d = bin_edges_2d,
                                                            y = y,
                                                            y_up = y_up,
                                                            y_down = y_down,
                                                            param_shifted = f'a{j+1}',
                                                            logx0 = logx0,
                                                            logx1 = logx1,
                                                            logy = logy,
                                                            cbar_min = cbar_min,
                                                            cbar_max = cbar_max,
                                                            cmap = cmap,
                                                            contour = contour
                                                            )
                            
                            plt.savefig(pdf, format='pdf')
                            plt.close()
                else:
                    plot_single_syst_single_func_2D(func_candidate = func_candidate,
                                                    candidate_idx = len(func_candidates) - 1 - i,
                                                    x = x,
                                                    bin_edges_2d = bin_edges_2d,
                                                    y = y,
                                                    y_up = y_up,
                                                    y_down = y_down,
                                                    param_shifted = None,
                                                    logx0 = logx0,
                                                    logx1 = logx1,
                                                    logy = logy,
                                                    cbar_min = cbar_min,
                                                    cbar_max = cbar_max,
                                                    cmap = cmap,
                                                    contour = contour
                                                    )
                    
                    plt.savefig(pdf, format='pdf')
                    plt.close()
                    
            else:
                plot_single_syst_single_func_2D(func_candidate = func_candidate,
                                                candidate_idx = len(func_candidates) - 1 - i,
                                                x = x,
                                                bin_edges_2d = bin_edges_2d,
                                                y = y,
                                                y_up = y_up,
                                                y_down = y_down,
                                                param_shifted = None,
                                                logx0 = logx0,
                                                logx1 = logx1,
                                                logy = logy,
                                                cbar_min = cbar_min,
                                                cbar_max = cbar_max,
                                                cmap = cmap,
                                                contour = contour
                                                )
                
                plt.savefig(pdf, format = 'pdf')
                plt.close()
    

def plot_correlation(
    func_candidate,
    candidate_idx,
    y_up,
    y_down
):
    '''
    Plot correlation matrix for the fitted parameters of a candidate function.
    
    Arguments
    ---------
    func_candidate (pd.dataframe):
        A particular candidate function (one row of the full func_candidates).
    
    candidate_idx (np.int):
        Candidate function # (ranked by function complexity).
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
    '''
    
    corr_dict = func_candidate['Correlation']
    
    # Retrieve the correlation for all pairs of fitted parameters.
    parameters = []
    
    pairs = list(corr_dict.keys())
    
    for pair in pairs:
        param1, param2 = pair.split(', ')
        
        parameters.append(param1)
        parameters.append(param2)
        
    parameters = sorted(list(set(parameters)), key = lambda x: (int(x[1:])))
    
    # Create the correlation matrix.
    df = pd.DataFrame(None, index = parameters, columns = parameters, dtype = float)
    
    for pair, value in corr_dict.items():
        param1, param2 = pair.split(', ')
        df.at[param2, param1] = value

    fig = plt.figure(figsize=(9, 8))
    
    sns.heatmap(df, annot = True, cmap = 'bwr', center = 0, vmin = -1, vmax = 1, fmt = '.3f')
    
    # Define the parameter string showing the best-fit and +/-1 sigma values.
    parameters_string = ""
    
    parameters = func_candidate['Parameters: (best-fit, +1, -1)']
    
    for i in range(len(parameters)):
        if parameters[f'a{i+1}'][1] == 0 and parameters[f'a{i+1}'][2] == 0:
            parameters_string += r"{0}$ = {1}$".format(
                f'a{i+1}',
                round_a_number(parameters[f'a{i+1}'][0], 6),
                )
                
        else:
            parameters_string += r"{0}$ = {1}^{{+ {2} ({4}\%) }}_{{- {3} ({5}\%)}}$".format(
                f'a{i+1}',
                round_a_number(parameters[f'a{i+1}'][0], 6),
                round_a_number(parameters[f'a{i+1}'][1], 4),
                round_a_number(np.abs(parameters[f'a{i+1}'][2]), 4),
                round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][1]) / float(parameters[f'a{i+1}'][0])), 3),
                round_a_number(100 * np.abs(float(parameters[f'a{i+1}'][2]) / float(parameters[f'a{i+1}'][0])), 3)
                )
                
        if i < len(parameters) - 1:
            parameters_string += ",  "
            
        if np.mod(i+1, 2) == 0:
            parameters_string += "\n"
    
    # Set the parameter string as the title.
    title = textwrap.fill(func_candidate['Parameterized equation, unscaled'], width=95) + "\n\n" + parameters_string
    
    plt.title(title, loc='left', size=9.5)
    
    # Display the candidate # being plotted and some of the gof metrics.
    if y_up is not None and y_down is not None:
        plt.title(r"$\bfit{{Candidate\,\#{}}}$".format(candidate_idx) + "\n$\\chi^2$/NDF = {0}/{1}, p-value = {3}, RMSE = {2}".format(func_candidate['Chi2'], func_candidate['NDF'], func_candidate['RMSE'], round_a_number(func_candidate['p-value'], 4)), loc='right', size=9.5)
        
    else:
        plt.title(r"$\bfit{{Candidate\,\#{}}}$".format(candidate_idx) + "\nRMSE = {0}, R2 = {1}".format(func_candidate['RMSE'], func_candidate['R2']), loc='right', size=9.5)
        
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    # Add logo to every plot.
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'img/logo.png'
                             )
    logo_img = mpimg.imread(logo_path)
    
    logo_width = 0.1
    logo_height = logo_width * (logo_img.shape[0] / logo_img.shape[1])

    ax_inset = fig.add_axes([0.832,
                             0.955,
                             logo_width,
                             logo_height])

    ax_inset.imshow(logo_img)
    ax_inset.axis('off')
    
    plt.tight_layout()
    

def plot_all_corr(
    func_candidates,
    y_up,
    y_down,
    pdf_path
):
    '''
    Plot correlation matrix for all candidate functions at once.
    
    Arguments
    ---------
    func_candidates (pd.dataframe):
        Full dataframe containing all candidate functions after fits.
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
        
    pdf_path (str):
        Save the output files to this directory.
    '''
    
    with PdfPages(pdf_path) as pdf:
        for i in range(len(func_candidates)):
            # Print candidate # page.
            fig, axes = plt.subplots(figsize = (9, 7))
            axes.axis('off')
            
            plt.text(0.5,
                     0.5,
                     'Candidate function #{}'.format(len(func_candidates) - 1 - i),
                     fontsize = 20,
                     ha = 'center',
                     va = 'center'
                     )
                     
            plt.tight_layout()
            
            plt.savefig(pdf, format = 'pdf')
            
            plt.close()
        
            if i < len(func_candidates) - 1:
                print('Plotting correlation matrices {0}/{1} >>> {2}'.format(i+1, len(func_candidates), pdf_path), end='\r')
                
            else:
                print('Plotting correlation matrices {0}/{1} >>> {2}'.format(i+1, len(func_candidates), pdf_path))
                
            plot_correlation(func_candidate = func_candidates.iloc[len(func_candidates) - 1 - i],
                             candidate_idx = len(func_candidates) - 1 - i,
                             y_up = y_up,
                             y_down = y_down
                             )
            
            plt.savefig(pdf, format='pdf')
            plt.close()


def plot_gof(
    func_candidates,
    gof,
    log_scale = True
):
    '''
    Plot a goodness-of-fit metric vs. function complexity comparing all candidate functions.
    
    Arguments
    ---------
    func_candidates (pd.dataframe):
        Full dataframe containing all candidate functions after fits.
    
    gof (str):
        Which gof to plot.
        
    log_scale (bool):
        Plot gof in log scale.
    
    
    Returns
    -------
    Plot gof vs. function complexity.
    '''
    
    fig = plt.figure(figsize=(12,8))
    
    # Gof vs. complexity.
    plt.scatter(func_candidates['Complexity'], func_candidates[gof], marker = 'o', c = 'r', label = 'Candidate# indicated')
    
    # Display the candidate # next to the corresponding point.
    candidate_idx = list(range(len(func_candidates)))
    
    for i, idx in enumerate(candidate_idx):
        plt.annotate(idx,
                     (func_candidates['Complexity'][i], func_candidates[gof][i]),
                     textcoords = "offset points",
                     xytext = (0, 5),
                     ha = 'center',
                     size = 13
                     )
    
    plt.xticks(size = 18)
    plt.yticks(size = 18)
    
    plt.xlabel('Complexity', size = 20)
    plt.ylabel(gof, size = 20)
    
    plt.legend(loc = 'best', fontsize = 20)
    
    if log_scale:
        if gof != 'p-value':
            plt.yscale('log')
        
    plt.title(gof, loc='center', size=25)
    
    # Add logo to every plot.
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'img/logo.png'
                             )
    logo_img = mpimg.imread(logo_path)
    
    logo_width = 0.15
    logo_height = logo_width * (logo_img.shape[0] / logo_img.shape[1])
    
    ax_inset = fig.add_axes([0.85,
                             0.945,
                             logo_width,
                             logo_height])

    ax_inset.imshow(logo_img)
    ax_inset.axis('off')
    
    plt.tight_layout()
        
        
def plot_all_gof(
    func_candidates,
    y_up,
    y_down,
    pdf_path
):
    '''
    Plot all gof metrices at once.
    
    Arguments
    ---------
    func_candidates (pd.dataframe):
        Full dataframe containing all candidate functions after fits.
    
    y_up (np.ndarray):
        +1 sigma of y.
        
    y_down (np.ndarray):
        -1 sigma of y.
        
    pdf_path (str):
        Save the output files to this directory.
    
    
    Returns
    -------
    Plot all gof metrices at once and save to an output file.
    '''
    
    print('Plotting goodness-of-fit scores >>> {}'.format(pdf_path))
    
    # List of gof to plot.
    gof = ['RMSE', 'R2']
    if y_up is not None and y_down is not None:
        gof.append('Chi2/NDF')
        gof.append('p-value')
        
    with PdfPages(pdf_path) as pdf:
        for i in range(len(gof)):
            plot_gof(func_candidates = func_candidates,
                     gof = gof[i],
                     log_scale = True
                     )
            
            plt.savefig(pdf, format = 'pdf')
            
            plt.close()


