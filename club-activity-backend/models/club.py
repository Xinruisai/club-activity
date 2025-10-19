from app import db

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    founder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    founder = db.relationship('User', backref='founded_clubs')