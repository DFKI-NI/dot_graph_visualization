from rqt_gui_py.plugin import Plugin

from .plan_visualization_widget import PlanVisualizationWidget

class PlanVisualization(Plugin):

    def __init__(self, context):
        super(PlanVisualization, self).__init__(context)
        self.setObjectName('PlanVisualization')

        self._widget = PlanVisualizationWidget(self)

        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

    def shutdown_plugin(self):
        self._widget.shutdown_plugin()
