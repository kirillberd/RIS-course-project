from flask import Blueprint, render_template, request, session
from datetime import datetime
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required
from infrastructure.container import Container
from dependency_injector.wiring import inject, Provide
from domain.billboards import Billboard
from application.services.billboard_service import BillboardService
import logging

module_logger = logging.getLogger(__name__)


billboard_blueprint = Blueprint("billboard_blueprint", __name__, template_folder="templates", static_folder="static")


@billboard_blueprint.route("/add", methods=["GET"])
@auth_required
@role_required(role="owner")
def add_billboard_handler_get():
    return render_template("add_billboard_template.html")


@billboard_blueprint.route("/add", methods=["POST"])
@auth_required
@role_required(role="owner")
@inject
def add_billboard_handler_post(billboard_service: BillboardService = Provide[Container.billboard_service]):
    billboard_object = {
        "cost": request.form.get("cost", type=float),
        "size": request.form.get("size", type=float),
        "addres": request.form.get("addres"),
        "direction": request.form.get("direction"),
        "city": request.form.get("city"),
        "billboard_owner_id": session.get("id"),
        "quality_indicator": request.form.get("quality_indicator", type=int),
        "installation_date": datetime.strptime(request.form.get("installation_date"), "%Y-%m-%d") if request.form.get("installation_date") else None
    }

    billboard = Billboard.model_validate(billboard_object)
    billboard_service.add_billboard(billboard)
    return render_template("add_billboard_template.html", message="Билборд успешно добавлен.")
