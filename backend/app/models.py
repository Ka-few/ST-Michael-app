from datetime import datetime
from . import db

# ---------- User / Roles ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='staff')  # 'admin' or 'staff'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sacraments = db.relationship("Sacrament", backref="user", lazy=True)

# ---------- Members / Parishioners ----------
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(100))
    address = db.Column(db.String(250))
    family = db.Column(db.String(150))  # optional grouping
    status = db.Column(db.String(50), default='active')  # active/inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))


# ---------- Sacraments ----------
class Sacrament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Baptism, Confirmation, Marriage
    date = db.Column(db.Date)
    certificate_path = db.Column(db.String(250))  # optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    member = db.relationship('Member', backref=db.backref('sacraments', lazy=True))

# ---------- Events / Mass ----------
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(250))
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Church Districts / Jumuiya ----------
class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    leader_name = db.Column(db.String(150))  # district leader / chairperson
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship('Member', backref='district', lazy=True)


# ---------- Donations / Tithes ----------
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), default='tithe')  # tithe / offering / pledge
    date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship('Member', backref=db.backref('donations', lazy=True))

# ---------- Announcements ----------
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.String(50),
        default='general'
    )  # general, mass, event, fundraising
    publish_date = db.Column(db.Date, default=datetime.utcnow)
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))

