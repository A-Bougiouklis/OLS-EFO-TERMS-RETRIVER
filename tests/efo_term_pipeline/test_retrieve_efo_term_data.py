from unittest import TestCase
from efo_term_pipeline import TermDataRetriever, NoMorePagesError, retrieve
from efo_term_pipeline.pipeline_methods import get_label


class TermDataRetrieverTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.retriever = TermDataRetriever()

    def test_init_current_url(self):
        self.assertEqual("", self.retriever.current_url)

    def test_init_next_url(self):
        self.assertIsNotNone(self.retriever.next_url)

    def test_init_last_url(self):
        self.assertIsNotNone(self.retriever.last_url)

    def test_init_page_number(self):
        self.assertEqual(0, self.retriever.page_number)

    def test_next_data(self):

        old_next_url = self.retriever.next_url
        old_current_url = self.retriever.current_url
        old_page_number = self.retriever.page_number

        data = self.retriever.next_data()

        with self.subTest("updates_next_url"):
            self.assertNotEqual(old_next_url, self.retriever.next_url)

        with self.subTest("updates_current_url"):
            self.assertNotEqual(old_current_url, self.retriever.current_url)

        with self.subTest("updates_page_number"):
            self.assertNotEqual(old_page_number, self.retriever.page_number)

        with self.subTest("fetches_the_new_data"):
            self.assertIsNotNone(data)


class RetrieveTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pipeline = [get_label]

    def test_retrieves_data(self):
        data = retrieve(pipeline=self.pipeline, repetitions=1)
        self.assertGreater(len(data), 1)
        self.assertEqual(["label"], list(data[0].keys()))

    def test_finishes_when_the_next_data_are_empty(self):

        class Retriever(TermDataRetriever):

            def next_data(self) -> dict:
                return {}

        data = retrieve(pipeline=self.pipeline, retriever_class=Retriever)
        self.assertEqual(len(data), 0)

    def test_finishes_when_there_are_no_more_pages(self):

        counter = 0

        class Retriever(TermDataRetriever):

            def next_data(self) -> dict:
                nonlocal counter

                if counter == 0:
                    counter += 1
                    return super().next_data()
                else:
                    raise NoMorePagesError

        data = retrieve(pipeline=self.pipeline, retriever_class=Retriever)

        # Each page includes 20 terms
        self.assertEqual(20, len(data))

    def test_when_there_are_no_labels_the_data_are_empty(self):

        class Retriever(TermDataRetriever):

            def next_data(self) -> dict:
                return {
                    '_embedded':
                        {'terms':
                             [{'synonyms': ['Bile Reflux', 'bile reflux']}]
                         }
                }

        data = retrieve(pipeline=self.pipeline, repetitions=1, retriever_class=Retriever)
        self.assertEqual(({},), data)
