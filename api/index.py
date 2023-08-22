from flask import Flask
from boyd_bot import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)
