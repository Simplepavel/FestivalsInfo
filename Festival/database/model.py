# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from Festival.database.engine import Base, Session
from Festival import db, app
from flask_login import UserMixin
from Festival import login_manager
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature


@login_manager.user_loader
def load_user(user_id):
    result = User.query.get(user_id)
    return result


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    username = db.Column("username", db.String(20), unique=True)
    email = db.Column("email", db.String(128), unique=True)
    password = db.Column("password", db.String(128))
    image = db.Column("img", db.String(20), default='default.png')
    # у поста будет атрибут author-ссылка на объект User
    posts = db.relationship('Festival', backref="author", lazy=True)

    def __repr__(self):
        return f"Username: {self.username}, Email: {self.email}"

    def get_own_verify_token(self):
        s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_token(token):
        s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, max_age=1800)
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id["user_id"])


class Festival(db.Model):
    __tablename__ = "festival"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(256))
    country = db.Column("country", db.String(40))
    city = db.Column("city", db.String(40))
    start = db.Column("start", db.DateTime)
    end = db.Column("end", db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Name: {self.name}, Country: {self.country}, City: {self.city}, Start: {self.start}, End: {self.end}"
