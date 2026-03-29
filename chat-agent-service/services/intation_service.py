import logging
from typing import List

from clients.llm_client import LlmClient
from models.interaction import (
    InteractionOutputV2,
    InteractionRequest,
)
from langchain_core.prompts import ChatPromptTemplate
from prompts.intation_prompt import intation_template


class IntationService:
    def __init__(self, llm_client: LlmClient):
        self.logger = logging.getLogger(__name__)
        self.llm_client = llm_client

    async def get_intation(
        self, input: InteractionRequest, history: List[dict] = None
    ) -> InteractionOutputV2:
        self.logger.info("Getting chat intation v2")
        prompt_template = ChatPromptTemplate.from_template(intation_template)

        prompt_message = prompt_template.format_messages(
            text=input.input,
            customer_email=input.customer_email,
            history=history,
        )

        output = await self.llm_client.invoke(prompt_message)

        parsed_output = InteractionOutputV2(output=output)
        self.logger.info(f"Intation v2 response: {parsed_output.model_dump()}")

        return parsed_output
