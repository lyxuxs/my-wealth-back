from app import db


class MainRef(db.Model):
    refTreeID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(255))
    Ref = db.Column(db.String(255))
