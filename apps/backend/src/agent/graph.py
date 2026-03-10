from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from agent.state import AgentState
from agent.tools import get_tools, rag_search_tool

# Initialize LLM
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)


def planner(state: AgentState):
    """
    Analyzes the user's request and creates a plan.
    Determines if search/tools are needed.
    """
    messages = state["messages"]
    system_msg = SystemMessage(
        content=(
            "You are a planning agent. Analyze the conversation and decide the next step. "
            "If the user asks a question requiring external information, tools, or time, "
            "output 'search'. If you can answer directly or it's a simple greeting, "
            "output 'do'. Provide a brief plan text."
        )
    )

    response = llm.invoke([system_msg] + messages)

    # Very simplified logic for deciding the next node
    content = response.content.lower()
    next_step = "search" if "search" in content or "tool" in content else "do"

    return {"plan": response.content, "next_step": next_step}


def searcher(state: AgentState):
    """
    Executes RAG search and other tools to gather information.
    """
    messages = state["messages"]
    last_user_content = ""
    for m in reversed(messages):
        if isinstance(m, HumanMessage):
            last_user_content = m.content
            break

    search_results_parts = []
    retrieval_sources: list[dict] = []
    if last_user_content:
        try:
            from services.vector_store_service import retrieve

            raw = retrieve(last_user_content)
            if raw:
                retrieval_sources = raw
                rag_result = rag_search_tool.invoke({"query": last_user_content})
                if rag_result and "failed" not in str(rag_result).lower():
                    search_results_parts.append(rag_result)
        except Exception as e:
            search_results_parts.append(f"Knowledge base search error: {e}")

    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(messages)

    search_results = (
        "\n\n".join(search_results_parts)
        if search_results_parts
        else "No additional context from tools."
    )

    return {
        "search_results": search_results,
        "messages": [response],
        "retrieval_sources": retrieval_sources,
    }


def doer(state: AgentState):
    """
    Compiles the final answer.
    """
    messages = state["messages"]
    system_msg = SystemMessage(
        content="You are a helpful AI assistant named Janus. "
        "Use the provided context and conversation history to answer the user's query."
    )

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

    workflow.add_conditional_edges("planner", route_planner, {"search": "searcher", "do": "doer"})

    workflow.add_edge("searcher", "doer")
    workflow.add_edge("doer", END)

    return workflow.compile()


# Example usage singleton
janus_graph = create_janus_graph()
