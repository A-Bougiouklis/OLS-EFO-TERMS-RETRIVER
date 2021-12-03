from init_db import create_terms_table, bulk_insert
from .pipeline_methods import (
    get_label,
    NoLabelKeyError,
    get_synonyms,
    get_ontology,
    get_mesh_references
)

import requests


class NoMoreDataError(Exception):
    ...


class TermDataRetriever:

    TERMS_URL = "http://www.ebi.ac.uk/ols/api/ontologies/efo/terms"

    def __init__(self):
        data = requests.get(self.TERMS_URL).json()

        self.current_url = ""
        self.next_url = self.__get_next_url(data)
        self.last_url = self.__get_last_url(data)
        self.page_number = self.__get_page_number(data)

    @staticmethod
    def __get_next_url(data: dict) -> str:
        try:
            return data["_links"]["next"]['href']
        except KeyError:
            raise NoMoreDataError

    @staticmethod
    def __get_last_url(data: dict) -> str:
        return data["_links"]["last"]['href']

    @staticmethod
    def __get_page_number(data: dict) -> str:
        return data["page"]["number"]

    def next_data(self) -> dict:
        if self.current_url != self.last_url:
            print(f"We are retrieving data from the page with number: {self.page_number}")
            data = requests.get(self.next_url).json()
            self.current_url = self.next_url
            self.next_url = self.__get_next_url(data)
            self.page_number = self.__get_page_number(data)
            return data
        else:
            return {}


PIPELINE = (get_label, get_synonyms, get_ontology, get_mesh_references)


def retrieve(
        pipeline=PIPELINE, repetitions=None, retriever_class=TermDataRetriever
) -> tuple[dict[str, str], ...]:
    """
    Retrieves the needed data from the terms.

    :param repetitions: are used to finish the process quicker during testing
    :param retriever_class: is used mock the TermDataRetriever during testing
    """

    retriever = retriever_class()
    retrieved_data = retriever.next_data()
    retrieved_data_index = 0
    results = []

    while retrieved_data != {} and (repetitions is None or retrieved_data_index < repetitions):
        for term in retrieved_data["_embedded"]["terms"]:
            term_data = {}

            try:
                for pipe in pipeline:
                    column_name, value = pipe(term)
                    term_data[column_name] = value
            except NoLabelKeyError:
                # This term has no label and thus is ignored
                term_data = {}

            results.append(term_data)

        try:
            retrieved_data = retriever.next_data()
            retrieved_data_index += 1
        except NoMoreDataError:
            retrieved_data = {}

    return tuple(results)


def retrieve_efo_term_data():
    create_terms_table()
    retrieved_data = retrieve()
    bulk_insert(
        ["label", "synonyms", "ontology_link", "MeSH_reference"],
        retrieved_data
    )
