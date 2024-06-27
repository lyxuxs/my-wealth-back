from datetime import datetime

from app import db


class TransferOut(db.Model):
    transferOutID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

    user = db.relationship('User', backref=db.backref('transfers', lazy=True))
