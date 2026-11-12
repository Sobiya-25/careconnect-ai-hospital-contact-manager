
import re
import secrets

from flask import request, session
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, validate
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError

from models import db, User


auth_blp = Blueprint(
    "Authentication",
    __name__,
    url_prefix="/api/auth",
    description="Registration, login and member sessions",
)


# =====================================================
# REQUEST AND RESPONSE SCHEMAS
# =====================================================

class RegisterSchema(Schema):
    full_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=120),
    )

    username = fields.Str(
        required=True,
        validate=validate.Regexp(
            r"^[A-Za-z0-9_]{3,50}$"
        ),
    )

    email = fields.Email(required=True)

    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=12, max=128),
    )


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserSchema(Schema):
    id = fields.Int()
    full_name = fields.Str()
    username = fields.Str()
    email = fields.Email()
    role = fields.Str()
    is_active = fields.Bool()


class AuthResponseSchema(Schema):
    message = fields.Str()
    user = fields.Nested(UserSchema)


class CSRFResponseSchema(Schema):
    csrf_token = fields.Str()


class MessageSchema(Schema):
    message = fields.Str()


# =====================================================
# CSRF SECURITY
# =====================================================

CSRF_HEADER = [
    {
        "in": "header",
        "name": "X-CSRF-Token",
        "required": True,
        "schema": {"type": "string"},
        "description": (
            "Token obtained from GET /api/auth/csrf"
        ),
    }
]


def get_csrf_token():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_hex(32)

    return session["_csrf"]


def verify_csrf():
    expected = session.get("_csrf", "")
    provided = request.headers.get(
        "X-CSRF-Token", ""
    )

    if (
        not expected
        or not provided
        or not secrets.compare_digest(
            expected, provided
        )
    ):
        abort(403, message="Invalid CSRF token")


# =====================================================
# GET CSRF TOKEN
# =====================================================

@auth_blp.route("/csrf", methods=["GET"])
@auth_blp.response(200, CSRFResponseSchema)
def get_token():
    """Get the CSRF token for authentication requests."""
    return {"csrf_token": get_csrf_token()}


# =====================================================
# REGISTER
# =====================================================

@auth_blp.route("/register", methods=["POST"])
@auth_blp.doc(parameters=CSRF_HEADER)
@auth_blp.arguments(RegisterSchema)
@auth_blp.response(201, AuthResponseSchema)
def register_member(data):
    """Create a new member account."""
    verify_csrf()

    full_name = data["full_name"].strip()
    username = data["username"].strip().lower()
    email = data["email"].strip().lower()
    password = data["password"]

    if not 2 <= len(full_name) <= 120:
        abort(400, message="Invalid full name")

    if not re.fullmatch(
        r"[a-z0-9_]{3,50}", username
    ):
        abort(400, message="Invalid username")

    if not 12 <= len(password) <= 128:
        abort(400, message="Invalid password length")

    existing = db.session.execute(
        db.select(User).where(
            or_(
                func.lower(User.username) == username,
                func.lower(User.email) == email,
            )
        )
    ).scalar_one_or_none()

    if existing is not None:
        abort(
            409,
            message="Username or email already registered",
        )

    new_user = User(
        full_name=full_name,
        username=username,
        email=email,
        role="member",
        is_active=True,
    )

    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        abort(
            409,
            message="Username or email already registered",
        )

    return {
        "message": "Account created successfully. Please login.",
        "user": new_user.to_public_dict(),
    }


# =====================================================
# LOGIN
# =====================================================

@auth_blp.route("/login", methods=["POST"])
@auth_blp.doc(parameters=CSRF_HEADER)
@auth_blp.arguments(LoginSchema)
@auth_blp.response(200, AuthResponseSchema)
def login_member(data):
    """Login with username and password."""
    verify_csrf()

    username = data["username"].strip().lower()
    password = data["password"]

    user = db.session.execute(
        db.select(User).where(
            func.lower(User.username) == username
        )
    ).scalar_one_or_none()

    if (
        user is None
        or not user.check_password(password)
    ):
        abort(
            401,
            message="Invalid username or password",
        )

    if not user.is_active:
        abort(403, message="Account is disabled")

    session.clear()

    if not login_user(user, remember=False, fresh=True):
        abort(403, message="Login not permitted")

    session.permanent = True
    get_csrf_token()

    return {
        "message": "Login successful",
        "user": user.to_public_dict(),
    }


# =====================================================
# CURRENT USER
# =====================================================

@auth_blp.route("/me", methods=["GET"])
@auth_blp.response(200, UserSchema)
@login_required
def get_current_member():
    """Return the currently authenticated member."""
    return current_user.to_public_dict()


# =====================================================
# LOGOUT
# =====================================================

@auth_blp.route("/logout", methods=["POST"])
@auth_blp.doc(parameters=CSRF_HEADER)
@auth_blp.response(200, MessageSchema)
@login_required
def logout_member():
    """Logout from CareConnect AI."""
    verify_csrf()

    logout_user()
    session.clear()

    return {
        "message": "Logged out successfully"
    }
