import datetime
import os

import pytz
from langchain.tools import tool


@tool
def time_tool(timezone: str = "UTC") -> str:
    """Returns the current time for a given timezone."""
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz)
        return current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    except Exception as e:
        return f"Error: Invalid timezone '{timezone}'. {str(e)}"

@tool
def weather_tool(location: str) -> str:
    """Get the current weather for a specific location."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not configured."
    # Integration placeholder
    return f"The weather in {location} is currently sunny and 25°C."

@tool
def calendar_tool(action: str, event_details: str = "") -> str:
    """Manage Google Calendar events. action can be 'list' or 'create'. event_details specify title/time."""
    # Integration placeholder
    return f"Calendar action '{action}' executed successfully."

@tool
def messenger_tool(message: str, recipient: str) -> str:
    """Send a message to a user via Messenger."""
    # Integration placeholder
    return f"Message sent to {recipient}: {message}"

@tool
def rag_search_tool(query: str) -> str:
    """Search the knowledge base (Pinecone) for relevant context."""
    # Pinecone logic placeholder
    # from langchain_pinecone import PineconeVectorStore
    # from langchain_openai import OpenAIEmbeddings
    # embeddings = OpenAIEmbeddings()
    # vectorstore = PineconeVectorStore(index_name="janus-kb", embedding=embeddings)
    # docs = vectorstore.similarity_search(query)
    # return "\n".join([doc.page_content for doc in docs])
    return f"Search results from Knowledgebase for: {query}"

def get_tools():
    """Return a list of all available agent tools."""
    return [time_tool, weather_tool, calendar_tool, messenger_tool, rag_search_tool]
