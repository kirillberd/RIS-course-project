from flask import Blueprint, render_template, request, session
import logging
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required

moodule_logger = logging.getLogger(__name__)

report_bluerpint = Blueprint(
    "report_blueprint", __name__, template_folder="templates", static_folder="static"
)


@report_bluerpint.route("/", methods=["GET"])
@auth_required
@role_required(role="analyst")
def report_menu():
    return render_template("report_menu.html")