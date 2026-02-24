import logging

from clients.llm_client import LlmClient
from models.interaction import InteractionOutput, InteractionRequest, IntentationEnum
from services.intation_service import IntationService


class InteractionService:
    def __init__(self, intation_service: IntationService):
        self.logger = logging.getLogger(__name__)
        self.intation_service = intation_service

    def get_chat_interaction(
        self, interaction_request: InteractionRequest
    ) -> InteractionOutput:
        self.logger.info("Getting chat interaction")

        output: InteractionOutput = self.intation_service.get_intation(
            interaction_request.input
        )

        return output
