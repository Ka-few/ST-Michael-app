from flask import Blueprint, request, jsonify
from app.models import db, Event
from datetime import datetime

events_bp = Blueprint('events', __name__, url_prefix='/events')

# Get all events
@events_bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'description': e.description,
        'date': e.date.isoformat() if e.date else None,
        'created_at': e.created_at.isoformat()
    } for e in events])

# Get single event
@events_bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    e = Event.query.get_or_404(id)
    return jsonify({
        'id': e.id,
        'name': e.name,
        'description': e.description,
        'date': e.date.isoformat() if e.date else None,
        'created_at': e.created_at.isoformat()
    })

# Create new event
@events_bp.route('/', methods=['POST'])
def create_event():
    data = request.json
    if not all(k in data for k in ("name", "date")):
        return jsonify({'error': 'Missing required fields: name or date'}), 400

    # Parse date
    try:
        event_date = datetime.fromisoformat(data['date']).date()
    except:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    event = Event(
        name=data['name'],
        description=data.get('description'),
        date=event_date
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created', 'id': event.id}), 201

# Update event
@events_bp.route('/<int:id>', methods=['PUT'])
def update_event(id):
    e = Event.query.get_or_404(id)
    data = request.json

    e.name = data.get('name', e.name)
    e.description = data.get('description', e.description)
    if 'date' in data:
        try:
            e.date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    db.session.commit()
    return jsonify({'message': 'Event updated'})

# Delete event
@events_bp.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    e = Event.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({'message': 'Event deleted'})
