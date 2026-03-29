import logging

import httpx
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory


class StudiesLlmClient:
    def __init__(self, llm_ollama: ChatOllama, llm_groq: ChatGroq):
        self.logger = logging.getLogger(__name__)
        self.llm_ollama = llm_ollama
        self.llm_groq = llm_groq

        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=llm_ollama, memory=self.memory, verbose=True
        )

    def invoke(self, prompt: str) -> str:
        try:
            self.logger.info(f"Generating LLM output for prompt={prompt}")

            response = self.llm_ollama.invoke([HumanMessage(content=prompt)])

            content = response.content

            self.logger.info(f"LLM output response: {content}")

            return content

        except httpx.RequestError as e:
            self.logger.error(f"Failed to generate LLM output: {e}")
            raise

    def invoke2(self, prompt) -> str:
        try:
            self.logger.info(f"Generating LLM output for prompt={prompt}")

            response = self.llm_groq.invoke(prompt)

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
