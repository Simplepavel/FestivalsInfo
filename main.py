from flask import Flask, render_template, request
from DataBase.engine import create, drop, Sessesion_obj
from DataBase.model import Festival
from datetime import date
app = Flask(__name__)


def from_string(date: str) -> tuple:
    return [int(i) for i in date.split('-')]


@app.route("/", methods=["POST", "GET"])
@app.route("/home")
def home_page():
    with Sessesion_obj() as session:
        if (request.method == "POST"):
            id = int(request.form.get("id"))
            user_obj = session.get(Festival, id)
            if (user_obj):
                session.delete(user_obj)
                session.commit()
        result = session.query(Festival).all()
    return render_template("home.html", queries=result)



@app.route("/add", methods=["GET", "POST"])
def add_festival():
    if (request.method == "GET"):
        return render_template("add.html", flag=False)
    else:
        start_date = date(*from_string(request.form.get("start")))
        end_date = date(*from_string(request.form.get("end")))
        new_record = Festival(name=request.form.get("name"), country=request.form.get(
            "country"), city=request.form.get("city"), start=start_date, end=end_date)
        with Sessesion_obj() as session:
            session.add(new_record)
            session.commit()
        return render_template("add.html", flag=True)


def main():
    create()
    app.run()


if __name__ == "__main__":
    main()
