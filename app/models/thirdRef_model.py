from app import db


class ThirdRef(db.Model):
    refTreeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.String(255))
    Ref = db.Column(db.String(255))
