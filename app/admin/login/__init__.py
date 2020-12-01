from flask_login import LoginManager

def start_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    return login_manager