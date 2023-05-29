import networkx as nx
import matplotlib.pyplot as plt
from entities import entities,relationships

# Create an empty graph
graph = nx.Graph()

# Define the entities and relationships

# Add nodes and edges to the graph
for entity in entities:
    graph.add_node(entity)

for relation in relationships:
    subject, rel_type, obj = relation
    graph.add_edge(subject, obj, label=rel_type)

# Draw the graph
pos = nx.spring_layout(graph)
labels = nx.get_edge_attributes(graph, "label")
nx.draw(graph, pos, with_labels=True, font_size=8)
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_size=6)
plt.show()

nx.write_graphml(graph, "knowledge_graph.graphml")
