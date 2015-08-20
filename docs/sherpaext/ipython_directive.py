#
#  Copyright (C) 2015  Smithsonian Astrophysical Observatory
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
Extend Ipython.sphinxext.ipython.ipython_directive so that it captures
the output of the sherpa logging interface.

This could be made more generic, but it's not clear what the use
cases are, so is it worth the effort.
"""

import logging

import IPython.sphinxext.ipython_directive as ipy

import sherpa


class SherpaIPythonDirective(ipy.IPythonDirective):

    # Overload setup so that the sherpa logger is connected
    # to the stdout of the EmbeddedSphinxShell. This should
    # only be done once.
    #
    _added_logger = False

    def add_logger(self, name):
        if self._added_logger:
            return

        logger = logging.getLogger(name)
        handler = logging.StreamHandler(self.shell.cout)
        handler.setFormatter(sherpa.Formatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        self._added_logger = True

    def setup(self):
        out = ipy.IPythonDirective.setup(self)
        self.add_logger('sherpa')
        return out


def setup(app):

    # It seems that this works to "sub class" the ipython directive
    ipy.setup(app)
    setup.app = app
    app.add_directive('ipython', SherpaIPythonDirective)
