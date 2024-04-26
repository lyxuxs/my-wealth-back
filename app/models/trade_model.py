from datetime import datetime

from app import db


class Trade(db.Model):
    tradeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    trade_on_off = db.Column(db.Boolean, nullable=False, default=False)
