from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from app.models import db, User, Member

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    contact = data.get("contact")  # optional

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    # 1️⃣ Create User
    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role="member"
    )

    db.session.add(user)
    db.session.flush()  # 🔑 get user.id without committing

    # 2️⃣ Create linked Member profile
    member = Member(
        name=name,
        contact=contact,
        user_id=user.id
    )

    db.session.add(member)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
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

    # Create access token with optional role claim
    additional_claims = {}
    if hasattr(user, 'role'):
        additional_claims["role"] = user.role
    
    token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims
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
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    return jsonify({
        "id": user.id,
        "email": user.email
    }), 200