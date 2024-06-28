from app import db


class MainRef(db.Model):
    refTreeID = db.Column(db.Integer, primary_key=True)
    Ref = db.Column(db.String(255))
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    user = db.relationship('User', backref=db.backref('mainRefs', lazy=True))
