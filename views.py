from flask import render_template
from services import PostsService


def index_page():
    """
    Функция обработчик запросов, получающая запрос и возвращающая html ответ из шаблона (index.html)

    Для формирования страницы используется сервис PostsService
    """
    posts = PostsService.get_all_posts()
    return render_template("index.html", posts=posts)


def post_page(post_id):
    post = PostsService.get_post_by_id(post_id)
    return render_template("article.html", post=post)


def register_views(app):
    app.route("/")(index_page)
    app.route("/post/<int:post_id>")(post_page)
