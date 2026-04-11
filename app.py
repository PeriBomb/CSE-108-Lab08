from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import User, Course, Enrollment
from extensions import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
