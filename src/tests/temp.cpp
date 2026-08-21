#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const int ONE_WIRE_BUS = 4; // Your pin according to the schematic

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
  Serial.println("Temperature test started.");
}

void loop() {
  sensors.requestTemperatures(); 
  float temp = sensors.getTempCByIndex(0);
  
  Serial.print("Current temperature: ");
  Serial.print(temp);
  Serial.println(" C");
  
  delay(1000);
}
