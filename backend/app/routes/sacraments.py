from flask import Blueprint, request, jsonify
from app.models import db, Sacrament, Member
from datetime import datetime

sacraments_bp = Blueprint('sacraments', __name__, url_prefix='/sacraments')

# Get all sacraments
@sacraments_bp.route('/', methods=['GET'])
def get_sacraments():
    sacraments = Sacrament.query.all()
    return jsonify([{
        'id': s.id,
        'member_id': s.member_id,
        'member_name': s.member.name if s.member else None,
        'type': s.type,
        'date': s.date.isoformat() if s.date else None,
        'certificate_path': s.certificate_path
    } for s in sacraments])

# Get single sacrament
@sacraments_bp.route('/<int:id>', methods=['GET'])
def get_sacrament(id):
    s = Sacrament.query.get_or_404(id)
    return jsonify({
        'id': s.id,
        'member_id': s.member_id,
        'member_name': s.member.name if s.member else None,
        'type': s.type,
        'date': s.date.isoformat() if s.date else None,
        'certificate_path': s.certificate_path
    })

# Create new sacrament
@sacraments_bp.route('/', methods=['POST'])
def create_sacrament():
    data = request.json
    if not all(k in data for k in ("member_id", "type")):
        return jsonify({'error': 'Missing required fields: member_id or type'}), 400

    # Optional: parse date
    sacrament_date = None
    if 'date' in data:
        try:
            sacrament_date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    sacrament = Sacrament(
        member_id=data['member_id'],
        type=data['type'],
        date=sacrament_date,
        certificate_path=data.get('certificate_path')
    )
    db.session.add(sacrament)
    db.session.commit()
    return jsonify({'message': 'Sacrament created', 'id': sacrament.id}), 201

# Update sacrament
@sacraments_bp.route('/<int:id>', methods=['PUT'])
def update_sacrament(id):
    s = Sacrament.query.get_or_404(id)
    data = request.json

    s.member_id = data.get('member_id', s.member_id)
    s.type = data.get('type', s.type)
    if 'date' in data:
        try:
            s.date = datetime.fromisoformat(data['date']).date()
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    s.certificate_path = data.get('certificate_path', s.certificate_path)
    
    db.session.commit()
    return jsonify({'message': 'Sacrament updated'})

# Delete sacrament
@sacraments_bp.route('/<int:id>', methods=['DELETE'])
def delete_sacrament(id):
    s = Sacrament.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Sacrament deleted'})
