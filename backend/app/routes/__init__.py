from .members import members_bp
from .users import users_bp
from .sacraments import sacraments_bp
from .events import events_bp
from .districts import districts_bp
from .donations import donations_bp
from .announcement import announcements_bp

def register_routes(app):
    app.register_blueprint(members_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(sacraments_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(districts_bp)
    app.register_blueprint(announcements_bp)
   
    app.register_blueprint(donations_bp)
