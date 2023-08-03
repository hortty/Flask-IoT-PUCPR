from models import db, Sensor
from datetime import datetime

class Alarme(db.Model):
    __tablename__ = "alarme"
    id = db.Column("id", db.Integer(), primary_key=True)
    sensor_id = db.Column("sensor_id", db.Integer(), db.ForeignKey(Sensor.id), nullable=False)
    descricao = db.Column("descricao", db.String(100), nullable=False, default="alarme!")
    hora = db.Column("hora", db.DateTime(), nullable=False, default=datetime.now())
    
    def get_alarme():
        alarme = Alarme.query.all()
        
        return alarme
    
    def save_alarme(sensor_id, descricao):
        alarme = Alarme(sensor_id = sensor_id, descricao = descricao)
        
        db.session.add(alarme)
        db.session.commit()