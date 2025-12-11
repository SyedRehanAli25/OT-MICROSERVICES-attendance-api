"""
Module for Redis data and interface
"""

import os
import yaml
import redis
from unittest.mock import MagicMock

CONFIG_FILE = os.getenv("CONFIG_FILE", "config.yaml")


def get_caching_data():
    """Function to get cache config for redis cache"""
    with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
        yaml_value = yaml.load(config_file, Loader=yaml.FullLoader)

    return {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_HOST": yaml_value["redis"]["host"],
        "CACHE_REDIS_PORT": yaml_value["redis"]["port"],
        "CACHE_REDIS_URL": f"redis://{yaml_value['redis']['host']}:{yaml_value['redis']['port']}/0",
    }


class CoreRedisClient:
    """Class for defining the structure of Redis database"""

    def __init__(self):
        # If Jenkins is running → use mock client
        if os.environ.get("JENKINS_HOME"):
            print("  Jenkins detected — Using MOCK Redis client (no real Redis connection)")
            self.client = MagicMock()
            return

        # Local development → use real Redis config
        with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
            yaml_values = yaml.load(config_file, Loader=yaml.FullLoader)

        self.client = redis.Redis(
            host=yaml_values["redis"]["host"],
            port=yaml_values["redis"]["port"],
            password=yaml_values["redis"].get("password", None),
            decode_responses=True,
        )

    def redis_status(self):
        """Function for getting the health of redis"""
        try:
            self.client.ping()
            return "up"
        except Exception:
            return "down"
