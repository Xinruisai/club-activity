from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.String(100))  # 简化：日期字符串
    location = db.Column(db.String(100))
    max_participants = db.Column(db.Integer, default=100)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    club = db.relationship('Club', backref='events')