from datetime import datetime
from app.extensions import db

# ---------- User / Roles ----------
class User(db.Model):
    __tablename__ = 'user'  # Explicitly set table name
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='member')  # Changed default to 'member'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sacraments = db.relationship("Sacrament", backref="user", lazy=True)
    member = db.relationship("Member", back_populates="user", uselist=False)

# ---------- Members / Parishioners ----------
class Member(db.Model):
    __tablename__ = 'member'  # Explicitly set table name
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(100))
    address = db.Column(db.String(250))
    family = db.Column(db.String(150))  # optional grouping
    status = db.Column(db.String(50), default='active')  # active/inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),  # FIXED: Changed from "users.id" to "user.id"
        unique=True,
        nullable=True
    )
    # 🔐 CLAIM CODE (NEW)
    claim_code = db.Column(db.String(64), unique=True, nullable=True)
    claim_code_expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship("User", back_populates="member")


# ---------- Sacraments ----------
class Sacrament(db.Model):
    __tablename__ = 'sacrament'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Baptism, Confirmation, Marriage
    date = db.Column(db.Date)
    certificate_path = db.Column(db.String(250))  # optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    member = db.relationship('Member', backref=db.backref('sacraments', lazy=True))

# ---------- Events / Mass ----------
class Event(db.Model):
    __tablename__ = 'event'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(250))
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Church Districts / Jumuiya ----------
class District(db.Model):
    __tablename__ = 'district'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    leader_name = db.Column(db.String(150))  # district leader / chairperson
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship('Member', backref='district', lazy=True)


# ---------- Donations / Tithes ----------
class Donation(db.Model):
    __tablename__ = 'donation'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), default='tithe')  # tithe / offering / pledge
    date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship('Member', backref=db.backref('donations', lazy=True))

# ---------- Announcements ----------
class Announcement(db.Model):
    __tablename__ = 'announcement'
    
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