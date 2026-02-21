import uuid
from repositories.models import ChatSession, ChatMessage
from core.database import db

class ChatRepository:
    def create_session(self):
        session_id = str(uuid.uuid4())
        session = ChatSession(id=session_id)
        db.session.add(session)
        db.session.commit()
        return session_id

    def get_session_history(self, session_id: str):
        session = ChatSession.query.get(session_id)
        if not session:
            return None
        return session.messages

    def add_message(self, session_id: str, role: str, content: str):
        msg = ChatMessage(session_id=session_id, role=role, content=content)
        db.session.add(msg)
        db.session.commit()
        return msg
