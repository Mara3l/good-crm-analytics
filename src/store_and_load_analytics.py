from libs.logger import get_logger
import os
import sys

from analytics.credentials import GoodDataCredentials
from analytics.impl import GoodDataAnalytics


logger = get_logger("analytics")

gooddata_credentials = GoodDataCredentials(
    os.getenv("ANALYTICS_GOODDATA_HOST"),
    os.getenv("ANALYTICS_GOODDATA_TOKEN"),
    os.getenv("ANALYTICS_GOODDATA_DATASOURCE_ID"),
)
gooddata_analytics = GoodDataAnalytics(logger, gooddata_credentials)
arguments = sys.argv

if len(arguments) < 3:
    logger.error("Please provide operation (store or load) and workspace ID")
    sys.exit(5)

operation = arguments[1]
workspace = arguments[2]

if operation != "store" and operation != "load":
    logger.error("Unknown operation")
    sys.exit(5)

if operation == "store":
    gooddata_analytics.store_content(workspace)

if operation == "load":
    gooddata_analytics.load_and_put_content(workspace)
    