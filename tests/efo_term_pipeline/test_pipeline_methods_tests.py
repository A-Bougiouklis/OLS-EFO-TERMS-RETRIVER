from unittest import TestCase
from efo_term_pipeline.pipeline_methods import (
    get_label,
    NoLabelKeyError,
    get_synonyms,
    get_ontology,
    get_mesh_references,
)


class GetLabelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {"label": "bile reflux"}

    def test_get_label(self):
        self.assertEqual(("label", "bile reflux"), get_label(self.data))

    def test_get_label_when_there_is_no_label_raises_error(self):
        with self.assertRaises(NoLabelKeyError):
            get_label({})


class GetSynonymsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {'synonyms': ['Bile Reflux', 'bile reflux']}

    def test_get_synonyms(self):
        self.assertEqual(
            ("synonyms", ['Bile Reflux', 'bile reflux']), get_synonyms(self.data)
        )

    def test_get_synonyms_when_there_is_no_synonyms_key(self):
        self.assertEqual(("synonyms", []), get_synonyms({}))


class GetOntologyTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            '_links': {
                'parents': {
                    'href': 'url'
                }
            }
        }

    def test_get_ontology(self):
        self.assertEqual(("ontology_link", "url"), get_ontology(self.data))

    def test_get_ontology_when_there_is_no_ontology_key(self):
        self.assertEqual(("ontology_link", ""), get_ontology({}))


class GetMeSHReferencesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            'annotation': {
                'database_cross_reference': [
                    'DOID:12237',
                    'MONDO:0006677',
                    'MeSH:D001655',
                    'MESH:D001655',
                    'UMLS:C0005403'
                ],
            }
        }

    def test_get_MeSH_references(self):
        self.assertEqual(("MeSH_reference", "D001655"), get_mesh_references(self.data))

    def test_get_MeSH_reference_with_no_MeSH_cross_reference(self):
        data = {
            'annotation': {
                'database_cross_reference': [
                    'DOID:12237',
                    'MONDO:0006677',
                    'MESH:D001655',
                    'UMLS:C0005403'
                ],
            }
        }

        self.assertEqual(("MeSH_reference", ""), get_mesh_references(data))

    def test_get_MeSH_reference_with_no_annotation_or_database_cross_reference_key(self):
        self.assertEqual(("MeSH_reference", ""), get_mesh_references({}))
