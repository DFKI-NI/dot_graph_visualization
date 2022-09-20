#!/usr/bin/env python3

# Copyright 2022, DFKI GmbH
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from rqt_gui_py.plugin import Plugin

from .dot_graph_visualization_widget import DotGraphVisualizationWidget

class DotGraphVisualization(Plugin):

    def __init__(self, context):
        super(DotGraphVisualization, self).__init__(context)
        self.setObjectName('DotGraphVisualization')

        self._widget = DotGraphVisualizationWidget(self)

        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

    def shutdown_plugin(self):
        self._widget.shutdown_plugin()
