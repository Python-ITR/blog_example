from os import path
from flask import Blueprint
from .views import admin_posts, admin_posts_delete, admin_post_new, admin_post_edit

CURRENT_DIR = path.dirname(path.abspath(__file__))
TEMPLATES_FOLDER = path.join(CURRENT_DIR, "templates")

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin", template_folder=TEMPLATES_FOLDER)

# Регистрируем view-функции в blueprint 'admin'
admin_blueprint.route("/")(admin_posts)  # Posts list
admin_blueprint.route("/post/<int:post_id>", methods=["DELETE"])(
    admin_posts_delete
)  # Delete post
admin_blueprint.route("/post/new", methods=["GET", "POST"])(admin_post_new)  # New post
admin_blueprint.route("/post/<int:post_id>", methods=["GET", "POST"])(
    admin_post_edit
)  # Edit post

