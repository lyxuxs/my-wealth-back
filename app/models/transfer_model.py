from datetime import datetime

from app import db


class Transfer(db.Model):
    transferID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    From = db.Column(db.String(20), nullable=False)
    to = db.Column(db.String(20), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

    user = db.relationship('User', backref=db.backref('transfers', lazy=True))
