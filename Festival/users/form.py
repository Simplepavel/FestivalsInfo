from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from Festival.database.model import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[
        DataRequired("Поле не должно быть пустым"), Length(max=20)])
    email = StringField("Email", validators=[DataRequired("Поле не должно быть пустым"), Email("Email не корректен!")])
    password = PasswordField("Пароль", validators=[
                             DataRequired("Поле не должно быть пустым"), Length(min=5)])
    confirm_password = PasswordField("Подтвердите пароль", validators=[
                                     DataRequired("Поле не должно быть пустым"), EqualTo("password", "Пароли не совпадают!")])
    submit = SubmitField("Регистрация")

    def validate_username(self, argv: StringField):
        query = User.query.filter(User.username == argv._value()).first()
        if (query is not None):
            raise ValidationError(
                "Имя пользователя уже занято. Используйте другое")

    def validate_email(self, email):
        query = User.query.filter(User.email == email._value()).first()
        if (query is not None):
            raise ValidationError(
                "Email уже занят. Используйте другой")


class LoginForm(FlaskForm):
    email = StringField("Имя пользователя", validators=[
                        DataRequired("Поле не должно быть пустым"), Email("Email не корректен!")])
    password = PasswordField("Пароль", validators=[
                             DataRequired("Поле не должно быть пустым"), Length(min=5)])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class UpdateAccountForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired("Поле не должно быть пустым")])
    email = StringField("Email", validators=[DataRequired("Поле не должно быть пустым"), Email("Email не корректен")])
    picture = FileField("Фото профиля", validators=[
                        FileAllowed(["png", "jpg"])])
    submit = SubmitField("Обновить")

    def validate_username(self, argv):
        if current_user.username != self.username.data:
            user = User.query.filter(User.username == argv._value()).first()
            if (user is not None):
                raise ValidationError(
                    "Пользователь с таким именем уже существует. Попробуйте другое")

    def validate_email(self, argv):
        if current_user.email != self.email.data:
            user = User.query.filter(User.email == argv._value()).first()
            if (user is not None):
                raise ValidationError(
                    "Пользователь с таким email уже существует. Попробуйте другой")


class SendRequestForm(FlaskForm):
    email = StringField("Введите email", validators=[DataRequired("Поле не должно быть пустым"), Email("Email не корректен!")])
    submit = SubmitField("Отправить код")

    def validate_email(self, argv):
        user = User.query.filter_by(email=argv._value()).first()
        if user is None:
            raise ValidationError("Нет пользователя с подобным email!")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Введите новый пароль", validators=[DataRequired("Поле не должно быть пустым")])
    confirm_password = PasswordField(
        "Подтвердите новый пароль", validators=[DataRequired("Поле не должно быть пустым"), EqualTo("password", "Пароли не совпадают!")])
    submit = SubmitField("Подтвердить")