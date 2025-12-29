from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from app.models import User

def admin_required():
    """
    Decorator to require admin role for accessing a route.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                # Verify JWT is present
                verify_jwt_in_request()
                
                # Get user identity from JWT (as string)
                user_id_str = get_jwt_identity()
                
                # Convert to integer for database query
                try:
                    user_id = int(user_id_str)
                except (ValueError, TypeError):
                    return jsonify({"error": "Invalid user ID"}), 400
                
                # Fetch user from database
                user = User.query.get(user_id)
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                # Check if user has admin role
                if not hasattr(user, 'role') or user.role != 'admin':
                    return jsonify({"error": "Admin access required"}), 403
                
                return fn(*args, **kwargs)
                
            except Exception as e:
                print(f"ERROR in admin_required: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({"error": "Authorization failed"}), 500
                
        return decorator
    return wrapper


def role_required(required_role):
    """
    Decorator to require a specific role for accessing a route.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                
                user_id_str = get_jwt_identity()
                user_id = int(user_id_str)
                
                user = User.query.get(user_id)
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                if not hasattr(user, 'role') or user.role != required_role:
                    return jsonify({"error": f"{required_role.capitalize()} access required"}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                print(f"ERROR in role_required: {str(e)}")
                return jsonify({"error": "Authorization failed"}), 500
                
        return decorator
    return wrapper


def roles_required(*required_roles):
    """
    Decorator to require one of multiple roles for accessing a route.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                
                user_id_str = get_jwt_identity()
                user_id = int(user_id_str)
                
                user = User.query.get(user_id)
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                if not hasattr(user, 'role') or user.role not in required_roles:
                    return jsonify({"error": "Insufficient permissions"}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                print(f"ERROR in roles_required: {str(e)}")
                return jsonify({"error": "Authorization failed"}), 500
                
        return decorator
    return wrapper