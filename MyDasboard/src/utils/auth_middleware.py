from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required
from models.models import User


def token_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        id_user = get_jwt_identity()
        user = User.query.get(id_user)
        if not user:
            return {"message": "Usuario no encontrado"}, 401
        return fn(current_user=user, *args, **kwargs)

    return wrapper
