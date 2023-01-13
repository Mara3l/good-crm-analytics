from logging import Logger
from typing import Any
import psycopg2
from libs.sql import get_insert_sql
from load.adapters.postgres.credentials import PostgresCredentials
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors, errorcodes


class PostgresAdapter:
    def __init__(self, logger: Logger, credentials: PostgresCredentials):
        self.logger = logger
        self.host = credentials.host
        self.port = credentials.port
        self.user = credentials.user
        self.password = credentials.password
        self.name = credentials.database_name
        self.schema = credentials.database_schema
        self._conn = self.get_connection()
        self._cur = self._conn.cursor()
        self.execute_query(f"SET SEARCH_PATH TO {self.schema}")

    def close_connections(self) -> None:
        if self._conn:
            self._conn.close()

    def get_connection(self) -> Any:
        conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn

    def execute_query(self, query: str) -> None:
        self._cur.execute(query)

    def execute_query_fetch_results(self, query: str, include_header: bool = False) -> list[Any]:
        self.execute_query(query)
        data = self._cur.fetchall()
        if include_header:
            data.insert(0, [x.name for x in self._cur.description])
        return data

    def create_tables_if_not_exists(self, sql_dict: dict) -> None:
        for item in sql_dict:
            try:
                self.execute_query(sql_dict[item])
                self.logger.info(f"creating of table {item} has been successful")
            except errors.lookup(errorcodes.DUPLICATE_TABLE):
                self.logger.info(f"skip creating table {item}, it has already been created")

    def clear_tables(self, sql_dict: dict) -> None:
        for item in sql_dict:
            try:
                self.execute_query(sql_dict[item])
                self.logger.info(f"removal of table {item} has been successful")
            except RuntimeError:
                self.logger.info(f"removal of table {item} has not been successful")

    def load_data(self, airtable_data: dict, postgres_table_names: dict) -> None:
        loaded = {}

        for index, airtable_data_item in enumerate(airtable_data):
            for record in airtable_data[airtable_data_item]:
                table_name = postgres_table_names[index]
                insert_sql = get_insert_sql(table_name, record)
                try:
                    self.execute_query(insert_sql)
                    if table_name not in loaded:
                        loaded[postgres_table_names[index]] = True
                except RuntimeError:
                    self.logger.error(f"loading to table {postgres_table_names[index]} has not been successful")

        for item in loaded:
            self.logger.info(f"loading to table {item} has  been successful")
