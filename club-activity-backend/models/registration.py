from app import db

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registered_at = db.Column(db.String(100), default='now')  # 简化

    user = db.relationship('User', backref='my_registrations')
    event = db.relationship('Event', backref='registrations')