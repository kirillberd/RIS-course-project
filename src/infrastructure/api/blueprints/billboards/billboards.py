from flask import Blueprint, render_template, request, session, redirect
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from infrastructure.decorators.auth_required import auth_required
from infrastructure.decorators.role_required import role_required
from infrastructure.container import Container
from dependency_injector.wiring import inject, Provide
from domain.billboards import Billboard
from application.services.billboard_service import BillboardService
from application.services.order_service import OrderService
import logging
from domain.billboards import BillboardQuery
from domain.order import Order, OrderLine

module_logger = logging.getLogger(__name__)


billboard_blueprint = Blueprint(
    "billboard_blueprint", __name__, template_folder="templates", static_folder="static"
)


@billboard_blueprint.route("/", methods=["GET"])
@auth_required
def query_menu():
    return render_template("search_billboards.html", today = date.today().isoformat())


@billboard_blueprint.route("/add", methods=["GET"])
@auth_required
@role_required(role="owner")
def add_billboard_handler_get():
    return render_template("add_billboard_template.html")


@billboard_blueprint.route("/add", methods=["POST"])
@auth_required
@role_required(role="owner")
@inject
def add_billboard_handler_post(
    billboard_service: BillboardService = Provide[Container.billboard_service],
):
    billboard_object = {
        "cost": request.form.get("cost", type=float),
        "size": request.form.get("size", type=float),
        "addres": request.form.get("addres"),
        "direction": request.form.get("direction"),
        "city": request.form.get("city"),
        "billboard_owner_id": session.get("id"),
        "quality_indicator": request.form.get("quality_indicator", type=int),
        "installation_date": (
            datetime.strptime(request.form.get("installation_date"), "%Y-%m-%d")
            if request.form.get("installation_date")
            else None
        ),
    }

    billboard = Billboard.model_validate(billboard_object)
    billboard_service.add_billboard(billboard)
    return render_template(
        "add_billboard_template.html", message="Билборд успешно добавлен."
    )


@billboard_blueprint.route("/search", methods=["GET"])
@auth_required
@inject
def search_handler(
    billboard_service: BillboardService = Provide[Container.billboard_service],
):
    query_params = {
        "city": request.args.get("city") if request.args.get("city") else None,
        "direction": (
            request.args.get("direction") if request.args.get("direction") else None
        ),
        "cost_min": (
            request.args.get("cost_min", type=float)
            if request.args.get("cost_min", type=float)
            else None
        ),
        "cost_max": (
            request.args.get("cost_max", type=float)
            if request.args.get("cost_max", type=float)
            else None
        ),
        "size_min": (
            request.args.get("size_min", type=float)
            if request.args.get("size_min", type=float)
            else None
        ),
        "size_max": (
            request.args.get("size_max", type=float)
            if request.args.get("size_max", type=float)
            else None
        ),
        "min_quality": (
            request.args.get("min_quality", type=int)
            if request.args.get("min_quality", type=int)
            else None
        ),
        "address": request.args.get("address") if request.args.get("address") else None,
        "date_start": (
            datetime.strptime(request.args.get("date_start"), "%Y-%m-%d")
            if request.args.get("date_start")
            else None
        ),

    }
    date_start = query_params.get("date_start")
    months = request.args.get("rental_months", type=int)
    date_end = date_start + relativedelta(months=months)
    query_params["date_end"] = date_end
    query_obj = BillboardQuery.model_validate(query_params)
    module_logger.info(query_obj)
    result = billboard_service.get_billboards(query_obj)
    return render_template("billboards.html", billboards=result, rental_months=months, date_start=date_start)



@billboard_blueprint.route("/cart/add", methods=["POST"])
@auth_required
@role_required(role="customer")
@inject
def add_to_cart_handler(
    billboard_service: BillboardService = Provide[Container.billboard_service],
):
    billboard_id = int(request.form.get("billboard_id"))
    rental_months = int(request.form.get("rental_months"))
    date_start = datetime.strptime(request.form.get("date_start"), "%Y-%m-%d %H:%M:%S")
    module_logger.info(date_start)
    module_logger.info(rental_months)
    user_id = str(session.get("id"))
    if "cart" not in session:
        session["cart"] = {user_id: []}
    module_logger.info(session["cart"])
    billboards_list: list = session["cart"][user_id]

    new_billboard = billboard_service.get_billboard_by_id(billboard_id)
    for billboard in billboards_list:
        if billboard["id"] == new_billboard.id:
            break
    else:
        billboard_dict = new_billboard.model_dump()
        billboard_dict["rental_months"] = rental_months
        billboard_dict["date_start"] = date_start
        billboards_list.append(billboard_dict)
    session["cart"][user_id] = billboards_list
    session.modified = True
    return redirect(request.referrer)


@billboard_blueprint.route("/cart/remove", methods=["POST"])
@auth_required
@role_required(role="customer")
@inject
def remove_from_cart_handler(
    billboard_service: BillboardService = Provide[Container.billboard_service],
):
    billboard_id = int(request.form.get("billboard_id"))
    user_id = str(session.get("id"))
    billboards_list = session.get("cart").get(user_id)
    billboards_list_filtered = list(
        filter(lambda billboard: int(billboard["id"]) != billboard_id, billboards_list)
    )
    module_logger.info(f"Filtered list {len(billboards_list_filtered)}")
    module_logger.info(f"Not filtered list {len(billboards_list)}")

    session["cart"][user_id] = billboards_list_filtered
    session.modified = True
    return redirect(request.referrer)


@billboard_blueprint.route("/cart/clear", methods=["POST"])
@auth_required
@role_required(role="customer")
def cleaar_cart_handler():
    user_id = str(session.get("id"))
    session["cart"][user_id] = []
    session.modified = True
    return redirect(request.referrer)


@billboard_blueprint.route("/order", methods=["GET"])
@auth_required
@role_required(role="customer")
def order_handler():
    user_id = str(session.get("id"))
    if "cart" not in session or user_id not in session["cart"]:
        return redirect("/billboards")

    billboards = session["cart"][user_id]
    return render_template("order_form.html", billboards=billboards)


@billboard_blueprint.route("/order/submit", methods=["POST"])
@auth_required
@role_required(role="customer")
@inject
def order_submit_handler(order_service: OrderService = Provide[Container.order_service]):
    billboard_ids = request.form.getlist("billboard_ids[]")
    start_dates = request.form.getlist("date_begin[]")
    months = request.form.getlist("months[]")
    costs = request.form.getlist("costs[]")
    total_cost = float(request.form.get("total_cost"))

    registration_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    module_logger.info(registration_time)
    order = Order(
        registration_date=registration_time,
        total_cost=total_cost,
        tenant_id=int(session.get("id")),
    )

    order_lines = []
    for i in range(len(billboard_ids)):
        start_date = datetime.strptime(start_dates[i], "%Y-%m-%d")
        end_date = start_date + relativedelta(months=int(months[i]))
        module_logger.info(start_date)
        order_line = OrderLine(
            date_begin=start_date,
            date_end=end_date,
            cost = float(costs[i]) * int(months[i]),
            billboard_id=int(billboard_ids[i])
        )
        order_lines.append(order_line)
    
    order_id = order_service.make_order(order, order_lines)
    user_id = str(session.get("id"))
    session["cart"][user_id] = []
    session.modified = True
    module_logger.info(order_id)
    return render_template("order_form.html", order_id=order_id)
