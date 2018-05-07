"""
A simple shortest path problem on a digraph with 4 nodes.

Expected solution:
    - Negative cycle? False
    - Shortest path length = 3
    - Shortest path = [1, 2, 3, 4]
"""

import networkx as nx
import bellmanford as bf

G = nx.DiGraph()
G.add_edge(1, 2, length=1)
G.add_edge(1, 3, length=100)
G.add_edge(2, 3, length=1)
G.add_edge(2, 4, length=100)
G.add_edge(3, 4, length=1)

length, nodes, negative_cycle = bf.bellman_ford(G, source=1, target=4, weight='length')

print("Negative cycle?", negative_cycle)
print("Shortest path length =", length)
print("Shortest path =", nodes)

