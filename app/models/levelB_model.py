from app import db


class LevelB(db.Model):
    refTreeID = db.Column(db.Integer, primary_key=True)
    isFriendAdmin = db.Column(db.Boolean, nullable=False, default=False)
    friendUserID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    user = db.relationship('User', backref=db.backref('levelAs', lazy=True))
