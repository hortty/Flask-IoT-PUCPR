from flask import Blueprint, render_template,redirect,url_for, request
from datetime import date
from models import Sensor
from flask_login import login_required

sensor = Blueprint("sensor", __name__, template_folder='./views/', static_folder='./static/', root_path="./")

@sensor.route("/cadastro_sensor")
@login_required
def cadastro_sensor():
    return render_template("/sensor/cadastro_sensor.html")

@sensor.route("/listar_sensor", methods=["POST", "GET", "DELETE", "PUT"])
@login_required
def listar_sensor():
    sensores = Sensor.get_sensor()
    return render_template("/sensor/listar_sensor.html", sensores=sensores)

@sensor.route("/cadastrar_sensor", methods = ["POST"])
@login_required
def cadastrar_sensor():
    nome = request.form.get("nome")
    tipo = request.form.get("tipo")
    
    Sensor.save_sensor(nome, tipo)

    return redirect(url_for("admin.sensor.listar_sensor"))

@sensor.route("/atualizar_sensor", methods = ["POST"])
@login_required
def atualizar_sensor():
    id = request.form.get("id")
    nome = request.form.get("nome")
    tipo = request.form.get("tipo")
    
    Sensor.update_sensor(id, nome, tipo)

    return redirect("/admin/sensor/listar_sensor")
    
@sensor.route("/excluir_sensor", methods=["POST", "DELETE"])
@login_required
def excluir_sensor():
    id = request.form.get("id")
    
    Sensor.deletar(id)
    
    return redirect(url_for("admin.sensor.listar_sensor"))