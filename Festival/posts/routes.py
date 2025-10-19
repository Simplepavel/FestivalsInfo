from flask import Blueprint
from flask_login import login_required, current_user
from flask import request, flash, render_template, redirect, url_for
from Festival.database.model import Festival
from Festival.posts.form import AddFestival
from Festival import db

posts_bl = Blueprint("posts_bl", __name__)


@login_required
@posts_bl.route("/add", methods=["GET", "POST"])
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
                                  start=form_obj.start.data, end=form_obj.end.data, author=current_user.id)
            db.session.add(new_record)
            db.session.commit()
            flash('Информация успешно добавлена!')
            form_obj.clear()
    return render_template("add.html", flag=flag, title="Add new festival", form=form_obj)


@login_required
@posts_bl.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form_obj = AddFestival()
    if (request.method == "GET"):
        fest_obj = db.session.get(Festival, int(id))
        form_obj.fill(fest_obj)
        return render_template("add.html", flag="Редактирование", title="Update Festval", form=form_obj)
    fest_obj = Festival.query.get(int(id))
    fest_obj.name = form_obj.name.data
    fest_obj.country = form_obj.country.data
    fest_obj.city = form_obj.city.data
    fest_obj.start = form_obj.start.data
    fest_obj.end = form_obj.end.data
    db.session.commit()
    flash("Успешно!")
    return render_template("add.html", flag="Редактирование", title="Update Festival", form=form_obj)


@login_required
@posts_bl.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    fest_obj = Festival.query.get(int(id))
    db.session.delete(fest_obj)
    db.session.commit()
    return redirect(url_for("users_bl.account"))
