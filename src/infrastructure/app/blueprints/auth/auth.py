from flask import Blueprint
from pathlib import Path
auth_blueprint = Blueprint(
    "auth_blueprint",
    __name__,
    template_folder=Path(__name__).parent / "templates"
)


@auth_blueprint.route("/", methods=["GET"])
def auth_main():
    return "Auth menu"