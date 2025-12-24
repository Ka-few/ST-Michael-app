from app import create_app
from app.models import (
    db,
    User,
    Member,
    Sacrament,
    Event,
    Donation,
    District,
    Announcement
)
from datetime import date
import random

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # ---------------- USERS ----------------
    admin = User(
        name="Admin User",
        email="admin@church.com",
        password_hash="admin123",
        role="admin"
    )

    staff = User(
        name="Staff User",
        email="staff@church.com",
        password_hash="staff123",
        role="staff"
    )

    db.session.add_all([admin, staff])
    db.session.commit()

    # ---------------- DISTRICTS ----------------
    districts = [
        District(name="St. Peter Jumuiya", leader_name="Joseph Mwangi"),
        District(name="St. Paul Jumuiya", leader_name="Mary Wanjiku"),
        District(name="St. John Jumuiya", leader_name="Peter Otieno"),
    ]

    db.session.add_all(districts)
    db.session.commit()

    # ---------------- MEMBERS ----------------
    members = []
    for i in range(1, 11):
        member = Member(
            name=f"Member {i}",
            contact=f"0722{i:06d}",
            address=f"{i} Church Street, Nairobi",
            family=f"Family {i % 3 + 1}",
            status="active",
            district_id=random.choice(districts).id
        )
        members.append(member)

    db.session.add_all(members)
    db.session.commit()

    # ---------------- SACRAMENTS ----------------
    sacrament_types = ["Baptism", "Confirmation", "Marriage"]

    for member in members:
        for sac_type in random.sample(sacrament_types, k=random.randint(1, 2)):
            sacrament = Sacrament(
                member_id=member.id,
                type=sac_type,
                date=date(
                    2020 + random.randint(0, 4),
                    random.randint(1, 12),
                    random.randint(1, 28)
                )
            )
            db.session.add(sacrament)

    db.session.commit()

    # ---------------- EVENTS ----------------
    events = []
    for i in range(1, 6):
        event = Event(
            name=f"Sunday Mass {i}",
            description="Weekly Sunday service",
            date=date(2025, 12, i)
        )
        events.append(event)

    db.session.add_all(events)
    db.session.commit()

    # ---------------- DONATIONS ----------------
    for member in members:
        for _ in range(random.randint(1, 3)):
            donation = Donation(
                member_id=member.id,
                amount=random.randint(200, 5000),
                type=random.choice(["tithe", "offering"]),
                date=date(
                    2025,
                    random.randint(1, 12),
                    random.randint(1, 28)
                )
            )
            db.session.add(donation)

    db.session.commit()

    # ---------------- ANNOUNCEMENTS ----------------
    announcements = [
        Announcement(
            title="Sunday Mass Schedule",
            message="Sunday Mass will be held at 8:00 AM, 10:00 AM, and 12:00 PM.",
            category="mass"
        ),
        Announcement(
            title="Youth Fundraiser",
            message="Youth group fundraiser will take place next Saturday after Mass.",
            category="fundraising"
        ),
        Announcement(
            title="Parish Council Meeting",
            message="All district leaders are requested to attend the parish council meeting on Friday.",
            category="general"
        ),
    ]

    db.session.add_all(announcements)
    db.session.commit()

    print("✅ Database seeded successfully with districts & announcements!")
