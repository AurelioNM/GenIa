import logging
from typing import List

from clients.llm_client import LlmClient
from models.interaction import InteractionOutput, InteractionRequest
from models.product import ProductSummary
from models.weather import Weather
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from prompts.intation_prompt import intation_template
from prompts.weather_prompt import weather_template
from prompts.question_prompt import question_template


class IntationService:
    def __init__(self, llm_client: LlmClient):
        self.logger = logging.getLogger(__name__)
        self.llm_client = llm_client

    def get_intation(
        self, input: InteractionRequest, history: List[dict] = None
    ) -> InteractionOutput:
        self.logger.info("Getting chat intation")
        prompt_template = ChatPromptTemplate.from_template(intation_template)

        parser = PydanticOutputParser(pydantic_object=InteractionOutput)

        prompt_message = prompt_template.format_messages(
            text=input.input,
            customer_email=input.customer_email,
            history=history,
            format_instructions=parser.get_format_instructions(),
        )

        output = self.llm_client.invoke(prompt_message)

        parsed_output = parser.parse(output)
        self.logger.info(f"Intation response: {parsed_output.model_dump()}")

        return parsed_output

    def process_weather_intation(
        self,
        customer_input: str,
        forecast: List[Weather],
        products: List[ProductSummary],
    ) -> str:
        self.logger.info("Processing weather intation")
        prompt_template = ChatPromptTemplate.from_template(weather_template)

        self.logger.info(f"Forecast: size={len(forecast)}")

        prompt_message = prompt_template.format_messages(
            text=customer_input, forecast=forecast, products=products
        )

        output = self.llm_client.invoke(prompt_message)
        return output

    def process_question_intation(
        self,
        customer_input: str,
        questions_base: List[dict],
    ) -> str:
        self.logger.info("Processing question intation")
        prompt_template = ChatPromptTemplate.from_template(question_template)

        self.logger.info(f"Questions base: size={len(questions_base)}")

        prompt_message = prompt_template.format_messages(
            text=customer_input, question_base=questions_base
        )

        output = self.llm_client.invoke(prompt_message)
        return output
