from app import create_app
from app.models import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print("-" * 30)
    print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Role':<10}")
    print("-" * 70)
    for u in users:
        print(f"{u.id:<5} {u.name:<20} {u.email:<30} {u.role:<10}")
    print("-" * 30)
