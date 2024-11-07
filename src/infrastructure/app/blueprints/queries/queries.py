from flask import Blueprint, render_template
from pathlib import Path

query_blueprint = Blueprint(
    "query_blueprint",
    __name__,
     template_folder=Path(__name__).parent / "templates",
)



@query_blueprint.route('/', methods=["GET"])
def query_menu():
    return render_template("query_menu_template.html")