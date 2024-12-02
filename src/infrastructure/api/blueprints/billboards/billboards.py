from flask import Blueprint, render_template, request
from datetime import datetime
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required
from infrastructure.container import Container
from dependency_injector.wiring import inject, Provide
from application.services.billboard_service import BillboardService
import logging

module_logger = logging.getLogger(__name__)


billboard_blueprint = Blueprint("billboard_blueprint", __name__, template_folder="templates", static_folder="static")


@billboard_blueprint.route("/add", methods=["GET"])
@auth_required
@role_required(role="owner")
def add_billboard_handler():
    return render_template("add_billboard_template.html")


