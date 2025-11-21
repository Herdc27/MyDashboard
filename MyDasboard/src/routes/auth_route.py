from ext import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models.models import User
from schemas import login_schema, register_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/mydashboard/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    errors = register_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    username = data["username"]
    email = data["email"]
    password = data["password"]

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Usuario ya existe"})

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario creado correctamente"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    errors = login_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=user.id_user)
    return jsonify({"access_token": access_token}), 200
