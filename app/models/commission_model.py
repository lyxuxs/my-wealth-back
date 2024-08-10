from app import db


class Commission(db.Model):
    commissionID = db.Column(db.Integer, primary_key=True)
    commissionAmount = db.Column(db.Float, nullable=False)
    commissionType = db.Column(db.String(100), nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=True)
    user = db.relationship(
        'User', backref=db.backref('commissions', lazy=True))
