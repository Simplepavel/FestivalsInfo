from flask import Flask, render_template, request, redirect, flash, url_for
from DataBase.engine import create, Sessesion_obj
from DataBase.model import Festival
from form import RegistrationForm, LoginForm
from datetime import date

app = Flask(__name__)
app.config["SECRET_KEY"] = '24185145a2eeb15bdfd87216873761ba'


def from_string(date: str) -> tuple:
    return [int(i) for i in date.split('-')]


@app.route("/", methods=["POST", "GET"])
@app.route("/home")
def home_page():
    with Sessesion_obj() as session:
        if (request.method == "POST"):
            action, id_str = tuple(request.form.items())[0]
            id = str(id_str)
            fest_obj = session.get(Festival, id)
            if (action == "delete"):
                if (fest_obj):
                    session.delete(fest_obj)
                    session.commit()
            elif (action == "update"):
                return render_template("update.html", title="Update festivals", memory=fest_obj)
        result = session.query(Festival).all()
    return render_template("home.html", queries=result, title="Festivals")


@app.route("/add", methods=["GET", "POST"])
def add_festival():
    if (request.method == "GET"):
        return render_template("add.html", title="Add new festival")
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
        return render_template("add.html", flag="Информация успешно добавлена!", title="Add new festival")


@app.route("/update", methods=["POST", "GET"])
def update_festival():
    with Sessesion_obj() as session:
        print(request.form)
    return "Updating!"


@app.route("/register", methods = ["POST", "GET"])
def register():
    reg_form = RegistrationForm()
    if (request.method == "POST"):
        result = reg_form.validate()
        if (result):
            return redirect(url_for('home_page'))
    return render_template("register.html", title="Sing Up", form=reg_form)


@app.route("/login")
def login():
    return render_template("login.html", title="Sing Up")


def main():
    create()
    app.run()


if __name__ == "__main__":
    main()
