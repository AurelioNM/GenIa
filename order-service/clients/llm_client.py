import logging
import httpx

from langchain.chat_models import BaseChatModel
from langchain_classic.agents import AgentExecutor


class LlmClient:
    def __init__(
        self,
        default_model: BaseChatModel,
        agent_executor: AgentExecutor,
    ):
        self.logger = logging.getLogger(__name__)
        self.default_model = default_model

        self.agent_executor = agent_executor

    async def invoke(self, prompt) -> str:
        try:
            self.logger.info(f"Generating LLM output with tools")

            response = await self.agent_executor.ainvoke({"input": prompt})

            content = response["output"]

            self.logger.info(f"LLM output response: response={response}")

            return content

        except httpx.RequestError as e:
            self.logger.error(f"Failed to generate LLM output: {e}")
            raise
