from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = '24185145a2eeb15bdfd87216873761ba'

from Festival import routes