from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Get all users
@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'email': u.email,
        'role': u.role,
        'created_at': u.created_at.isoformat()
    } for u in users])

# Get single user
@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    u = User.query.get_or_404(id)
    return jsonify({
        'id': u.id,
        'name': u.name,
        'email': u.email,
        'role': u.role,
        'created_at': u.created_at.isoformat()
    })

# Create new user
@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    if not all(k in data for k in ("name", "email", "password_hash")):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=data['password_hash'],
        role=data.get('role', 'staff')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created', 'id': user.id}), 201

# Update user
@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    u = User.query.get_or_404(id)
    u.name = data.get('name', u.name)
    u.email = data.get('email', u.email)
    u.password_hash = data.get('password_hash', u.password_hash)
    u.role = data.get('role', u.role)
    db.session.commit()
    return jsonify({'message': 'User updated'})

# Delete user
@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    u = User.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
