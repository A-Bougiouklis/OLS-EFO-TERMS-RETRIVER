from unittest import TestCase
from init_db import create_terms_table, bulk_insert, db_connection


class BulkInsertTests(TestCase):

    def setUp(self):
        self.conn = db_connection()
        self.cur = self.conn.cursor()
        create_terms_table()
        self.delete_foo_baz_records()

    def tearDown(self):
        self.delete_foo_baz_records()
        self.conn.close()
        self.cur.close()

    def delete_foo_baz_records(self):
        # Delete the created records from the database
        self.cur.execute("""DELETE FROM terms WHERE label = 'foo' or label = 'baz'""")
        self.conn.commit()

    def test_bulk_insert(self):

        bulk_insert(
            ["label", "synonyms", "ontology_link", "MeSH_reference"],
            (
                {
                    "label": "foo",
                    "synonyms": ["bar"],
                    "ontology_link": "ontology_foo",
                    "MeSH_reference": "MeSH_reference_foo",
                },
                {
                    "label": "baz",
                    "synonyms": ["bar"],
                    "ontology_link": "ontology_baz",
                    "MeSH_reference": "MeSH_reference_baz",
                },
            )
        )

        self.cur.execute("""SELECT * From terms WHERE label = 'foo' or label = 'baz'""")
        records = self.cur.fetchall()
        foo_records = records[0]
        baz_records = records[1]

        self.assertEqual("foo", foo_records[0])
        self.assertEqual(["bar"], foo_records[1])
        self.assertEqual("ontology_foo", foo_records[2])
        self.assertEqual("MeSH_reference_foo", foo_records[3])

        self.assertEqual("baz", baz_records[0])
        self.assertEqual(["bar"], baz_records[1])
        self.assertEqual("ontology_baz", baz_records[2])
        self.assertEqual("MeSH_reference_baz", baz_records[3])

    def test_ignores_duplicates(self):

        bulk_insert(
            ["label", "synonyms", "ontology_link", "MeSH_reference"],
            (
                {
                    "label": "foo",
                    "synonyms": ["bar"],
                    "ontology_link": "ontology_baz",
                    "MeSH_reference": "MeSH_reference_baz",
                },
                {
                    "label": "foo",
                    "synonyms": ["bar"],
                    "ontology_link": "ontology_foo",
                    "MeSH_reference": "MeSH_reference_foo",
                },
            )
        )

        self.cur.execute("""SELECT * From terms WHERE label = 'foo'""")
        foo_records = self.cur.fetchall()[0]

        self.assertEqual("foo", foo_records[0])
        self.assertEqual(["bar"], foo_records[1])
        self.assertEqual("ontology_baz", foo_records[2])
        self.assertEqual("MeSH_reference_baz", foo_records[3])
