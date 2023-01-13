from logging import Logger
from pathlib import Path
from gooddata_sdk import GoodDataSdk

from analytics.credentials import GoodDataCredentials


class GoodDataAnalytics:
    def __init__(self, logger: Logger, credentials: GoodDataCredentials):
        self.logger = logger
        self.host = credentials.host
        self.token = credentials.token
        self.data_source_id = credentials.data_source_id
        self.sdk = GoodDataSdk.create(self.host, self.token)

    def invalid_cache(self) -> None:
        try:
            self.sdk.catalog_data_source.register_upload_notification(
                self.data_source_id
            )
            self.logger.info("Cache has been invalided")
        except RuntimeError:
            self.logger.error("Cache has not been invalided")

    def store_content(self, workspace_id: str) -> None:
        self.sdk.catalog_workspace_content.store_ldm_to_disk(workspace_id, Path("./layouts"))
        self.sdk.catalog_workspace_content.store_analytics_model_to_disk(workspace_id, Path("./layouts"))

        self.logger.info("Analytics has been stored")
    
    def load_and_put_content(self, workspace_id: str) -> None:
        ldm = self.sdk.catalog_workspace_content.load_ldm_from_disk(Path("./layouts"))
        analytics_model = self.sdk.catalog_workspace_content.load_analytics_model_from_disk(Path("./layouts"))


        self.sdk.catalog_workspace_content.put_declarative_ldm(workspace_id, ldm)
        self.sdk.catalog_workspace_content.put_declarative_analytics_model(workspace_id, analytics_model)

        self.logger.info("Analytics has been loaded")
