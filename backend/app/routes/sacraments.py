from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Sacrament, Member, User
from datetime import datetime
from app.utils.roles import admin_required

sacraments_bp = Blueprint('sacraments', __name__, url_prefix='/sacraments')


# ============== ADMIN ROUTES ==============

@sacraments_bp.route("/admin/all", methods=["GET"], strict_slashes=False)
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

@sacraments_bp.route("/admin/add", methods=["POST"], strict_slashes=False)
@admin_required()
def admin_create_sacrament():
    print("DEBUG: admin_create_sacrament called") # Debug print
    data = request.get_json()
    user_id = data.get("user_id")
    sacrament_type = data.get("type")
    sacrament_date = data.get("date")
    certificate_path = data.get("certificate_path")

    if not user_id or not sacrament_type:
        return jsonify({"error": "user_id and type are required"}), 400

    user = User.query.get(user_id)
    if not user:
        print(f"DEBUG: User {user_id} not found")
        return jsonify({"error": "User not found"}), 404

    if not user.member:
        print(f"DEBUG: User {user_id} has no member")
        return jsonify({"error": "This user has no linked member profile"}), 404

    if sacrament_date:
        try:
            sacrament_date = datetime.fromisoformat(sacrament_date).date()
        except ValueError:
             return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

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

@sacraments_bp.route("/admin/<int:id>", methods=["DELETE"], strict_slashes=False)
@admin_required()
def admin_delete_sacrament(id):
    sacrament = Sacrament.query.get_or_404(id)
    db.session.delete(sacrament)
    db.session.commit()
    return jsonify({"message": "Sacrament deleted"}), 200

# ============== USER ROUTES ==============

@sacraments_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_my_sacraments():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or not user.member:
        return jsonify([]), 200

    # Filter by member_id to get all history for this member
    sacraments = Sacrament.query.filter_by(member_id=user.member.id).all()
    
    return jsonify([
        {
            "id": s.id,
            "type": s.type,
            "date": s.date.isoformat() if s.date else None,
            "certificate_path": s.certificate_path
        } for s in sacraments
    ]), 200

