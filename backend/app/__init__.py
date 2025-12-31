import os
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models import db


def create_app():
    app = Flask(__name__)

    # ---------------- BASIC CONFIG ----------------
    app.url_map.strict_slashes = False

    # ---------------- CORS (RENDER SAFE) ----------------
    allowed_origins = [
        o.strip()
        for o in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,https://st-michael-app-9uok.vercel.app"
        ).split(",")
        if o
    ]

    # Flask-CORS (primary)
    CORS(
        app,
        origins=allowed_origins,
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Force headers (fallback for Render preflight)
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin")
        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    # Always allow OPTIONS
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return "", 200

    # ---------------- DATABASE ----------------
    database_url = os.getenv("DATABASE_URL", "sqlite:///church.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if "postgresql://" in database_url:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"sslmode": "require"}
        }

    # ---------------- JWT ----------------
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "change-this-in-production"
    )

    # ---------------- INIT EXTENSIONS ----------------
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified!")

    # ---------------- ROUTES ----------------
    from app.routes.auth import auth_bp
    from app.routes.sacraments import sacraments_bp
    from app.routes.donations import donations_bp
    from app.routes.announcement import announcements_bp
    from app.routes.events import events_bp
    from app.routes.members import members_bp
    from app.routes.districts import districts_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(announcements_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(sacraments_bp)
    app.register_blueprint(donations_bp)
    app.register_blueprint(districts_bp)

    return app
