from ext import db
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from models.models import Device
from schemas import device_schema, devices_schema
from utils.auth_middleware import token_required

from . import api


class Devices(Resource):
    @token_required
    def get(self, current_user):
        devices = Device.query.order_by(Device.id_device.asc()).all()
        return devices_schema.dump(devices), 200

    @token_required
    def post(self, current_user):
        data = request.get_json()
        if not data:
            return {"message":"Cuerpo JSON requerido"}, 400
        try:
            device = device_schema.load(data)
            device.user_id = current_user.id_user
        except ValidationError as err:
            return {"error": err.messages}, 422

        db.session.add(device)
        db.session.commit()
        return device_schema.dump(device), 201


class DeviceDetail(Resource):
    @token_required
    def get(self, id_device, current_user):
        device = Device.query.get_or_404(id_device)
        return device_schema.dump(device), 200

    @token_required
    def put(self, id_device, current_user):
        device = Device.query.get_or_404(id_device)
        data = request.get_json()
        if not data:
            return {"message": "Cuerpo JSON requerido"}, 400
        try:
            data.pop('user_id', None)
            device = device_schema.load(data, instance=device, partial=False)
            device.user_id = current_user.id_user
        except ValidationError as err:
            return {"error": err.messages}, 422
        db.session.add(device)
        db.session.commit()
        return device_schema.dump(device), 200

    @token_required
    def delete(self, id_device, current_user):
        device = Device.query.get_or_404(id_device)
        db.session.delete(device)
        db.session.commit()
        return {"message": "Device Eliminado"}, 200


api.add_resource(Devices, "/devices", endpoint="devices")
api.add_resource(DeviceDetail, "/devices/<uuid:id_device>")



