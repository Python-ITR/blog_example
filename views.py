from flask import render_template, url_for
from services import PostsService, CategoriesService, AuthorsService


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
    post = PostsService.get_post_by_id(post_id)
    return render_template("article.html", post=post)


def category_page(category_id):
    category = CategoriesService.get_category_by_id(category_id)
    category_posts = PostsService.get_all_posts_by_category(category_id)
    return render_template(
        "category.html", category=category, category_posts=category_posts
    )


def author_page(author_id):
    author = AuthorsService.get_author_by_id(author_id)
    author_posts = PostsService.get_all_posts_by_author(author_id)
    return render_template("author.html", author=author, author_posts=author_posts)


def register_views(app):
    app.route("/")(index_page)
    app.route("/post/<int:post_id>")(post_page)
    app.route("/category/<int:category_id>")(category_page)
    app.route("/author/<int:author_id>")(author_page)
