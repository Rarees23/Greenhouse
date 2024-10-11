#include "Display.h"
#include <DHT.h>
#include <ArduinoJson.h>  // Include the ArduinoJson library

#define DHTTYPE DHT11

const int sensorPin = A0; 
const int humidityin = 2;
const int DHTPIN = 12;
const int lightPin = 16;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Read sensor data
  int humidity = dht.readHumidity();
  int lightlvl = analogRead(lightPin);
  int sensorValue = analogRead(sensorPin);
  
  // Convert analog value to voltage and then to temperature in Celsius
  float voltage = sensorValue * (5.0 / 1023.0); 
  int temperatureC = voltage * 10.0; 
  
  // Create a JSON object
  StaticJsonDocument<200> doc;  
  doc["timestamp"] = millis(); 
  doc["humidity"] = humidity;
  doc["light_level"] = lightlvl;
  doc["temperature"] = temperatureC;

  // Serialize JSON to string
  String output;
  serializeJson(doc, output);

  // Send the JSON string over serial
  Serial.println(output);
  
  delay(1000);  // Send data every second
}
