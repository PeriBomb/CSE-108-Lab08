from app import db

class User(db.model):
    __tablename__ = "users"
    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    role       = db.Column(db.String(20), nullable=False, default="student")
    first_name = db.Column(db.String(80), nullable=False)
    last_name  = db.Column(db.String(80), nullable=False)

def set_password(self, password):
    from werkzeug.security import generate_password_hash
    self.password = generate_password_hash(password)

def check_password(self, password):
    from werkzeug.security import check_password_hash
    return check_password_hash(self.password, password)
