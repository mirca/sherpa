.. Sherpa documentation master file, created by
   sphinx-quickstart on Wed Aug 19 16:30:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. hide the title (based on astropy)
.. raw:: html

    <style media="screen" type="text/css">h1 { display: none; }</style>
   
Welcome to Sherpa's documentation
=================================

.. image:: _static/sherpa_logo.png
    :width: 350px
    :height: 132px
    :target: http://cxc.harvard.edu/sherpa/

.. note::

   This is an *experimental build* of the Sherpa documentation. The
   information presented here is not guaranteed to be correct.

Welcome to the Sherpa documentation. Sherpa is a Python package for
modeling and fitting data. It was originally developed by the
`Chandra X-ray Center <http://cxc.harvard.edu/>`_ for use in
`analysing X-ray data (both spectral and imaging)
<http://cxc.harvard.edu/sherpa>`_
from the  Chandra X-ray telescope, but it is designed to be a
general-purpose package, which can be enhanced with domain-specific
tasks (such as X-ray Astronomy).

.. _user_docs::

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   example

.. _help_docs::

.. toctree::
   :maxdepth: 2
   :caption: Getting Help

If you have found a bug in Sherpa please report it. The preferred way
is to create a new issue on the Sherpa
`GitHub issue page <https://github.com/sherpa/sherpa/issues/>`_; that
requires creating a free account on GitHub if you do not have one.
For those using Sherpa as part of _CIAO, please use the
`CXC HelpDesk system <http://cxc.harvard.edu/helpdesk/>`_.

Please include an example that demonstrates the issue that will allow
the developers to reproduce and fix the problem. You may be asked to
also provide information about your operating system and a full Python
stack trace; the Sherpa developers will walk you through obtaining a
stack trace if it is necessary.

At present there is no developer mailing list for Sherpa.

.. _indices::

.. toctree::
   :maxdepth: 2
   :caption: Indices and tables

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
