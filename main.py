from matplotlib.widgets import Button
import networkx as nx
import matplotlib.pyplot as plt
from random import choice as unif_choose
import numpy as np
from maths_util import *
from qol_util import *

n =  7 # int(input("Graph size: "))
d = 3 # int(input("Dimension: "))

graph = nx.complete_graph(n)
spin_set = [get_e_k(i+1, d) for i in range(d)] + [get_e_k(-i-1, d) for i in range(d)]
print(spin_set)

# assign random spins
for vertex in graph.nodes:
    graph.add_node(vertex, spin=unif_choose(spin_set))

# Prepare custom labels
spin_labels = {node: data['spin'] for node, data in graph.nodes(data=True)}
# Prepare custom colours
colors = ["skyblue"] * len(graph.nodes)

# Draw the graph
pos = nx.spring_layout(graph)  # positions for all nodes
nx.draw(graph, pos, with_labels=False, node_size=2000, node_color=colors)
nx.draw_networkx_labels(graph, pos, labels=spin_labels, font_size=20, font_weight="bold")

# Add a button
button_ax = plt.axes((0.8, 0.05, 0.1, 0.075))
button = Button(button_ax, "1. Choose vertex")

state = 0  # keep track of button state
w = graph.nodes()[0]  # keep track of chosen vertex
probabilities = dict()  # keep track of transition probabilities

def on_button_click(event):
    global state, w, button, probabilities
    if state == 0:
        # choose a random vertex
        w = choose_vertex(graph)
        print(w)

        # todo highlight the vertex
        colors[w]= "red"
        plt.clf()  # clear the figure
        nx.draw(graph, pos, with_labels=False, node_size=2000, node_color=colors)
        nx.draw_networkx_labels(graph, pos, labels=spin_labels, font_size=20, font_weight="bold")
        button_ax = plt.axes((0.8, 0.05, 0.1, 0.075))
        button = Button(button_ax, "2. Calculate transition probabilities")
        button.on_clicked(on_button_click)
        plt.draw()

        # update button label
        button.label.set_text("2. Calculate transition probabilities")
    elif state == 1:
        probabilities = compute_transition_probabilities(graph, w, d, 1.0)
        print(probabilities)
        print(sum(probabilities.values()))

        button.label.set_text("3. Update spin")
        plt.draw()

    elif state == 2: 
        # remove the highlighted vertex
        colors[w]= "skyblue"

        # todo choose new spin and update the graph
        new_spin = choose_new_spin(probabilities, d)
        spin_labels[w] = new_spin


        # redraw the graph
        plt.clf()  # clear the figure
        nx.draw(graph, pos, with_labels=False, node_size=2000, node_color=colors)
        nx.draw_networkx_labels(graph, pos, labels=spin_labels, font_size=20, font_weight="bold")
        button_ax = plt.axes((0.8, 0.05, 0.1, 0.075))
        button = Button(button_ax, "1. Choose vertex")
        button.on_clicked(on_button_click)
        plt.draw()
    

    state = (state + 1) % 3

button.on_clicked(on_button_click)

plt.show()