#include "Display.h"
#include <DHT.h>

#define DHTTYPE DHT11

const int sensorPin = A0;//tempreture sensor
const int button1in=8;
const int humidityin=2;
const int DHTPIN=12;
const int lightPin=16;

int ok=0;
int temperatureC;
int lightlvl=0;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  pinMode(button1in,INPUT_PULLUP);
  dht.begin();
}

void loop() {

  int button1 = digitalRead(button1in);// Read the analog value from the sensor (0 to 1023) 
  int humidity = dht.readHumidity();
  lightlvl = analogRead(lightPin);
  int sensorValue= dht.readTemperature(sensorPin);

  
  float voltage = sensorValue * (5.0 / 1023.0);// Convert the analog value to voltage (assuming 5V power)
  temperatureC = voltage * 10.0; // Convert the voltage to temperature in Celsius (LM35 gives 10mV per °C)

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(", Light Level: ");
  Serial.print(lightlvl);
  Serial.print(", Tempreture: ");
  Serial.println(temperatureC);

  Display.show(0);
  if(button1==LOW) ok=1;
  while(ok==1)
  {
    sensorValue= dht.readTemperature(sensorPin);
    voltage = sensorValue * (5.0 / 1023.0);
    temperatureC = voltage * 10.0;

    Display.show(temperatureC);

    delay(200);
    button1=digitalRead(button1in);
    
    if(button1==LOW)
    {      
      ok=2;
    }
  }
  while(ok==2)
  {
    humidity = dht.readHumidity();

    Display.show(humidity);

    delay(200);
    button1=digitalRead(button1in);

    if(button1==LOW)
    {      
      ok=3;
    }
  }
  while(ok==3)
  {
    lightlvl = analogRead(lightPin);

    Display.show(lightlvl);

    delay(200);
    button1=digitalRead(button1in);

    if(button1==LOW)
    {      
      ok=4;
    }
  }
}