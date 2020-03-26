from flask import Flask, render_template
from views import register_views
from services import PostsService

app = Flask(__name__)
register_views(app)

if __name__ == "__main__":
    app.run("localhost", 9999)
