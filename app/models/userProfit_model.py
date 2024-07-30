from app import db


class UserProfit(db.Model):
    userProfitID = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime, nullable=False)
    profitType = db.Column(db.String(100), nullable=False)
    profitAmount = db.Column(db.Float, nullable=False)
    profitID = db.Column(db.Integer, db.ForeignKey('profit.profitID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    
    profit = db.relationship('Profit', backref=db.backref('userProfits', lazy=True))
    user = db.relationship('User', backref=db.backref('userProfits', lazy=True))
    