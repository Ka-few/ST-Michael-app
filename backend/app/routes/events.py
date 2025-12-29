from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Event
from datetime import datetime
from app.utils.roles import admin_required

events_bp = Blueprint('events', __name__, url_prefix='/events')

# OPTIONS handler
@events_bp.route('/<path:path>', methods=['OPTIONS'])
@events_bp.route('/', methods=['OPTIONS'], defaults={'path': ''})
def handle_options(path):
    return '', 204

# Get all events
@events_bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_events():
    events = Event.query.order_by(Event.date.desc()).all()
    
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'description': e.description,
        'date': e.date.isoformat() if e.date else None,
        'created_at': e.created_at.isoformat() if e.created_at else None
    } for e in events]), 200

# Create event (admin only)
@events_bp.route('/', methods=['POST'])
@admin_required()
def create_event():
    data = request.get_json()
    
    if not data.get('name') or not data.get('date'):
        return jsonify({'error': 'name and date are required'}), 400
    
    event = Event(
        name=data['name'],
        description=data.get('description', ''),
        date=datetime.fromisoformat(data['date']).date()
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'message': 'Event created', 'id': event.id}), 201

# Update event (admin only)
@events_bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()
    
    event.name = data.get('name', event.name)
    event.description = data.get('description', event.description)
    if data.get('date'):
        event.date = datetime.fromisoformat(data['date']).date()
    
    db.session.commit()
    return jsonify({'message': 'Event updated'}), 200

# Delete event (admin only)
@events_bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200