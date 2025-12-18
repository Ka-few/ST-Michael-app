from flask import Blueprint, request, jsonify
from app.models import db, Attendance, Event, Member

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

# Get all attendance records
@attendance_bp.route('/', methods=['GET'])
def get_all_attendance():
    records = Attendance.query.all()
    return jsonify([{
        'id': a.id,
        'event_id': a.event_id,
        'event_name': a.event.name if a.event else None,
        'member_id': a.member_id,
        'member_name': a.member.name if a.member else None,
        'status': a.status,
        'created_at': a.created_at.isoformat()
    } for a in records])

# Get single attendance record
@attendance_bp.route('/<int:id>', methods=['GET'])
def get_attendance(id):
    a = Attendance.query.get_or_404(id)
    return jsonify({
        'id': a.id,
        'event_id': a.event_id,
        'event_name': a.event.name if a.event else None,
        'member_id': a.member_id,
        'member_name': a.member.name if a.member else None,
        'status': a.status,
        'created_at': a.created_at.isoformat()
    })

# Create new attendance record
@attendance_bp.route('/', methods=['POST'])
def create_attendance():
    data = request.json
    if not all(k in data for k in ("event_id", "member_id")):
        return jsonify({'error': 'Missing required fields: event_id or member_id'}), 400

    # Optional: validate foreign keys
    if not Event.query.get(data['event_id']):
        return jsonify({'error': 'Event not found'}), 404
    if not Member.query.get(data['member_id']):
        return jsonify({'error': 'Member not found'}), 404

    attendance = Attendance(
        event_id=data['event_id'],
        member_id=data['member_id'],
        status=data.get('status', 'present')
    )
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance record created', 'id': attendance.id}), 201

# Update attendance record
@attendance_bp.route('/<int:id>', methods=['PUT'])
def update_attendance(id):
    a = Attendance.query.get_or_404(id)
    data = request.json

    if 'event_id' in data and Event.query.get(data['event_id']):
        a.event_id = data['event_id']
    if 'member_id' in data and Member.query.get(data['member_id']):
        a.member_id = data['member_id']
    a.status = data.get('status', a.status)

    db.session.commit()
    return jsonify({'message': 'Attendance record updated'})

# Delete attendance record
@attendance_bp.route('/<int:id>', methods=['DELETE'])
def delete_attendance(id):
    a = Attendance.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({'message': 'Attendance record deleted'})
