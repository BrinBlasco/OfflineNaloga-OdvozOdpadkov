
from DataParser import DataProcessor
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


data = DataProcessor.loadFile("Data/testodvoz00.json")

# Create a graph object
G = nx.Graph()

# Add nodes for customers, trash locations, and driver starting locations
for i in range(data["L"]):
    G.add_node(i)

# Add edges between nodes with their respective weights (time and distance)
for i in range(data["L"]):
    for j in range(data["L"]):
        if i != j:
            G.add_edge(i, j, distance=data["casovne_razdalje"][i][j], weight=data["razdalje"][i][j])

            # Set positions for nodes

def is_customer(location_id):
    return location_id in range(data["S"])

def is_trash_location(location_id):
    return location_id in data["smetisce"]

# Set colors for nodes
node_colors = ['red' if is_customer(i) else 'blue' if is_trash_location(i) else 'green' for i in range(data["L"])]

# Set labels for nodes
node_labels = {i: f"L{i+1}" for i in range(data["L"])}

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color=node_colors)


# Add labels to edges
for i, j in G.edges():
    label = f"{data["casovne_razdalje"][i][j]} / {data["razdalje"][i][j]}"

# Show the plot
plt.show()