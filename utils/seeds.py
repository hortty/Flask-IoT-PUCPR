from models import *
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def generate_seeds(db:SQLAlchemy):

    user1 = User(email = "admin@pucpr.br", username = "admin", password = generate_password_hash("admin", method='sha256'), permission = "admin")
    user2 = User(email = "gabriel@pucpr.br", username = "gabriel", password = generate_password_hash("gabriel", method='sha256'), permission = "default")
    user2 = User(email = "asd@asd", username = "asd", password = generate_password_hash("asd", method='sha256'), permission = "default")

    db.session.add_all([user1, user2])
    db.session.commit()

    sensor1 = Sensor(nome = "SensorA", tipo="temperatura")
    sensor2 = Sensor(nome = "SensorB", tipo="umidade")

    db.session.add_all([sensor1, sensor2])
    db.session.commit()

    alarme1 = Alarme(sensor_id = 1, descricao = "Temperatura alta", hora = datetime.today())

    db.session.add_all([alarme1])
    db.session.commit()

    parametro1 = Parametro(nome = "Temperatura máxima", sensor_id = 1, valor = 40, descricao = "temperatura muito alta!")
    parametro2 = Parametro(nome = "Temperatura mínima", sensor_id = 1, valor = -5, descricao = "temperatura muito baixa!")
    parametro3 = Parametro(nome = "Umidade máxima", sensor_id = 1, valor = 80, descricao = "umidade muito alta!")
    parametro4 = Parametro(nome = "Umidade mínima", sensor_id = 1, valor = 0, descricao = "umidade muito baixa!")
    
    parametro5 = Parametro(nome = "Temperatura máxima", sensor_id = 2, valor = 50, descricao = "temperatura  alta!")
    parametro6 = Parametro(nome = "Temperatura mínima", sensor_id = 2, valor = 0, descricao = "temperatura  baixa!")
    parametro7 = Parametro(nome = "Umidade máxima", sensor_id = 2, valor = 40, descricao = "umidade  alta!")
    parametro8 = Parametro(nome = "Umidade mínima", sensor_id = 2, valor = 10, descricao = "umidade  baixa!")
    
    db.session.add_all([parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7, parametro8])
    db.session.commit()
    
    