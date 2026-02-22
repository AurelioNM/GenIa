import logging

from clients.llm_client import LlmClient
from models.suggestion import ProductReviewOutput, SuggestionInput, SuggestionOutput
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


class SuggestionService:
    def __init__(self, llm_client: LlmClient):
        self.logger = logging.getLogger(__name__)
        self.llm_client = llm_client
        self.model = "tinyllama"

    # Simple prompt
    def get_suggestion1(self, suggestion: SuggestionInput) -> SuggestionOutput:
        self.logger.info("Getting suggestion")

        prompt = f"""
        Give me a marketing description for the product: {suggestion.input}.
        Keep it under 50 characters and make it catchy and engaging. 
        Include the product name in the description.
        """

        output = self.llm_client.invoke(prompt=prompt)
        return SuggestionOutput(output=output)

    # Langchain prompt template
    def get_suggestion2(self) -> SuggestionOutput:
        self.logger.info("Getting suggestion")

        template_string = """Translate the text \
        that is delimited by triple backticks \
        into a style that is {style}. \
        text: ```{text}```
        """
        prompt_template = ChatPromptTemplate.from_template(template_string)

        self.logger.info(
            f"Promt template: type={type(prompt_template)}, template={prompt_template}"
        )

        customer_style = """American English \
        in a calm and respectful tone
        """
        customer_email = """
        Arrr, I be fuming that me blender lid \
        flew off and splattered me kitchen walls \
        with smoothie! And to make matters worse, \
        the warranty don't cover the cost of \
        cleaning up me kitchen. I need yer help \
        right now, matey!
        """

        prompt_message = prompt_template.format_messages(
            style=customer_style, text=customer_email
        )
        self.logger.info(
            f"Promt message: type={type(prompt_message)}, message={prompt_message}"
        )
        output = self.llm_client.invoke2(prompt=prompt_message)
        return SuggestionOutput(output=output)

    # Langchain parse handling
    def get_suggestion3(self) -> ProductReviewOutput:
        self.logger.info("Getting suggestion")

        # INPUT
        review_template = """\
        For the following text, extract the following information:

        gift: Was the item purchased as a gift for someone else? \
        Answer True if yes, False if not or unknown.

        delivery_days: How many days did it take for the product\
        to arrive? If this information is not found, output -1.

        price_value: Extract any sentences about the value or price,\
        and output them as a comma separated Python list.

        text: {text}

        {format_instructions}
        """
        prompt_template = ChatPromptTemplate.from_template(review_template)

        self.logger.info(
            f"Promt template: type={type(prompt_template)}, template={prompt_template}"
        )

        customer_review = """\
        This leaf blower is pretty amazing.  It has four settings:\
        candle blower, gentle breeze, windy city, and tornado. \
        It arrived in two days, just in time for my wife's \
        anniversary present. \
        I think my wife liked it so much she was speechless. \
        So far I've been the only one using it, and I've been \
        using it every other morning to clear the leaves on our lawn. \
        It's slightly more expensive than the other leaf blowers \
        out there, but I think it's worth it for the extra features.
        """

        # OUTPUT
        parser = PydanticOutputParser(pydantic_object=ProductReviewOutput)

        prompt_message = prompt_template.format_messages(
            text=customer_review, format_instructions=parser.get_format_instructions()
        )
        self.logger.info(
            f"Promt message: type={type(prompt_message)}, message={prompt_message}"
        )

        output = self.llm_client.invoke2(prompt=prompt_message)

        parsed_output = parser.parse(output)

        return parsed_output

    # Memory
    def get_suggestion4(self, suggestion: SuggestionInput) -> SuggestionOutput:
        self.logger.info("Getting suggestion")

        output = self.llm_client.invoke3(suggestion.input)
        return SuggestionOutput(output=output)
