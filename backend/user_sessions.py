from database import get_session
from datetime import datetime
from uuid import uuid4, UUID
from typing import TypedDict, Dict, Literal

ModelType = Literal["models/gemini-1.5-pro-latest", "models/gemini-1.0-ultra-latest"]

class UserSession(TypedDict):
    user_id: str
    session_id: str
    model: ModelType
    created_at: datetime

def create_user_sessions(user_id: str, session_id: str, created_at: datetime, model: ModelType):
    session = get_session()
    session.execute_query(
        """
        INSERT INTO chat.user_sessions (user_id, session_id, created_at, model)
        VALUES (%s, %s, %s, %s)
        """,
        (UUID(user_id), UUID(session_id), created_at, model),
    )
    return {
        "user_id": user_id,
        "session_id": session_id,
        "created_at": created_at,
        "model": model,
    }

def update_user_sessions(user_id: str, session_id: str, model: ModelType):
    session = get_session()
    session.execute_query(
        """
        UPDATE chat.user_sessions SET model = %s WHERE user_id = %s AND session_id = %s
        """,
        (model, UUID(user_id), UUID(session_id)),
    )
    return {
        "user_id": user_id,
        "session_id": session_id,
        "model": model,
    }

def delete_user_session(user_id: str, session_id: str,):
    session = get_session()  # Ensure this returns a Cassandra session
    session.execute_query(
            """
            DELETE FROM chat.user_sessions WHERE session_id = %s AND user_id = %s
            """,
            (UUID(session_id), UUID(user_id))
        )
    print(f"Session with ID {session_id} deleted.")
    return

def get_user_sessions_from_user_id(user_id: str):
    session = get_session()
    rows = session.execute_query(
        """
        SELECT * FROM chat.user_sessions where user_id = %s
        """, (UUID(user_id),)
    )
    if rows == None:
        return []
    user_sessions = [row._asdict() for row in rows]
    return user_sessions

def get_user_session(user_id:str, session_id: str):
    session = get_session()
    rows = session.execute_query(
        """
        SELECT * FROM chat.user_sessions where user_id = %s AND session_id = %s
        """, (UUID(user_id), UUID(session_id))
    )
    if rows == None:
        return None
    return [row._asdict() for row in rows][0]