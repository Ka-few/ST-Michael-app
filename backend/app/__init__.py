import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models import db

def create_app():
    app = Flask(__name__)

    # ---------------- BASIC CONFIG ----------------
    app.url_map.strict_slashes = False

    # ---------------- CORS CONFIGURATION ----------------
    # This reads the environment variable or defaults to your Vercel/Local URLs
    raw_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,https://st-michael-app-9uok.vercel.app"
    )
    allowed_origins = [o.strip() for o in raw_origins.split(",") if o]

    # Optimized CORS setup
    CORS(
        app,
        resources={r"/*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        expose_headers=["Content-Type", "Authorization"]
    )

    # ---------------- DATABASE ----------------
    database_url = os.getenv("DATABASE_URL", "sqlite:///church.db")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if database_url and "postgresql://" in database_url:
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
        try:
            db.create_all()
            print("✅ Database tables verified!")
        except Exception as e:
            print(f"❌ Database error: {e}")

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