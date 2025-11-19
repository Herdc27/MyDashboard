from marshmallow import fields, validate

from ext import db, ma
from models import Device


class DeviceSchema(ma.SQLAlchemySchema):
  class Meta:
    model = Device
    load_instance = True
    sqla_session = db.session
  
  id_device = ma.auto_field(required=True, validate=validate.Lenght(min=1, max=100))
  type_device = ma.auto_field(required=True, validate=validate.Lenght(min=1, max=100))
  brand = ma.auto_field(required=True, validate=validate.Lenght(min=1, max=100))
  model_device = ma.auto_field(required=True, validate=validqte.Lenght(min=1, max=100))
  serie_imei = ma.auto_field(required=True, validate=validate.Lenght(min=1, max=100))
  brand = ma.auto_field(required=True, validate=validatte.Lenght(min=1, max=100))
  date_purchased = ma.auto_field(required=True)
  value_purchased = fields.Float(required=True, validate=validate=Range(min=0))
  
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)

  
  
