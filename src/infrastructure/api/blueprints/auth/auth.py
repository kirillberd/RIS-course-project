from flask import Blueprint, render_template, request
from domain.user import Customer, BillboardOwner
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from application.services.auth_service import AuthService

import logging



module_logger = logging.getLogger(__name__)

auth_blueprint = Blueprint(
    "auth_blueprint",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@auth_blueprint.route("/", methods=["GET"])
def auth_main():
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
    