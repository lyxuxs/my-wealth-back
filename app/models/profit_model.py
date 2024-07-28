from app import db


class Profit(db.Model):
    profitID = db.Column(db.Integer, primary_key=True)
    shareAmount = db.Column(db.JSON, nullable=False)
    profitType = db.Column(db.String(100), nullable=False)
    shareType = db.Column(db.String(100), nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    tradeID = db.Column(db.Integer, db.ForeignKey('trade.tradeID'), nullable=False)
    trade = db.relationship('Trade', backref=db.backref('profits', lazy=True))
    