from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import User, Course, Enrollment
from extensions import db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

app.config["SECRET_KEY"] = "dev-secret-key"

admin = Admin(app, name="Lab-08 Admin View")
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Enrollment, db.session))


@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            if user.role == "admin":
                return redirect("/admin")
            elif user.role == "teacher":
                return redirect(url_for("teacher_dashboard"))
            else:
                return redirect(url_for("student_dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")

@app.route("/student/dashboard")
@login_required
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route("/teacher/dashboard")
@login_required
def teacher_dashboard():
    return render_template("teacher_dashboard.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
