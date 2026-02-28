import logging
from typing import List

from clients.llm_client import LlmClient
from models.interaction import InteractionOutput
from models.product import ProductSummary
from models.weather import Weather
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


class IntationService:
    def __init__(self, llm_client: LlmClient):
        self.logger = logging.getLogger(__name__)
        self.llm_client = llm_client

    def get_intation(self, input: str, history: List[dict] = None) -> InteractionOutput:
        self.logger.info("Getting chat intation")

        # INPUT
        intation_template = """\
        You are a helpful, proactive conversational assistant for an e-commerce platform.

        Your job has TWO responsibilities:
        1) Identify the customer's intention.
        2) Always respond helpfully and continue the conversation naturally.

        IMPORTANT:
        - Even if the intention is UNKNOWN, you MUST continue the conversation.
        - NEVER say you cannot identify the intention.
        - NEVER ask the user to rephrase unless absolutely necessary.
        - Your main goal is to help the customer move forward.

        For the following customer interaction, extract the information in JSON format:

        intation:
        Classify the customer intention using ONLY one of these values:
        - PURCHASE_PRODUCT
        - SUGGEST_PRODUCT_BASED_ON_CATEGORY
        - SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY
        - SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER
        - UNKNOWN

        Use UNKNOWN only if no category clearly applies.
        UNKNOWN does NOT mean the conversation stops.

        output:
        Your response to the customer.
        - If intation is PURCHASE_PRODUCT → confirm the purchase was successfully processed.
        - Otherwise → respond naturally, helpfully, and conversationally.
        - Ask clarifying questions if helpful.
        - Keep the response under 80 words.
        - Sound human and friendly.
        - Continue the interaction.

        category:
        - If intation is SUGGEST_PRODUCT_BASED_ON_CATEGORY → extract in UPPERCASE the category mentioned.
        - Otherwise → null.

        products:
        - If intation is PURCHASE_PRODUCT:
            - Extract ALL mentioned products.
            - Return a list of objects.
            - Each object must contain:
                - name: string
                - quantity: integer
            - If quantity is not mentioned, assume quantity = 1.
        - Otherwise → null.

        Use chat history for context when determining intention and crafting the response.

        Customer text:
        {text}

        Chat history:
        {history}

        {format_instructions}
        """
        prompt_template = ChatPromptTemplate.from_template(intation_template)

        # OUTPUT
        parser = PydanticOutputParser(pydantic_object=InteractionOutput)

        prompt_message = prompt_template.format_messages(
            text=input,
            history=history,
            format_instructions=parser.get_format_instructions(),
        )

        output = self.llm_client.invoke2(prompt_message)

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

        weather_intation_template = """\
        You are an assistant that helps customers decide the best day \
        to go out based on weather forecast and suggests related products.

        Your task:

        Based ONLY on:
        1) The customer message
        2) The provided weather forecast list
        3) The provided climate-related products list

        You must:

        1. Identify what kind of weather the customer prefers (e.g., sunny, rainy, cold, hot, etc.).
        2. From the forecast list, select ONLY the days that match the customer's preference.
        3. For each suggested day, include:
        - Date
        - Weather condition
        - Temperature in Celsius
        4. Suggest products that match the weather condition mentioned by the customer.
        5. Do NOT invent days or products.
        6. If no forecast matches the customer's preference, clearly say that no suitable day was found.
        7. Keep the tone natural and helpful.

        Return your response in the following structured format:

        Weather Suggestion
        Customer preference: <identified weather preference>

        Recommended Days
        - Date: <date>
        - Condition: <weather condition>
        - Temperature: <temperature> °C

        (Repeat for each matching day. If none, say: "No suitable days found based on the forecast.")

        ---

        Here are some great products for for the weather condition
        - <product name> — $<product price>
        - <product name> — $<product price>

        (If no products are relevant, say: "No specific products recommended for this weather.")

        ---

        Customer message:
        {text}

        Weather forecast list:
        {forecast}

        Climate-related products:
        {products}
        """
        prompt_template = ChatPromptTemplate.from_template(weather_intation_template)

        self.logger.info(f"Forecast: size={len(forecast)}")

        prompt_message = prompt_template.format_messages(
            text=customer_input, forecast=forecast, products=products
        )

        output = self.llm_client.invoke2(prompt_message)
        return output
