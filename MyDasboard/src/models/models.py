from datetime import date
from enum import unique

from ext import db
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = "user"

    id_user = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text("uuid_generate_v4()"),
    )
    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Device(db.Model):
    __tablename__ = "device"

    id_device = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text("uuid_generate_v4()"),
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("user.id_user", ondelete="CASCADE"),
        nullable=False,
    )
    type_device = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model_device = db.Column(db.String(100), nullable=False)
    serie_imei = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_value = db.Column(Numeric(10, 2), nullable=False)

    def __repr__(self) -> str:
        return f"<Emplesdo {self.id_device} - {self.brand}>"
