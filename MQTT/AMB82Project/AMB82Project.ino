/*
 發現畫面中有人，就傳MQTT紀錄
 請將此檔案，覆蓋原本的ObjectDetectionCallback.ino
 本修改的地方說明：
 1. VideoSetting config(1024, 768, 30, VIDEO_H264_JPEG, 1); 使用800x600，格式是VIDEO_H264_JPEG
                 若要傳Line，則必須使用800x600
 2. 將MQTT的副程式複製到後方
 3. 在ODPostProcess新增變數personCount計算人數，當人數>=1時，就傳MQTT

 Example guide:
 https://www.amebaiot.com/en/amebapro2-arduino-neuralnework-object-detection/

 NN Model Selection
 Select Neural Network(NN) task and models using .modelSelect(nntask, objdetmodel, facedetmodel, facerecogmodel).
 Replace with NA_MODEL if they are not necessary for your selected NN Task.

 NN task
 =======
 OBJECT_DETECTION/ FACE_DETECTION/ F/Users/kate/Desktop/obDetectMQTT/ObjectClassList.hACE_RECOGNITION

 Models
 =======
 YOLOv3 model         DEFAULT_YOLOV3TINY   / CUSTOMIZED_YOLOV3TINY
 YOLOv4 model         DEFAULT_YOLOV4TINY   / CUSTOMIZED_YOLOV4TINY
 YOLOv7 model         DEFAULT_YOLOV7TINY   / CUSTOMIZED_YOLOV7TINY
 SCRFD model          DEFAULT_SCRFD        / CUSTOMIZED_SCRFD
 MobileFaceNet model  DEFAULT_MOBILEFACENET/ CUSTOMIZED_MOBILEFACENET
 No model             NA_MODEL
 */

#include "WiFi.h"
#include "StreamIO.h"
#include "VideoStream.h"
#include "RTSP.h"
#include "NNObjectDetection.h"
#include "VideoStreamOverlay.h"
#include "ObjectClassList.h"
#include <PubSubClient.h>  //請先安裝PubSubClient程式庫

#define CHANNEL 0
#define CHANNELNN 3

// Lower resolution for NN processing
#define NNWIDTH 576
#define NNHEIGHT 320

VideoSetting config(800, 600, 30, VIDEO_H264_JPEG, 1);
VideoSetting configNN(NNWIDTH, NNHEIGHT, 10, VIDEO_RGB, 0);
NNObjectDetection ObjDet;

RTSP rtsp;
StreamIO videoStreamer(1, 1);
StreamIO videoStreamerNN(1, 1);

char ssid[] = "";         // your network SSID (name)
char pass[] = "";  // your network password
int status = WL_IDLE_STATUS;

IPAddress ip;
int rtsp_portnum;

char* MQTTServer = "mqttgo.io";                      //免註冊MQTT伺服器
int MQTTPort = 1883;                                 //MQTT Port
char* MQTTUser = "";                                 //不須帳密
char* MQTTPassword = "";                             //不須帳密
char* MQTTPubTopic1 = "KT/home/video";  //推播主題1:即時影像
char* MQTTPubTopic2 = "KT/home";
long MQTTLastPublishTime;                            //此變數用來記錄推播時間
long MQTTPublishInterval = 100;                      //每1秒推撥4-5次影像
WiFiClient WifiClient;
PubSubClient MQTTClient(WifiClient);

void setup() {
  Serial.begin(115200);

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);

    // wait 2 seconds for connection:
    delay(2000);
  }
  ip = WiFi.localIP();

  // Configure camera video channels with video format information
  // Adjust the bitrate based on your WiFi network quality
  config.setBitrate(2 * 1024 * 1024);  // Recommend to use 2Mbps for RTSP streaming to prevent network congestion
  Camera.configVideoChannel(CHANNEL, config);
  Camera.configVideoChannel(CHANNELNN, configNN);
  Camera.videoInit();

  // Configure RTSP with corresponding video format information
  rtsp.configVideo(config);
  rtsp.begin();
  rtsp_portnum = rtsp.getPort();

  // Configure object detection with corresponding video format information
  // Select Neural Network(NN) task and models
  ObjDet.configVideo(configNN);
  ObjDet.setResultCallback(ODPostProcess);
  ObjDet.modelSelect(OBJECT_DETECTION, DEFAULT_YOLOV4TINY, NA_MODEL, NA_MODEL);
  ObjDet.begin();

  // Configure StreamIO object to stream data from video channel to RTSP
  videoStreamer.registerInput(Camera.getStream(CHANNEL));
  videoStreamer.registerOutput(rtsp);
  if (videoStreamer.begin() != 0) {
    Serial.println("StreamIO link start failed");
  }

  // Start data stream from video channel
  Camera.channelBegin(CHANNEL);

  // Configure StreamIO object to stream data from RGB video channel to object detection
  videoStreamerNN.registerInput(Camera.getStream(CHANNELNN));
  videoStreamerNN.setStackSize();
  videoStreamerNN.setTaskPriority();
  videoStreamerNN.registerOutput(ObjDet);
  if (videoStreamerNN.begin() != 0) {
    Serial.println("StreamIO link start failed");
  }

  // Start video channel for NN
  Camera.channelBegin(CHANNELNN);

  // Start OSD drawing on RTSP video channel
  OSD.configVideo(CHANNEL, config);
  OSD.begin();
  MQTTConnecte();
}

void loop() {
  // Do nothing
}

// User callback function for post processing of object detection results
void ODPostProcess(std::vector<ObjectDetectionResult> results) {
  uint16_t im_h = config.height();
  uint16_t im_w = config.width();

  Serial.print("Network URL for RTSP Streaming: ");
  Serial.print("rtsp://");
  Serial.print(ip);
  Serial.print(":");
  Serial.println(rtsp_portnum);
  Serial.println(" ");

  printf("Total number of objects detected = %d\r\n", ObjDet.getResultCount());
  OSD.createBitmap(CHANNEL);
  int personCount = 0;
  int dogCount = 0;
  int carCount = 0;
  if (ObjDet.getResultCount() > 0) {
    for (uint32_t i = 0; i < ObjDet.getResultCount(); i++) {
      int obj_type = results[i].type();
      if (itemList[obj_type].filter) {  // check if item should be ignored
        if (obj_type == 0) personCount++;
        if (obj_type == 2) carCount++;
        if (obj_type == 16) dogCount++;
        ObjectDetectionResult item = results[i];
        // Result coordinates are floats ranging from 0.00 to 1.00
        // Multiply with RTSP resolution to get coordinates in pixels
        int xmin = (int)(item.xMin() * im_w);
        int xmax = (int)(item.xMax() * im_w);
        int ymin = (int)(item.yMin() * im_h);
        int ymax = (int)(item.yMax() * im_h);

        // Draw boundary box
        printf("Item %d %s:\t%d %d %d %d\n\r", i, itemList[obj_type].objectName, xmin, xmax, ymin, ymax);
        OSD.drawRect(CHANNEL, xmin, ymin, xmax, ymax, 3, OSD_COLOR_WHITE);

        // Print identification text
        char text_str[20];
        snprintf(text_str, sizeof(text_str), "%s %d", itemList[obj_type].objectName, item.score());
        OSD.drawText(CHANNEL, xmin, ymin - OSD.getTextHeight(CHANNEL), text_str, OSD_COLOR_CYAN);

      }
    }
  }
  
  OSD.update(CHANNEL);
  
  if (personCount >= 1) {
    MQTTConnecte();
    Serial.println(SendImageMQTT());
    const char msg[] = "Person";
    MQTTClient.publish(MQTTPubTopic2, msg);
  }else if (carCount >= 1){
    MQTTConnecte();
    Serial.println(SendImageMQTT());
    const char msg[] = "Car";
    MQTTClient.publish(MQTTPubTopic2, msg);
  }else if (dogCount >= 1){
    MQTTConnecte();
    Serial.println(SendImageMQTT());
    const char msg[] = "Dog";
    MQTTClient.publish(MQTTPubTopic2, msg);
  }
  delay(1000);
  

}

String SendImageMQTT() {
  int buf = 8192;
  uint32_t img_addr = 0;
  uint32_t img_len = 0;
  Camera.getImage(CHANNEL, &img_addr, &img_len);
  //int ps = 512;
  //開始傳遞影像檔，批次傳檔案
  MQTTClient.beginPublish(MQTTPubTopic1, img_len, false);

  uint8_t* fbBuf = (uint8_t*)img_addr;
  size_t fbLen = img_len;
  for (size_t n = 0; n < fbLen; n = n + buf) {
    if (n + buf < fbLen) {
      MQTTClient.write(fbBuf, buf);
      fbBuf += buf;
    } else if (fbLen % buf > 0) {
      size_t remainder = fbLen % buf;
      MQTTClient.write(fbBuf, remainder);
    }
  }
  boolean isPublished = MQTTClient.endPublish();
  if (isPublished) return "MQTT傳輸成功";
  else return "MQTT傳輸失敗，請檢查網路設定";
}

void MQTTConnecte() {
  //MQTTClient.setCallback(MQTTCallback);
  while (!MQTTClient.connected()) {
    //以亂數為ClientID
    MQTTClient.setServer(MQTTServer, MQTTPort);
    String MQTTClientid = "esp32-" + String(random(1000000, 9999999));
    if (MQTTClient.connect(MQTTClientid.c_str(), MQTTUser, MQTTPassword)) {
      //連結成功，顯示「已連線」。
      Serial.println("MQTT已連線");
      //訂閱SubTopic1主題
      MQTTClient.subscribe(MQTTPubTopic1);
    } else {
      //若連線不成功，則顯示錯誤訊息，並重新連線
      Serial.print("MQTT連線失敗,狀態碼=");
      Serial.println(MQTTClient.state());
      Serial.println("五秒後重新連線");
      delay(5000);
    }
  }
}


