from models import *
from flask import Flask
from utils.seeds import generate_seeds

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
        generate_seeds(db)