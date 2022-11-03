from ml.lda.lda_inference import LDAModel


def test_inference():
    model = LDAModel()

    papers = [
        "system control",
        "network data protocol"
    ]

    result = model.inference(papers)

    assert len(result) == len(papers)

    for topic in result:
        assert type(topic) is str


def test_inference_with_probs():
    model = LDAModel()

    papers = [
        "system control",
        "network data protocol"
    ]

    result = model.inference(papers, return_probs=True)

    assert len(result) == len(papers)

    for (topic, prob) in result:
        assert type(topic) is str
        assert type(prob) is float
