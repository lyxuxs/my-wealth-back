from app import db


class Package(db.Model):
    packageID = db.Column(db.Integer, primary_key=True)
    packageName = db.Column(db.String(100), nullable=False)
    personalMinFund = db.Column(db.Integer, nullable=False)
    personalMaxFund = db.Column(db.Integer, nullable=False)
    rebateFee = db.Column(db.Float, nullable=False)
