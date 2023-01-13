from libs.logger import get_logger
import os

from analytics.credentials import GoodDataCredentials
from analytics.impl import GoodDataAnalytics


logger = get_logger("analytics")

gooddata_credentials = GoodDataCredentials(
    os.getenv("ANALYTICS_GOODDATA_HOST"),
    os.getenv("ANALYTICS_GOODDATA_TOKEN"),
    os.getenv("ANALYTICS_GOODDATA_DATASOURCE_ID"),
)
gooddata_analytics = GoodDataAnalytics(logger, gooddata_credentials)

gooddata_analytics.invalid_cache()
