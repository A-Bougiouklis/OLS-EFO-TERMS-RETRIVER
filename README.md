# The end goal of the exercise

With this exercise we needed to use the Ontology Lookup Service API
(https://www.ebi.ac.uk/ols/docs/api) to extract the following data:

- EFO terms
- EFO term synonyms
- EFO term ontology (parent links)
- MeSH term references

The retrieved data should be saved into a PostgreSQL database.

# How to run the data extraction pipeline

First of all the user has to have the PostgreSQL install in his/her computer and have 
PostgreSQL running. This process might be different depending the os of preference.

Also in order to execute this data retriever you will need Python 3.9

As soon as the PostgreSQL is running and the appropriate Python version is installed
then you can install the requirements by executing the following:

`pip3 install -r requirements.txt`

Finally in order to retrieve and store the data you need to execute:

`python3 retrieve_data.py`

This module will :
   1. create a PostgreSQL table named `terms` in which it will store the retrieved data
   2. use the Ontology Lookup Service API to bring every EFO term page from the database
   3. use the declared pipeline in order to fetch the data from the retrieved json
   4. store in bulk into the `terms` table all the retrieved data. In this case we ignore 
   any duplicates

If you want to run all the unit tests you need to execute `python3 -m unittest discover`
in the home directory.

# Conclusion

The `retrieve_data` method presented into this repository is capable to retrieve all the
records from the database and store all the data mentioned above in a PostgreSQL table.

Furthermore the architecture is capable of incremental updates as:
- if we need to retrieve more data from the efo terms then we just need to add more pipes
in the PIPELINE stored in `ols-efo-term-retriever/efo_term_pipeline/__init__.py`
- if we need to retrieve other types of data we just need to add more retrieving methods
in the PIPELINE stored in  `ols-efo-term-retriever/retrieve_data.py`

# Improvement

It might be better to use Docker in order to create the environment in which the application
runs in order to isolate it from the user computer.
Furthermore a more robust database structure is needed with user credentials in 
order keep the data safe.
