from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from app.extensions import db
from app.models import User, Member
from datetime import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")



# ---------------- REGISTER ----------------

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    claim_code = data.get("claim_code")

    if not name or not email or not password or not claim_code:
        return jsonify({"error": "Name, email, password and claim code required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    # 🔍 Find member by claim code
    member = Member.query.filter_by(claim_code=claim_code).first()

    if not member:
        return jsonify({"error": "Invalid claim code"}), 400

    if member.user_id:
        return jsonify({"error": "Member already linked"}), 400

    if member.claim_code_expires_at and member.claim_code_expires_at < datetime.utcnow():
        return jsonify({"error": "Claim code expired"}), 400

    # 1️⃣ Create User
    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role="member"
    )

    db.session.add(user)
    db.session.flush()  # get user.id

    # 2️⃣ Link member
    member.user_id = user.id
    member.claim_code = None
    member.claim_code_expires_at = None

    db.session.commit()

    return jsonify({
        "message": "Registration successful",
        "user_id": user.id,
        "member_id": member.id
    }), 201

# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create access token with user ID as STRING
    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200


# ---------------- CURRENT USER ----------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)  # Convert to int
    user = User.query.get_or_404(user_id)

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200