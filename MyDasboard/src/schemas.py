from marshmallow import Schema, fields, validate

from ext import db, ma
from models.models import Device, User


def validate_no_spaces(value):
    if " " in value:
        raise ValueError("El nombre de usuartio no puede contener espacios")


class RegisterSchema(Schema):
    username = fields.String(
        required=True, validate=[validate.Length(min=3, max=40), validate_no_spaces]
    )
    email = fields.String(
        required=True,
        validate=validate.Email(error="El email no tiene un formato valido"),
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(
            min=8, error="la password debe contener al menos 8 caracteres"
        ),
    )


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class DeviceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Device
        load_instance = True
        sqla_session = db.session

    id_device = ma.auto_field(dump_only=True)
    user_id = fields.UUID(required=True, dump_only=True)
    user = fields.Nested(
        "UserSchema", only=("id_user", "user_name", "email"), dump_only=True
    )
    type_device = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    brand = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    model_device = ma.auto_field(
        required=True, validate=validate.Length(min=1, max=100)
    )
    serie_imei = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    purchase_date = ma.auto_field(required=True)
    purchase_value = fields.Float(required=True, validate=validate.Range(min=0))


register_schema = RegisterSchema()
login_schema = LoginSchema()
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)
