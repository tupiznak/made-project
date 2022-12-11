import click
import fasttext
import os
from enities.title_params import read_vectorizing_pipeline_params


@click.command("train")
@click.argument("config_path")
def train(config_path: str):
    params = read_vectorizing_pipeline_params(
        config_path).train_params
    corpus_path = read_vectorizing_pipeline_params(
        config_path).title_params.corpus_path
    model = fasttext.train_unsupervised(corpus_path,
                                        model=params.model,
                                        dim=params.dim,
                                        minn=params.minn,
                                        maxn=params.maxn,
                                        epoch=params.epoch,
                                        lr=params.lr,
                                        thread=params.thread,
                                        )
    os.makedirs(params.model_path.split("/")[0], exist_ok=True)
    model.save_model(params.model_path)


if __name__ == '__main__':
    train()
