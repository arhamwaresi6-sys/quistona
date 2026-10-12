from flask import Flask
from .extensions import db,login_manager
from .modules import User
from .routes.main import main
from .routes.auth import auth
from .commands import create_table
def create_app(config = "project.settings"):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view  = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User,user_id)

    app.cli.add_command(create_table)

    app.register_blueprint(auth)
    app.register_blueprint(main)
    return app