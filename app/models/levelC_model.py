from app import db


class LevelC(db.Model):
    refTreeID = db.Column(db.Integer, primary_key=True)
    isFriendAdmin = db.Column(db.Boolean, nullable=False, default=False)
    friendUserID = db.Column(db.Integer,  nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    user = db.relationship('User', backref=db.backref('levelCs', lazy=True))
