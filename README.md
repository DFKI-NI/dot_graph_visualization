# dot_graph_visualization

A plugin for rqt to visualize DOT graphs. It contains a simple UI, which visualizes a DOT graph sent to the plugin via ROS topic. The graph needs to be sent as a String to the plugin in correct DOT format.

# Usage

To run the plugin use:

    rqt --standalone dot_graph_visualization

or:

    rqt --standalone dot_graph_visualization.dot_graph_visualization.DotGraphVisualization

Additionally you can call the script using:

    rosrun dot_graph_visualization graph_visualization.py

This is helpful if you want to include it into a launch file.

# Topic

The plugin listens to the following rostopic:

    /dot_graph_visualization/dot_graph std_msgs/String

This topic is changeable inside the plugin at the top.