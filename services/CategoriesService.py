from typing import List
from dataclasses import dataclass
from connection import connection


class CategoriesServiceException(Exception):
    pass


class CategoriesServiceNotFoundException(CategoriesServiceException):
    pass


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
        try:
            c = connection.cursor()
            c.execute("SELECT id, title FROM categories WHERE id=%s;", (category_id,))
            data = c.fetchone()
            if not data:
                raise CategoriesServiceNotFoundException()
            return CategoryDto(*data)
        except CategoriesServiceNotFoundException as error:
            raise error
        except Exception as error:
            raise CategoriesServiceException() from error
