#include <Arduino.h>
#include <HardwareSerial.h>

const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;

HardwareSerial SerialGPS(2); // UART 2

void setup() {
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN); // 9600 is standard for GPS
  Serial.println("Waiting for GPS raw data...");
}

void loop() {
  // If the GPS module sends data, print it immediately to the monitor
  while (SerialGPS.available()) {
    char c = SerialGPS.read();
    Serial.print(c);
  }
}
