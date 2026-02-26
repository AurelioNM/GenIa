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

    def get_intation(self, input: str) -> InteractionOutput:
        self.logger.info("Getting chat intation")

        # INPUT
        intation_template = """\
        For the following customer interaction, extract the following information in a JSON format:

        intation: What is the intation of the client based ONLY on this list of intations in uppercase:
        - PURCHASE_PRODUCT (customer wants to purchase one or more products)
        - SUGGEST_PRODUCT_BASED_ON_CATEGORY (customer wants suggestions of products to buy based on a specific category)
        - SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY (customer wants suggestions of products to buy based on his/her purchase history)
        - SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER (customer wants to go out based on the weather)
        - UNKNOWN (if you cannot clearly identify the intation)

        output: Your response to the customer input.
        - If the intation is PURCHASE_PRODUCT, tell the customer the purchase was successfully processed.
        - Otherwise, respond naturally and helpfully according to the intation.

        category:
        - If the intation is SUGGEST_PRODUCT_BASED_ON_CATEGORY, extract in uppercase the category mentioned.
        - If the intation is NOT SUGGEST_PRODUCT_BASED_ON_CATEGORY, this field must be null.

        products:
        - If the intation is PURCHASE_PRODUCT, extract ALL products mentioned.
        - Return a list of objects.
        - Each object must contain:
            - name: product name as string
            - quantity: integer quantity requested
        - If quantity is not explicitly mentioned, assume quantity = 1.
        - If the intation is NOT PURCHASE_PRODUCT, this field must be null.

        Customer text:
        {text}

        {format_instructions}
        """
        prompt_template = ChatPromptTemplate.from_template(intation_template)

        # OUTPUT
        parser = PydanticOutputParser(pydantic_object=InteractionOutput)

        prompt_message = prompt_template.format_messages(
            text=input,
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
