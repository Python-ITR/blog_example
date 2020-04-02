from flask import (
    redirect,
    render_template,
    request,
    url_for,
    redirect,
)

from services import (
    AuthorsService,
    CategoriesService,
    PostsService,
)

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