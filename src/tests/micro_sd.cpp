#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

const int SD_CS_PIN = 5;

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing SD card...");

  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Error: SD card not found or wired incorrectly!");
    return;
  }
  Serial.println("SD card found.");

  // Create and write test file
  File dataFile = SD.open("/test.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Hello from the ESP32! The card is working.");
    dataFile.close();
    Serial.println("Successfully written to test.txt.");
  } else {
    Serial.println("Error opening the file.");
  }
}

void loop() {
  // Nothing else happens here
}
