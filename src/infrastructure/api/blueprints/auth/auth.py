from flask import Blueprint, render_template, request, redirect, session
from domain.user import Customer, BillboardOwner, UserLogin
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from application.services.auth_service import AuthService
from infrastructure.exceptions.auth_errors import AuthError


import logging


module_logger = logging.getLogger(__name__)

auth_blueprint = Blueprint(
    "auth_blueprint", __name__, template_folder="templates", static_folder="static"
)


@auth_blueprint.errorhandler(AuthError)
def auth_error_handler(err):
    return render_template("auth_template.html", error="Ошибка авторизациии", message=err.name), 401

@auth_blueprint.route("/", methods=["GET"])
def auth_main():
    if session.get("username"):
        return redirect("/")
    return render_template("auth_template.html")


@auth_blueprint.route("/register", methods=["POST"])
@inject
def register_handler(auth_service: AuthService = Provide[Container.auth_service]):
    user_obj = {
        "username": request.form.get("username"),
        "password": request.form.get("password"),
        "firstname": request.form.get("firstname"),
        "lastname": request.form.get("lastname"),
        "phone": request.form.get("phone"),
    }
    if request.form.get("is_owner"):
        user = BillboardOwner.model_validate(user_obj)
    else:
        user = Customer.model_validate(user_obj)

    auth_service.register_user(user)
    return redirect("/auth/")

@auth_blueprint.route("/login", methods=["POST"])
@inject
def login_handler(auth_service: AuthService = Provide[Container.auth_service]):
    user_obj = {
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }
    user_login = UserLogin.model_validate(user_obj)
    user = auth_service.login(user_login)
    session["username"] = user.username
    session["role"] = user.role
    session["firstname"] = user.firstname
    session["lastname"] = user.lastname

    return redirect("/")

@auth_blueprint.route("/logout", methods=["GET"])
def logout_handler():
    session.clear()
    return redirect("/")