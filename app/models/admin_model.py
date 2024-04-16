from app import db


class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    top = db.Column(db.Boolean, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
