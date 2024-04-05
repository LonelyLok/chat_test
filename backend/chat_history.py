from database import get_session
from datetime import datetime
from uuid import uuid4, UUID


def create_chat_history(id: str, session_id: str, message: str, is_bot: bool, timestamp: datetime):
    session = get_session()
    fake_id = uuid4() if id is None else UUID(id)
    session.execute_query(
        """
        INSERT INTO chat.chat_history (id, session_id, message, is_bot, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (fake_id, UUID(session_id), message, is_bot, timestamp),
    )
    return str(fake_id)


def delete_chat_history_by_session_id(session_id: str):
    session = get_session()  # Ensure this returns a Cassandra session
    session_id = UUID(session_id)  # Convert the string to a UUID object
    session.execute_query(
            """
            DELETE FROM chat.chat_history WHERE session_id = %s
            """,
            (session_id,)
        )
    print(f"Message with Session ID {session_id} deleted.")
    return


def get_chat_history_from_session_id(session_id: str):
    session = get_session()
    rows = session.execute_query(
        """
        SELECT * FROM chat.chat_history where session_id = %s
        """, (UUID(session_id),)
    )

    if(rows == None):
         return []
    chat_history = [row._asdict() for row in rows]
    return chat_history