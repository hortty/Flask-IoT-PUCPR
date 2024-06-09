from models import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column("id",  db.Integer(), primary_key=True)
    username = db.Column("username",  db.String(30), nullable=False, unique=True)
    email = db.Column("email", db.String(30), nullable=False, unique=True)
    password = db.Column("password", db.String(1024), nullable=False) 
    permission = db.Column("permission", db.String(255), nullable=True) 
    
    def save_user(username, email, password, permission):
        user = User(username = username, email = email, password = password, permission = permission)
        
        db.session.add(user)
        db.session.commit()