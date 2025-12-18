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

# ---------- Members / Parishioners ----------
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(100))
    address = db.Column(db.String(250))
    family = db.Column(db.String(150))  # optional grouping
    status = db.Column(db.String(50), default='active')  # active/inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Sacraments ----------
class Sacrament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Baptism, Confirmation, Marriage
    date = db.Column(db.Date)
    certificate_path = db.Column(db.String(250))  # optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship('Member', backref=db.backref('sacraments', lazy=True))

# ---------- Events / Mass ----------
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(250))
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Attendance ----------
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    status = db.Column(db.String(50), default='present')  # present / absent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship('Event', backref=db.backref('attendances', lazy=True))
    member = db.relationship('Member', backref=db.backref('attendances', lazy=True))

# ---------- Donations / Tithes ----------
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), default='tithe')  # tithe / offering / pledge
    date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship('Member', backref=db.backref('donations', lazy=True))
