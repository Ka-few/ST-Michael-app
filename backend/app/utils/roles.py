from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from app.models import User

def admin_required():
    """
    Decorator to require admin role for accessing a route.
    Use after @jwt_required() or it will verify JWT itself.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verify JWT is present
            verify_jwt_in_request()
            
            # Get user identity from JWT
            user_id = get_jwt_identity()
            
            # Fetch user from database
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            # Check if user has admin role
            if not hasattr(user, 'role') or user.role != 'admin':
                return jsonify({"error": "Admin access required"}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def role_required(required_role):
    """
    Decorator to require a specific role for accessing a route.
    
    Usage:
        @role_required('admin')
        @role_required('moderator')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            if not hasattr(user, 'role') or user.role != required_role:
                return jsonify({"error": f"{required_role.capitalize()} access required"}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def roles_required(*required_roles):
    """
    Decorator to require one of multiple roles for accessing a route.
    
    Usage:
        @roles_required('admin', 'moderator')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            if not hasattr(user, 'role') or user.role not in required_roles:
                return jsonify({"error": "Insufficient permissions"}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper