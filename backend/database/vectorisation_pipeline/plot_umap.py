import bokeh.models as bm
import bokeh.plotting as pl
import umap
from bokeh.io import output_file
import fasttext
from enities.title_params import read_vectorizing_pipeline_params
import click
import random
import os


def draw_vectors(x, y, radius=10, alpha=0.25, color='blue',
                 width=1440, height=900, show=True, **kwargs):
    """ draws an interactive plot for data points with auxilirary info on hover """
    if isinstance(color, str): color = [color] * len(x)
    data_source = bm.ColumnDataSource({'x': x, 'y': y, 'color': color, **kwargs})

    fig = pl.figure(active_scroll='wheel_zoom', width=width, height=height)
    fig.scatter('x', 'y', size=radius, color='color', alpha=alpha, source=data_source)
    fig.add_tools(bm.HoverTool(tooltips=[(key, "@" + key) for key in kwargs.keys()]))
    if show: pl.show(fig)
    return fig


@click.command("plot_umap")
@click.argument("config_path")
def plot_umap_sample(config_path: str):
    params = read_vectorizing_pipeline_params(
        config_path).plot_params
    model_path = read_vectorizing_pipeline_params(
        config_path).train_params.model_path
    model = fasttext.load_model(model_path)

    os.makedirs(params.plot_path, exist_ok=True)
    output_file(filename=params.plot_path, title="Umap token representations")
    corpus = random.sample(model.get_words(), params.sample_size)
    word_vectors = [model.get_word_vector(word) for word in corpus]
    embedding = umap.UMAP(n_neighbors=params.umap_n_neghb,
                          metric=params.umap_metric,
                          n_components=params.umap_n_components,
                          min_dist=params.umap_min_dist
                          ).fit_transform(word_vectors)
    draw_vectors(embedding[:, 0], embedding[:, 1], token=corpus)