# client/redis/redis_conn.py
import os
import yaml
import redis


class CoreRedisClient:
    def __init__(self):
        self.client = self._connect()

    def _connect(self):
        # Load Redis config from YAML
        config_file = os.environ.get("CONFIG_FILE", "config.yaml")
        with open(config_file, "r") as f:
            cfg = yaml.safe_load(f)

        redis_cfg = cfg.get("redis", {})
        host = redis_cfg.get("host", "localhost")
        port = redis_cfg.get("port", 6379)
        password = redis_cfg.get("password", "")

        return redis.Redis(host=host, port=port, password=password, decode_responses=True)

    def redis_status(self):
        """Check if Redis is up or down"""
        try:
            self.client.ping()
            return "up"
        except Exception:
            return "down"


# Singleton instance to be used across your app
MiddlewareSDKFacade = type("MiddlewareSDKFacade", (), {})()
MiddlewareSDKFacade.cache = CoreRedisClient()


def get_caching_data():
    """Helper to extract caching config"""
    config_file = os.environ.get("CONFIG_FILE", "config.yaml")
    with open(config_file, "r") as f:
        cfg = yaml.safe_load(f)

    redis_cfg = cfg.get("redis", {})
    host = redis_cfg.get("host", "localhost")
    port = redis_cfg.get("port", 6379)

    return {
        "CACHE_REDIS_HOST": host,
        "CACHE_REDIS_PORT": port,
        "CACHE_REDIS_URL": f"redis://{host}:{port}/0"
    }
