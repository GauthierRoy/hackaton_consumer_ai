import plotly.graph_objects as go
import networkx as nx
import numpy as np


def graph_plotting(nested_dict_clean):
    import plotly.graph_objects as go
    import networkx as nx
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

            # Order topics by name or opacity to reduce messiness
            ordered_topics = sorted(topics, key=lambda x: (-x[2], x[0]))  # Sort by opacity (desc) then name (asc)
            for topic, lesson, opacity in ordered_topics:
                G.add_node(topic, type='Topic', title=lesson, opacity=opacity)
                G.add_edge(topic, category_node)

    # Manually set positions for level nodes
    level_positions = {'A1': (0, 0), 'A2': (1, 0), 'B1': (2, 0), 'B2': (3, 0)}
    pos = {node: position for node, position in level_positions.items()}

    # Function to arrange nodes in a bounded area (e.g., left and right of A2)
    def arrange_leaf_nodes(center_pos, leaf_nodes, width=1.5, height=1):
        num_nodes = len(leaf_nodes)
        x_start = center_pos[0] - width / 2
        x_step = width / (num_nodes + 1)  # Even spacing
        y_start = center_pos[1] - height

        positions = {}
        for i, node in enumerate(sorted(leaf_nodes)):  # Sort to maintain consistent ordering
            x = x_start + (i + 1) * x_step
            y = y_start - (i % 2) * 0.1  # Slight vertical offset to avoid perfect alignment
            positions[node] = (x, y)
        return positions

    # Identify leaf nodes from A2 and arrange them
    leaf_nodes_a2 = [node for node in G.nodes if list(G.successors(node)) == [] and 'A2' in node]
    pos.update(arrange_leaf_nodes(level_positions['A2'], leaf_nodes_a2))

    # Use spring layout for other nodes
    remaining_nodes = [node for node in G.nodes if node not in pos]
    remaining_pos = nx.spring_layout(G, pos=pos, fixed=list(pos.keys()), seed=42)
    pos.update(remaining_pos)

    # Assign mean opacity for category and level nodes
    for category_node in [node for node in G.nodes() if G.nodes[node].get('type') == 'Category']:
        child_nodes = list(G.predecessors(category_node))
        mean_opacity = (
            sum(G.nodes[child].get('opacity', 0) for child in child_nodes) / len(child_nodes)
            if child_nodes else 0
        )
        G.nodes[category_node]['opacity'] = mean_opacity

    for level_node in [node for node in G.nodes() if G.nodes[node].get('type') == 'Level']:
        child_nodes = list(G.predecessors(level_node))
        mean_opacity = (
            sum(G.nodes[child].get('opacity', 0) for child in child_nodes) / len(child_nodes)
            if child_nodes else 0
        )
        G.nodes[level_node]['opacity'] = mean_opacity

    # Extract node positions for plotting
    x_nodes = [pos[node][0] for node in G.nodes()]
    y_nodes = [pos[node][1] for node in G.nodes()]

    # Prepare node colors and texts
    node_colors = []
    node_texts = []
    node_hovertexts = []
    node_line_widths = []  # Line widths for borders

    for node in G.nodes():
        opacity = G.nodes[node].get('opacity', 0)
        rgba_color = f'rgba(255, 165, 0, {opacity})'
        node_colors.append(rgba_color)

        # Set hover text for all nodes
        node_hovertexts.append(f"{node} ({G.nodes[node].get('title', '')})")

        # Only add text for Level nodes; remove it for categories and topics
        if G.nodes[node]['type'] == 'Level':
            node_texts.append(node)
        else:
            node_texts.append("")  # No text for Category or Topic nodes

        # Make borders thicker for A1, A2, B1, B2
        if node in level_positions:
            node_line_widths.append(3)  # Thicker border for key nodes
        else:
            node_line_widths.append(1)  # Default border for other nodes

    # Extract edges for plotting
    edges_x = []
    edges_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edges_x.extend([x0, x1, None])
        edges_y.extend([y0, y1, None])

    # Add white background nodes for better visibility
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        marker=dict(
            size=20,
            color=node_colors,
            line=dict(
                color='black',
                width=node_line_widths  # Adjust border width
            )
        ),
        text=node_texts,
        textposition="bottom center",
        hoverinfo="text",
        hovertext=node_hovertexts
    ))

    # Add edges
    fig.add_trace(go.Scatter(
        x=edges_x, y=edges_y,
        mode='lines',
        line=dict(color='gray', width=1),
        hoverinfo='none'
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


if __name__ == "__main__":
    nested_dict_clean = {'A1': {'Grammaire': [['articles définis et indéfinis', 'utilisation de le la les et un une des', 0.9], ['pronoms personnels sujets', 'utilisation de je tu il/elle nous vous ils/elles', 0.9], ['adjectifs qualificatifs', 'accord des adjectifs en genre et en nombre', 0.8], ['structure de la phrase simple', 'construction de phrases simples sujet-verbe-objet', 0.9], ['négation', 'formation de la négation avec ne... pas', 0.8], ['questions simples', 'formation de questions avec qui que où pourquoi', 0.8]], 'Vocabulaire': [['présentations', 'se présenter et poser des questions simples', 0.8], ['famille et relations', 'nommer les membres de la famille et les relations', 0.7], ['maison et objets quotidiens', 'décrire les pièces et objets courants', 0.7], ['alimentation et boissons', 'nommer des aliments et des boissons', 0.9], ['transports', 'nommer les moyens de transport courants', 0.7], ['couleurs nombres et jours', 'apprendre les couleurs nombres et jours', 0.7]], 'Orthographe': [['genres des noms', 'différencier masculin et féminin', 0.8], ['pluriels réguliers et irréguliers', 'formation des pluriels -s -x', 0.8], ['accents sur les voyelles', 'utilisation correcte des accents é è à etc.', 0.7], ['liaison et élision', 'usage des apostrophes et des liaisons', 0.7], ['confusions courantes', 'différencier les homophones courants a/à et/est', 0.7], ['ponctuation', 'règles basiques de ponctuation', 0.7]], 'Conjugaison': [['présent des verbes en -er', 'conjuguer les verbes réguliers en -er', 0.9], ['présent des verbes en -ir', 'conjuguer les verbes réguliers en -ir', 0.8], ['présent des verbes irréguliers', 'conjuguer les verbes être avoir aller faire', 0.8], ['futur proche', 'utiliser aller + infinitif pour parler du futur', 0.8], ['impératif', 'donner des ordres ou conseils avec limpératif', 0.7], ['verbes pronominaux', 'utilisation de se lever sappeler etc.', 0.7]]}, 'A2': {'Grammaire': [['articles contractés', 'utilisation de au du des', 0.8], ['pronoms compléments', 'utilisation de me te lui nous vous leur', 0.8], ['adjectifs démonstratifs', 'utilisation de ce cet cette ces', 0.7], ['adverbes de fréquence', 'placer les adverbes souvent toujours parfois', 0.7], ['comparatif et superlatif', 'exprimer des comparaisons plus que moins que', 0.7], ['discours rapporté au présent', 'utilisation de que et dautres subordonnées', 0.7]], 'Vocabulaire': [['santé et bien-être', 'nommer les parties du corps et parler de la santé', 0.7], ['vie quotidienne', 'parler de ses activités et de ses routines', 0.8], ['voyages et vacances', 'nommer les lieux et les activités de voyage', 0.7], ['météo et environnement', 'décrire la météo et parler de la nature', 0.7], ['loisirs et intérêts', 'parler de ses hobbies et activités', 0.7], ['achats et consommation', 'nommer les produits et faire des achats', 0.7]], 'Orthographe': [['accord sujet-verbe', 'respecter les accords dans les phrases complexes', 0.7], ['pluriels irréguliers avancés', 'formation des pluriels complexes bijou -> bijoux', 0.7], ['accents et prononciation', 'maitriser les nuances daccents sur les voyelles', 0.6], ['mots composés', 'comprendre lécriture des mots composés', 0.6], ['homonymes et paronymes', 'différencier les mots proches cest/ses/ces', 0.6]], 'Conjugaison': [['passé composé avec avoir', 'conjuguer les verbes réguliers et irréguliers au passé composé', 0.8], ['passé composé avec être', 'conjuguer les verbes de mouvement au passé composé', 0.7], ['imparfait', 'conjuguer les verbes pour décrire des actions habituelles ou continues', 0.7], ['futur simple', 'utiliser le futur simple pour des événements à venir', 0.7], ['conditionnel présent', 'exprimer la politesse ou une hypothèse avec le conditionnel', 0.6], ['verbes pronominaux au passé', 'conjuguer les verbes pronominaux au passé composé', 0.6]]}, 'B1': {'Grammaire': [['pronoms relatifs', 'utilisation de qui que dont où', 0.6], ['exprimer le subjonctif présent', 'exprimer le doute le désir ou lobligation', 0.5], ['voix passive', 'formation et utilisation de la voix passive', 0.5], ['pronoms toniques', 'utilisation de moi toi lui elle nous vous eux elles', 0.5], ['gérondif', 'formation et utilisation du gérondif', 0.4]], 'Vocabulaire': [['travail et emploi', 'parler du monde professionnel', 0.5], ['éducation et études', 'parler de lécole de luniversité et des formations', 0.5], ['médias et technologie', 'nommer les outils technologiques et parler des médias', 0.4], ['vie sociale', 'parler des interactions sociales et des relations', 0.4], ['voyages et expériences', 'décrire des expériences de voyages ou daventures', 0.4], ['problèmes de société', 'nommer les défis sociaux et économiques', 0.4]], 'Orthographe': [['homophones grammaticaux complexes', 'différencier leurs ce/se on/ont', 0.4], ['accord des participes passés', 'règles daccord des participes avec avoir et être', 0.4], ['noms et adjectifs dérivés', 'écriture correcte des dérivés ex. science -> scientifique', 0.3], ['préfixes et suffixes', 'comprendre les préfixes et suffixes pour créer des mots', 0.3], ['verbes irréguliers complexes', 'écrire correctement les conjugaisons irrégulières', 0.3]], 'Conjugaison': [['subjonctif présent', 'conjuguer les verbes réguliers et irréguliers au subjonctif', 0.5], ['futur antérieur', 'utiliser le futur antérieur pour parler dactions futures accomplies', 0.4], ['conditionnel passé', 'exprimer des regrets ou des hypothèses non réalisées', 0.4], ['participe présent', 'utilisation et formation du participe présent', 0.3], ['plus-que-parfait', 'exprimer une action antérieure à une autre action passée', 0.3], ['discours indirect au passé', 'rapporter des propos au passé', 0.3]]}, 'B2': {'Grammaire': [['pronoms relatifs composés', 'utilisation de lequel laquelle duquel auquel etc.', 0.2], ['concordance des temps avancée', 'harmonisation des temps dans des phrases complexes', 0.2], ['hypothèses', 'utilisation de si + imparfait conditionnel ou plus-que-parfait', 0.2], ['connecteurs logiques', 'utilisation de connecteurs comme cependant néanmoins puisque', 0.2], ['expressions idiomatiques', 'comprendre et utiliser des expressions courantes', 0.1]], 'Vocabulaire': [['relations internationales', 'nommer et décrire les enjeux internationaux', 0.1], ['actualités et politique', 'parler des sujets dactualité et des systèmes politiques', 0.1], ['sciences et technologies', 'nommer des avancées scientifiques et parler des nouvelles technologies', 0.1], ['arts et culture', 'parler de la littérature de lart et de la musique', 0.1], ['développement durable', 'nommer les concepts liés à lécologie et au développement durable', 0.1], ['vie professionnelle', 'parler des compétences des métiers et des enjeux professionnels', 0.1]], 'Orthographe': [['néologismes et emprunts', 'écrire correctement les mots nouveaux ou empruntés à dautres langues', 0.1], ['subtilités des accents', 'maîtriser les nuances des accents sur les voyelles complexes', 0.1], ['homophones avancés', 'différencier des homophones rares comme bal/balle saut/sot', 0.1], ['ponctuation stylistique', 'utilisation avancée des parenthèses tirets longs et points-virgules', 0.1], ['orthographe des verbes complexes', 'écrire correctement les conjugaisons des verbes rares', 0.1], ['pluriels complexes', 'gérer les pluriels des noms composés et des mots dorigine étrangère', 0.1]], 'Conjugaison': [['subjonctif passé', 'conjuguer les verbes réguliers et irréguliers au subjonctif passé', 0.2], ['conditionnel passé deuxième forme', 'utilisation avancée du conditionnel passé', 0.1], ['futur antérieur avancé', 'expliquer des actions futures déjà terminées', 0.1], ['plus-que-parfait avancé', 'utiliser le plus-que-parfait dans des contextes complexes', 0.1], ['participes passés et accords complexes', 'accords avancés des participes passés', 0.1]]}}
    graph_plotting(nested_dict_clean)