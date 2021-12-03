from unittest import TestCase
from retrieve_data import retrieve_data


class RetrieveDataTests(TestCase):

    def test_executes_every_pipe_in_the_pipeline_in_order(self):
        result = ""

        def a():
            nonlocal result
            result = result + "a"

        def b():
            nonlocal result
            result = result + "b"

        pipeline = [a, b]
        retrieve_data(pipeline)
        self.assertEqual("ab", result)
