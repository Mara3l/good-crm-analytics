import os
import sys

from extract.adapters.airtable.credentials import AirtableCredentials
from extract.adapters.airtable.impl import AirTableAdapter
from libs.sql import get_basic_table_sql_from_list, get_delete_table_sql_from_list
from load.adapters.postgres.credentials import PostgresCredentials
from load.adapters.postgres.impl import PostgresAdapter
from libs.logger import get_logger
import json

logger = get_logger("extract-load")

# Load env variables
airtable_credentials = AirtableCredentials(
    os.getenv("EXTRACT_AIRTABLE_API_KEY"),
    os.getenv("EXTRACT_AIRTABLE_BASE_ID")
)
postgres_credentials = PostgresCredentials(
    os.getenv("LOAD_DATABASE_HOST"),
    os.getenv("LOAD_DATABASE_PORT"),
    os.getenv("LOAD_DATABASE_USERNAME"),
    os.getenv("LOAD_DATABASE_PASSWORD"),
    os.getenv("LOAD_DATABASE_NAME"),
    os.getenv("LOAD_DATABASE_SCHEMA")
)
airtable_table_ids_plain = os.getenv("EXTRACT_AIRTABLE_TABLES")
postgres_table_names_plain = os.getenv("LOAD_DATABASE_TABLE_NAMES")
airtable_table_ids = []
postgres_table_names = []

try:
    airtable_table_ids = json.loads(airtable_table_ids_plain)
except json.decoder.JSONDecodeError:
    logger.error("Environment variable EXTRACT_AIRTABLE_TABLES is not list!")
    sys.exit(5)
except TypeError:
    logger.error("Environment variable EXTRACT_AIRTABLE_TABLES is not setup correctly!")
    sys.exit(5)

try:
    postgres_table_names = json.loads(postgres_table_names_plain)
except json.decoder.JSONDecodeError:
    logger.error("Environment variable LOAD_DATABASE_TABLE_NAMES is not list!")
    sys.exit(5)
except TypeError:
    logger.error("Environment variable LOAD_DATABASE_TABLE_NAMES is not setup correctly!")
    sys.exit(5)

if len(airtable_table_ids) == 0:
    logger.error("Environment variable EXTRACT_AIRTABLE_TABLES must have at least 1 item!")
    sys.exit(5)

if len(postgres_table_names) == 0:
    logger.error("Environment variable LOAD_DATABASE_TABLE_NAMES must have at least 1 item!")
    sys.exit(5)

# Extract & Load
airtable = AirTableAdapter(logger, airtable_credentials)
airtable_data = airtable.extract(airtable_table_ids)

postgres = PostgresAdapter(logger, postgres_credentials)

postgres.create_tables_if_not_exists(get_basic_table_sql_from_list(postgres_table_names))
postgres.clear_tables(get_delete_table_sql_from_list(postgres_table_names))
# Records are load in to the tables according to position in list. It is not the best solution.
postgres.load_data(airtable_data, postgres_table_names)
