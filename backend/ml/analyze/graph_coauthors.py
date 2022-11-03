import networkx as nx
import plotly.graph_objects as go
import numpy as np


def plot_authors_graph(authors: nx.Graph):
    weights = dict(authors.degree)

    layout = nx.spring_layout(authors)
    nodes_data = np.array(tuple((p[0], p[1], weights[a]) for a, p in layout.items()))
    names = tuple(f'{name}-{int(data[2])}' for data, name in zip(nodes_data, layout.keys()))

    nodes_data = nodes_data[nodes_data[:, 2] > 0]
    edge_poses = np.vstack(tuple(np.vstack((layout[a[0]], layout[a[1]], (np.nan, np.nan))) for a in authors.edges))

    sizes = nodes_data[:, 2] / (nodes_data[:, 2].max() - nodes_data[:, 2].min())

    nodes = go.Scatter(
        x=nodes_data[:, 0], y=nodes_data[:, 1],
        mode='markers',
        text=names,
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Hot',
            reversescale=True,
            color=sizes,
            size=sizes * 1000,
            sizemin=10,
            sizemode='area',
            colorbar=dict(
                title='Coauthors',
                xanchor='left',
                titleside='right'
            ),
            line_width=2)
    )
    edges = go.Scatter(
        x=edge_poses[:, 0], y=edge_poses[:, 1],
        line=dict(color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    fig = go.Figure(data=[edges, nodes])
    return fig


if __name__ == '__main__':
    authors = nx.Graph()
    authors.add_nodes_from(['a1', 'a2', 'a3', 'a4', 'a5', '6', '7', '8', '9', '10', '11', '12'])
    authors.add_edges_from(
        [['a1', 'a3'], ['a1', 'a2'], ['a1', 'a4'], ['a1', '6'], ['a1', '7'], ['a1', '8'], ['a1', '9'], ['a1', '10'],
         ['a1', '11'], ['a1', '12'], ['a3', 'a4'], ['a3', 'a1']])

    fig = plot_authors_graph(authors)
    fig.show()
