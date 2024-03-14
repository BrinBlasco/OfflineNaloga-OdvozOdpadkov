import heapq
from DataParser import DataProcessor 

class Graph:
    def __init__(self, num_vertices):
        self.V = num_vertices
        self.edges = [[] for i in range(num_vertices)]

    def add_edge(self, u, v, weight, distance):
        self.edges[u].append((v, weight, distance))  # Store weight and distance
        self.edges[v].append((u, weight, distance))  # Add edge in both directions

class DirectedGraph:
  def __init__(self, num_vertices):
    self.V = num_vertices
    self.outgoing_edges = [[] for i in range(num_vertices)]
    self.incoming_edges = [[] for i in range(num_vertices)]

  def add_edge(self, u, v, weight, distance, InOut):
    """
    This function adds a directed edge from u to v with weight and distance.

    Args:
        u: Source node.
        v: Destination node.
        weight: Weight of the edge.
        distance: Distance of the edge.
    """
    self.outgoing_edges[u].append((v, weight, distance)) if InOut == "o" else None
    self.incoming_edges[v].append((u, weight, distance)) if InOut == "i" else None



data = DataProcessor.loadFile("Data/testodvoz00.json")

t = data["casovne_razdalje"]
d = data["razdalje"]
L = data["L"]

graph = DirectedGraph(L)

for i in range(L):
    for j in range(L):
        if i != j:
            # Add edge from i to j with time t[i][j] and distance d[i][j]
            graph.add_edge(i, j, t[i][j], d[i][j], "i")
            # Add edge from j to i with potentially different time and distance
            graph.add_edge(j, i, t[j][i], d[j][i], "o")  # Assuming t[j][i] and d[j][i] are available


def print_graph(graph):
  """
  This function prints the directed graph structure.

  Args:
      graph: A DirectedGraph object representing the graph.
  """
  for vertex in range(1, graph.V+1):
    print(f"Vertex {vertex}:")
    print(f"\tOutgoing Edges:")
    for neighbor, weight, distance in graph.outgoing_edges[vertex-1]:
      print(f"\t\t-> {neighbor+1} (Weight: {weight}, Distance: {distance})")
    print(f"\tIncoming Edges:")  # Print incoming edges for reference
    for neighbor, weight, distance in graph.incoming_edges[vertex-1]:
      print(f"\t\t<- {neighbor+1} (Weight: {weight}, Distance: {distance})")  # Note the "<-" symbol

print_graph(graph)  # Assuming you have a DirectedGraph object 'graph'

# for voznik in data["vozniki"]:
#     vozniki.append(vo)

#assign_customers_to_drivers(data["vozniki"])
#select_customer_driver_pair()