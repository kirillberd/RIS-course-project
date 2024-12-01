from flask import Blueprint, render_template

query_blueprint = Blueprint(
    "query_blueprint",
    __name__,
     template_folder="templates",
     static_folder="static"
)



@query_blueprint.route('/', methods=["GET"])
def query_menu():
    return render_template("query_menu_template.html")
