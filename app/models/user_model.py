from app import db


class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    myReferral = db.Column(db.String(100), nullable=False)
    friendReferral = db.Column(db.String(100), nullable=False)
    spotBalance = db.Column(db.Float, nullable=False)
    fundingBalance = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=False)
    RT = db.Column(db.Boolean, default=False, nullable=False)
    isVerify = db.Column(db.Boolean, default=False, nullable=False)
    OTP = db.Column(db.Integer, nullable=False)
    packageID = db.Column(db.Integer, db.ForeignKey('package.packageID'), nullable=False)

    package = db.relationship('Package', backref=db.backref('users', lazy=True))
