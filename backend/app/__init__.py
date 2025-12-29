from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models import db

def create_app():
    app = Flask(__name__)
    
    # Disable strict slashes globally
    app.url_map.strict_slashes = False
    
    # CORS Configuration - IMPORTANT: Must come before route registration
    CORS(app, 
         resources={r"/*": {
             "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "expose_headers": ["Content-Type", "Authorization"]
         }})
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT configuration
    app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this-in-production'
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
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