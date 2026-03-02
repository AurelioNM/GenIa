import logging
import httpx

from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from tools.purchase_tool import PurchaseTool
from models.interaction import InteractionOutput


class LlmClient:
    def __init__(
        self,
        llm_ollama: ChatOllama,
        llm_groq: ChatGroq,
        purchase_tool: PurchaseTool,
    ):
        self.logger = logging.getLogger(__name__)
        self.llm_ollama = llm_ollama
        self.llm_groq = llm_groq
        self.llm_with_tools = llm_groq.bind_tools([purchase_product])

    def invoke(self, prompt) -> str:
        try:
            self.logger.info(f"Generating LLM output for prompt={prompt}")

            response = self.llm_groq.invoke(prompt)

            content = response.content

            self.logger.info(f"LLM output response: {content}")
            return content

        except httpx.RequestError as e:
            self.logger.error(f"Failed to generate LLM output: {e}")
            raise

    def invoke_with_tool(self, prompt) -> str:
        try:
            self.logger.info(f"Generating LLM output with tools")

            response = self.llm_with_tools.invoke(prompt)

            content = response.content

            self.logger.info(f"LLM output response: {content}")

            return content

        except httpx.RequestError as e:
            self.logger.error(f"Failed to generate LLM output: {e}")
            raise


@tool
def purchase_product(output: InteractionOutput) -> str:
    """
    Creates a purchase order for the given customer with the specified products.
    """
    print("===================================================================")
    print("===================================================================")
    print("TOOL purchase_product called with output:", output.model_dump())

    return "Order successfully created."
