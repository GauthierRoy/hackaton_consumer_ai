import plotly.graph_objects as go
import networkx as nx
from FrenchA1B2Topics import nested_dict_clean
import numpy as np

# Create a NetworkX graph
G = nx.DiGraph()

# Add nodes and edges from nested_dict_clean
for level, categories in nested_dict_clean.items():
    G.add_node(level, type='Level')
    for category, topics in categories.items():
        category_node = f"{category}_{level}"
        G.add_node(category_node, type='Category')
        G.add_edge(category_node, level)

        for topic, lesson, opacity in topics:
            G.add_node(topic, type='Topic', title=lesson, opacity=opacity)
            G.add_edge(topic, category_node)

# Manually set positions for level nodes
level_positions = {'A1': (0, 0), 'A2': (1, 0), 'B1': (2, 0), 'B2': (3, 0)}
pos = {node: position for node, position in level_positions.items()}

# Function to arrange nodes in a circle around the center with an angle offset
def arrange_in_circle(center_pos, nodes, base_radius, offset_angle=0):
    angle_step = 360 / len(nodes)
    radius = base_radius + 0.1 * len(nodes)  # Dynamically adjust radius based on node count
    positions = {}
    for i, node in enumerate(nodes):
        angle = np.radians(i * angle_step + offset_angle)
        x = center_pos[0] + radius * np.cos(angle)
        y = center_pos[1] + radius * np.sin(angle)
        positions[node] = (x, y)
    return positions

# Adjust positions for A2 and B1 nodes to improve structure
a2_categories = [node for node in G.nodes() if node.endswith('_A2')]
b1_categories = [node for node in G.nodes() if node.endswith('_B1')]
# Use a base radius and adjust dynamically with an angle offset
pos.update(arrange_in_circle(level_positions['A2'], a2_categories, 0.5, offset_angle=15))  # Offset angle in degrees
pos.update(arrange_in_circle(level_positions['B1'], b1_categories, 0.5, offset_angle=15))  # Offset angle in degrees

# Manual adjustments for specific nodes
# Increase spacing between Conjugaison_B1 and Orthographe_B1
conjugaison_b1_pos = pos['Conjugaison_B1']
orthographe_b1_pos = (conjugaison_b1_pos[0] + 0.2, conjugaison_b1_pos[1])  # Move Orthographe_B1 to the right
pos['Orthographe_B1'] = orthographe_b1_pos

# Increase spacing between Vocabulaire_A2 and Grammaire_A2
vocabulaire_a2_pos = pos['Vocabulaire_A2']
grammaire_a2_pos = (vocabulaire_a2_pos[0] + 0.2, vocabulaire_a2_pos[1])  # Move Grammaire_A2 to the right
pos['Grammaire_A2'] = grammaire_a2_pos

# Move Orthographe_A2 a bit more down
orthographe_a2_pos = pos['Orthographe_A2']
orthographe_a2_new_pos = (orthographe_a2_pos[0], orthographe_a2_pos[1] - 0.1)  # Adjust y slightly downwards
pos['Orthographe_A2'] = orthographe_a2_new_pos

# Generate positions for other nodes using a layout strategy
# Ensure that the positions for level nodes are not overwritten
fixed_nodes = list(level_positions.keys()) + a2_categories + b1_categories
pos.update(nx.spring_layout(G, pos=pos, fixed=fixed_nodes, seed=42))

# Extract node positions and opacity
x_nodes = [pos[node][0] for node in G.nodes()]
y_nodes = [pos[node][1] for node in G.nodes()]
node_opacities = [G.nodes[node].get('opacity', 1) for node in G.nodes()]  # Default opacity is 1

# Extract edges
edges_x = []
edges_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edges_x.extend([x0, x1, None])
    edges_y.extend([y0, y1, None])

# Create the Plotly figure
fig = go.Figure()

# Add edges to the figure
fig.add_trace(go.Scatter(
    x=edges_x, y=edges_y,
    mode='lines',
    line=dict(color='gray', width=1),
    hoverinfo='none'
))

# Define RGB values for colors
color_rgb = {
    'Level': '0, 0, 255',  # Blue
    'Category': '0, 128, 0',  # Green
    'Topic': '255, 165, 0'  # Orange
}

# Function to calculate average opacity for main nodes based on connected nodes
def calculate_average_opacity(graph, main_node):
    connected_nodes = list(graph.successors(main_node))  # Use successors for directed edges from level to category
    if not connected_nodes:
        return 1  # Default opacity if no connected nodes
    opacities = [graph.nodes[node].get('opacity', 1) for node in connected_nodes]
    average_opacity = sum(opacities) / len(opacities)
    return average_opacity

# First, apply average opacity to Category nodes
for node in G.nodes():
    node_type = G.nodes[node]['type']
    if node_type == 'Category':
        G.nodes[node]['opacity'] = calculate_average_opacity(G, node)

# Then, apply average opacity to Level nodes
for level in ['A1', 'A2', 'B1', 'B2']:
    G.nodes[level]['opacity'] = calculate_average_opacity(G, level)

# Now construct the node colors with the updated opacities
node_colors = []
node_texts = []  # List to hold text labels for nodes
node_hovertexts = []  # List to hold hover texts for nodes

for node in G.nodes():
    base_color = color_rgb[G.nodes[node]['type']]
    opacity = G.nodes[node].get('opacity', 1)  # Use the updated opacity
    rgba_color = f'rgba({base_color}, {opacity})'
    node_colors.append(rgba_color)
    print(f"Node: {node}, Color: {rgba_color}")  # Debugging output
    # Set hover text for all nodes
    node_hovertexts.append(f"{node} ({G.nodes[node].get('title', '')})")  # Include title in hover text
    # Only add text labels for non-Topic nodes
    if G.nodes[node]['type'] != 'Topic':
        node_texts.append(node)  # Use node name as label
    else:
        node_texts.append("")  # No label for Topic nodes

fig.add_trace(go.Scatter(
    x=x_nodes, y=y_nodes,
    mode='markers+text',
    marker=dict(size=20, color=node_colors),
    text=node_texts,  # Use the conditional text list
    textposition="bottom center",
    hoverinfo="text",
    hovertext=node_hovertexts  # Use hover texts for all nodes
))

# Customize layout
fig.update_layout(
    title="Language Learning Topics Graph",
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
    plot_bgcolor='white',
    width=1000,
    height=800
)

# Show the graph
fig.show()