#include <Arduino.h>

#include <ESP8266WiFi.h>

#define STATUS_LED 2

const char* addr = "host.example.com";
const int port = 8888;

const char* ssid = "SSID";
const char* password = "PASSWORD";

const uint16 sampleSize = 4096;
uint16 data[sampleSize];


float smooth1 = 0;
#define SMOOTH 0.995
float smooth2 = 0;
#define SMOOTH2 0.2

float sampleCap();

void setup() {
  pinMode(STATUS_LED, OUTPUT);
  digitalWrite(STATUS_LED, HIGH);
  
  Serial.begin(9600);
  smooth1 = sampleCap();
  smooth2 = smooth1;
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid);
//  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  digitalWrite(STATUS_LED, LOW);
}


bool writeToServer(float size, float speed) {
  digitalWrite(STATUS_LED, HIGH);

  WiFiClient client;
  if (!client.connect(addr, port)) {
    digitalWrite(STATUS_LED, LOW);
    delay(500);
    digitalWrite(STATUS_LED, HIGH);
  }
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    delay(500);
    digitalWrite(STATUS_LED, LOW);
//    WiFi.mode(WIFI_OFF);
    return false;
  }

  client.printf("%f,%f\n", size, speed);
  client.stop();
  while (client.available()) {
    String line = client.readStringUntil('\n');
//    Serial.print(line);
  }
  digitalWrite(STATUS_LED, LOW);
  return true;
}


float sampleCap() {
  ets_intr_lock();
  system_adc_read_fast(data, sampleSize, 8);
  ets_intr_unlock();
  int crossCt = 0;
  for (int i = 1; i < sampleSize; i++) {
    if (data[i] < 512 && data[i-1] >= 512 || data[i] >= 512 && data[i-1] < 512 ) crossCt++;
  }
  float freq = (float)crossCt / sampleSize;
  return freq;
}

bool inPeak = false;
float peakVal = 0;
unsigned long peakTime=0;
bool haveLastPeak = false;
float lastPeak = 0;
unsigned long lastPeakTime = 0;
void loop() {
  float v1 = sampleCap();
  smooth1 = smooth1 * SMOOTH + v1 * (1.0 - SMOOTH);
  smooth2 = smooth2 * SMOOTH2 + v1 * (1.0 - SMOOTH2);
  float norm = smooth2 - smooth1;

  // 0.5 is arbitrary threshold for a peak. Looks about right visually
  if (norm > 0.008) {
//    Serial.println("Peak Start");
    inPeak = true;
  }
  else if (inPeak) {
    inPeak = false;
    if (haveLastPeak) {
//      Serial.println("Second Peak");
      float peakSize = (peakVal + lastPeak) / 2;
      // Approximate conversion to cm/s
      float peakSpeed = 5.0e6 / (peakTime - lastPeakTime);
      writeToServer(peakSize, peakSpeed);
//      Serial.printf("%f,%f\n",peakSize, peakSpeed);
//      Serial.printf("%d,%d\n",peakTime, lastPeakTime);
      haveLastPeak = false;
      
    }
    else {
//      Serial.println("First Peak");
      lastPeak = peakVal;
      lastPeakTime = peakTime;
      peakVal = 0;
      haveLastPeak = true;
    }
  }

  if (inPeak && norm > peakVal) {
    peakVal = norm;
    peakTime = micros();
//    Serial.printf("Update peak %f, %d\n", peakVal, peakTime);
  }

  if (micros() - lastPeakTime > 1000000) {
    haveLastPeak = false;
  }
  
  Serial.printf("%f\n", norm * 100.0);
  delay(5);
}
