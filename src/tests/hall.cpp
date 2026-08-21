#include <Arduino.h>

const int HALL_PIN = 2; // Your pin according to the schematic
volatile int magnetDetected = 0;

// This function is called in milliseconds when the magnet flies by
void IRAM_ATTR countPulse() {
  magnetDetected++;
}

void setup() {
  Serial.begin(115200);
  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);
  Serial.println("Waiting for magnet...");
}

void loop() {
  if (magnetDetected > 0) {
    Serial.print("Magnet detected! Counter: ");
    Serial.println(magnetDetected);
    magnetDetected = 0; // Reset counter for the next pass
  }
  delay(100);
}
