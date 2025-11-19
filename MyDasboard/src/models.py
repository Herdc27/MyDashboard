from ext import db
import uuid
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID
from datetime import date

class Devices(db.Model):
  __tablename__ = "device"
  
  id_device = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  type_device = db.Column(db.String(100), nullablr=False)
  brand = db.Column(db.String(100), nullable=False)
  model_device = db.Column(db.String(100), nullable=False)
  serie_imei = db.Column(db.String(100), nullable=False)
  date_purchased = db.Column(db.Date, nullable=False, default=date.today )
  value_purchased = db.Column(Numeric(10,2), nullable=False)
  
  def __repr__(self) -> str:
    return f"<Emplesdo {self.id_device} - {self.brand}>"
