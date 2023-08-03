from flask import Blueprint, render_template,redirect,url_for, request
from datetime import date
from models import Alarme
from flask_login import login_required

alarme = Blueprint("alarme", __name__, template_folder='./views/', static_folder='./static/', root_path="./")

@alarme.route("/listar_alarme")
@login_required
def listar_alarme():
    alarmes = Alarme.get_alarme()
    return render_template("/alarme/listar_alarme.html", alarmes=alarmes)