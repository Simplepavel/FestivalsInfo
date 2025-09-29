from flask import Flask, render_template, request, redirect, flash, url_for
from DataBase.engine import create, Sessesion_obj
from DataBase.model import Festival
from form import RegistrationForm, LoginForm, AddFestival
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
    flag = None
    form_obj = AddFestival()
    if (request.method == "POST"):
        result = form_obj.validate()
        if result:
            if (form_obj.end.data < form_obj.start.data):
                return render_template("add.html", flag="Введите корректные даты! Конец не может быть позже начала", form=form_obj)
            new_record = Festival(name=form_obj.name.data,
                                  country=form_obj.country.data, city=form_obj.city.data,
                                  start=form_obj.start.data, end=form_obj.end.data)
            with Sessesion_obj() as session:
                session.add(new_record)
                session.commit()
            flag = "Информация успешно добавлена!"
            form_obj.clear()
    return render_template("add.html", flag=flag, title="Add new festival", form=form_obj)


@app.route("/update", methods=["POST", "GET"])
def update_festival():
    with Sessesion_obj() as session:
        print(request.form)
    return "Updating!"


@app.route("/register", methods=["POST", "GET"])
def register():
    reg_form = RegistrationForm()
    if (request.method == "POST"):
        if (reg_form.validate()):
            flash(
                f"Зарегистрирован новый пользователь {reg_form.user_name.data}")
            return redirect(url_for('home_page'))
    return render_template("register.html", title="Sing Up", form=reg_form)


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if (request.method == "POST"):
        result = login_form.validate()
        if (result):
            flash(f"Вы успешно вошли!", "succes")
            return redirect(url_for("home_page"))
    return render_template("login.html", title="Sing Up", form=login_form)


def main():
    create()
    app.run()


if __name__ == "__main__":
    main()
