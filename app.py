from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField
from extensions import db
from models import User, Course, Enrollment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserAdminView(ModelView):
    column_exclude_list = ["password"]
    form_excluded_columns = ["password"]
    form_columns = ["first_name", "last_name", "username", "password_input", "email", "role"]
    form_extra_fields = {
        "password_input": PasswordField("Password")
    }
    def on_model_change(self, form, model, is_created):
        if form.password_input.data:
            model.set_password(form.password_input.data)

class CourseAdminView(ModelView):
    form_args = {
        "teacher": {
            "query_factory": lambda: User.query.filter_by(role="teacher").all()
        }
    }

admin = Admin(app, name="Lab-08 Admin View")
admin.add_view(UserAdminView(User, db.session))
admin.add_view(CourseAdminView(Course, db.session))
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
    enrollments = Enrollment.query.filter_by(student_id=current_user.id, status="active").all()
    courses = Course.query.all()
    return render_template("student_dashboard.html", enrollments=enrollments, courses=courses)

@app.route("/student/enroll/<int:id>", methods=['POST'])
@login_required
def student_enroll(id):
    enrollment = Enrollment(student_id=current_user.id, course_id=id, grade="100", status="active")
    db.session.add(enrollment)
    db.session.commit()
    return redirect(url_for('student_dashboard'))

@app.route("/student/drop/<int:id>", methods=['POST'])
@login_required
def student_drop(id):
    enrollment = Enrollment.query.filter_by(student_id=current_user.id, course_id=id, status="active").first()
    db.session.delete(enrollment)
    db.session.commit()
    return redirect(url_for('student_dashboard'))

@app.route("/teacher/dashboard")
@login_required
def teacher_dashboard():
    return render_template("teacher_dashboard.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
    
if __name__ == "__main__":
    app.run(debug=True)