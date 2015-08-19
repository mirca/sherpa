
.. currentmodule:: sherpa.ui

******************************
Using the high-level interface
******************************

.. note::

   Can I set up logging so there's no screen output from the fit/import?
   Or perhaps it's worth it as a visual cue. This refers to the screen
   output during the documentation build.

.. note::

   It is not clear to me whether this will be a good example for the
   documentation (at least in the form as presented). It does
   provide some good test cases for the documentation system though.

The high-level "UI" is provided by either the 
:mod:`sherpa.ui` or :mod:`sherpa.astro.ui` modules. 
For this run through the "general" version
will be used, rather than the Astronomy-specific version:

.. ipython::

    In [1]: from sherpa import ui

    In [2]: import numpy as np

    In [3]: import matplotlib.pyplot as plt
    
It is possible that loading Sherpa for the first time - whether
:mod:`sherpa.ui` or :mod:`sherpa.astro.ui` - will result in one or
more warning messages. These identify optional packages which are not
supported in the current environment.

When using _matplotlib for plotting, there is no need to initialize it
since Sherpa will do this automatically.

The basic steps are going to be:

 1. load data
 2. define the model
 3. chose the statistic
 4. chose the optimisation method
 5. fit the data
 6. error analysis

The steps do not need to be run in this order, although there are
obviously some dependencies. It is also possible to iterate through
several steps, such as to tweak the model after a fit, or to change
the range of data included in a fit. The following example runs
through these steps.

Loading data
============

The example uses the same data as the
`Frequentism and Bayesianism II: When Results Differ <http://jakevdp.github.io/blog/2014/06/06/frequentism-and-bayesianism-2-when-results-differ/#Example-#2:-Linear-Fit-with-Outliers>`_
post by 
`Jake VanderPlas <http://www.astro.washington.edu/users/vanderplas/>`_.
The ``y`` array contains the dependent variable - that is, the variable
to be modelled - and ``e`` the error on that value.

.. note::

   How much of this should be a comparison to Jake's post? I think I may
   move away from this example since it invites too much discussion rather
   than just focussing on the steps and analysis.

.. ipython::

    In [3]: x = np.array([ 0,  3,  9, 14, 15, 19, 20, 21, 30, 35,\
       ...: 40, 41, 42, 43, 54, 56, 67, 69, 72, 88])

    In [4]: y = np.array([33, 68, 34, 34, 37, 71, 37, 44, 48, 49,\
       ...: 53, 49, 50, 48, 56, 60, 61, 63, 44, 71])

    In [5]: e = np.array([ 3.6, 3.9, 2.6, 3.4, 3.8, 3.8, 2.2, 2.1,\
       ...: 2.3, 3.8, 2.2, 2.8, 3.9, 3.1, 3.4, 2.6, 3.4, 3.7, 2.0, 3.5])

The Sherpa UI interface handles data management for you; that is, the
data to be fitted is \"loaded\" into a dataset which is identified by
an integer or string, and then that identifier is used in later commands
(e.g. to set up the model, fit the data, or plot up the residuals).

Data can be loaded from a file, but in this case the 
:func:`load_arrays` function is used. The first argument is the
dataset identifier; here ``1`` is used as it is the default value,
and so can be left out of many commands, such as the 
:func:`plot_data` call:

.. ipython::

    In [6]: ui.load_arrays(1, x, y)

    @savefig plot_data.png width=5in
    In [7]: ui.plot_data()

The default statistic is chi-squared, with errors - when not
given explicity - calculated from the data using the approximation
from `Gehrels 1986, Astrophysical Journal, volume 303, 
pages 336-346 <http://adsabs.harvard.edu/abs/1986ApJ...303..336G>`_.

.. ipython::

    @doctest
    In [8]: ui.get_stat_name()
    Out[8]: 'chi2gehrels'

    In [9]: ui.get_stat()
    Out[9]: Chi Squared with Gehrels variance

.. note::
    The data does not have to be sorted by the independent value (in
    this case ``x``); that is, the following is valid

        >>> ui.load_arrays("test", [10,5,20], [12,18,-5])
        >>> ui.plot_data("test")
        >>> plt.xlim(4, 21)
	>>> plt.ylim(-6, 19)
        >>> ui.delete_data("test")

    This also shows loading of data without an error array and
    using a string value as the dataset identifier.

Defining the model
==================

As the model to be fit is a straight line, the ``ui.polynom1d`` model
is used, with the instance being named ``mdl``:

.. ipython::

    In [10]: ui.set_source(ui.polynom1d.mdl)

    In [11]: print(mdl)
    polynom1d.mdl
       Param        Type          Value          Min          Max      Units
       -----        ----          -----          ---          ---      -----
       mdl.c0       thawed            1 -3.40282e+38  3.40282e+38           
       mdl.c1       frozen            0 -3.40282e+38  3.40282e+38           
       mdl.c2       frozen            0 -3.40282e+38  3.40282e+38           
       mdl.c3       frozen            0 -3.40282e+38  3.40282e+38           
       mdl.c4       frozen            0 -3.40282e+38  3.40282e+38           
       mdl.c5       frozen            0 -3.40282e+38  3.40282e+38           
       mdl.c6       frozen            0 -3.40282e+38  3.40282e+38           
       mdl.c7       frozen            0 -3.40282e+38  3.40282e+38           
       mdl.c8       frozen            0 -3.40282e+38  3.40282e+38           
       mdl.offset   frozen            0 -3.40282e+38  3.40282e+38           

The default behavior for the ``polynom1d`` model is to only vary the
offset (the ``c0`` parameter); for this case the slope is also to be
fit:

.. ipython::

    In [12]: ui.thaw(mdl.c1)

.. note::
    At present the model documentation - that is, an explanation of
    each model and its parameters - is only available from the
    `CIAO version of Sherpa <http://cxc.harvard.edu/sherpa/ahelp/>`_,
    but this information will be added to the Python code to be
    available with the `help` command.

    The :func:`list_models` routine lists the models that are 
    available -
    this depends on whether the ``sherpa.ui`` or ``sherpa.astro.ui``
    module is being used - and the :func:`list_model_components` routine
    lists the instances of these models. For the current example:

    >>> print(ui.list_model_components())
    ['mdl']
    >>> print(ui.list_models()[0:5])
    ['box1d', 'box2d', 'const1d', 'const2d', 'cos']


Choosing the statistic
======================

For the initial attempt, the statistic to be minimized is the
`least squares <http://en.wikipedia.org/wiki/Least_squares>`_ difference
between the data and the model; that is, the error values are ignored.
The Sherpa name for this model is `leastsq`, and it is set with the
:func:`set_stat` routine:

.. ipython::

    In [13]: ui.set_stat('leastsq')

    @doctest float
    In [14]: ui.calc_stat()
    Out [14]: 51862.0

    In [15]: mdl.c1 = 2

    @doctest float
    In [16]: ui.calc_stat()
    Out [16]: 49718.0

.. note::
    The :func:`list_stats` routine lists the various statistic options
    that are available.

    >>> print(ui.list_stats())
    ['cash', 'chi2', 'chi2constvar', 'chi2datavar', 'chi2gehrels', 'chi2modvar', 'chi2xspecvar', 'cstat', 'leastsq']

Choosing the optimisation method
================================

As can be seen, varying the parameter values of the model varies the
statistic value (calculated by :func:`calc_stat`). The default
optimisation method - ``levmar`` - is used here; the
:func:`ui.set_method` routine would be used to change the optimiser,
which can be one of

``levmar``
  The Levenberg-Marquardt method is an interface to the MINPACK 
  subroutine ``lmdif`` to find the local minimum of nonlinear 
  least squares functions of several variables by a modification 
  of the Levenberg-Marquardt algorithm (J.J. More, "The Levenberg 
  Marquardt algorithm: implementation and theory," in Lecture Notes 
  in Mathematics 630: Numerical Analysis, G.A. Watson (Ed.), 
  Springer-Verlag: Berlin, 1978, pp.105-116).

``neldermead`` or ``simplex``
  The implementation of the Nelder Mead Simplex direct search is 
  based on the paper: Jeffrey C. Lagarias, James A. Reeds, 
  Margaret H. Wright, Paul E. Wright "Convergence Properties of 
  the Nelder-Mead Simplex Algorithm in Low Dimensions", SIAM 
  Journal on Optimization,Vol. 9, No. 1 (1998), pages 112-147. 

``moncar``
  The implementation of the moncar method is based on the paper by 
  Storn, R. and Price, K. "Differential Evolution: A Simple and
  Efficient Adaptive Scheme for Global Optimization over Continuous 
  Spaces." J. Global Optimization 11, 341-359, 1997.

``gridsearch``
  Something about grid searches

.. ipython::

    @doctest
    In [17]: ui.get_method_name()
    Out [17]: levmar

    In [18]: print(ui.get_method())
    name    = levmar
    ftol    = 1.19209289551e-07
    xtol    = 1.19209289551e-07
    gtol    = 1.19209289551e-07
    maxfev  = None
    epsfcn  = 1.19209289551e-07
    factor  = 100.0
    verbose = 0

The parameters of the optimisation routine can be changed by the
:func:`set_method_opt` function, if necessary.

.. note::
    The :func:`list_methods` routine lists the optimisation
    methods that are available.

    >>> print(ui.list_methods())
    ['gridsearch', 'levmar', 'moncar', 'neldermead', 'simplex']


Fitting the data
================

The :func:`fit` routine will perform the fit, looping until either the
change in statistic is small enough or the maximum number of
iterations has been reached, and at completion a summary of the fit
results is displayed:

.. ipython::

    In [19]: ui.fit()
    Dataset               = 1
    Method                = levmar
    Statistic             = leastsq
    Initial fit statistic = 49718
    Final fit statistic   = 2106.51 at function evaluation 6
    Data points           = 20
    Degrees of freedom    = 18
    Change in statistic   = 47611.5
       mdl.c0         41.1663     
       mdl.c1         0.252945    

    @savefig leastsq_fit_resit.png width=5in
    In [20]: ui.plot_fit_resid()
    Out [20]: WARNING: The displayed errorbars have been supplied with the data or calculated using chi2xspecvar; the errors are not used in fits with leastsq
    WARNING: The displayed errorbars have been supplied with the data or calculated using chi2xspecvar; the errors are not used in fits with leastsq

The warning is displayed twice, once for each plot, where the top plot shows
the data (blue points) along with the best-fit model (green line), and
the bottom plot shows the residuals (that is, the y value shows the 
``data - model`` values):

Changing to a chi-squared statistic
===================================

As shown earlier, Sherpa can estimate errors on the dependent values,
depending on the chosen statistic (there are several options for
estimateing a gaussian-like error). The error values can also be
given directly, in which case the particular choice of "chi square"
statistic is unimportant. In this case, after setting the errors
on ``y`` to the values given in the ``e`` array, the ``chi2datavar``
statistic is chosen:

.. ipython::

    In [21]: ui.load_arrays(2, x, y, e)

    In [22]: ui.set_source(2, ui.polynom1d.mdl2)

    In [23]: ui.thaw(mdl2.c1)
   
    In [22]: ui.set_stat('chi2')

    In [23]: ui.get_stat()
    Out [23]: Chi Squared statistic.

.. note::
   Although the data has been changed for dataset ``1``, the
   model expression - set by the earlier ``ui.set_source`` call -
   remains. This is now *outdated* since I am using a different
   data set.

Repeating the fit changes the values slightly, and also provides
some measure of the
`goodness of the fit <http://en.wikipedia.org/wiki/Goodness_of_fit>`_,
based on the reduced chi-squared value; in this case it is 
*not* very good, due to the outliers:

.. ipython::

    In [24]: ui.fit(2)
    Dataset               = 2
    Method                = levmar
    Statistic             = chi2
    Initial fit statistic = 5794.07
    Final fit statistic   = 201.417 at function evaluation 6
    Data points           = 20
    Degrees of freedom    = 18
    Probability [Q-value] = 5.2159e-33
    Reduced statistic     = 11.1899
    Change in statistic   = 5592.65
       mdl2.c0        39.6998     
       mdl2.c1        0.236211    

    In [25]: ui.plot_fit(2)

    @savefig compare_fits.png width=5in
    In [26]: ui.plot_model(1, overplot=True)

Here the best-fit from the original case has been added to the plot,
as the red line.

As before, the residuals can also be shown, either as ``data - model``:

.. ipython ::
    
    @savefig chisq_resid.2.png width=5in
    In [25]: ui.plot_resid(2)

or as relative errors, namely ``(data - model) / error`` (with
"errors" of ±1):

.. ipython::

    @savefig chisq_delchi.2.png width=5in
    In [26]: ui.plot_delchi(2)

The model parameters can be accessed by the instance name, as before:
   
.. ipython::
   
    In [27]: print(mdl2)
    polynom1d.mdl2
       Param        Type          Value          Min          Max      Units
       -----        ----          -----          ---          ---      -----
       mdl2.c0      thawed      39.6998 -3.40282e+38  3.40282e+38           
       mdl2.c1      thawed     0.236211 -3.40282e+38  3.40282e+38           
       mdl2.c2      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c3      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c4      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c5      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c6      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c7      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c8      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.offset  frozen            0 -3.40282e+38  3.40282e+38           

The parameter values have been updated by the fit, and can be accessed
directly (note the use of the ``.val`` accessor, rather than just the
parameter name):

.. ipython::
    
    In [28]: print("Offset = {}".format(mdl2.c0.val))
    Offset = 39.6997908926

    In [29]: print("Slope  = {}".format(mdl2.c1.val))
    Slope  = 0.236211139189

Removing points manually
------------------------

Although the discrepant points can be seen on the graph, they can
also be identified using the 
:func:`calc_chisqr` routine, which returns the residuals in units 
of \"reduced chi square\"; that is the square of
``(data - model) / error``.

.. ipython::

    In [30]: resid = ui.calc_chisqr(2)

    @doctest
    In [31]: x[resid > 25]
    Out [31]: array([ 3, 19, 72])

The :func:`notice` and :func:`ignore` routines are used to identify
ranges of the dependent variable that should be included, or ignored
from, the fit. The following will remove the points more than 
five-sigma from the model

.. ipython::

    @doctest float
    In [32]: ui.calc_stat(2)
    Out [32]: 201.41742478507388

    In [33]: ui.ignore_id(2, 2, 4)

    In [34]: ui.ignore_id(2, 18, 20)

    In [35]: ui.ignore_id(2, 70, 75)

    @doctest float
    In [36]: ui.calc_stat(2)
    Out [36]: 49.82573871224715

    In [37]: ui.fit(2)
    Dataset               = 2
    Method                = levmar
    Statistic             = chi2
    Initial fit statistic = 49.8257
    Final fit statistic   = 9.6559 at function evaluation 6
    Data points           = 16
    Degrees of freedom    = 14
    Probability [Q-value] = 0.786884
    Reduced statistic     = 0.689707
    Change in statistic   = 40.1698
       mdl2.c0        32.1562     
       mdl2.c1        0.45577 

    @savefig ignore_fit_delchi.2.png width=5in
    In [38]: ui.plot_fit_delchi(2)

Removing points using an iterative fit algorithm
------------------------------------------------

An iterative algorithm can be used instead of a manual
approach: in this case a sigma-rejection routine
is chosen which removes all points that are larger than three
sigma from the best fit. To start with, all the previously-ignored
points must be restored using :func:`notice`, and then the
iterative method set up using :func:`set_iter_method`:

.. ipython::

    In [39]: ui.notice(None, None)

    @doctest
    In [49]: ui.get_iter_method_name()
    Out [49]: 'none'

    In [50]: ui.set_iter_method('sigmarej')

    @doctest
    In [51]: ui.get_iter_method_name()
    Out [51]: 'sigmarej'

    @doctest
    In [52]: ui.get_iter_method_opt()
    Out [52]: {'grow': 0, 'hrej': 3, 'lrej': 3, 'maxiters': 5}

Since the model is already close to the best fit, the parameters
are reset, which uses the last set of values set by the user. In this
case the only change to the default settings is that ``mdl2.c1``
is free to vary.

.. ipython::

    In [53]: mdl2.reset()

    In [54]: print(mdl2)
    polynom1d.mdl
       Param        Type          Value          Min          Max      Units
       -----        ----          -----          ---          ---      -----
       mdl2.c0      thawed            1 -3.40282e+38  3.40282e+38           
       mdl2.c1      thawed            0 -3.40282e+38  3.40282e+38           
       mdl2.c2      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c3      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c4      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c5      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c6      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c7      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.c8      frozen            0 -3.40282e+38  3.40282e+38           
       mdl2.offset  frozen            0 -3.40282e+38  3.40282e+38           

Since the residuals show some values around ``-4 sigma``, the limits
are relaxed using :func:`set_iter_method_opt`:

.. ipython::

    In [55]: ui.set_iter_method_opt('lrej', 5)

    In [56]: ui.set_iter_method_opt('hrej', 5)

and the data is re-fit:

.. ipython::

    In [57]: ui.fit(2)
    Dataset               = 2
    Iterative Fit Method  = Sigmarej
    Method                = levmar
    Statistic             = chi2
    Initial fit statistic = 5794.07
    Final fit statistic   = 12.8399 at function evaluation 12
    Data points           = 17
    Degrees of freedom    = 15
    Probability [Q-value] = 0.614666
    Reduced statistic     = 0.85599
    Change in statistic   = 5781.23
       mdl2.c0        31.185      
       mdl2.c1        0.471133    

    @savefig sigmarej_fit_resid.2.png width=5in
    In [57]: ui.plot_fit_resid(2)

The fit results can be accessed via the best-fit model parameter
values:

.. ipython::

    In [58]: print("Offset = {}\nSlope  = {}".format(mdl2.c0.val, mdl2.c1.val))
    Offset = 31.1850002829
    Slope  = 0.471132988676

or directly:

.. ipython::

    In [59]: fr = ui.get_fit_results()

    @doctest
    In [60]: fr.succeeded
    Out [60]: True

    @doctest float
    In [61]: fr.statval
    Out [61]: 12.839856998617966

    @doctest
    In [62]: fr.dof
    Out [62]: 15

    @doctest float
    In [63]: fr.rstat
    Out [63]: 0.855990466574531

This is a much-better fit than earlier.

The :func:`notice` function can be used to select all the points, and
so display the residuals of those points excluded by the sigma-rejection
routine (note that this means that the statistic value will change).
The best-fit results (from the sigma-rejection fit, and from the
first dataset) are displayed compared to the full data set:

.. ipython::

    In [64]: ui.notice(None, None)

    @doctest float
    In [65]: ui.calc_stat(2)
    Out [65]: 272.57606375120804

    In [66]: ui.plot_fit_delchi(2)

    In [67]: plt.subplot(2, 1, 1)

    @savefig sigmarej_fit_delchi_all.2.png width=5in
    In [67]: ui.plot_model(1, overplot=True)

Error analysis
==============

Once a best-fit location has been found, errors on the parameter
values can be calculated. In this case the
data has to be re-fit because of the call to 
:func:`notice`, and then the 
:func:`conf` routine is used to calculate the one-sigma (68.3%)
error values for the parameters:

.. ipython::

    In [67]: ui.fit(2)
    Dataset               = 2
    Iterative Fit Method  = Sigmarej
    Method                = levmar
    Statistic             = chi2
    Initial fit statistic = 272.576
    Final fit statistic   = 12.8399 at function evaluation 12
    Data points           = 17
    Degrees of freedom    = 15
    Probability [Q-value] = 0.614666
    Reduced statistic     = 0.85599
    Change in statistic   = 259.736
       mdl2.c0        31.185      
       mdl2.c1        0.471133    

    In [68]: ui.conf(2)
    mdl2.c0 lower bound:	-1.38059
    mdl2.c1 lower bound:	-0.0338185
    mdl2.c0 upper bound:	1.38059
    mdl2.c1 upper bound:	0.0338185
    Dataset               = 2
    Confidence Method     = confidence
    Iterative Fit Method  = Sigmarej
    Fitting Method        = levmar
    Statistic             = chi2datavar
    confidence 1-sigma (68.2689%) bounds:
       Param            Best-Fit  Lower Bound  Upper Bound
       -----            --------  -----------  -----------
       mdl2.c0            31.185     -1.38059      1.38059
       mdl2.c1          0.471133   -0.0338185    0.0338185

The errors can also be viewed graphically: for instance
the :func:`reg_proj` routine shows the variation of two parameters
(the ``nloop`` parameter is increased from the default of 10
points per axis since the model evaluation here is quick, as there
are no free parameters):

.. ipython::

    @savefig sigmarej_reg_proj.2.png width=5in
    In [69]: ui.reg_proj(mdl2.c0, mdl2.c1, id=2, nloop=[41,41])

and a one-dimensional profile can be calculated for a single
parameter using :func:`int_proj`, where the solid horizontal
lines indicate the expected one- and two-sigma limits for
the parameter:

.. ipython::

    In [70]: ui.int_proj(mdl2.c1, id=2, min=0.4, max=0.54, nloop=101)

    In [71]: (xlo, xhi) = plt.xlim()

    In [72]: plt.hlines(fr.statval + 1, xlo, xhi)

    @savefig sigmarej_int_proj_c1.2.png width=5in
    In [73]: plt.hlines(fr.statval + 4, xlo, xhi)

.. note::

   **TODO** can we show an extension to include the Huber loss, a la the
   original blog post?

