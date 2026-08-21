# Test Procedures and Verification

## Table of Contents
* [1. Methodology and Acceptance Criteria](#1-methodology-and-acceptance-criteria)
* [2. General Preparation](#2-general-preparation)
* [3. Phase 1: System Boot](#3-phase-1-system-boot)
* [4. Phase 2A: Temperature Sensor](#4-phase-2a-temperature-sensor)
* [5. Phase 2B: Hall Sensor](#5-phase-2b-hall-sensor)
* [6. Phase 3: MicroSD Card](#6-phase-3-microsd-card)
* [7. Phase 4: GPS Module](#7-phase-4-gps-module)

## 1. Methodology and Acceptance Criteria
The following test routines serve for isolated hardware verification (peripheral unit tests). Each component must strictly be tested individually before flashing the complete firmware.
A test is considered passed if the output in the Serial Monitor precisely matches the defined expected values and no hardware timeouts are reported.

## 2. General Preparation
1. Connect the ESP32 to the PC via a data USB cable (strictly with intact D+/D- lines).
2. Open the Arduino IDE and paste the respective test code into the editor.
3. In menu `Tools` -> `Board`: Select `ESP32 Dev Module`.
4. In menu `Tools` -> `Port`: Assign the recognized COM port (Windows) or `/dev/ttyUSB*` (Linux/macOS).
5. Press the Upload button. If the connection stalls, hold the `BOOT` button on the ESP32 for two seconds.
6. Open the Serial Monitor and set the baud rate exactly to `115200`.

## 3. Phase 1: System Boot
**Goal:** Testing the basic ESP32 functionality, serial interface, and flash process.
**Acceptance Criterion:** The serial monitor alternately outputs "LED ON" and "LED OFF" every second. The onboard LED blinks synchronously.

```cpp
#include <Arduino.h>

const int LED_PIN = 2; 

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("System Boot");
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED ON");
  delay(1000);
  
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED OFF");
  delay(1000);
}
```

## 4. Phase 2A: Temperature Sensor
**Goal:** Verification of 1-Wire communication. DS18B20 sensor connected to Pin 4.
**Acceptance Criterion:** Measured temperature is output in Celsius. Reading a value of `-127.00 C` indicates a connection drop or wiring error.

```cpp
#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const int ONE_WIRE_BUS = 4;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
  Serial.println("Temperature Test");
}

void loop() {
  sensors.requestTemperatures(); 
  float temp = sensors.getTempCByIndex(0);
  
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" C");
  
  delay(1000);
}
```

## 5. Phase 2B: Hall Sensor
**Goal:** Functional check of the hardware interrupt on the A3144 Hall sensor (Pin 2).
**Acceptance Criterion:** Manual approach of the neodymium magnet to the sensor registers exactly one pulse on the Serial Monitor. Multiple triggers indicate bouncing.

```cpp
#include <Arduino.h>

const int HALL_PIN = 2;
volatile int magnetDetected = 0;

void IRAM_ATTR countPulse() {
  magnetDetected++;
}

void setup() {
  Serial.begin(115200);
  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);
  Serial.println("Ready");
}

void loop() {
  if (magnetDetected > 0) {
    Serial.print("Pulses: ");
    Serial.println(magnetDetected);
    magnetDetected = 0;
  }
  delay(100);
}
```

## 6. Phase 3: MicroSD Card
**Goal:** Verification of the SPI bus and read/write cycles. The module must strictly be powered via 3.3V.
**Acceptance Criterion:** Output confirmation "Write process completed". The SD card (FAT32) subsequently contains a file `test.txt` with the text "SD test successful".

```cpp
#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

const int SD_CS_PIN = 5;

void setup() {
  Serial.begin(115200);
  
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Error during SD initialization");
    return;
  }
  
  File dataFile = SD.open("/test.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("SD test successful");
    dataFile.close();
    Serial.println("Write process completed");
  } else {
    Serial.println("File access error");
  }
}

void loop() {}
```

## 7. Phase 4: GPS Module
**Goal:** Evaluation of hardware UART reception of NMEA datasets from the BN-220 module (RX to Pin 16, TX to Pin 17).
**Acceptance Criterion:** The monitor displays raw NMEA sentences (e.g., `$GPRMC...`). These must contain valid coordinates under an open sky, otherwise data fields remain empty.

```cpp
#include <Arduino.h>
#include <HardwareSerial.h>

const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;
HardwareSerial SerialGPS(2);

void setup() {
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
}

void loop() {
  while (SerialGPS.available()) {
    char c = SerialGPS.read();
    Serial.print(c);
  }
}
```
