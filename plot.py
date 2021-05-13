import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node(1)
G.add_node(2)
G.add_edge(1, 2)

nx.draw_networkx(G)

plt.show()
