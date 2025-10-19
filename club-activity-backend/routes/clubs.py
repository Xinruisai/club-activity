from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.club import Club
from models.user import User
from app import db

club_bp = Blueprint('clubs', __name__)

# POST /api/clubs —— 创建社团
@club_bp.route('', methods=['POST'])
@jwt_required()
def create_club():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({'message': 'Club name is required'}), 400

    # 创建社团，关联当前用户为创始人
    club = Club(name=name, description=description, founder_id=current_user_id)
    db.session.add(club)
    db.session.commit()

    return jsonify({'message': 'Club created', 'club_id': club.id}), 201

# GET /api/clubs —— 获取社团列表（可扩展筛选逻辑）
@club_bp.route('', methods=['GET'])
def get_clubs():
    clubs = Club.query.all()
    return jsonify([{
        'id': club.id,
        'name': club.name,
        'description': club.description,
        'founder_id': club.founder_id
    } for club in clubs]), 200