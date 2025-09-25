from flask import Flask, render_template, request
from DataBase.engine import create, Sessesion_obj
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
            action, id_str = tuple(request.form.items())[0]
            if (action == "delete"):
                id = str(id_str)
                user_obj = session.get(Festival, id)
                if (user_obj):
                    session.delete(user_obj)
                    session.commit()
            elif (action == "update"):
                print("Hello world!")
        result = session.query(Festival).all()
    return render_template("home.html", queries=result)


@app.route("/add", methods=["GET", "POST"])
def add_festival():
    if (request.method == "GET"):
        return render_template("add.html")
    else:
        start_date = date(*from_string(request.form.get("start")))
        end_date = date(*from_string(request.form.get("end")))
        new_record = Festival(name=request.form.get("name"), country=request.form.get(
            "country"), city=request.form.get("city"), start=start_date, end=end_date)
        if (end_date < start_date):
            memorization = {"name": request.form.get("name"), "country": request.form.get(
                "country"), "city": request.form.get("city")}
            return render_template("add.html", flag="Введите корректные даты! Конец не может быть позже начала", memory=memorization)

        with Sessesion_obj() as session:
            session.add(new_record)
            session.commit()
        return render_template("add.html", flag="Информация успешно добавлена!")


def main():
    create()
    app.run()


if __name__ == "__main__":
    main()
