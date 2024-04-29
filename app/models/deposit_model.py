from datetime import datetime

from app import db


class Deposit(db.Model):
    depositID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)

    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    user = db.relationship('User', backref=db.backref('deposits', lazy=True))
