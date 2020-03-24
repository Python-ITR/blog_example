from typing import List
from dataclasses import dataclass
from connection import connection


@dataclass
class CategoryDto:
    id: int
    title: str


class CategoriesService:
    @staticmethod
    def get_all_categories() -> List[CategoryDto]:
        c = connection.cursor()
        c.execute("SELECT id, title FROM categories;")
        data = c.fetchall()
        data = list(map(lambda i: CategoryDto(*i), data))
        return data

    @staticmethod
    def get_category_by_id(category_id: int) -> CategoryDto:
        c = connection.cursor()
        c.execute("SELECT id, title FROM categories WHERE id=%s;", (category_id,))
        data = c.fetchone()
        return CategoryDto(*data)
