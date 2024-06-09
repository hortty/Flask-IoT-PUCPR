from datetime import datetime
from flask_login import login_required
from flask import Blueprint, render_template, request
import paho.mqtt.client as mqtt
import time
from models import Alarme, Sensor, Parametro
# from models import Parametro
# from models import Sensor
# from app import app

iot = Blueprint("iot", __name__, template_folder='./views/', static_folder='./static/', root_path="./")
flag_envia_parametros = True
topic_envia_parametros = "/GabrielTopicoReceberParametros"  # envia os parametros para o esp32

# Variáveis globais para temperatura e umidade atual
temperatura_atual = 0.0
umidade_atual = 0.0

# Configurações do cliente MQTT
broker_address = "broker.hivemq.com"
broker_port = 1883
topic_recebe_leituras = "/GabrielTopicoEnviarValores"
sensor_atual_id = 0
temp_min = Parametro()
temp_max = Parametro()
umid_min = Parametro()
umid_max = Parametro()

temp_min.valor = 0.0
temp_max.valor = 0.0
umid_min.valor = 0.0
umid_max.valor = 0.0

temp_min_flag = False
temp_max_flag = False
umid_min_flag = False
umid_max_flag = False

umidade_list = []
temp_list = []
time_list = []

def on_connect(client, userdata, flags, rc):
    global temp_min, temp_max, umid_min, umid_max
    
    print("Conectado ao broker MQTT.")
    client.subscribe("/GabrielTopicoReceberParametros")  # se inscrevendo no tópico

    sinal = f"{temp_min.valor} {temp_max.valor} {umid_min.valor} {umid_max.valor}"
    client.publish("/GabrielTopicoReceberParametros", sinal)  # efetuando o envio dos parâmetros
    time.sleep(1)


def on_message(client, userdata, msg):
    global flag_envia_parametros, temperatura_atual, umidade_atual, sensor_atual_id, temp_min, temp_max, umid_min, umid_max

    if sensor_atual_id != 0:
        if flag_envia_parametros:
            
            client.subscribe(topic_envia_parametros)  # topico que enviará os valores de parametro para o ESP32, que então irá saber quais são os valores de temperatura maxima, minima, umidade maxima e umidade minima
            
            sinal = f"{temp_min.valor} {temp_max.valor} {umid_min.valor} {umid_max.valor}"  # os parâmetros serão enviados sempre nessa ordem: temperatura_min, temperatura_max, umidade_min, umidade_max
            client.publish(topic_envia_parametros, sinal)  # efetuando o envio dos parâmetros
            print("Valores enviados:", sinal)
            time.sleep(1)
        else:
            client.subscribe(topic_recebe_leituras)  # tópico utilizado para receber os valores enviados do ESP32, de temperatura e umidade
            valores = msg.payload.decode().split()
            print("Valor recebido:", msg.payload)

            if(valores is None or valores[0] is None or valores[1] is None):
                flag_envia_parametros = True
                return

            temperatura_atual = float(valores[0])
            umidade_atual = float(valores[1])
            
            temp_list.append(float(valores[0])) 
            umidade_list.append(float(valores[1]))
            time_list.append(datetime.now())
            
            # with app.app_context():
            #     if(float(temperatura_atual) > temp_max or float(temperatura_atual) < temp_min):
            #         Alarme.save_alarme(sensor_atual_id, "ocorreu um problema na temperatura sistema!")
                
            #     if(float(umidade_atual) > umid_max or float(umidade_atual) < umid_min):
            #         Alarme.save_alarme(sensor_atual_id, "ocorreu um problema na umidade do sistema!")   
                
            time.sleep(0.2)
            
        if "conectado" in msg.payload.decode():
            flag_envia_parametros = False


broker_address = "broker.hivemq.com"  # Endereço do servidor MQTT
broker_port = 1883  # Porta padrão para conexão MQTT
topic_recebe_leituras = "/GabrielTopicoEnviarValores"  # Tópico para receber as leituras

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conexão ao broker MQTT
client.connect(broker_address, broker_port, 60)

@iot.route("/")
@iot.route("/interface_iot")
@login_required
def interface_iot():
    
    sensores = Sensor.get_sensor()
    
    return render_template("interface_iot.html", temperatura_atual=temperatura_atual, umidade_atual=umidade_atual, sensores=sensores)

@iot.route("/dashboard")
@login_required
def dashboard():
    
    labels = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in time_list]
    umidades = umidade_list
    temperaturas = temp_list
    
    return render_template("dashboard.html", labels=labels, umidades=umidades, temperaturas=temperaturas)
    
    

@iot.route("/dados")
@login_required
def dados():
    global temp_max_flag, temp_min_flag, umid_max_flag, umid_min_flag
    
    if(temperatura_atual > temp_max.valor and not(temp_max_flag)):
        print(temp_max.descricao)
        Alarme.save_alarme(sensor_atual_id, temp_max.descricao)
        temp_max_flag = True
        temp_min_flag = False
    elif(temperatura_atual < temp_min.valor and not(temp_min_flag)):
        print(temp_min.descricao)
        Alarme.save_alarme(sensor_atual_id, temp_min.descricao)
        temp_min_flag = True
        temp_max_flag = False
        
    if(umidade_atual > umid_max.valor and not(umid_max_flag)):
        print(umid_max.descricao)
        Alarme.save_alarme(sensor_atual_id, umid_max.descricao)
        umid_max_flag = True 
        umid_min_flag = False
    elif(umidade_atual < umid_min.valor and not(umid_min_flag)):
        print(umid_min.descricao)
        Alarme.save_alarme(sensor_atual_id, umid_min.descricao)
        umid_min_flag = True
        umid_max_flag = False
    
    return {
        'temperatura_atual': temperatura_atual,
        'umidade_atual': umidade_atual
    }

@iot.route("/atualizar-sensor", methods=["POST"])
@login_required
def atualizar_sensor():
    global sensor_atual_id, temp_min, temp_max, umid_min, umid_max
    
    sensor_atual_id = request.form.get('sensorId')
    print("sensorId: ", sensor_atual_id)
    
    parametros = Parametro.get_parametro_by_sensor_id(sensor_atual_id)
            
    for parametro in parametros:
        if "umidade" in parametro.descricao.lower():
            umid_min = parametro
            if umid_min.valor >= umid_max.valor:
                aux = umid_max 
                umid_max = umid_min 
                umid_min = aux
                
        elif "temperatura" in parametro.descricao.lower():
            temp_min = parametro
            if temp_min.valor >= temp_max.valor:
                aux = temp_max 
                temp_max = temp_min 
                temp_min = aux
    
    client.loop_start()
    client.publish("/GabrielTopicoReceberParametros", "sinal")

    return '', 204

