from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Donation, User
from datetime import datetime
from app.utils.roles import admin_required

donations_bp = Blueprint('donations', __name__, url_prefix='/donations')

# ============== ADMIN ROUTES ==============

# Get all donations (admin only)
@donations_bp.route('/', methods=['GET'], strict_slashes=False)
@admin_required()
def get_all_donations():
    donations = Donation.query.all()
    return jsonify([{
        'id': d.id,
        'user_id': d.user_id,
        'amount': float(d.amount),
        'type': d.type,
        'date': d.date.isoformat() if d.date else None,
        'created_at': d.created_at.isoformat() if d.created_at else None
    } for d in donations]), 200

# Create donation for any user (admin only)
@donations_bp.route('/admin/add', methods=['POST'], strict_slashes=False)
@admin_required()
def admin_create_donation():
    data = request.get_json()
    
    if not data.get('user_id') or not data.get('amount') or not data.get('type'):
        return jsonify({'error': 'user_id, amount, and type are required'}), 400
    
    # Validate user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Parse date if provided
    donation_date = None
    if 'date' in data:
        try:
            donation_date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    donation = Donation(
        user_id=data['user_id'],
        amount=data['amount'],
        type=data.get('type', 'tithe'),
        date=donation_date
    )
    
    db.session.add(donation)
    db.session.commit()
    
    return jsonify({
        'message': 'Donation added',
        'donation': {
            'id': donation.id,
            'user_id': donation.user_id,
            'amount': float(donation.amount),
            'type': donation.type,
            'date': donation.date.isoformat() if donation.date else None
        }
    }), 201

# Delete any donation (admin only)
@donations_bp.route('/admin/<int:id>', methods=['DELETE'])
@admin_required()
def admin_delete_donation(id):
    donation = Donation.query.get_or_404(id)
    
    db.session.delete(donation)
    db.session.commit()
    
    return jsonify({'message': 'Donation deleted'}), 200

# Update any donation (admin only)
@donations_bp.route('/admin/<int:id>', methods=['PUT'])
@admin_required()
def admin_update_donation(id):
    donation = Donation.query.get_or_404(id)
    data = request.get_json()
    
    if 'user_id' in data:
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        donation.user_id = data['user_id']
    
    donation.amount = data.get('amount', donation.amount)
    donation.type = data.get('type', donation.type)
    
    if 'date' in data:
        try:
            donation.date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    db.session.commit()
    
    return jsonify({'message': 'Donation updated'}), 200


# ============== USER ROUTES ==============

# Get current user's donations
@donations_bp.route('/my-donations', methods=['GET'])
@jwt_required()
def get_my_donations():
    user_id = get_jwt_identity()
    
    donations = Donation.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': d.id,
        'amount': float(d.amount),
        'type': d.type,
        'date': d.date.isoformat() if d.date else None,
        'created_at': d.created_at.isoformat() if d.created_at else None
    } for d in donations]), 200

# Create donation for current user
@donations_bp.route('/', methods=['POST'])
@jwt_required()
def create_donation():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('amount') or not data.get('type'):
        return jsonify({'error': 'amount and type are required'}), 400
    
    # Parse date if provided
    donation_date = None
    if 'date' in data:
        try:
            donation_date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    donation = Donation(
        user_id=user_id,
        amount=data['amount'],
        type=data.get('type', 'tithe'),
        date=donation_date
    )
    
    db.session.add(donation)
    db.session.commit()
    
    return jsonify({
        'message': 'Donation created successfully',
        'donation': {
            'id': donation.id,
            'amount': float(donation.amount),
            'type': donation.type,
            'date': donation.date.isoformat() if donation.date else None
        }
    }), 201

# Get single donation (own donations only)
@donations_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_donation(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Admin can view any donation, regular users only their own
    if user.role == 'admin':
        donation = Donation.query.get_or_404(id)
    else:
        donation = Donation.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    return jsonify({
        'id': donation.id,
        'user_id': donation.user_id if user.role == 'admin' else None,
        'amount': float(donation.amount),
        'type': donation.type,
        'date': donation.date.isoformat() if donation.date else None,
        'created_at': donation.created_at.isoformat() if donation.created_at else None
    }), 200

# Update own donation
@donations_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_donation(id):
    user_id = get_jwt_identity()
    
    donation = Donation.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()
    
    donation.amount = data.get('amount', donation.amount)
    donation.type = data.get('type', donation.type)
    
    if 'date' in data:
        try:
            donation.date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    db.session.commit()
    
    return jsonify({'message': 'Donation updated'}), 200

# Delete own donation
@donations_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_donation(id):
    user_id = get_jwt_identity()
    
    donation = Donation.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    db.session.delete(donation)
    db.session.commit()
    
    return jsonify({'message': 'Donation deleted'}), 200