import networkx as nx
import matplotlib.pyplot as plt
from random import choice as unif_choose
import numpy as np
from maths_util import *
from qol_util import *

n = 15 # int(input("Graph size: "))
d = 15 # int(input("Dimension: "))

graph = nx.complete_graph(n)
spin_set = [get_e_k(i+1, d) for i in range(d)] + [get_e_k(-i-1, d) for i in range(d)]
print(spin_set)

# assign random spins
for vertex in graph.nodes:
    graph.add_node(vertex, spin=unif_choose(spin_set))

# Prepare custom labels
spin_labels = {node: label_from_vector(data['spin']) for node, data in graph.nodes(data=True)}

# Draw the graph
pos = nx.spring_layout(graph)  # positions for all nodes
nx.draw(graph, pos, with_labels=False, node_size=2000, node_color="skyblue")
nx.draw_networkx_labels(graph, pos, labels=spin_labels, font_size=20, font_weight="bold")

plt.show()