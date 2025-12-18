from flask import Blueprint, request, jsonify
from app.models import db, Member

members_bp = Blueprint('members', __name__, url_prefix='/members')

# Get all members
@members_bp.route('/', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'contact': m.contact,
        'address': m.address,
        'family': m.family,
        'status': m.status
    } for m in members])

# Get single member
@members_bp.route('/<int:id>', methods=['GET'])
def get_member(id):
    m = Member.query.get_or_404(id)
    return jsonify({
        'id': m.id,
        'name': m.name,
        'contact': m.contact,
        'address': m.address,
        'family': m.family,
        'status': m.status
    })

# Create member
@members_bp.route('/', methods=['POST'])
def create_member():
    data = request.json
    member = Member(
        name=data.get('name'),
        contact=data.get('contact'),
        address=data.get('address'),
        family=data.get('family'),
        status=data.get('status', 'active')
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Member created', 'id': member.id}), 201

# Update member
@members_bp.route('/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.json
    m = Member.query.get_or_404(id)
    m.name = data.get('name', m.name)
    m.contact = data.get('contact', m.contact)
    m.address = data.get('address', m.address)
    m.family = data.get('family', m.family)
    m.status = data.get('status', m.status)
    db.session.commit()
    return jsonify({'message': 'Member updated'})

# Delete member
@members_bp.route('/<int:id>', methods=['DELETE'])
def delete_member(id):
    m = Member.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'Member deleted'})
