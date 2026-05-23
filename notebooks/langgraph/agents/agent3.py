import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int):
    """This is an addition function that adds 2 numbers together"""
    return a + b


@tool
def subtract(a: int, b: int):
    """This is a subtraction function that subtracts 2 numbers"""
    return a - b


@tool
def multiply(a: int, b: int):
    """This is a multiplication function that multiplies 2 numbers"""
    return a * b


tools = [add, subtract, multiply]

llm = ChatGroq(model_name="openai/gpt-oss-120b").bind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content="You are my AI assistant, answer my query to the best of your ability."
    )
    response = llm.invoke([system_prompt] + state["messages"])

    return {"messages": [response]}


def should_continue(state: AgentState):
    messages = state["messages"]
    last_messages = messages[-1]

    if not last_messages.tool_calls:
        return "end"
    else:
        return "continue"


graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {"continue": "tools", "end": END},
)

graph.add_edge("tools", "our_agent")

app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {
    "messages": [
        (
            "user",
            "Using tools, add 40 + 12 and then multiply the result by 6. Also tell me a joke please",
        )
    ]
}
print_stream(app.stream(inputs, stream_mode="values"))
