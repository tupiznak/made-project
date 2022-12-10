from dataclasses import dataclass
from typing import Optional

import yaml
from marshmallow_dataclass import class_schema


@dataclass()
class TitleParams:
    corpus_path: str
    title_regex: str
    use_lowercase: bool
    drop_symbols: str
    data_size_limit: Optional[int] = None


@dataclass()
class TrainVectorizerParams:
    model_path: str
    model: str = "skipgram"
    dim: int = 100
    minn: int = 3
    maxn: int = 6
    epoch: int = 5
    lr: float = 0.05
    thread: int = 12


@dataclass()
class PlotUmapParams:
    plot_path: str
    sample_size: int = 10000
    umap_n_neghb: int = 10
    umap_metric: str = "cosine"
    umap_n_components: int = 2
    umap_min_dist: float = 0.01


@dataclass()
class VectorizingPipelineParams:
    title_params: TitleParams
    train_params: TrainVectorizerParams
    plot_params: PlotUmapParams


VectorizingPipelineParamsSchema = class_schema(VectorizingPipelineParams)


def read_vectorizing_pipeline_params(path: str) -> VectorizingPipelineParams:
    with open(path, "r") as input_stream:
        schema = VectorizingPipelineParamsSchema()
        return schema.load(yaml.safe_load(input_stream))
