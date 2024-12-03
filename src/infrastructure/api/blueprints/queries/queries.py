from flask import Blueprint, session, render_template
from infrastructure.container import Container
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required



query_blueprint = Blueprint(
    "query_blueprint", __name__, template_folder="templates", static_folder="static"
)


@query_blueprint.route("/", methods=["GET"])
@auth_required
@role_required("analyst")
def query_menu():
    return render_template("query_template.html")

