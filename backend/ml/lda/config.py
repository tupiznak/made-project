from pathlib import Path

p = Path(__file__)
ML_PATH = p.parents[1]

MODELS_PATH = ML_PATH / "models"

LDA_MODEL_PATH = str(MODELS_PATH / "lda.model")
LDA_DICTIONARY_PATH = str(MODELS_PATH / "dictionary.dict")

NLTK_PATH = MODELS_PATH / "nltk"

id2topic = {
    0: "machine learning",
    1: "human understanding",
    2: "signal processing",
    3: "deep learning",
    4: "tracking",
    5: "information security",
    6: "robotics",
    7: "patient health monitoring",
    8: "function estimation",
    9: "game theory",
    10: "supply chain",
    11: "system analysis",
    12: "image classification",
    13: "system design",
    14: "computer networks",
    15: "optimization methods",
    16: "botany",
    17: "linear algebra",
    18: "computational methods",
    19: "artificial intelligence"
}
