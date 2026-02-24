import logging

from clients.llm_client import LlmClient
from models.interaction import InteractionOutput, IntentationEnum
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

        output: Your response to the customer input.

        intation: What is the intation of the client based on this list of intations in uppercase: \
        PURCHASE_PRODUCT (means the customer wants to purchase an item), \
        SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER (means the customer wants to go out based on the weather), \
        SUGGEST_PRODUCT_BASED_ON_CATEGORY (means the customer wants suggestions of itens \
        to purchased based on a specific category), \
        SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY (means the customer wants suggestions of itens \
        to purchased based on his/her purchase history), \
        UNKNOWN (if you can not identify the intation based on the list);

        products_names: If the intation is PURCHASE_PRODUCT, fill this field with the product names list.

        text: {text}

        {format_instructions}
        """
        prompt_template = ChatPromptTemplate.from_template(intation_template)

        self.logger.info(
            f"Promt template: type={type(prompt_template)}, template={prompt_template}"
        )

        # OUTPUT
        parser = PydanticOutputParser(pydantic_object=InteractionOutput)

        prompt_message = prompt_template.format_messages(
            text=input,
            format_instructions=parser.get_format_instructions(),
        )
        self.logger.info(
            f"Promt message: type={type(prompt_message)}, message={prompt_message}"
        )

        output = self.llm_client.invoke2(prompt=prompt_message)

        parsed_output = parser.parse(output)
        self.logger.info(
            "========================================================================================"
        )
        self.logger.debug(f"Intation response: {parsed_output.model_dump()}")

        return parsed_output
