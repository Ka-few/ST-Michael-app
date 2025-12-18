from app import create_app
from app.models import db, User, Member, Sacrament, Event, Attendance, Donation
from datetime import date
import random

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    admin = User(name="Admin User", email="admin@church.com", password_hash="admin123", role="admin")
    staff = User(name="Staff User", email="staff@church.com", password_hash="staff123", role="staff")
    db.session.add_all([admin, staff])
    db.session.commit()

    # Members
    members = []
    for i in range(1, 11):
        member = Member(
            name=f"Member {i}",
            contact=f"0722{i:06d}",
            address=f"{i} Church Street, Nairobi",
            family=f"Family {i%3 + 1}",
            status="active"
        )
        members.append(member)
    db.session.add_all(members)
    db.session.commit()

    # Sacraments
    sacraments_types = ["Baptism", "Confirmation", "Marriage"]
    for member in members:
        for sac_type in random.sample(sacraments_types, k=random.randint(1,2)):
            sacrament = Sacrament(
                member_id=member.id,
                type=sac_type,
                date=date(2020 + random.randint(0,3), random.randint(1,12), random.randint(1,28))
            )
            db.session.add(sacrament)
    db.session.commit()

    # Events
    events = []
    for i in range(1,6):
        event = Event(name=f"Sunday Mass {i}", description="Weekly Sunday service", date=date(2025,12,i))
        events.append(event)
    db.session.add_all(events)
    db.session.commit()

    # Attendance
    for event in events:
        for member in members:
            attendance = Attendance(event_id=event.id, member_id=member.id, status=random.choice(["present","absent"]))
            db.session.add(attendance)
    db.session.commit()

    # Donations
    for member in members:
        for _ in range(random.randint(1,3)):
            donation = Donation(
                member_id=member.id,
                amount=random.randint(100,1000),
                type=random.choice(["tithe","offering"]),
                date=date(2025, random.randint(1,12), random.randint(1,28))
            )
            db.session.add(donation)
    db.session.commit()

    print("✅ Database seeded successfully!")
