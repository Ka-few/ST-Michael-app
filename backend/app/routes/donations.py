from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Donation, User, Member
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
        'member_id': d.member_id,
        'amount': float(d.amount),
        'type': d.type,
        'date': d.date.isoformat() if d.date else None,
        'created_at': d.created_at.isoformat() if d.created_at else None
    } for d in donations]), 200

# Create donation for any member (admin only)
@donations_bp.route('/admin/add', methods=['POST'], strict_slashes=False)
@admin_required()
def admin_create_donation():
    data = request.get_json()
    
    if not data.get('member_id') or not data.get('amount') or not data.get('type'):
        return jsonify({'error': 'member_id, amount, and type are required'}), 400
    
    # Validate member exists
    member = Member.query.get(data['member_id'])
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    # Parse date if provided
    donation_date = None
    if 'date' in data:
        try:
            donation_date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    donation = Donation(
        member_id=data['member_id'],
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
            'member_id': donation.member_id,
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
    
    if 'member_id' in data:
        member = Member.query.get(data['member_id'])
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        donation.member_id = data['member_id']
    
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

# Get current user's donations (via their member record)
@donations_bp.route('/my-donations', methods=['GET'])
@jwt_required()
def get_my_donations():
    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)
    
    # Find the member associated with this user
    # Assuming Member model has a user_id or email field to link to User
    user = User.query.get(user_id)
    if not user:
        return jsonify([]), 200
    
    # Try to find member by email or other linking field
    member = Member.query.filter_by(email=user.email).first() if hasattr(Member, 'email') else None
    
    if not member:
        return jsonify([]), 200
    
    donations = Donation.query.filter_by(member_id=member.id).all()
    
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
    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)
    data = request.get_json()
    
    if not data.get('amount') or not data.get('type'):
        return jsonify({'error': 'amount and type are required'}), 400
    
    # Find the member associated with this user
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    member = Member.query.filter_by(email=user.email).first() if hasattr(Member, 'email') else None
    
    if not member:
        return jsonify({'error': 'No member profile found for this user'}), 404
    
    # Parse date if provided
    donation_date = None
    if 'date' in data:
        try:
            donation_date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    donation = Donation(
        member_id=member.id,
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

# Delete own donation
@donations_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_donation(id):
    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)
    
    user = User.query.get(user_id)
    member = Member.query.filter_by(email=user.email).first() if user and hasattr(Member, 'email') else None
    
    if not member:
        return jsonify({'error': 'Member profile not found'}), 404
    
    donation = Donation.query.filter_by(id=id, member_id=member.id).first_or_404()
    db.session.delete(donation)
    db.session.commit()
    return jsonify({'message': 'Donation deleted'}), 200