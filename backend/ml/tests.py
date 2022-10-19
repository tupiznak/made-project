import unittest
from ml.lda.lda_inference import inference


class LDATest(unittest.TestCase):
    def inference_test(self):
        papers = [
            "system control",
            "network data protocol"
        ]

        result = inference(papers)

        self.assertTrue(len(result) == len(papers))

        for (topic_number, prob) in result:
            self.assertIsInstance(topic_number, int)
            self.assertIsInstance(prob, float)
