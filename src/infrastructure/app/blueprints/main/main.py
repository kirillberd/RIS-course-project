from flask import Blueprint, render_template
from pathlib import Path

main_blueprint = Blueprint(
    "main_blueprint",
    __name__,
    template_folder=Path(__name__).parent / "templates"
)

@main_blueprint.route("/", methods=["GET"])
def main_menu():
    return render_template("main_menu_template.html")