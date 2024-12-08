from domain.queries import UserQuery, OwnerBillboardsQuery
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
    return render_template("query_menu_template.html")

@query_blueprint.route("/users", methods=["GET"])
@auth_required
@role_required("analyst")
@inject
def user_query_handler(query_service: QueryService = Provide[Container.query_service]):
    query_dict= {
        "firstname":request.args.get("firstname") if request.args.get("firstname") else None,
        "lastname": request.args.get("lastname") if request.args.get("lastname") else None,
        "role": request.args.get("role") if request.args.get("role") else None
    }

    user_query = UserQuery.model_validate(query_dict)
    users = query_service.get_users(user_query)
    return render_template("users.html", users=users)



@query_blueprint.route("/owner_billboards", methods = ["GET"])
@auth_required
@role_required("analyst")
@inject
def owner_billboards_query_handler(query_service: QueryService = Provide[Container.query_service]):
    query_dict = {
        "owner_id": request.args.get("owner_id", type=int),
        "city": request.args.get("city") if request.args.get("city") else None,
        "min_quality": request.args.get("min_quality") if request.args.get("min_quality") else None,
    }

    owner_query = OwnerBillboardsQuery.model_validate(query_dict)
    result = query_service.get_owner_billboards(owner_query)
    return render_template("owner_billboards.html", billboards=result, owner_id=owner_query.owner_id)
