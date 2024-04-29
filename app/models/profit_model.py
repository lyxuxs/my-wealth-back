from app import db


class Profit(db.Model):
    profitID = db.Column(db.Integer, primary_key=True)
    profitAmount = db.Column(db.Float, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    tradeID = db.Column(db.Integer, db.ForeignKey('trade.tradeID'), nullable=False)
    trade = db.relationship('Trade', backref=db.backref('profits', lazy=True))
