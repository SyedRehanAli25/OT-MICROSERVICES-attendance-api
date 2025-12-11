"""
Module for client SDK of Postgres and respective actions.
- Creation of record
- Read particular record
- Read all records
- Healthcheck for application
"""
# pylint: disable=import-error
import os
from unittest.mock import MagicMock
from .postgres_conn import CorePostgresClient


# pylint: disable=too-few-public-methods
class DatabaseSDKFacade:
    """Class wrapper method for client db related actions"""

    # Use real DB locally, mock DB in Jenkins
    if os.environ.get("JENKINS_HOME"):
        print("  Jenkins detected — Using MOCK Postgres client (no real DB connection)")
        database = MagicMock()
    else:
        database = CorePostgresClient()
