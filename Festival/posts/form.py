from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from Festival.database.model import Festival


class AddFestival(FlaskForm):
    name = StringField("Название фестиваля", validators=[
                       DataRequired("Поле не должно быть пустым")])
    country = StringField("Страна, проводящая фестиваль", validators=[
                          DataRequired("Поле не должно быть пустым")])
    city = StringField("Город", validators=[
                       DataRequired("Поле не должно быть пустым")])
    start = DateField("Дата начала: ", validators=[
                      DataRequired("Поле не должно быть пустым")])
    end = DateField("Дата окончания: ", validators=[
                    DataRequired("Поле не должно быть пустым")])
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
