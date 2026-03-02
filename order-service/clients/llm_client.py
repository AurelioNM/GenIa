import logging
import httpx

from langchain.tools import tool
from langchain_classic.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from tools.process_purchase_tool import ProcessPurchaseTool
from tools.suggest_product_on_category_tool import SuggestProductOnCategoryTool
from tools.suggest_product_on_history_tool import SuggestProductOnHistoryTool
from tools.answer_question_tool import GetQuestionAnswerBaseTool
from tools.suggest_day_and_product_on_weather import SuggestDayAndProductOnWeatherTool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent


class LlmClient:
    def __init__(
        self,
        llm_ollama: ChatOllama,
        llm_groq: ChatGroq,
        process_purchase_tool: ProcessPurchaseTool,
        suggest_product_on_category_tool: SuggestProductOnCategoryTool,
        suggest_product_on_history_tool: SuggestProductOnHistoryTool,
        suggest_day_and_product_on_weather_tool: SuggestDayAndProductOnWeatherTool,
        get_question_answer_base_tool: GetQuestionAnswerBaseTool,
    ):
        self.logger = logging.getLogger(__name__)
        self.llm_ollama = llm_ollama
        self.llm_groq = llm_groq

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant."),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        tools = [
            process_purchase_tool.get_tool(),
            suggest_product_on_category_tool.get_tool(),
            suggest_product_on_history_tool.get_tool(),
            suggest_day_and_product_on_weather_tool.get_tool(),
            get_question_answer_base_tool.get_tool(),
        ]
        agent = create_tool_calling_agent(self.llm_groq, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

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

    async def invoke_with_tools(self, prompt) -> str:
        try:
            self.logger.info(f"Generating LLM output with tools")

            response = await self.agent_executor.ainvoke({"input": prompt})

            content = response["output"]

            self.logger.info(f"LLM output response: response={response}")

            return content

        except httpx.RequestError as e:
            self.logger.error(f"Failed to generate LLM output: {e}")
            raise
