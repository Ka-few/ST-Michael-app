from flask import Blueprint, request, jsonify
from app.models import db, Donation, Member
from datetime import datetime

donations_bp = Blueprint('donations', __name__, url_prefix='/donations')

# Get all donations
@donations_bp.route('/', methods=['GET'])
def get_donations():
    donations = Donation.query.all()
    return jsonify([{
        'id': d.id,
        'member_id': d.member_id,
        'member_name': d.member.name if d.member else None,
        'amount': d.amount,
        'type': d.type,
        'date': d.date.isoformat() if d.date else None,
        'created_at': d.created_at.isoformat()
    } for d in donations])

# Get single donation
@donations_bp.route('/<int:id>', methods=['GET'])
def get_donation(id):
    d = Donation.query.get_or_404(id)
    return jsonify({
        'id': d.id,
        'member_id': d.member_id,
        'member_name': d.member.name if d.member else None,
        'amount': d.amount,
        'type': d.type,
        'date': d.date.isoformat() if d.date else None,
        'created_at': d.created_at.isoformat()
    })

# Create new donation
@donations_bp.route('/', methods=['POST'])
def create_donation():
    data = request.json
    if not all(k in data for k in ("member_id", "amount")):
        return jsonify({'error': 'Missing required fields: member_id or amount'}), 400

    # Validate member exists
    if not Member.query.get(data['member_id']):
        return jsonify({'error': 'Member not found'}), 404

    # Optional: parse date
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
    return jsonify({'message': 'Donation created', 'id': donation.id}), 201

# Update donation
@donations_bp.route('/<int:id>', methods=['PUT'])
def update_donation(id):
    d = Donation.query.get_or_404(id)
    data = request.json

    if 'member_id' in data and Member.query.get(data['member_id']):
        d.member_id = data['member_id']
    d.amount = data.get('amount', d.amount)
    d.type = data.get('type', d.type)
    if 'date' in data:
        try:
            d.date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    db.session.commit()
    return jsonify({'message': 'Donation updated'})

# Delete donation
@donations_bp.route('/<int:id>', methods=['DELETE'])
def delete_donation(id):
    d = Donation.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({'message': 'Donation deleted'})
