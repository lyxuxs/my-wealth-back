from datetime import datetime

from app import db


class Transaction(db.Model):
    transactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transactionType = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    withdrawalID = db.Column(db.Integer, db.ForeignKey('withdrawal.withdrawalID'))
    depositID = db.Column(db.Integer, db.ForeignKey('deposit.depositID'))
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
