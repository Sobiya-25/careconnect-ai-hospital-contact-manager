
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

db = SQLAlchemy()


# =====================================================
# CONTACT MODEL - EXISTING POSTGRESQL CONTACTS TABLE
# =====================================================

class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(254),
        nullable=False
    )

    phone = db.Column(db.String(25))

    company = db.Column(db.String(150))

    category = db.Column(
        db.String(50),
        nullable=False,
        server_default="Other"
    )

    notes = db.Column(db.Text)

    hospital_name = db.Column(db.String(150))

    department = db.Column(db.String(100))

    location = db.Column(db.String(150))

    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "category": self.category,
            "notes": self.notes,
            "hospital_name": self.hospital_name,
            "department": self.department,
            "location": self.location,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }


# =====================================================
# USER MODEL - AUTHENTICATION
# =====================================================

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
        index=True
    )

    email = db.Column(
        db.String(254),
        nullable=False,
        unique=True,
        index=True
    )

    password_hash = db.Column(
        db.String(512),
        nullable=False
    )

    role = db.Column(
        db.String(30),
        nullable=False,
        server_default="member"
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        server_default=db.true()
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    # Save a secure password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password,
            method="scrypt"
        )

    # Verify the entered password
    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    # Return public user details, never the password hash
    def to_public_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }
