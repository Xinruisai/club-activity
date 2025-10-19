from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.registration import Registration
from models.event import Event
from models.user import User
from app import db

registration_bp = Blueprint('registrations', __name__)

# POST /api/registrations —— 报名活动
@registration_bp.route('', methods=['POST'])
@jwt_required()
def register_for_event():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    event_id = data.get('event_id')

    if not event_id:
        return jsonify({'message': 'event_id is required'}), 400

    # 检查活动是否存在
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    # 检查是否已经报名
    existing = Registration.query.filter_by(user_id=current_user_id, event_id=event_id).first()
    if existing:
        return jsonify({'message': 'You have already registered for this event'}), 400

    reg = Registration(user_id=current_user_id, event_id=event_id)
    db.session.add(reg)
    db.session.commit()

    return jsonify({'message': 'Successfully registered for event'}), 201

# GET /api/registrations —— 获取我的报名
@registration_bp.route('', methods=['GET'])
@jwt_required()
def get_my_registrations():
    current_user_id = get_jwt_identity()
    regs = Registration.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        'id': r.id,
        'event_id': r.event_id,
        'registered_at': r.registered_at,
        'event': {
            'title': r.event.title,
            'date': r.event.date,
            'location': r.event.location
        }
    } for r in regs]), 200