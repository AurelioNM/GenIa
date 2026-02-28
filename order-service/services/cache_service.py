import logging
from typing import List

from storage.cache_storage import CacheStorage
from models.interaction import InteractionRequest, InteractionOutput


class CacheService:
    def __init__(
        self,
        cache_storage: CacheStorage,
    ):
        self.logger = logging.getLogger(__name__)
        self.cache_storage = cache_storage
        self.session_key_prefix = "chat:session:"

    def get_chat_history(self, session_id: str):
        self.logger.info(f"Getting chat history from cahce: session_id={session_id}")

        key = self.session_key_prefix + session_id
        result = self.cache_storage.get_cache(key)

        self.logger.info(
            f"Got chat history from cache for session_id={session_id}, result={result}"
        )
        return result

    def save_chat_history(
        self,
        session_id: str,
        history: List[dict],
        input: InteractionRequest,
        output: InteractionOutput,
    ):
        self.logger.info(
            f"Saving chat history on cache: session_id={session_id}, input={input.input}, output={output.output}"
        )

        key = self.session_key_prefix + session_id
        history: List[dict] = history[-18:]
        history.append(
            {
                "role": "user",
                "content": input.input,
            }
        )
        history.append(
            {
                "role": "assistant",
                "content": output.output,
            }
        )

        self.cache_storage.save_cache(key, history)

        self.logger.info(f"Saved chat history on cache: session_id={session_id}")
