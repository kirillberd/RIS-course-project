from flask import Flask
from infrastructure.container import Container
from infrastructure.app.blueprints.queries import queries
from infrastructure.app.blueprints.main import main
from infrastructure.app.blueprints.auth import auth

def init_config(container: Container):
    container.config.db_host.from_env("DB_HOST")
    container.config.db_name.from_env("DB_NAME")
    container.config.db_password.from_env("DB_PASSWORD")
    container.config.db_port.from_env("DB_PORT")
    container.config.db_user.from_env("DB_USER")

def setup(app: Flask, container: Container):
    init_config(container)
    container.wire(modules=[queries])
    app.register_blueprint(main.main_blueprint, url_prefix="/")
    app.register_blueprint(queries.query_blueprint, url_prefix="/queries")
    app.register_blueprint(auth.auth_blueprint, url_prefix="/auth")
    app.template_folder = "infrastructure/app/base_templates"
    app.static_folder = "infrastructure/app/base_templates/static"