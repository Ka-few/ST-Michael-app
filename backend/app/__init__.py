import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models import db
from app.seed_admin import create_admin

def create_app():
    app = Flask(__name__)

    # 1. BASIC CONFIG
    app.url_map.strict_slashes = False

    # 2. CORS CONFIGURATION (REPLACE PREVIOUS CORS BLOCKS)
    # Reads environment variable or defaults to your exact production/local URLs
    raw_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,https://st-michael-app-9uok.vercel.app"
    )
    allowed_origins = [o.strip() for o in raw_origins.split(",") if o]

    # This resource mapping ensures ALL routes (/*) allow your frontend origin
    CORS(
        app,
        resources={r"/*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # 3. DATABASE CONFIG
    database_url = os.getenv("DATABASE_URL", "sqlite:///church.db")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if database_url and "postgresql://" in database_url:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"sslmode": "require"}
        }

    # 4. JWT & EXTENSIONS
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")
    db.init_app(app)
    JWTManager(app)

    # 5. INITIALIZATION (DB & ADMIN)
    with app.app_context():
        try:
            db.create_all()
            create_admin()  # Call this INSIDE context to avoid "Outside Context" errors
            print("✅ Database and Admin initialized!")
        except Exception as e:
            print(f"❌ Initialization error: {e}")

    # 6. REGISTER BLUEPRINTS
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