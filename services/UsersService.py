from dataclasses import dataclass
from datetime import datetime
from utils import get_password_hash

from connection import connection


@dataclass
class UserDto:
    id: int
    username: str
    password: str
    created_at: datetime
    updated_at: datetime


class UsersService:
    @staticmethod
    def create_user(username: str, password: str) -> UserDto:
        now = datetime.now()
        c = connection.cursor()
        password = get_password_hash(password)
        c.execute(
            "INSERT INTO users (username, password, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING id;",
            (username, password, now, now),
        )
        (user_id,) = c.fetchone()
        return UsersService.get_user_by_id(user_id)

    @staticmethod
    def get_user_by_username(username: str) -> UserDto:
        c = connection.cursor()
        c.execute(
            "SELECT id, username, password, created_at, updated_at from users WHERE username=%s;",
            (username,),
        )
        user_data = c.fetchone()
        return UserDto(*user_data)

    @staticmethod
    def get_user_by_id(user_id: int) -> UserDto:
        c = connection.cursor()
        c.execute(
            "SELECT id, username, password, created_at, updated_at from users WHERE id=%s;",
            (user_id,),
        )
        user_data = c.fetchone()
        return UserDto(*user_data)
