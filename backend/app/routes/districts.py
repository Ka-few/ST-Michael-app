from flask import Blueprint, request, jsonify
from app.models import db, District, Member

districts_bp = Blueprint("districts", __name__, url_prefix="/districts")

# ---------------- CREATE DISTRICT ----------------
@districts_bp.route("/", methods=["POST"])
def create_district():
    data = request.get_json()

    district = District(
        name=data.get("name"),
        leader_name=data.get("leader_name"),
        description=data.get("description")
    )

    db.session.add(district)
    db.session.commit()

    return jsonify({"message": "District created", "id": district.id}), 201


# ---------------- GET ALL DISTRICTS ----------------
@districts_bp.route("/", methods=["GET"])
def get_districts():
    districts = District.query.all()

    results = []
    for d in districts:
        results.append({
            "id": d.id,
            "name": d.name,
            "leader_name": d.leader_name,
            "description": d.description,
            "member_count": len(d.members)
        })

    return jsonify(results), 200


# ---------------- GET SINGLE DISTRICT ----------------
@districts_bp.route("/<int:id>", methods=["GET"])
def get_district(id):
    district = District.query.get_or_404(id)

    return jsonify({
        "id": district.id,
        "name": district.name,
        "leader_name": district.leader_name,
        "description": district.description,
        "members": [
            {"id": m.id, "name": m.name}
            for m in district.members
        ]
    }), 200


# ---------------- UPDATE DISTRICT ----------------
@districts_bp.route("/<int:id>", methods=["PUT"])
def update_district(id):
    district = District.query.get_or_404(id)
    data = request.get_json()

    district.name = data.get("name", district.name)
    district.leader_name = data.get("leader_name", district.leader_name)
    district.description = data.get("description", district.description)

    db.session.commit()

    return jsonify({"message": "District updated"}), 200


# ---------------- DELETE DISTRICT ----------------
@districts_bp.route("/<int:id>", methods=["DELETE"])
def delete_district(id):
    district = District.query.get_or_404(id)

    db.session.delete(district)
    db.session.commit()

    return jsonify({"message": "District deleted"}), 200
