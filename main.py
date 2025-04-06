import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Arxiv and Wikipedia API wrappers
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=500)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

wiki_tool.invoke("Who is Cristiano Ronaldo")

tools = [wiki_tool]

# Loading the Groq_api_key
load_dotenv("/home/abcom/langGraph/groq-langgraph-chatbot/key.env")
groq_api_key = os.getenv("chatbot_api_key")

# Initializing the Llm and binding it to the tools
llm = ChatGroq(groq_api_key=groq_api_key, model="llama3-70b-8192")
llm_with_tools = llm.bind_tools(tools=tools)

# LangGraph Applications
class State:
    message: Annotated[list, add_messages]

# Creating the chatbot
def chatbot(state:State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Building the StateGraph
graph_bulider = StateGraph(State)
graph_bulider.add_node("chatbot", chatbot)
graph_bulider.add_edge(START, "chatbot")
tool_node = ToolNode(tools=tools)
graph_bulider.add_node("tools", tool_node)

graph_bulider.add_conditional_edges(
    "chatbot",
    tools_condition
)
graph_bulider.add_edge("tools", "chatbot")
graph_bulider.add_edge("chatbot", END)

graph = graph_bulider.compile()

user_input = "Hi there! My name is Suvrat"
events = graph.stream(
    {"messages": [("user", user_input)]}, stream_mode="values"
)
for event in events:
    event["messages"][-1].pretty_print()