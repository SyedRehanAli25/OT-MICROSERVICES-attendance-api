# client/tests/test_redis_conn.py
import os
from unittest import mock
import pytest
from client.redis import MiddlewareSDKFacade
from client.redis.redis_conn import CoreRedisClient, get_caching_data


@pytest.fixture
def mock_config_yaml(tmp_path):
    content = """
    redis:
        host: localhost
        port: 6379
        password: ""
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(content)
    os.environ['CONFIG_FILE'] = str(config_file)
    yield config_file
    del os.environ['CONFIG_FILE']


def test_get_caching_data(mock_config_yaml):
    with mock.patch("builtins.open", mock.mock_open(read_data=mock_config_yaml.read_text())):
        result = get_caching_data()
        assert result["CACHE_REDIS_HOST"] == "localhost"
        assert result["CACHE_REDIS_PORT"] == 6379
        assert result["CACHE_REDIS_URL"] == "redis://localhost:6379/0"


def test_redis_status_up():
    # Patch the Redis client ping to return True
    with mock.patch.object(MiddlewareSDKFacade.cache.client, "ping", return_value=True):
        status = MiddlewareSDKFacade.cache.redis_status()
        assert status == "up"


def test_redis_status_down():
    # Patch the Redis client ping to raise an Exception
    with mock.patch.object(MiddlewareSDKFacade.cache.client, "ping", side_effect=Exception("Redis down")):
        status = MiddlewareSDKFacade.cache.redis_status()
        assert status == "down"
