import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import (
    BaseMessage,
    ToolMessage,
    SystemMessage,
    AIMessage,
    HumanMessage,
)
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv

load_dotenv()

document_content = ""


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def update(content: str) -> str:
    """Updates the document with the provided content."""

    global document_content
    document_content = content

    return f"Document was updated. The current content is: \n{document_content}"


@tool
def save(file_name: str) -> str:
    """Saves the document to a text file and finish the process

    Args:
        file_name: Name for the text file.
    """

    try:
        if not file_name.endswith(".txt"):
            file_name = f"{file_name}.txt"

        with open(file_name, "w") as file:
            file.write(document_content)

        result = f"\nDocument was saved on: {file_name}"
        print(result)
        return result
    except Exception as e:
        return f"Error saving document: {str(e)}"


tools = [update, save]
llm = ChatGroq(model_name="openai/gpt-oss-120b").bind_tools(tools)


def agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
                                  
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.
                                  
    The current document is:{document_content}
    """)

    if not state["messages"]:
        user_input = (
            "I'm ready to help you update a document. What would you like to create?"
        )
        user_message = HumanMessage(content=user_input)

    else:
        user_input = input("\nWhat would you like to do with the document?")
        print(f"\n USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = llm.invoke(all_messages)

    print(f"\n AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"\n TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}


def should_continue(state: AgentState) -> str:
    """Determine if the flow should continue or end the conversation."""

    messages = state["messages"]

    if not messages:
        return "continue"

    for message in reversed(messages):
        if (
            isinstance(message, ToolMessage)
            and "saved" in message.content.lower()
            and "document" in message.content.lower()
        ):
            return "end"

    return "continue"


def print_messages(messages):
    if not messages:
        return

    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n TOOL RESULT: {message.content}")


graph = StateGraph(AgentState)

graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges("tools", should_continue, {"continue": "agent", "end": END})

app = graph.compile()


def run_document_agent():
    print("\n === Drafter Start ===")
    state = {"messages": []}

    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])

    print("\n === Drafter End ===")


if __name__ == "__main__":
    run_document_agent()
