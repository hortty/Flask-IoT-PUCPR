from flask import Blueprint, render_template,redirect,url_for, request
from datetime import date
from models import Parametro
from flask_login import login_required

parametro = Blueprint("parametro", __name__, template_folder='./views/', static_folder='./static/', root_path="./")

@parametro.route("/cadastro_parametro")
@login_required
def cadastro_parametro():
    return render_template("/parametro/cadastro_parametro.html")

@parametro.route("/listar_parametro", methods=["POST", "GET", "DELETE", "PUT"])
@login_required
def listar_parametro():
    parametros = Parametro.get_parametro()
    return render_template("/parametro/listar_parametro.html", parametros=parametros)

@parametro.route("/cadastrar_parametro", methods = ["POST"])
@login_required
def cadastrar_parametro():
    nome = request.form.get("nome")
    sensor_id = request.form.get("sensor_id")
    valor = request.form.get("valor")
    descricao = request.form.get("descricao")
    
    Parametro.save_parametro(nome, sensor_id, valor, descricao)

    return redirect(url_for("admin.parametro.listar_parametro"))

@parametro.route("/atualizar_parametro", methods = ["POST"])
@login_required
def atualizar_parametro():
    id = request.form.get("id")
    nome = request.form.get("nome")
    sensor_id = request.form.get("sensor_id")
    valor = request.form.get("valor")
    descricao = request.form.get("descricao")
    
    Parametro.update_parametro(id, nome, sensor_id, valor, descricao)

    return redirect("/admin/parametro/listar_parametro")
    
@parametro.route("/excluir_parametro", methods=["POST", "DELETE"])
@login_required
def excluir_parametro():
    id = request.form.get("id")
    
    Parametro.deletar(id)
    
    return redirect(url_for("admin.parametro.listar_parametro"))