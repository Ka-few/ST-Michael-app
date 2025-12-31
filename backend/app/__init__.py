import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models import db

def create_app():
    app = Flask(__name__)
    
    # Disable strict slashes globally
    app.url_map.strict_slashes = False
    
    # CORS Configuration
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,https://st-michael-app-9uok.vercel.app').split(',')
    
    CORS(app, 
         resources={r"/*": {
             "origins": allowed_origins,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "expose_headers": ["Content-Type", "Authorization"]
         }})
    
    # Database configuration - PostgreSQL for production, SQLite for dev
    if os.getenv('DATABASE_URL'):
        # Production: Use PostgreSQL from Render
        database_url = os.getenv('DATABASE_URL')
        # Fix for SQLAlchemy (Render uses postgres://, SQLAlchemy needs postgresql://)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {
                'sslmode': 'require'
            }
        }
    else:
        # Development: Use SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT configuration - Use environment variable in production
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # AUTO-CREATE DATABASE TABLES ON STARTUP
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified!")
    
    # Register blueprints
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