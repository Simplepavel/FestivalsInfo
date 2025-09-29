from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from Festival.database.model import Festival

class AddFestival(FlaskForm):
    name = StringField("Название фестиваля", validators=[DataRequired()])
    country = StringField("Страна, проводящая фестиваль", validators=[
                          DataRequired()])
    city = StringField("Город", validators=[
                       DataRequired()])
    start = DateField("Дата начала: ", validators=[DataRequired()])
    end = DateField("Дата окончания: ", validators=[DataRequired()])
    submit = SubmitField("Отправить")

    def clear(self):
        self.name.data = ""
        self.country.data = ""
        self.city.data = ""
    
    def fill(self, ORM_obj: Festival):
        self.name.data = ORM_obj.name
        self.country.data = ORM_obj.country
        self.city.data = ORM_obj.city
        self.start.data = ORM_obj.start
        self.end.data = ORM_obj.end


class RegistrationForm(FlaskForm):
    user_name = StringField("Имя пользователя", validators=[
                            DataRequired(), Length(max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[
                             DataRequired(), Length(min=5)])
    confirm_password = PasswordField("Подтвердите пароль", validators=[
                                     DataRequired(), EqualTo("password")])
    submit = SubmitField("Регистрация")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[
                             DataRequired(), Length(min=5)])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
