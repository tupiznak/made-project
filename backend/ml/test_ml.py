from ml.lda.lda_inference import inference


def test_inference():
    papers = [
        "system control",
        "network data protocol"
    ]

    result = inference(papers)

    assert len(result) == len(papers)

    for topic in result:
        assert type(topic) is str


def test_inference_with_probs():
    papers = [
        "system control",
        "network data protocol"
    ]

    result = inference(papers, return_probs=True)

    assert len(result) == len(papers)

    for (topic, prob) in result:
        assert type(topic) is str
        assert type(prob) is float
