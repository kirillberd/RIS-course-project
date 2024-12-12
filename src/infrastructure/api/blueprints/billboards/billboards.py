from flask import Blueprint, render_template, request, session, redirect
from datetime import datetime
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required
from infrastructure.container import Container
from dependency_injector.wiring import inject, Provide
from domain.billboards import Billboard
from application.services.billboard_service import BillboardService
import logging
from domain.billboards import BillboardQuery

module_logger = logging.getLogger(__name__)


billboard_blueprint = Blueprint(
    "billboard_blueprint", __name__, template_folder="templates", static_folder="static"
)


@billboard_blueprint.route("/", methods=["GET"])
@auth_required
def query_menu():
    return render_template("search_billboards.html")


@billboard_blueprint.route("/add", methods=["GET"])
@auth_required
@role_required(role="owner")
def add_billboard_handler_get():
    return render_template("add_billboard_template.html")


@billboard_blueprint.route("/add", methods=["POST"])
@auth_required
@role_required(role="owner")
@inject
def add_billboard_handler_post(
    billboard_service: BillboardService = Provide[Container.billboard_service],
):
    billboard_object = {
        "cost": request.form.get("cost", type=float),
        "size": request.form.get("size", type=float),
        "addres": request.form.get("addres"),
        "direction": request.form.get("direction"),
        "city": request.form.get("city"),
        "billboard_owner_id": session.get("id"),
        "quality_indicator": request.form.get("quality_indicator", type=int),
        "installation_date": (
            datetime.strptime(request.form.get("installation_date"), "%Y-%m-%d")
            if request.form.get("installation_date")
            else None
        ),
    }

    billboard = Billboard.model_validate(billboard_object)
    billboard_service.add_billboard(billboard)
    return render_template(
        "add_billboard_template.html", message="Билборд успешно добавлен."
    )


@billboard_blueprint.route("/search", methods=["GET"])
@auth_required
@inject
def search_handler(
    billboard_service: BillboardService = Provide[Container.billboard_service],
):
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

    query_obj = BillboardQuery.model_validate(query_params)
    result = billboard_service.get_billboards(query_obj)
    return render_template("billboards.html", billboards=result)


@billboard_blueprint.route("/cart/add", methods=["POST"])
@auth_required
@role_required(role="customer")
@inject
def add_to_cart_handler(billboard_service: BillboardService = Provide[Container.billboard_service]):
    billboard_id = int(request.form.get("billboard_id"))
    if "cart" not in session:
        session["cart"] = {session.get("id"):[]}
    module_logger.info(session["cart"])
    
    billboard = billboard_service.get_billboard_by_id(billboard_id)
    module_logger.info(billboard)
    session["cart"][str(session.get("id"))].append(billboard.model_dump())
    session.modified = True
    return redirect(request.referrer)