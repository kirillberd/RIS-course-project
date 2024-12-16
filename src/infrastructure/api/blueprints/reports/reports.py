from flask import Blueprint, render_template, request, session
import logging
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from application.services.report_service import ReportService

module_logger = logging.getLogger(__name__)

report_bluerpint = Blueprint(
    "report_blueprint", __name__, template_folder="templates", static_folder="static"
)


@report_bluerpint.route("/", methods=["GET"])
@auth_required
@role_required(role="analyst")
def report_menu():
    return render_template("report_menu.html")


@report_bluerpint.route("/generate", methods=["POST"])
@auth_required
@role_required(role="analyst")
@inject
def view_report_handler(
    report_service: ReportService = Provide[Container.report_service]
):
    action = request.form.get("action")
    name = request.form.get("report_type")
    month = int(request.form.get("month"))
    year = int(request.form.get("year"))

    try:
        if action == "generate":
            report_service.create_report(name, year, month)
            return render_template("report_menu.html", message="Отчет успешно создан")
        else:
            report_service.view_report(name, year, month)
            return render_template("report_menu.html")
    except Exception as e:
        return render_template("report_menu.html", error=str(e))

