from efo_term_pipeline import retrieve_efo_term_data

PIPELINE = (retrieve_efo_term_data, )


def retrieve_data(pipeline=PIPELINE):

    for retrieve_method in pipeline:
        retrieve_method()


if __name__ == "__main__":
    retrieve_data()
