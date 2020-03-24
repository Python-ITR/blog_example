from typing import List
from dataclasses import dataclass
from connection import connection
from datetime import datetime


@dataclass
class PostDto:
    _id: int
    title: str
    body: str
    created_at: datetime
    updated_at: datetime
    author_id: int
    author_first_name: str
    author_last_name: str
    category_title: str


POST_DTO_SELECT_SQL = """
                posts.id,
                posts.title,
                body,
                created_at,
                updated_at,
                author_id,
                authors.first_name AS author_first_name,
                authors.last_name AS author_last_name,
                categories.title AS category_title"""

POST_DTO_FROM_SQL = """
                posts
                LEFT JOIN authors ON posts.author_id = authors.id
                LEFT JOIN categories ON posts.category_id= categories.id"""


class PostsService:
    @staticmethod
    def get_all_posts() -> List[PostDto]:
        c = connection.cursor()
        c.execute(
            f"""
            SELECT
                {POST_DTO_SELECT_SQL}
            FROM
                {POST_DTO_FROM_SQL};
        """
        )
        data = c.fetchall()  # [(), ()]
        data = list(map(lambda i: PostDto(*i), data))
        return data

    @staticmethod
    def get_post_by_id(post_id: int) -> List[PostDto]:
        c = connection.cursor()
        c.execute(
            f"""
            SELECT
                {POST_DTO_SELECT_SQL}
            FROM
                {POST_DTO_FROM_SQL}
            WHERE posts.id=%s;
        """,
            (post_id,),
        )
        data = c.fetchone()
        data = PostDto(*data)
        return data
