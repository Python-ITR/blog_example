import os
import dotenv
import markdown
import jinja2
from os import path
from flask import Flask
from views import register_views
from middlewaries import register_middlewaries
from admin import admin_blueprint
from auth import auth_blueprint
from services import FilesService

# Load config
dotenv.load_dotenv()

# Configure markdown
md = markdown.Markdown()

# Create Flask application
app = Flask(__name__)
app.config["DEBUG"] = os.environ.get("DEBUG", None) in ["1", "true", "True"]
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "")
app.config["SESSION_COOKIE"] = "session_token"
app.config["MEDIA_DIR"] = path.join(path.dirname(__file__), "media")

@app.template_filter("markdown")
def markdown_filter(text=""):
    try:
        text = md.convert(text)
    except:
        return text
    return jinja2.Markup(text)

app.template_global()(FilesService.get_media_url)


register_views(app)
register_middlewaries(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(auth_blueprint)


if __name__ == "__main__":
    app.run("localhost", 9999)
