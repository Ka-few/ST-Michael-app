from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import db
from app.models import Announcement
from app.utils.roles import admin_required

announcements_bp = Blueprint("announcements", __name__, url_prefix="/announcements")

# OPTIONS handler


# ---------------- CREATE ANNOUNCEMENT ----------------
@announcements_bp.route("/", methods=["POST"])
@admin_required()  # Only admin can create
def create_announcement():
    data = request.get_json()

    announcement = Announcement(
        title=data.get("title"),
        message=data.get("message"),
        category=data.get("category", "general"),
        publish_date=datetime.utcnow(),
        expiry_date=data.get("expiry_date")
    )

    db.session.add(announcement)
    db.session.commit()

    return jsonify({"message": "Announcement created", "id": announcement.id}), 201


# ---------------- GET ALL ANNOUNCEMENTS ----------------
@announcements_bp.route("/", methods=["GET"], strict_slashes=False)
def get_announcements():
    announcements = Announcement.query.order_by(
        Announcement.publish_date.desc()
    ).all()

    results = []
    for a in announcements:
        results.append({
            "id": a.id,
            "title": a.title,
            "message": a.message,
            "category": a.category,
            "publish_date": a.publish_date.isoformat() if a.publish_date else None,  # Fixed serialization
            "expiry_date": a.expiry_date.isoformat() if a.expiry_date else None  # Fixed serialization
        })

    return jsonify(results), 200


# ---------------- GET SINGLE ANNOUNCEMENT ----------------
@announcements_bp.route("/<int:id>", methods=["GET"])
def get_announcement(id):
    a = Announcement.query.get_or_404(id)

    return jsonify({
        "id": a.id,
        "title": a.title,
        "message": a.message,
        "category": a.category,
        "publish_date": a.publish_date.isoformat() if a.publish_date else None,
        "expiry_date": a.expiry_date.isoformat() if a.expiry_date else None
    }), 200


# ---------------- UPDATE ANNOUNCEMENT ----------------
@announcements_bp.route("/<int:id>", methods=["PUT"])
@admin_required()  # Only admin can update
def update_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    data = request.get_json()

    announcement.title = data.get("title", announcement.title)
    announcement.message = data.get("message", announcement.message)
    announcement.category = data.get("category", announcement.category)
    announcement.expiry_date = data.get("expiry_date", announcement.expiry_date)

    db.session.commit()

    return jsonify({"message": "Announcement updated"}), 200


# ---------------- DELETE ANNOUNCEMENT ----------------
@announcements_bp.route("/<int:id>", methods=["DELETE"])
@admin_required()  # Only admin can delete
def delete_announcement(id):
    announcement = Announcement.query.get_or_404(id)

    db.session.delete(announcement)
    db.session.commit()

    return jsonify({"message": "Announcement deleted"}), 200