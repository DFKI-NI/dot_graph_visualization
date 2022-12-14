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

import os
import rospy
import rospkg
from std_msgs.msg import String

# reused from ros smach
from dot_graph_visualization.xdot_qt import DotWidget

# common imports that work for both versions PyQt4 and PyQt5
from python_qt_binding import loadUi, QT_BINDING_VERSION

# check user Qt version and import libraries accordingly
if QT_BINDING_VERSION.startswith('4'):
    from PyQt4.QtGui import QWidget, QFileDialog
elif QT_BINDING_VERSION.startswith('5'):
    from PyQt5.QtWidgets import QWidget, QFileDialog
else:
    raise ValueError('Unsupported Qt version, supported versions: PyQt4, PyQt5')


class DotGraphVisualizationWidget(QWidget):

    def __init__(self, plugin=None):
        super(DotGraphVisualizationWidget, self).__init__()

        # Create QWidget
        ui_file = os.path.join(rospkg.RosPack().get_path('dot_graph_visualization'), 'resource', 'dot_graph_visualization.ui')
        loadUi(ui_file, self, {'DotWidget':DotWidget})
        self.setObjectName('DotGraphVisualization')

        self.refreshButton.clicked[bool].connect(self._handle_refresh_clicked)
        self.saveButton.clicked[bool].connect(self._handle_save_button_clicked)

        self._sub = rospy.Subscriber('/dot_graph_visualization/dot_graph', String, self.graphReceivedCallback)

        # flag used to zoom out to fit graph the first time it's received
        self.first_time_graph_received = True
        # to store the graph msg received in callback, later on is used to save the graph if needed
        self.graph = None
        # inform user that no graph has been received by drawing a single node in the rqt
        self.gen_single_node('No graph received!')

    def gen_single_node(self, node_text):
        '''
        input: the node content (text)
        return dot code corresponding to a graph of 1 node
        '''
        # generate dot code (of a single node) from received text
        graph = 'digraph "graph" {0[ label="' + node_text + '",style=filled,fillcolor=white,fontcolor=black];}'
        # render single node graph
        self.xdot_widget.set_dotcode(graph)
        # zoom the single node to be clearly visible
        self.xdot_widget.zoom_image(5.0, center=True)

    def graphReceivedCallback(self, msg):
        '''
        updating graph view
        '''
        # save graph in member variable in case user clicks save button later
        self.graph = msg.data
        # render graph using DotWidget class
        rospy.loginfo('Rendering graph started...')
        # inform the user his graph is being rendered
        if self.first_time_graph_received:
            self.gen_single_node('Graph received! Rendering...')
            self.first_time_graph_received = False
        # start rendering graph, might take a while depending on the graph size
        self.xdot_widget.set_dotcode(msg.data)
        # update the widget to show the graph
        self.xdot_widget.update()
        # zoom to fit the graph
        self.xdot_widget.zoom_to_fit()
        rospy.loginfo('Rendering graph ended!')

    def _handle_refresh_clicked(self, checked):
        '''
        called when the refresh button is clicked
        '''
        self._sub.unregister()
        self._sub = rospy.Subscriber(self.topicText.text(), String, self.graphReceivedCallback)

    def save_graph(self, full_path):
        '''
        check if last graph msg received is valid (non empty), then save in file.dot
        '''
        if self.graph:
            dot_file = open(full_path,'w')
            dot_file.write(self.graph)
            dot_file.close()
            rospy.loginfo('Graph saved succesfully in %s', full_path)
        else:
            # if self.graph is None it will fall in this case
            rospy.logerr('Could not save Graph: Graph is empty, currently subscribing to: %s, try' +\
                         ' clicking "Update subscriber" button and make sure a graph is published at least one time'\
                         , self.topicText.text())

    def _handle_save_button_clicked(self, checked):
        '''
        called when the save button is clicked
        '''
        rospy.loginfo('Saving graph to dot file')
        fileName = QFileDialog.getSaveFileName(self, 'Save graph to dot file','','Graph xdot Files (*.dot)')
        if fileName[0] == '':
            rospy.loginfo("User has cancelled saving process")
        else:
            # add .dot at the end of the filename
            full_dot_path = fileName[0]
            if not '.dot' in full_dot_path:
                full_dot_path += '.dot'
            rospy.loginfo("path to save dot file: %s", full_dot_path)
            self.save_graph(full_dot_path)

    # Qt methods
    def shutdown_plugin(self):
        pass

    def save_settings(self, plugin_settings, instance_settings):
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        pass
