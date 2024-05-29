#include <DHT11.h>
#include <WiFi.h>
#include <ArduinoMqttClient.h>
#include <ArtronShop_LineNotify.h>

DHT11 dht11(7);
const int fire = A0;
int trig = 9;
int echo = 10;
int beep = 11;
int led = 12;
int homestatus = 0; // alarm off
int objstatus = 0; //object show

char ssid[]="";
char password[]="";
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
const char broker[]="broker.MQTTGO.io"; //MQTT Broker 郵局
int port = 1883;
const char topic[]="KT/home";

char token[] = "v3jiTzItqPaRN6NDPY6mzrvzXQAUXeGxDmKI6ZcUWBi";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(fire, INPUT);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(beep, OUTPUT);
  pinMode(led, OUTPUT);

  while(WiFi.begin(ssid, password) != WL_CONNECTED){
    Serial.print(".");
    delay(3000);
  }

  Serial.println("Wifi Connect!");
  Serial.println("MQTT...");
  // 判斷 MQTT 連線是否成功
  if(!mqttClient.connect(broker, port)){
    Serial.println("MQTT Fail!");
    while(1);
  }
  Serial.println("MQTT Connect!");
  Serial.println(broker);

  //設定接收的東西
  mqttClient.onMessage(onMqttMessage);
  //訂閱
  mqttClient.subscribe(topic);
  Serial.println("Wait Message...");

}

void loop() {
  // put your main code here, to run repeatedly:

  //溫溼度
  int temp = dht11.readTemperature();
  delay(1000);

  mqttClient.poll();
  LINE.begin(token);
  // 類位腳位接火焰感測器
  int sensor = analogRead(fire);
  Serial.print("Fire:");
  Serial.println(sensor);
  delay(1000);

  if (temp >= 27 && sensor <= 900){
    LINE.send("Warn!! Fire!");
  }

  //超聲波與led燈
  if (homestatus == 1){
    
    if (getDistance() < 20){
      if (objstatus == 1){
        LINE.send("Unknow Person! Please check on MQTT or camera!");
        digitalWrite(led, LOW);
      }else if (objstatus == 2){
        LINE.send("Dog Coming!");
        digitalWrite(led, HIGH);
        for (int i= 0; i <= 3; i++){
          tone(beep, 1319, 200);
          delay(100);
          tone(beep, 1319, 200);
          delay(100);
          tone(beep, 1319, 200);
          delay(400);
          tone(beep, 1047, 200);
          delay(100);
          tone(beep, 1319, 200);
          delay(100);
          tone(beep, 1586, 400);
          delay(500);
          tone(beep, 784, 400);
          delay(500);
        }
        noTone(beep);
      }else if (objstatus == 3){
        LINE.send("There is a car!");
        digitalWrite(led, HIGH);
      }else{
        digitalWrite(led, LOW);
        noTone(beep);
      }
    }else{
      digitalWrite(led, LOW);
    }
      
  }
}

void onMqttMessage(int messageSize){

  // 當MQTT可用的時候
  String msg="";
  while(mqttClient.available()){
    char word = (char)mqttClient.read();
    msg += word;
  }
  Serial.println(msg);
  int index = msg.indexOf('-');
  String device = msg.substring(0, index); // 抓到 - 之前
  String status = msg.substring(index+1);

  //Serial.println(device);
  //Serial.println(status);

  if (device=="home" && status=="on"){
    homestatus = 1;
    Serial.println("Alarm on!");
  }else if (device=="home" && status=="off"){
    homestatus = 0;
    Serial.println("Alarm off!");
  }

  if (homestatus == 1 && device=="Person"){
    homestatus = 1;
    objstatus = 1;
  }else if (homestatus == 1 && device=="Dog"){
    homestatus = 1;
    objstatus = 2;
  }else if (homestatus == 1 && device=="Car"){
    homestatus = 1;
    objstatus = 3;
  }

}

int getDistance(){
  digitalWrite(trig, LOW); // 通常會先確認關閉
  delayMicroseconds(2); // 微秒 暫停一下 ； 1秒 = 1000 毫秒，1毫秒 = 1000微秒
  digitalWrite(trig, HIGH); //發送訊號
  delayMicroseconds(10);
  digitalWrite(trig, LOW); // 關閉訊號

  unsigned long distance = pulseIn(echo, HIGH) / 58; // 公分
  Serial.print("Distance:");
  Serial.println(distance);
  return distance;
}

