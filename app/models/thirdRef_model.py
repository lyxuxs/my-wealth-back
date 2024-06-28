from app import db


class ThirdRef(db.Model):
    refTreeID = db.Column(db.Integer, primary_key=True)
    Ref = db.Column(db.String(255))
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    user = db.relationship('User', backref=db.backref('thirdRefs', lazy=True))
