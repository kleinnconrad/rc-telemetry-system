#include <Arduino.h>

// For the ESP32, the internal blue LED is often on pin 2
const int LED_PIN = 2; 

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("ESP32 is alive and starting the test!");
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // LED on
  Serial.println("LED ON");
  delay(1000);                 // Wait 1 second
  
  digitalWrite(LED_PIN, LOW);  // LED off
  Serial.println("LED OFF");
  delay(1000);
}
