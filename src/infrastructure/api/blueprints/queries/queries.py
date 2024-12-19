from domain.queries import UserQuery, OwnerBillboardsQuery
from flask import Blueprint, render_template, request
from infrastructure.container import Container
from dependency_injector.wiring import inject, Provide
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required
from application.services.query_service import QueryService
import logging

module_logger = logging.getLogger(__name__)
query_blueprint = Blueprint(
    "query_blueprint", __name__, template_folder="templates", static_folder="static"
)


@query_blueprint.route("/", methods=["GET"])
@auth_required
@role_required("analyst")
def query_menu():
    return render_template("query_menu_template.html")


@query_blueprint.route("/customer-form", methods=["GET"])
@auth_required
@role_required("analyst")
def customer_form():
    return render_template("customer_form.html")


@query_blueprint.route("/customers", methods=["GET"])
@auth_required
@role_required("analyst")
@inject
def customer_query(query_service: QueryService = Provide[Container.query_service]):
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    module_logger.info(year)
    module_logger.info(month)
    result = query_service.get_customers(year, month)
    return render_template("customer_query.html", tenants=result, year=year, month=month)
 

@query_blueprint.route("/billboard-form", methods=["GET"])
@auth_required
@role_required("analyst")
def tenant_form():
    return render_template("billboard_form.html")

@query_blueprint.route("/billboards", methods=["GET"])
@auth_required
@role_required("analyst")
@inject
def billboard_query(query_service: QueryService = Provide[Container.query_service]):
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    lastname = request.args.get("lastname")
    
    result = query_service.get_billboards(year, month, lastname)
    module_logger.info(result)
    return render_template("billboard_query.html", tenant_lastname = lastname, month=month, year=year, billboards=result)