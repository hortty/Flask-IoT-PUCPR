#include <WiFi.h>
#include "PubSubClient.h"
#include "NewPing.h"
#include "DHT.h"
#include <string.h>

//Conexão com o WiFI
const char *SSID = "Wokwi-GUEST";
const char *PWD = "";

//configurações de pinos de hardware
#define DHTPIN 4     // Pino de dados do sensor DHT
#define DHTTYPE DHT22   // Tipo do sensor DHT (DHT22)
#define led_verde 2
#define led_vermelho 12
DHT dht(DHTPIN, DHTTYPE); // Config do DHT

//range de valores sensor
float temp_min = 0;
float temp_max = 0;
float umid_min = 0;
float umid_max = 0;

// variavel para analisar se o dispositivo foi conectado
bool conectado = false;

//configurações de conexão MQTT
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 
char *mqttServer = "broker.hivemq.com";
int mqttPort = 1883;
char payload[50];

// tópico utilizado para receber os parâmetros que virão do Python, que são: temperatura máxima, temperatura minima, umidade maxima, umidade minima
char topico_receber_parametros[] = "/GabrielTopicoReceberParametros";

// tópico utilizado para enviar valores das leituras de temperatura e umidade de volta para o Python
char topico_enviar_valores[] = "/GabrielTopicoEnviarValores";

//função para conectar ao WiFi
void ConectaNoWiFi() {
  Serial.print("Conectando ao WiFi");
  WiFi.begin(SSID, PWD);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.print("Conectado.");
}

// configurações do MQTT 
void setupMQTT() {
  mqttClient.setServer(mqttServer, mqttPort);
}


//A função callback é responsável por receber as msgs. Toda vez que uma nova msg chega, a função será ativada.  
void callback(char* topic, byte* payload, unsigned int length) {

  if(!conectado)
  {
    //Se a msg chega do tópico “/GabrielTopicoReceberParametros ela chega aqui.  
    if (strcmp(topic, topico_receber_parametros)==0) {

      // lendo dados recebidos do tópico
      char dadosChar[length];
      for (int i = 0; i < length; i++) {
          dadosChar[i] = ((char)payload[i]);
      }

      // utilizados para receber o payload
      char *token;
      char *arrayValores[4];
      int i=0;
      
      // separando esses valores, por cada "espaço" presente no array de char
      token = strtok(dadosChar, " ");
      
      // armazenar os valores no array
      while (token != NULL && i < 4) {
          arrayValores[i] = token;
          token = strtok(NULL, " ");
          i++;
      }

      //a função atof() converte char em float.
      temp_min = atof(arrayValores[0]);
      temp_max = atof(arrayValores[1]);
      umid_min = atof(arrayValores[2]);
      umid_max = atof(arrayValores[3]);

      Serial.println(temp_min);
      Serial.println(temp_max);
      Serial.println(umid_min);
      Serial.println(umid_max);

      // envia um valor, para o Python saber que é necessário parar o envio de dados do parâmetro
      mqttClient.publish(topico_receber_parametros, "conectado");
      delay(5000); 
      conectado = true;
    }
  }
}


//Realiza a conceção com o Broker MQTT 
void conectaBrokerMQTT() {
  Serial.println("Conectando ao broker");
  //A função mqttClient.connected() verifica se existe uma conexão ativa.  Depende do Broker, a conexão pode se manter ativa, ou desativar a cada envio de msg.  
  while (!mqttClient.connected()) {
      //Se entrou aqui, é porque não está conectado. Então será feito uma tentativa de conexão infinita, até ser conectado.  
      Serial.println("Conectando ao Broker MQTT");
      //define o nome da ESP na conexão. Está sendo gerado um nome aleatório, para evitar ter duas ESPs com o mesmo nome. Neste caso, uma derrubaria a outra.  
      String clientId = "ESP32Client-";
      clientId += String(random(0xffff), HEX);
      //Realiza a conexão com a função “mqttClient.connect”. Caso seja um sucesso, entra no if e imprime “Conectado ao Broker MQTT.” 
      if (mqttClient.connect(clientId.c_str())) {
        Serial.println("Conectado ao Broker MQTT.");
      }
  }
}

//setup
void setup() {
  Serial.begin(9600);
  pinMode(led_verde, OUTPUT);
  pinMode(led_vermelho, OUTPUT);
  ConectaNoWiFi();
  setupMQTT();
}

//loop
void loop() {

  //Verifica se a conexão está ativa, caso não esteja, tenta conectar novamente.  
  if (!mqttClient.connected()){
      // conexão ao broker
      conectaBrokerMQTT();
      //Define quais tópicos vão ser assinados, ou seja, toda vez que alguma informação chegar destes tópicos, receberemos a informação.  
      // esse tópico está sendo utilizado para receber os parâmetros do Python, de umidade e temperatura
      mqttClient.subscribe(topico_receber_parametros);
      //Define o nome da função que será o callback, ou seja, toda vez que uma novo msg chegar de um dos tópicos, ela será enviada para a função ‘callback’ 
      mqttClient.setCallback(callback);
  }
      
  //realiza o sincronismo com o Broker, por exemplo, verifica se existem msgs para ler se estiver inscrito em algum tópico 
  mqttClient.loop();

    // primeiro os ranges precisam estar definidos pela informação que vêm do python, para só então
    // podermos validar se aqueles valores são permitidos ou não!
    if(temp_min != 0 || temp_max != 0 || umid_min != 0 || umid_max != 0)
    {
      // leitura da temperatura, utilizando o dht que foi inicializado lá na parte de cima do código
      float temperatura = dht.readTemperature();
      // leitura da umidade, utilizando o dht que foi inicializado lá na parte de cima do código
      float umidade = dht.readHumidity();

      // só podemos publicar char[], então fazemos a conversão e guardamos no paylod
      sprintf(payload, "%.2f %.2f", temperatura, umidade);
      // finalmente, publicamos os valores no tópico "GabrielTopicoEnviarValores", onde será recebido no Python
      mqttClient.publish(topico_enviar_valores, payload);

      Serial.println("\n\n");
      Serial.print("Temperatura: ");
      Serial.print(temperatura);
      Serial.println(" °C");
      
      Serial.print("Umidade: ");
      Serial.print(umidade);
      Serial.println(" %");

      Serial.print("Temperatura minima: ");
      Serial.println(temp_min);
      Serial.print("Temperatura maxima: ");
      Serial.println(temp_max);
      Serial.print("Umidade minima: ");
      Serial.println(umid_min);
      Serial.print("Umidade maxima: ");
      Serial.println(umid_max);

      // quando a umidade estiver dentro do valor minimo e maximo, e a temperatura tambem estiver dentro do
      //  valor minimo e maximo, entao o led_verde é acesso, caso contrário, o led_vermelho é acesso indicando
      //    que os valores lidos de umidade e temperatura estão fora da faixa necessária
      if((umidade > umid_min && umidade < umid_max) 
      && (temperatura > temp_min && temperatura < temp_max))
      {
        digitalWrite(led_vermelho, LOW);
        digitalWrite(led_verde, HIGH);
      }
      else 
      {
        digitalWrite(led_vermelho, HIGH);
        digitalWrite(led_verde, LOW);
      }
    }

  delay(500); 

}
