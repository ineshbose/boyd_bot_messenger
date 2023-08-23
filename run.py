from flask import Flask
from boyd_bot import bot_blueprint

app = Flask(__name__)
app.register_blueprint(bot_blueprint(), url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)
