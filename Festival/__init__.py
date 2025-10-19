from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
app = Flask(__name__)
app.config["SECRET_KEY"] = '24185145a2eeb15bdfd87216873761ba'



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"


app.config["MAIL_SERVER"] = "smtp.yandex.ru"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "pavel.mefokov@yandex.ru"
app.config["MAIL_DEFAULT_SENDER"] = "pavel.mefokov@yandex.ru"
app.config["MAIL_PASSWORD"] = "cuayaeqvihbahuky"
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bc = Bcrypt(app)



from Festival.users.routes import users_bl
from Festival.posts.routes import posts_bl
from Festival.main.routes import main_bl

app.register_blueprint(users_bl)
app.register_blueprint(posts_bl)
app.register_blueprint(main_bl)

