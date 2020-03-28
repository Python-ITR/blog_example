from flask import abort, current_app, redirect, render_template, request, url_for

from services import (
    AuthorsService,
    CategoriesService,
    PostsService,
    SessionsService,
    UsersService,
)


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


def admin_posts():
    posts = PostsService.get_all_posts()
    return render_template("admin_posts.html", posts=posts)


def admin_post_new():
    categories = CategoriesService.get_all_categories()
    authors = AuthorsService.get_all_authors()
    if request.method == "GET":
        # Отрендерить шаблон admin_post.html для создания нового поста
        return render_template(
            "admin_post.html", categories=categories, authors=authors
        )
    elif request.method == "POST":
        # Создать новый пост
        created_post = PostsService.create_new_post(
            request.form.get("title"),
            request.form.get("category_id"),
            request.form.get("author_id"),
            request.form.get("body"),
        )
        return redirect(url_for("admin_posts"))


def admin_post_edit(post_id: int):
    categories = CategoriesService.get_all_categories()
    authors = AuthorsService.get_all_authors()
    post = PostsService.get_post_by_id(post_id)
    if request.method == "GET":
        # Отрендерить шаблон admin_post.html для редактирования существующего поста
        return render_template(
            "admin_post.html", categories=categories, authors=authors, post=post
        )
    elif request.method == "POST":
        # Редактируем существующий пост
        edited_post = PostsService.edit_post_by_id(
            post_id,
            request.form.get("title"),
            request.form.get("category_id"),
            request.form.get("author_id"),
            request.form.get("body"),
        )
        return redirect(url_for("admin_posts"))


def admin_posts_delete(post_id: int):
    PostsService.delete_pots_by_id(post_id)
    return redirect(url_for("admin_posts"))


def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = UsersService.get_user_by_username(username)
        if user.password != password:
            abort(400)
        st = request.cookies.get(current_app.config.get("SESSION_COOKIE"))
        SessionsService.attach_user(st, user.id)
        return redirect(url_for("index_page"))


def register_views(app):
    app.route("/")(index_page)
    app.route("/post/<int:post_id>")(post_page)
    app.route("/category/<int:category_id>")(category_page)
    app.route("/author/<int:author_id>")(author_page)
    # AUTH
    app.route("/login", methods=["GET", "POST"])(login)
    # ADMIN
    app.route("/admin/")(admin_posts)  # Posts list
    app.route("/admin/post/<int:post_id>", methods=["DELETE"])(
        admin_posts_delete
    )  # Delete post
    app.route("/admin/post/new", methods=["GET", "POST"])(admin_post_new)  # New post
    app.route("/admin/post/<int:post_id>", methods=["GET", "POST"])(
        admin_post_edit
    )  # Edit post
