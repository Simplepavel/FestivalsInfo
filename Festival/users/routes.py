from flask import Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from Festival.users.form import RegistrationForm, LoginForm, UpdateAccountForm, SendRequestForm, ResetPasswordForm
from flask import redirect, flash, url_for, render_template, request
from Festival import db, bc
from Festival.database.model import User, Festival
from Festival.main.utils import send_mail, save_picture

users_bl = Blueprint("users_bl", __name__)


@users_bl.route("/register", methods=["POST", "GET"])
def register():
    if (current_user.is_authenticated):
        return redirect(url_for("main_bl.home"))
    reg_form = RegistrationForm()
    if (reg_form.validate_on_submit()):
        hashed_password = bc.generate_password_hash(
            reg_form.password.data).decode("utf-8")
        user = User(username=reg_form.username.data,
                    email=reg_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Зарегистрирован новый пользователь {reg_form.username.data}")
        return redirect(url_for('users_bl.login'))
    return render_template("register.html", title="Sing Up", form=reg_form)


@users_bl.route("/login", methods=["POST", "GET"])
def login():
    if (current_user.is_authenticated):
        return redirect(url_for("main_bl.home"))
    login_form = LoginForm()
    if (login_form.validate_on_submit()):
        # with Session() as session:
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bc.check_password_hash(user.password, login_form.password.data):
            flash(f"Вы успешно вошли!", "succes")
            login_user(user)
            return redirect(url_for("main_bl.home"))
        else:
            flash("Проверьте правильность введенных данных", "danger")
    return render_template("login.html", title="Sing Up", form=login_form)


@users_bl.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно вышли")
    return redirect(url_for("main_bl.home"))


@users_bl.route("/my_account", methods=["GET", "POST"])
@login_required
def account():
    UpdateForm = UpdateAccountForm()
    if (UpdateForm.validate_on_submit()):
        user = User.query.get(current_user.id)
        user.username = UpdateForm.username.data
        current_user.username = user.username
        user.email = UpdateForm.email.data
        current_user.email = user.email
        if (UpdateForm.picture.data):
            user.image = save_picture(UpdateForm.picture.data)
            current_user.image = user.image
        db.session.commit()
        flash("Ваша данные успешно обновлены!")
    elif (request.method == "GET"):
        UpdateForm.username.data = current_user.username
        UpdateForm.email.data = current_user.email
    image_jpg = url_for(
        "static", filename="image_profile/" + current_user.image)
    argv = request.args.get("page", 1, int)
    res = Festival.query.filter(
        Festival.author_id == current_user.id).paginate(per_page=5, page=argv)
    return render_template("account.html", title="Account", image=image_jpg, form=UpdateForm, queries=res)


@users_bl.route('/account/<int:id>')
def user_account(id):
    user = User.query.get(id)
    p = url_for("static", filename="image_profile/"+user.image)
    argv = request.args.get("page", 1, int)
    result = Festival.query.filter(
        Festival.author_id == id).paginate(per_page=5, page=argv)
    return render_template("user_account.html", title="Info", path=p, user=user, queries=result)


@users_bl.route("/send_request", methods=["GET", "POST"])
def send_request():
    if (current_user.is_authenticated):
        return redirect("home")
    form = SendRequestForm()
    if (form.validate_on_submit()):
        user = User.query.filter(User.email == form.email.data).first()
        flash("Дальнейшая инструкция выслана на почту")
        send_mail(user)
    return render_template("send_request.html", form=form)


@users_bl.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect("home")
    form = ResetPasswordForm()
    if (form.validate_on_submit()):
        user = User.verify_token(token)
        if (user is None):
            flash("Истекшая или недействительная ссылка")
            return redirect(url_for("users_bl.send_request"))
        user.password = bc.generate_password_hash(form.password.data)
        db.session.commit()
        flash("Пароль успешно изменен!")
        return redirect(url_for("users_bl.login"))
    return render_template("reset_password.html", form=form)
