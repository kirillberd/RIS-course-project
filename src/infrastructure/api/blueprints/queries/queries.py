from domain.queries import UserQuery
from flask import Blueprint, render_template, request
from infrastructure.container import Container
from dependency_injector.wiring import inject, Provide
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required
from application.services.query_service import QueryService
import logging

module_logger = logging.getLogger(__name__)
query_blueprint = Blueprint(
    "query_blueprint", __name__, template_folder="templates", static_folder="static"
)


@query_blueprint.route("/", methods=["GET"])
@auth_required
@role_required("analyst")
def query_menu():
    return render_template("query_template.html")

@query_blueprint.route("/users", methods=["GET"])
@auth_required
@role_required("analyst")
@inject
def user_query_handler(query_service: QueryService = Provide[Container.query_service]):
    query_dict= {
        "firstname":request.args["firstname"] if request.args["firstname"] else None,
        "lastname": request.args["lastname"] if request.args["lastname"] else None,
        "role": request.args["role"] if request.args["role"] else None
    }

    user_query = UserQuery.model_validate(query_dict)
    query_service.get_users(user_query)
    return "users"



