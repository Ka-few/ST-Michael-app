import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    CORS(app)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'church.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    jwt = JWTManager(app)

    db.init_app(app)

    # Test route
    @app.route('/')
    def home():
        return "✅ Church MVP backend is running!"

    # Register API routes
    from .routes import register_routes
    register_routes(app)

    return app
