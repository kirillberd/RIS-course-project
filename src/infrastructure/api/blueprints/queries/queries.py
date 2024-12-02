from flask import Blueprint, render_template, request
from domain.billboards import BillboardQuery
from datetime import datetime
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required
from infrastructure.container import Container
from dependency_injector.wiring import inject, Provide
from application.services.billboard_service import BillboardService

import logging

module_logger = logging.getLogger(__name__)
query_blueprint = Blueprint(
    "query_blueprint", __name__, template_folder="templates", static_folder="static"
)




@query_blueprint.route("/", methods=["GET"])
@auth_required
def query_menu():
    return render_template("query_menu_template.html")


@auth_required
@role_required(role="customer")
@query_blueprint.route("/search/", methods=["GET"])
@inject
def search_handler(billboard_service: BillboardService = Provide[Container.billboard_service]):
    query_params = {
        "city": request.args.get("city") if request.args.get("city") else None,
        "direction": (
            request.args.get("direction") if request.args.get("direction") else None
        ),
        "cost_min": (
            request.args.get("cost_min", type=float)
            if request.args.get("cost_min", type=float)
            else None
        ),
        "cost_max": (
            request.args.get("cost_max", type=float)
            if request.args.get("cost_max", type=float)
            else None
        ),
        "size_min": (
            request.args.get("size_min", type=float)
            if request.args.get("size_min", type=float)
            else None
        ),
        "size_max": (
            request.args.get("size_max", type=float)
            if request.args.get("size_max", type=float)
            else None
        ),
        "min_quality": (
            request.args.get("min_quality", type=int)
            if request.args.get("min_quality", type=int)
            else None
        ),
        "address": request.args.get("address") if request.args.get("address") else None,
        "date_from": (
            datetime.strptime(request.args.get("date_from"), "%Y-%m-%d")
            if request.args.get("date_from")
            else None
        ),
        "date_to": (
            datetime.strptime(request.args.get("date_to"), "%Y-%m-%d")
            if request.args.get("date_to")
            else None
        ),
    }

    module_logger.info(query_params)
    query_obj = BillboardQuery.model_validate(query_params)
    result = billboard_service.get_billboards(query_obj)
    module_logger.info(result)
    return render_template("billboards.html", billboards=result)

