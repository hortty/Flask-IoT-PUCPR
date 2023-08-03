from flask import Blueprint, render_template, redirect,url_for
from flask_login import current_user, login_required
from controllers.sensor_controller import sensor
from controllers.alarme_controller import alarme
from controllers.parametro_controller import parametro
from controllers.iot_controller import iot

admin = Blueprint("admin", __name__, 
                    template_folder="./views/", 
                    static_folder='./static/', 
                    root_path="./")

admin.register_blueprint(sensor, url_prefix='/sensor')
admin.register_blueprint(alarme, url_prefix='/alarme')
admin.register_blueprint(parametro, url_prefix='/parametro')
admin.register_blueprint(iot, url_prefix='/iot')

@admin.route("/")
@admin.route("/admin")
@login_required
def admin_index():
    # """
    # if not current_user.is_authenticated:
    #     return redirect(url_for("auth.login"))
    # else:
    #     return render_template("admin/admin_base.html", name = current_user.name)
    # """
    return redirect(url_for("admin.iot.interface_iot"))
    
    