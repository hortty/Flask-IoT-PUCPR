from models import db
# from models.iot.parametro import Parametro

class Sensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column("id",  db.Integer(), primary_key=True)
    nome = db.Column("nome", db.String(255), nullable=False, unique=True)
    tipo = db.Column("tipo", db.String(255), nullable=False) 
    parametros = db.relationship("Parametro", backref="sensor", cascade="all, delete-orphan")
    alarme = db.relationship("Alarme", backref="sensor", cascade="all, delete-orphan")

    def save_sensor(nome, tipo):
        sensor = Sensor(nome = nome, tipo = tipo)
        
        db.session.add(sensor)
        db.session.commit()
        
    def get_sensor():
        sensor = Sensor.query.all()
        
        return sensor

    def deletar(id):
        sensor = Sensor.query.filter(Sensor.id == id).first()

        # parametro = Parametro.get_parametro_by_sensor_id(sensor)
        
        # if parametro:
        #     parametro = Parametro.deletar(parametro.id)
        
        if sensor:
            db.session.delete(sensor)
            db.session.commit()
            return 'Sensor deletado com sucesso!'
        else:
            return 'Sensor não encontrado.'

    def update_sensor(id, nome, tipo):
        Sensor.query.filter_by(id = id)\
                .update(dict(nome = nome, tipo = tipo))
        
        db.session.commit()