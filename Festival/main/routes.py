from flask import Blueprint
from flask import render_template, request
from Festival.database.model import Festival
main_bl = Blueprint("main_bl", __name__)


@main_bl.route("/", methods=["GET"])
@main_bl.route("/home")
def home():
    args = request.args.get("page", 1, int)
    result = Festival.query.paginate(per_page=5, page=args)
    return render_template("home.html", queries=result, title="Festivals", a=True)
