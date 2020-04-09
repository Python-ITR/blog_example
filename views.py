import math
from flask import abort, redirect, render_template, request, url_for

from services import (
    AuthorsService,
    CategoriesService,
    PostsService,
    SessionsService,
    UsersService,
)
from services.PostsService import PostsServiceException, PostsServiceNotFoundException
from utils import auth_only


def error_404(error_text):
    return render_template("404.html", error_text=error_text)


def index_page():
    """
    Функция обработчик запросов, получающая запрос и возвращающая html ответ из шаблона (index.html)

    Для формирования страницы используется сервис PostsService
    """
    posts = PostsService.get_all_posts()
    categories = CategoriesService.get_all_categories()
    authors = AuthorsService.get_all_authors()
    first_posts = posts[:2]
    posts = posts[2:]
    return render_template(
        "index.html",
        first_posts=first_posts,
        posts=posts,
        categories=categories,
        authors=authors,
    )


def post_page(post_id):
    try:
        post = PostsService.get_post_by_id(post_id)
        return render_template("article.html", post=post)
    except PostsServiceNotFoundException as error:
        abort(404)


def catalog_page():
    try:
        page = int(request.args.get("page", 1))
        posts = PostsService.get_all_posts(limit=2, page=page)
        count = PostsService.get_count()
        page_count = math.ceil(count / 2)
        return render_template(
            "catalog.html", posts=posts, page_count=page_count, int=int
        )
    except PostsServiceNotFoundException as error:
        abort(404)


def category_page(category_id):
    category = CategoriesService.get_category_by_id(category_id)
    category_posts = PostsService.get_all_posts_by_category(category_id)
    return render_template(
        "category.html", category=category, category_posts=category_posts
    )


@auth_only
def author_page(author_id):
    author = AuthorsService.get_author_by_id(author_id)
    author_posts = PostsService.get_all_posts_by_author(author_id)
    return render_template("author.html", author=author, author_posts=author_posts)


def register_views(app):
    app.route("/")(index_page)
    app.route("/catalog")(catalog_page)
    app.route("/post/<int:post_id>")(post_page)
    app.route("/category/<int:category_id>")(category_page)
    app.route("/author/<int:author_id>")(author_page)
    app.errorhandler(404)(error_404)
