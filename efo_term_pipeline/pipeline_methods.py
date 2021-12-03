
class NoLabelKeyError(Exception):
    """
    Raised when the given dictionary has no label. We use label as our primary key
    so we always need it.
    """
    ...


def get_label(data: dict) -> tuple[str, str]:
    try:
        value = data["label"]
    except KeyError:
        raise NoLabelKeyError
    return "label", value


def get_synonyms(data: dict) -> tuple[str, str]:
    try:
        value = data["synonyms"]
    except KeyError:
        value = []
    return "synonyms", value


def get_ontology(data: dict) -> tuple[str, str]:
    try:
        value = data["_links"]["parents"]["href"]
    except KeyError:
        value = ""
    return "ontology_link", value


def get_mesh_references(data: dict) -> tuple[str, str]:
    """Gets the MeSH references from the given data"""

    try:
        references = data["annotation"]["database_cross_reference"]
        value = next(filter(lambda x: ("MeSH:" in x), references))
    except (StopIteration, KeyError):
        value = ""

    value = value[5:]  # MeSH:D001655 -> D001655
    return "MeSH_reference", value
