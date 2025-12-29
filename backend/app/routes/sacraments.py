from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Sacrament, Member, User
from datetime import datetime
from app.utils.roles import admin_required

sacraments_bp = Blueprint('sacraments', __name__, url_prefix='/sacraments')

# -------------------- ADMIN OPTIONS HANDLER --------------------
# Catch-all for admin preflight requests
@sacraments_bp.route("/admin/<path:path>", methods=["OPTIONS"])
def admin_options(path):
    return "", 204

# ============== ADMIN ROUTES ==============

@sacraments_bp.route("/admin/all", methods=["GET"])
@admin_required()
def get_all_sacraments():
    try:
        sacraments = Sacrament.query.all()
        return jsonify([
            {
                "id": s.id,
                "user_id": s.user_id,
                "member_id": s.member_id,
                "type": s.type,
                "date": s.date.isoformat() if s.date else None,
                "certificate_path": s.certificate_path
            } for s in sacraments
        ]), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@sacraments_bp.route("/admin/add", methods=["POST"])
@admin_required()
def admin_create_sacrament():
    data = request.get_json()
    user_id = data.get("user_id")
    sacrament_type = data.get("type")
    sacrament_date = data.get("date")
    certificate_path = data.get("certificate_path")

    if not user_id or not sacrament_type:
        return jsonify({"error": "user_id and type are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.member:
        return jsonify({"error": "This user has no linked member profile"}), 400

    sacrament = Sacrament(
        user_id=user.id,
        member_id=user.member.id,  # link member automatically
        type=sacrament_type,
        date=sacrament_date,
        certificate_path=certificate_path,
    )

    db.session.add(sacrament)
    db.session.commit()

    return jsonify({
        "message": "Sacrament added",
        "sacrament": {
            "id": sacrament.id,
            "user_id": sacrament.user_id,
            "member_id": sacrament.member_id,
            "type": sacrament.type,
            "date": sacrament.date.isoformat() if sacrament.date else None,
            "certificate_path": sacrament.certificate_path
        }
    }), 201

@sacraments_bp.route("/admin/<int:id>", methods=["DELETE"])
@admin_required()
def admin_delete_sacrament(id):
    sacrament = Sacrament.query.get_or_404(id)
    db.session.delete(sacrament)
    db.session.commit()
    return jsonify({"message": "Sacrament deleted"}), 200

# ============== USER ROUTES ==============

@sacraments_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_sacraments():
    user_id = int(get_jwt_identity())
    sacraments = Sacrament.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": s.id,
            "type": s.type,
            "date": s.date.isoformat() if s.date else None,
            "certificate_path": s.certificate_path
        } for s in sacraments
    ]), 200

@sacraments_bp.route("/", methods=["POST"])
@jwt_required()
def create_sacrament():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get("type"):
        return jsonify({"error": "type is required"}), 400

    user = User.query.get(user_id)
    if not user.member:
        return jsonify({"error": "Current user has no linked member profile"}), 400

    sacrament = Sacrament(
        user_id=user.id,
        member_id=user.member.id,
        type=data.get("type"),
        date=data.get("date"),
        certificate_path=data.get("certificate_path")
    )

    db.session.add(sacrament)
    db.session.commit()

    return jsonify({
        "message": "Sacrament added",
        "sacrament": {
            "id": sacrament.id,
            "type": sacrament.type,
            "date": sacrament.date.isoformat() if sacrament.date else None,
            "certificate_path": sacrament.certificate_path
        }
    }), 201

@sacraments_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_sacrament(id):
    user_id = int(get_jwt_identity())
    sacrament = Sacrament.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()

    sacrament.type = data.get("type", sacrament.type)
    sacrament.date = data.get("date", sacrament.date)
    sacrament.certificate_path = data.get("certificate_path", sacrament.certificate_path)

    db.session.commit()
    return jsonify({"message": "Sacrament updated"}), 200

@sacraments_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_sacrament(id):
    user_id = int(get_jwt_identity())
    sacrament = Sacrament.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(sacrament)
    db.session.commit()
    return jsonify({"message": "Sacrament deleted"}), 200
