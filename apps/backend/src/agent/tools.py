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
    """Manage Google Calendar events. action: 'list' or 'create'; event_details: title/time."""
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
    try:
        from services.vector_store_service import retrieve

        results = retrieve(query)
        if not results:
            return "No relevant documents found in the knowledge base."
        parts = []
        for i, r in enumerate(results, 1):
            content = r.get("content", "")
            score = r.get("score")
            meta = r.get("metadata", {})
            source = meta.get("filename", meta.get("file_path", "unknown"))
            line = f"[{i}] (Source: {source})\n{content}"
            if score is not None:
                line = f"[{i}] (Score: {score:.3f}, Source: {source})\n{content}"
            parts.append(line)
        return "\n\n---\n\n".join(parts)
    except Exception as e:
        return f"Knowledge base search failed: {e}"


def get_tools():
    """Return a list of all available agent tools."""
    return [time_tool, weather_tool, calendar_tool, messenger_tool, rag_search_tool]
