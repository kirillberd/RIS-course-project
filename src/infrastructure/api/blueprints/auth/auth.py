from flask import Blueprint, render_template

auth_blueprint = Blueprint(
    "auth_blueprint",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@auth_blueprint.route("/", methods=["GET"])
def auth_main():
    return render_template("auth_template.html")
