import logging
import os


import httpx
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory


class LlmClient:
    def __init__(self, llm: ChatOllama):
        self.logger = logging.getLogger(__name__)
        self.llm = llm

        # Memory config TODO move to constructor
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(llm=llm, memory=self.memory, verbose=True)

    def invoke(self, prompt: str) -> str:
        try:
            self.logger.info(f"Generating LLM output for prompt={prompt}")

            response = self.llm.invoke([HumanMessage(content=prompt)])

            content = response.content

            self.logger.info(f"LLM output response: {content}")

            return content

        except httpx.RequestError as e:
            self.logger.error(f"Failed to generate LLM output: {e}")
            raise

    def invoke2(self, prompt) -> str:
        try:
            self.logger.info(f"Generating LLM output for prompt={prompt}")

            response = self.llm.invoke(prompt)

            content = response.content

            self.logger.info(f"LLM output response: {content}")

            return content

        except httpx.RequestError as e:
            self.logger.error(f"Failed to generate LLM output: {e}")
            raise

    def invoke3(self, input) -> str:
        try:
            self.logger.info(f"Generating LLM output for prompt={input}")
            self.logger.info(f"LLM memory buffer: {self.memory.buffer}")

            response = self.conversation.predict(input=input)
            self.logger.info(f"LLM output response: {response}")

            return response

        except httpx.RequestError as e:
            self.logger.error(f"Failed to generate LLM output: {e}")
            raise
