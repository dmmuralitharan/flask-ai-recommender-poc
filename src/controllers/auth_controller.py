from datetime import datetime, timezone
import bcrypt
from src import db
from flask import jsonify, request
from src.models.user_model import User
from src.utils.jwt import generate_jwt_token


def register_controller():

    try:

        data = request.get_json()

        email = data.get("email")
        name = data.get("name")
        password = data.get("password")
        role = data.get("role", "user")

        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "User already exists", "status": 2})

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = User(
            email=email,
            name=name,
            password_hash=hashed_password.decode("utf-8"),
            role=role,
            last_login=datetime.now(timezone.utc),
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully", "status": 1}), 201

    except Exception as e:
        db.session.rollback()
        return (jsonify({"status": 0, "error": str(e)}), 500)


def login_controller():

    try:

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return (
                jsonify({"message": "email and password required", "status": 0}),
                400,
            )

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        ):
            return jsonify({"message": "Invalid credentials", "status": 0})

        access_token = generate_jwt_token(user.id)

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "last_login": user.last_login.isoformat(),
                    "status": 1,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (jsonify({"status": 0, "error": str(e)}), 500)
