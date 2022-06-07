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
