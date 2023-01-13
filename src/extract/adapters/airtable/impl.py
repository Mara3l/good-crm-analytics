from logging import Logger
from extract.adapters.airtable.credentials import AirtableCredentials
from pyairtable import Table


class AirTableAdapter:
    def __init__(self, logger: Logger, credentials: AirtableCredentials):
        self.logger = logger
        self.api_key = credentials.api_key
        self.base_id = credentials.base_id

    def extract(self, table_ids: list) -> dict:
        data_fetched = {}
        dict_of_data = {}

        for table_id in table_ids:
            try:
                table = Table(self.api_key, self.base_id, table_id)
                dict_of_data[table_id] = table.all()
                data_fetched[table_id] = True
            except RuntimeError:
                self.logger.error(f"loading of airtable '{table_id}' data has not been successful")

        for table_id in data_fetched:
            if data_fetched[table_id] is True:
                self.logger.info(f"loading of airtable '{table_id}' data has been successful")

        return dict_of_data
