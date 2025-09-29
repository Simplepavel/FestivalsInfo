from flask import Flask, render_template, request, redirect, flash, url_for
from DataBase.engine import create, Sessesion_obj, drop
from DataBase.model import Festival, User
from form import RegistrationForm, LoginForm, AddFestival

app = Flask(__name__)
app.config["SECRET_KEY"] = '24185145a2eeb15bdfd87216873761ba'


def from_string(date: str) -> tuple:
    return [int(i) for i in date.split('-')]


@app.route("/", methods=["GET"])
@app.route("/home")
def home():
    if (request.args):
        action, id = next(request.args.items())
        if (action == 'delete'):
            return redirect(url_for('delete', id=id))
        return redirect(url_for('update', id=id))
    with Sessesion_obj() as session:
        result = session.query(Festival, User.username).join(
            User, Festival.author == User.id).all()
    return render_template("home.html", queries=result, title="Festivals")


@app.route("/add", methods=["GET", "POST"])
def add():
    form_obj = AddFestival()
    flag = "Добавление информации о фестивале"
    if (request.method == "POST"):
        result = form_obj.validate()
        if result:
            if (form_obj.end.data < form_obj.start.data):
                flash("Введите корректные даты! Конец не может быть позже начала")
                return render_template("add.html", flag=flag, form=form_obj)
            new_record = Festival(name=form_obj.name.data,
                                  country=form_obj.country.data, city=form_obj.city.data,
                                  start=form_obj.start.data, end=form_obj.end.data)
            with Sessesion_obj() as session:
                session.add(new_record)
                session.commit()
            flash('Информация успешно добавлена!')
            form_obj.clear()
    return render_template("add.html", flag=flag, title="Add new festival", form=form_obj)


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form_obj = AddFestival()
    if (request.method == "GET"):
        with Sessesion_obj() as session:
            fest_obj = session.get(Festival, int(id))
            form_obj.fill(fest_obj)
            return render_template("add.html", flag="Редактирование", title="Update Festval", form=form_obj)
    with Sessesion_obj() as session:
        fest_obj = session.get(Festival, int(id))
        fest_obj.name = form_obj.name.data
        fest_obj.country = form_obj.country.data
        fest_obj.city = form_obj.city.data
        fest_obj.start = form_obj.start.data
        fest_obj.end = form_obj.end.data
        session.commit()
        flash("Успешно!")
    return render_template("add.html", flag="Редактирование", title="Update Festival", form=form_obj)


@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    with Sessesion_obj() as session:
        fest_obj = session.get(Festival, int(id))
        session.delete(fest_obj)
        session.commit()
    return redirect(url_for("home"))


@app.route("/register", methods=["POST", "GET"])
def register():
    reg_form = RegistrationForm()
    if (request.method == "POST"):
        if (reg_form.validate()):
            flash(
                f"Зарегистрирован новый пользователь {reg_form.user_name.data}")
            return redirect(url_for('home'))
    return render_template("register.html", title="Sing Up", form=reg_form)


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if (request.method == "POST"):
        result = login_form.validate()
        if (result):
            flash(f"Вы успешно вошли!", "succes")
            return redirect(url_for("home"))
    return render_template("login.html", title="Sing Up", form=login_form)


def main():
    create()
    app.run()


if __name__ == "__main__":
    main()
