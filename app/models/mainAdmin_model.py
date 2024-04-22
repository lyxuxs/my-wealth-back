from app import db


class MainAdmin(db.Model):
    email = db.Column(db.String(255), primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    adminReferral = db.Column(db.String(100), unique=True, nullable=False)
