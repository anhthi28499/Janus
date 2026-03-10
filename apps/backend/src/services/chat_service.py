from agent.graph import janus_graph
from langchain_core.messages import AIMessage, HumanMessage
from repositories.chat_repository import ChatRepository

repo = ChatRepository()


class ChatService:
    def get_or_create_session(self, session_id: str = None):
        if not session_id or not repo.get_session_history(session_id):
            return repo.create_session()
        return session_id

    def get_history(self, session_id: str):
        messages = repo.get_session_history(session_id)
        if messages is None:
            return []
        return [
            {"role": m.role, "content": m.content, "timestamp": m.created_at.isoformat()}
            for m in messages
        ]

    def chat(self, session_id: str, user_message: str):
        session_id = self.get_or_create_session(session_id)

        # Save user message
        repo.add_message(session_id, "user", user_message)

        # Retrieve history and format for LangGraph
        db_messages = repo.get_session_history(session_id)
        langchain_messages = []
        for msg in db_messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            else:
                langchain_messages.append(AIMessage(content=msg.content))

        # Invoke LangGraph
        initial_state = {"messages": langchain_messages}
        try:
            # We assume janus_graph returns an updated state dictionary
            final_state = janus_graph.invoke(initial_state)

            # Extract the last message content added by the doer
            ai_response = final_state["messages"][-1].content
            sources = final_state.get("retrieval_sources") or []

        except Exception as e:
            ai_response = f"I encountered an error while processing your request: {str(e)}"
            sources = []

        # Save AI message
        repo.add_message(session_id, "assistant", ai_response)

        result = {"response": ai_response, "session_id": session_id}
        if sources:
            result["sources"] = [
                {
                    "content": s.get("content", ""),
                    "score": s.get("score"),
                    "filename": (s.get("metadata") or {}).get("filename"),
                    "file_path": (s.get("metadata") or {}).get("file_path"),
                }
                for s in sources
            ]
        return result
