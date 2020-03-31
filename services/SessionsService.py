from typing import Optional
from dataclasses import dataclass
from datetime import date, datetime
from utils import gen_random_str
from connection import connection


@dataclass
class SessionDto:
    id: int
    token: str
    user_id: Optional[int]
    payload: str
    created_at: datetime
    updated_at: datetime


class SessionsService:
    @staticmethod
    def create_new_session() -> Optional[SessionDto]:
        """Создает новую запись в таблице 'sessions'"""
        token = gen_random_str(20)
        now = datetime.now()
        c = connection.cursor()
        c.execute(
            "INSERT INTO sessions (token, created_at, updated_at) VALUES (%s, %s, %s);",
            (token, now, now),
        )
        connection.commit()
        return SessionsService.get_session_by_token(token)

    @staticmethod
    def get_session_by_token(token: str) -> Optional[SessionDto]:
        """Получить запись из таблицы 'sessions' по токену"""
        c = connection.cursor()
        c.execute(
            "SELECT id, token, user_id, payload, created_at, updated_at FROM sessions WHERE token=%s;",
            (token,),
        )
        session_data = c.fetchone()
        if session_data:
            return SessionDto(*session_data)
        return None

    @staticmethod
    def attach_user(token: str, user_id: int):
        c = connection.cursor()
        c.execute("UPDATE sessions SET user_id=%s WHERE token=%s;", (user_id, token))
        connection.commit()

    @staticmethod
    def delete_session_by_token(token: str) -> SessionDto:
        c = connection.cursor()
        session = SessionsService.get_session_by_token(token)
        c.execute("DELETE FROM sessions WHERE token=%s;", (token,))
        return session
