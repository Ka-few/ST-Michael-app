# create_admin_member.py
from app import create_app
from app.extensions import db
from app.models import User, Member
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("CREATING/FIXING ADMIN USER AND MEMBER")
    print("="*60 + "\n")
    
    # 1. Get or create admin user
    admin = User.query.filter_by(email='admin@church.com').first()
    
    if not admin:
        print("Creating admin user...")
        admin = User(
            name='Administrator',
            email='admin@church.com',
            password_hash=generate_password_hash('Admin@123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✓ Admin user created (ID: {admin.id})")
    else:
        print(f"✓ Admin user exists (ID: {admin.id})")
    
    # 2. Check if admin has a member profile
    if admin.member:
        print(f"✓ Admin already has member profile (ID: {admin.member.id})")
    else:
        print("✗ Admin has no member profile. Creating one...")
        
        # Create a member profile for admin
        member = Member(
            name='Admin',
            
            contact='0721223355',        
            
            address='Church Office',
            user_id=admin.id
        )
        
        db.session.add(member)
        db.session.commit()
        print(f"✓ Member profile created (ID: {member.id})")
    
    # 3. List all users and their member status
    print("\n📋 ALL USERS:")
    users = User.query.all()
    for user in users:
        member_status = f"Member ID: {user.member.id}" if user.member else "NO MEMBER"
        print(f"  - User ID: {user.id:3} | {user.email:30} | Role: {user.role:10} | {member_status}")
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE")
    print("="*60)
    print("\nYou can now:")
    print("1. Add sacraments for User ID:", admin.id)
    print("2. Login with: admin@church.com / Admin@123")
    print()