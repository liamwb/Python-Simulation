from matplotlib.widgets import Button
import networkx as nx
import matplotlib.pyplot as plt
from random import choice as unif_choose
import numpy as np
from maths_util import *
from qol_util import *

# change these values to change the number of vertices and the dimension respectively
n =  5
d = 3

graph = nx.complete_graph(n)
spin_set = [get_e_k(i+1, d) for i in range(d)] + [get_e_k(-i-1, d) for i in range(d)]

# assign random spins
for vertex in graph.nodes:
    graph.add_node(vertex, spin=unif_choose(spin_set))

# Prepare custom labels
spin_labels = {node: data['spin'] for node, data in graph.nodes(data=True)}
# Prepare custom colours
colors = ["skyblue"] * len(graph.nodes)

# define a figure
fig, (graph_ax, table_ax) = plt.subplots(1, 2)

# Draw the graph in the first subplot
pos = nx.spring_layout(graph)  # positions for all nodes
nx.draw(graph, pos, ax=graph_ax, with_labels=False, node_size=2000, node_color=colors)
nx.draw_networkx_labels(graph, pos, ax=graph_ax, labels=spin_labels, font_size=20, font_weight="bold")

# Add a button
button_ax = plt.axes((0.8, 0.05, 0.1, 0.075))
button = Button(button_ax, "1. Choose vertex")

# Draw the table in the second subplot
table = table_ax.table(
    cellText=[[f"{get_e_k(k,d)}", ""] for k in range(-d,d+1) if k != 0],
    colLabels=["Spin", "Probability"],
    loc="center",
)
# Hide axes for the table subplot
table_ax.axis('off')

state = 0  # keep track of button state
w = graph.nodes()[0]  # keep track of chosen vertex
probabilities = dict()  # keep track of transition probabilities

def redraw_graph(button_text, highlight_vertex):
    global button_ax, button  # Ensure these are treated as global variables
    graph_ax.clear()  # clear the graph

    if highlight_vertex:
        colors[w]= "red"    
    nx.draw(graph, pos, ax=graph_ax, with_labels=False, node_size=2000, node_color=colors)
    nx.draw_networkx_labels(graph, pos, ax=graph_ax, labels=spin_labels, font_size=20, font_weight="bold")
    # update button text
    button.label.set_text(button_text)

    plt.draw()

def redraw_table(cellText=[[f"{get_e_k(k,d)}", ""] for k in range(-d,d+1) if k != 0]):
    global table, table_ax
    table_ax.clear()
    table_ax.axis('off')

    # Draw the table in the second subplot
    table = table_ax.table(
    cellText=cellText,
    colLabels=["Spin", "Probability"],
    loc="center",
    )

def on_button_click(event):
    global state, w, button, probabilities
    if state == 0:
        # choose a random vertex
        w = choose_vertex(graph)
        print(w)

        redraw_graph("2. Calculate transition probabilities", True)
        redraw_table()

        # update button label
        button.label.set_text("2. Calculate transition probabilities")
    elif state == 1:
        probabilities = compute_transition_probabilities(graph, w, d, 1.0)
        new_cell_text = [[f"{get_e_k(k,d)}", f"{probabilities[k]:.2f}"] for k in probabilities]

        redraw_graph("3. Update spin", False)
        redraw_table(new_cell_text)

    elif state == 2: 
        # remove the highlighted vertex
        colors[w]= "skyblue"

        # todo choose new spin and update the graph
        new_spin = choose_new_spin(probabilities, d)
        spin_labels[w] = new_spin


        # redraw the graph
        redraw_graph("1. Choose vertex", False)
    

    state = (state + 1) % 3


button.on_clicked(on_button_click)

plt.show()