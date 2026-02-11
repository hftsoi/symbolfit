# CMS dijet dataset

CMS search for high-mass dijet resonances at sqrt(s) = 13 TeV

- <https://arxiv.org/abs/1911.03947>
- <https://doi.org/10.1007/JHEP05(2020)033>

Differential dijet spectrum (Figure 5), public data taken from HEPDATA

- <https://www.hepdata.net/record/ins1764471>

See >>[notebook](notebooks/dijet.ipynb)<< for the complete procedure.

This fit generates 26 candidate functions in total! The output files can be found [here](https://github.com/hftsoi/symbolfit/tree/main/docs/demo/notebooks/output_dijet) (feel free to download them and look at what a typical fit will produce).

Lets look at the output file `candidates_reduced.csv`, which is a csv table storing all candidate functions and their evaluations:

{{ read_csv("notebooks/output_dijet/candidates_reduced.csv") }}

The goodness-of-fit scores are plotted in `candidates_gof.pdf`, such as the chi2/ndf:

![image](notebooks/img/dijet/gof-chi2.png)

For other goodness-of-fit scores:

??? note "Click to expand"
    ![image](notebooks/img/dijet/gof-pvalue.png)

    **^ p-value**

    ![image](notebooks/img/dijet/gof-rmse.png)

    **^ Root-mean-square error**

    ![image](notebooks/img/dijet/gof-r2.png)

    **^ Coefficient of determination R2**


Now, lets take a look at one of the candidate functions, say candidate #25.
The functional form can be found in the corresponding plots from the PDF files and in the csv table above, which is:

`1.0*((a2 + a3*((x0 - 1568.5) * 0.000145275))**(a1 + a7*((x0 - 1568.5) * 0.000145275))*(a5 + tanh(a6*((x0 - 1568.5) * 0.000145275)*(((x0 - 1568.5) * 0.000145275)**2)**a4)))`.

Here we have set `input_rescale = True` and `scale_y_by = None` when configuring the fits. Therefore the functions here have, i.e., no overall normaliztion (y -> 1.0\*y) and an un-standardization (rescaling x -> (x-1568.5)\*0.000145275)).

This candidate function has 7 parameters, originally: `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `a7`.
However, there are only 5 final varying parameters: `a3`, `a4`, `a5`, `a6`, `a7`, as can be seen from the `Parameters: (best-fit, +1, -1)` column in the csv tables or directly from the pdf files:

`{'a1': (-0.722, 0, 0), 'a2': (0.00055, 0, 0), 'a3': (0.00464521, 7.94e-05, -7.94e-05), 'a4': (0.564596, 0.0218, -0.0218), 'a5': (0.661954, 0.000489, -0.000489), 'a6': (3.72985, 0.341, -0.341), 'a7': (2.91192, 0.00894, -0.00894)}`

where `a1` and `a2` have zeros at both +1 and -1 unc entries, meaning they were both held fixed during the re-optimization.
This is because during the re-optimization loop, the objective function was too complex to minimize, therefore some parameters are held fixed to lower the number of degrees of freedom in order to achieve a better fit. 
This is common when the functions or the distribution shapes are not very simple.

To see how this candidate function behaves when each of these 4 parameters is varied to its +/-1 sigma value:

??? note "Click to expand"
    ![image](notebooks/img/dijet/p3.png)

    **^ +/-1 sigma variations of parameter a3**

    ![image](notebooks/img/dijet/p4.png)

    **^ +/-1 sigma variations of parameter a4**

    ![image](notebooks/img/dijet/p5.png)

    **^ +/-1 sigma variations of parameter a5**

    ![image](notebooks/img/dijet/p6.png)

    **^ +/-1 sigma variations of parameter a6**

    ![image](notebooks/img/dijet/p7.png)

    **^ +/-1 sigma variations of parameter a7**

    ![image](notebooks/img/dijet/corr.png)

    **^ Correlation matrix**


As shown in the correlation matrix, these parameters are not all independent to each other, so it will be nice to see the actual uncertainty coverage considering uncertainties from all parameters in a candidate function.
These are plotted in `candidates_sampling.pdf`.
Here, what it does is to generate an ensemble of functions for a candidate function by sampling its parameters, where the sampling is done by sampling from a multidimensional normal distribution for the parameters, with the best-fit parameter values being the mean location and the covariance matrix for the parameters being the covarience.
In this way, the total uncertainty is obtained by considering uncertainties from all parameters simultaneously.
Then the 68% quantile range of this function ensemble as green bands in the plots and compared with the input data.

![image](notebooks/img/dijet/sampling.png)

Note the 95% quantile range can also be added by `sampling_95quantile = True`.
