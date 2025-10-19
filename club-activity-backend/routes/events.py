from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.event import Event
from models.club import Club
from app import db

event_bp = Blueprint('events', __name__)

# POST /api/events —— 创建活动
@event_bp.route('', methods=['POST'])
@jwt_required()
def create_event():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    description = data.get('description', '')
    date = data.get('date')
    location = data.get('location')
    max_participants = data.get('max_participants', 100)
    club_id = data.get('club_id')

    if not all([title, club_id]):
        return jsonify({'message': 'Title and club_id are required'}), 400

    # 检查社团是否存在
    club = Club.query.get(club_id)
    if not club:
        return jsonify({'message': 'Club not found'}), 404

    event = Event(
        title=title,
        description=description,
        date=date,
        location=location,
        max_participants=max_participants,
        club_id=club_id
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({'message': 'Event created', 'event_id': event.id}), 201

# GET /api/events —— 获取活动列表
@event_bp.route('', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'date': e.date,
        'location': e.location,
        'max_participants': e.max_participants,
        'club_id': e.club_id
    } for e in events]), 200