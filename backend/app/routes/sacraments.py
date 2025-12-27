from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Sacrament, Member
from datetime import datetime
from app.utils.roles import admin_required

sacraments_bp = Blueprint('sacraments', __name__, url_prefix='/sacraments')

# ============== ADMIN ROUTES ==============

# Get all sacraments (admin only)
@sacraments_bp.route("/admin/all", methods=["GET"])
@admin_required()
def get_all_sacraments():
    sacraments = Sacrament.query.all()

    return jsonify([
        {
            "id": s.id,
            "user_id": s.user_id,
            "type": s.type,
            "date_received": s.date_received.isoformat() if s.date_received else None,
            "notes": s.notes
        }
        for s in sacraments
    ]), 200

# Create sacrament for any user (admin only)
@sacraments_bp.route("/admin/add", methods=["POST"])
@admin_required()
def admin_create_sacrament():
    data = request.get_json()

    # Validate required fields
    if not data.get("user_id") or not data.get("type"):
        return jsonify({"error": "user_id and type are required"}), 400

    sacrament = Sacrament(
        user_id=data.get("user_id"),
        type=data.get("type"),
        date_received=data.get("date_received"),
        notes=data.get("notes")
    )

    db.session.add(sacrament)
    db.session.commit()

    return jsonify({
        "message": "Sacrament added",
        "sacrament": {
            "id": sacrament.id,
            "user_id": sacrament.user_id,
            "type": sacrament.type,
            "date_received": sacrament.date_received.isoformat() if sacrament.date_received else None,
            "notes": sacrament.notes
        }
    }), 201

# Delete any sacrament (admin only)
@sacraments_bp.route("/admin/<int:id>", methods=["DELETE"])
@admin_required()
def admin_delete_sacrament(id):
    sacrament = Sacrament.query.get_or_404(id)

    db.session.delete(sacrament)
    db.session.commit()

    return jsonify({"message": "Sacrament deleted"}), 200


# ============== USER ROUTES ==============

# Get current user's sacraments
@sacraments_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_sacraments():
    user_id = get_jwt_identity()

    sacraments = Sacrament.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": s.id,
            "type": s.type,
            "date_received": s.date_received.isoformat() if s.date_received else None,
            "notes": s.notes
        }
        for s in sacraments
    ]), 200

# Get single sacrament (own sacraments only)
@sacraments_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_sacrament(id):
    user_id = get_jwt_identity()
    
    # Only allow users to view their own sacraments
    sacrament = Sacrament.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    return jsonify({
        'id': sacrament.id,
        'user_id': sacrament.user_id,
        'type': sacrament.type,
        'date_received': sacrament.date_received.isoformat() if sacrament.date_received else None,
        'notes': sacrament.notes
    }), 200

# Create sacrament for current user
@sacraments_bp.route("/", methods=["POST"])
@jwt_required()
def create_sacrament():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate required fields
    if not data.get("type"):
        return jsonify({"error": "type is required"}), 400

    sacrament = Sacrament(
        user_id=user_id,
        type=data.get("type"),
        date_received=data.get("date_received"),
        notes=data.get("notes")
    )

    db.session.add(sacrament)
    db.session.commit()

    return jsonify({
        "message": "Sacrament added",
        "sacrament": {
            "id": sacrament.id,
            "type": sacrament.type,
            "date_received": sacrament.date_received.isoformat() if sacrament.date_received else None,
            "notes": sacrament.notes
        }
    }), 201

# Update own sacrament
@sacraments_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_sacrament(id):
    user_id = get_jwt_identity()

    sacrament = Sacrament.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()

    sacrament.type = data.get("type", sacrament.type)
    sacrament.date_received = data.get("date_received", sacrament.date_received)
    sacrament.notes = data.get("notes", sacrament.notes)

    db.session.commit()

    return jsonify({
        "message": "Sacrament updated",
        "sacrament": {
            "id": sacrament.id,
            "type": sacrament.type,
            "date_received": sacrament.date_received.isoformat() if sacrament.date_received else None,
            "notes": sacrament.notes
        }
    }), 200

# Delete own sacrament
@sacraments_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_sacrament(id):
    user_id = get_jwt_identity()

    sacrament = Sacrament.query.filter_by(id=id, user_id=user_id).first_or_404()

    db.session.delete(sacrament)
    db.session.commit()

    return jsonify({"message": "Sacrament deleted"}), 200