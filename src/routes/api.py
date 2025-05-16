from flask import Blueprint, request, jsonify
from ..models.user import db, User

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        id=data['id'],
        display_name=data['display_name'],
        public_key=data['public_key']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@api_bp.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'display_name': user.display_name,
        'public_key': user.public_key
    })