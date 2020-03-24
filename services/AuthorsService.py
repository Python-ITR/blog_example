from typing import List
from dataclasses import dataclass
from connection import connection


@dataclass
class AuthorDto:
    id: int
    first_name: str
    last_name: str

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class AuthorsService:
    @staticmethod
    def get_all_authors() -> List[AuthorDto]:
        c = connection.cursor()
        c.execute("SELECT id, first_name, last_name FROM authors;")
        data = c.fetchall()
        data = list(map(lambda i: AuthorDto(*i), data))
        return data

    @staticmethod
    def get_author_by_id(author_id: int) -> AuthorDto:
        c = connection.cursor()
        c.execute(
            "SELECT id, first_name, last_name FROM authors WHERE id=%s;", (author_id,)
        )
        data = c.fetchone()
        return AuthorDto(*data)
