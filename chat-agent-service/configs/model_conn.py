import os

from langchain_classic.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_groq import ChatGroq
from tools.suggest_product_on_category_tool import SuggestProductOnCategoryTool
from tools.answer_question_tool import GetQuestionAnswerBaseTool
from tools.suggest_day_and_product_on_weather import SuggestDayAndProductOnWeatherTool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


from dotenv import load_dotenv

load_dotenv()


async def load_mcp_tools():
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "http",
                "url": f"{os.getenv("WISDOM_MCP_BASE_URL")}/mcp",
            },
        }
    )

    tools = await client.get_tools()
    return tools


async def get_agent_executor(
    llm_groq: ChatGroq,
    suggest_product_on_category_tool: SuggestProductOnCategoryTool,
    suggest_day_and_product_on_weather_tool: SuggestDayAndProductOnWeatherTool,
    get_question_answer_base_tool: GetQuestionAnswerBaseTool,
) -> AgentExecutor:

    mcp_tools = await load_mcp_tools()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    tools = [
        suggest_product_on_category_tool.get_tool(),
        suggest_day_and_product_on_weather_tool.get_tool(),
        get_question_answer_base_tool.get_tool(),
        *mcp_tools,
    ]

    agent = create_tool_calling_agent(llm_groq, tools, prompt)

    return AgentExecutor(agent=agent, tools=tools, verbose=True)
