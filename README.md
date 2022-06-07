# dot_graph_visualization

A rqt plugin to visualize dot graphs.

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