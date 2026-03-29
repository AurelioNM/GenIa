from typing import List
import json
import logging
import os

from redis import Redis


class CacheStorage:
    def __init__(self, cache_connection: Redis):
        self.logger = logging.getLogger(__name__)
        self.cache_connection: Redis = cache_connection
        self.ttl = int(os.getenv("REDIS_TTL"))

    def get_cache(self, key: str) -> List[dict]:
        try:
            self.logger.info(f"Getting cache for key={key}")

            data = self.cache_connection.get(key)

            if not data:
                return []

            return json.loads(data)
        except Exception as e:
            self.logger.error(f"Failed to get cache for key={key}. Exception: {e}")
            raise

    def save_cache(self, key: str, data: List[dict]):
        try:
            self.logger.info(f"Saving cache: key={key}, data={data}")

            self.cache_connection.set(key, json.dumps(data), ex=self.ttl)

        except Exception as e:
            self.logger.error(f"Failed to save cache for key={key}. Exception: {e}")
            raise
