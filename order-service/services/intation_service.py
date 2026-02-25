import logging

from clients.llm_client import LlmClient
from models.interaction import InteractionOutput, IntationEnum
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
        For the following customer interaction, extract the following information:

        intation: What is the intation of the client based ONLY on this list of intations in uppercase:
        - PURCHASE_PRODUCT (customer wants to purchase one or more products)
        - SUGGEST_PRODUCT_BASED_ON_CATEGORY (customer wants suggestions of products to buy based on a specific category)
        - SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY (customer wants suggestions of products to buy based on his/her purchase history)
        - SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER (customer wants to go out based on the weather)
        - UNKNOWN (if you cannot clearly identify the intation)

        output: Your response to the customer input.
        - If the intation is PURCHASE_PRODUCT, tell the customer the purchase was successfully processed.
        - Otherwise, respond naturally and helpfully according to the intation.

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

        output = self.llm_client.invoke2(prompt=prompt_message)

        parsed_output = parser.parse(output)
        self.logger.info(f"Intation response: {parsed_output.model_dump()}")

        return parsed_output
