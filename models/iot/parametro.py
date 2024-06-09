from models import db, Sensor

class Parametro(db.Model):
    __tablename__ = "parametro"
    id = db.Column("id", db.Integer(), primary_key=True)
    nome = db.Column("nome", db.String(255), nullable=False)
    sensor_id = db.Column("sensor_id", db.Integer(), db.ForeignKey(Sensor.id), nullable=False)
    valor = db.Column("valor", db.Float(), nullable=False, default=0.0)
    descricao = db.Column("descricao", db.String(255), nullable=True)
    
    def get_parametro():
        parametro = Parametro.query.all()
        
        return parametro
    
    def get_parametro_by_sensor_id(sensor_id):
        parametro = Parametro.query.filter(Parametro.sensor_id == sensor_id).all()
        
        return parametro
    
    # def get_parametro_by_sensor_id(sensor):
    #     parametro = Parametro.query.filter(Parametro.sensor_id == sensor.id).first()
        
    #     return parametro
    
    def deletar(id):
        parametro = Parametro.query.filter(Parametro.id == id).first()
        
        if parametro:
            db.session.delete(parametro)
            db.session.commit()
            return 'Parametro deletado com sucesso!'
        else:
            return 'Parametro não encontrado.'
        
    def save_parametro(nome, sensor_id, valor, descricao):
        parametro = Parametro(nome = nome, sensor_id = sensor_id, valor = valor, descricao = descricao)
        
        db.session.add(parametro)
        db.session.commit()


    def update_parametro(id, nome, sensor_id, valor, descricao):
        Parametro.query.filter_by(id = id)\
                .update(dict(nome = nome, sensor_id = sensor_id, valor = valor, descricao = descricao))
        
        db.session.commit()