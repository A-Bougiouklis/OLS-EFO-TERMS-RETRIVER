from psycopg2.extensions import connection

import psycopg2


def db_connection() -> connection:
    return psycopg2.connect(
        database="postgres",
        user="",
        password="",
    )


def create_terms_table():
    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
      CREATE TABLE terms (
                label text PRIMARY KEY,
                synonyms text[],
                ontology_link text NOT NULL,
                MeSH_reference text
            )
        """
        )
        conn.commit()
    except psycopg2.errors.DuplicateTable:
        print("The relation 'terms' already exists. No need to recreate it.")

    cur.close()
    conn.close()


def bulk_insert(columns: list[str], data: tuple[dict]):
    """
    It inserts in bulk the given data into the terms table.
    In case of key duplication it ignores the duplicates.

    The first given column has to be the PRIMARY KEY, the order of the rest does not matter.

    :param data should have the following form:
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
    """
    conn = db_connection()
    cur = conn.cursor()

    def insert_columns_sub_query():
        result = "("
        for column in columns:
            result += column + ","
        return result[:-1] + ")"

    def values_to_insert():
        result = "("
        for column in columns:
            result += "%(" + column + ")s, "
        return result[:-2] + ")"

    cur.executemany(
        f"""
            INSERT INTO terms {insert_columns_sub_query()}
            VALUES {values_to_insert()}
            ON CONFLICT ({columns[0]})
            DO NOTHING
        """,
        data
    )
    conn.commit()
    cur.close()
    conn.close()
