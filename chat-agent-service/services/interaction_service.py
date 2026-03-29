import logging
from typing import List

from models.order_request import OrderRequest
from models.interaction import (
    InteractionOutputV2,
    InteractionRequest,
)
from services.intation_service import IntationService
from services.cache_service import CacheService


class InteractionService:
    def __init__(
        self,
        intation_service: IntationService,
        cache_service: CacheService,
    ):
        self.logger = logging.getLogger(__name__)
        self.intation_service = intation_service
        self.cache_service = cache_service

    async def get_chat_interaction(
        self, interaction_request: InteractionRequest, session_id: str
    ) -> InteractionOutputV2:
        self.logger.info("Getting chat interaction")

        history = self.cache_service.get_chat_history(session_id)

        output: InteractionOutputV2 = await self.intation_service.get_intation(
            interaction_request, history
        )

        self.cache_service.save_chat_history(
            session_id, history, interaction_request, output
        )

        return output
