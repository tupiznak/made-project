import unittest
from ml.lda.lda_inference import inference


class LDATest(unittest.TestCase):
    def inference_test_0(self):
        papers = [
            "system control",
            "network data protocol"
        ]

        result = inference(papers)

        self.assertTrue(len(result) == len(papers))

        for topic in result:
            self.assertIsInstance(topic, str)

    def inference_test_1(self):
        papers = [
            "system control",
            "network data protocol"
        ]

        result = inference(papers, return_probs=True)

        self.assertTrue(len(result) == len(papers))

        for (topic, prob) in result:
            self.assertIsInstance(topic, str)
            self.assertIsInstance(prob, float)
