
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from agent.state import AgentState
from agent.tools import get_tools

# Initialize LLM
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

def planner(state: AgentState):
    """
    Analyzes the user's request and creates a plan.
    Determines if search/tools are needed.
    """
    messages = state["messages"]
    system_msg = SystemMessage(content="You are a planning agent. Analyze the conversation and decide the next step. "
                                       "If the user asks a question requiring external information, tools, or time, output 'search'. "
                                       "If you can answer it directly or if it's a simple greeting, output 'do'. "
                                       "Provide a brief plan text.")

    response = llm.invoke([system_msg] + messages)

    # Very simplified logic for deciding the next node
    content = response.content.lower()
    next_step = "search" if "search" in content or "tool" in content else "do"

    return {"plan": response.content, "next_step": next_step}

def searcher(state: AgentState):
    """
    Executes necessary tools to gather information.
    """
    messages = state["messages"]
    # Bind tools to LLM
    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)

    # Invoke tools (simplification for LangGraph's tool calling)
    response = llm_with_tools.invoke(messages)

    # In a full implementation, this node would invoke a ToolNode to actually execute the tools.
    # We will simulate the results here for structure purposes, then expand in the `tools` step.

    return {"search_results": "Tool execution results go here.", "messages": [response]}

def doer(state: AgentState):
    """
    Compiles the final answer.
    """
    messages = state["messages"]
    system_msg = SystemMessage(content="You are a helpful AI assistant named Janus. "
                                       "Use the provided context and conversation history to answer the user's query.")

    # Include search results if any
    if state.get("search_results"):
        system_msg.content += f"\nContext from tools: {state['search_results']}"

    response = llm.invoke([system_msg] + messages)

    return {"messages": [response]}

def route_planner(state: AgentState):
    return state["next_step"]

def create_janus_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner)
    workflow.add_node("searcher", searcher)
    workflow.add_node("doer", doer)

    workflow.set_entry_point("planner")

    workflow.add_conditional_edges(
        "planner",
        route_planner,
        {
            "search": "searcher",
            "do": "doer"
        }
    )

    workflow.add_edge("searcher", "doer")
    workflow.add_edge("doer", END)

    return workflow.compile()

# Example usage singleton
janus_graph = create_janus_graph()
