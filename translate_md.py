import os

cad_readme = """# 3D Printing Files for ESP32 Enclosure

## Table of Contents
* [1. Enclosure Description](#1-enclosure-description)
* [2. Specifications and Tolerances](#2-specifications-and-tolerances)
* [3. Printing Parameters](#3-printing-parameters)

## 1. Enclosure Description
These STL files contain the CAD data for a protective enclosure designed specifically for the 30-pin ESP32 Terminal Breakout Board. The design is modular, consisting of a base tray (`case.stl`) and a lid (`lid.stl`).

## 2. Specifications and Tolerances
* **Dimensions:** Adapted to the PCB dimensions of the standard 30-pin Breakout Board.
* **Tolerances:** A clearance of 0.2 mm is considered for the screw terminal cutouts to ensure mechanical stress relief.
* **Mounting:** The PCB is fixed via a press-fit without additional screws. The lid has a snap-in mechanism.

## 3. Printing Parameters
For manufacturing using the FDM process, adherence to the following parameters is mandatory to guarantee dimensional accuracy and layer adhesion:
* **Material:** PETG or ABS (Strictly no PLA due to insufficient heat resistance near the motor).
* **Layer Height:** 0.2 mm.
* **Infill:** 20% (Gyroid structure for optimal rigidity).
* **Support Structures:** Not required. The overhangs are designed for printing without supports.
"""

schematic_readme = """# Pin Mapping and Wiring

## Table of Contents
* [1. Architecture](#1-architecture)
* [2. Schematic](#2-schematic)
* [3. Pin Mapping](#3-pin-mapping)

## 1. Architecture
The architecture is based on an ESP32 as the central processing unit. The data lines are connected via a breakout board with screw terminals.
* GPS Tracking: A GPS module provides geodata and speed values via the NMEA protocol (hardware UART).
* Logging: The MicroSD card serves as primary storage.
* Sensor Reading: Data acquisition is asynchronous. Pulses from the Hall sensor are registered via a hardware counter (PCNT).

## 2. Schematic

![Schematic Offline](Schematic_Graphical.svg)

## 3. Pin Mapping
All components require a common ground (GND). Serial connections require crossed lines (TX to RX, RX to TX).

| Component | Interface | ESP32 Pin | Sensor Pin | Remark |
| :--- | :--- | :--- | :--- | :--- |
| RC Receiver | Power | `VIN` | 5V (Red) | Supply via ESC/Receiver |
| | | `GND` | GND (Black) | Common ground |
| GPS Module | UART 2 | `GPIO 16` (RX2) | TX | VCC to 3.3V ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| MicroSD Module | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | VCC to 3.3V ESP32 |
| DS18B20 | 1-Wire | `GPIO 4` | DQ (Data) | Parallel connection of both sensors |
| Hall Sensor | Digital In | `GPIO 2` | DO | Connection to ESP32 PCNT (Pulse Counter) |
"""

main_readme = """# Firmware Core

## Table of Contents
* [1. Program Logic](#1-program-logic)
* [2. Libraries](#2-libraries)

## 1. Program Logic
The main routine `main_offline.cpp` coordinates the non-blocking initialization of all sensors. Data acquisition runs cyclically at a defined rate of 2 Hz. Sensor data is concatenated into a CSV string and appended to the FAT32 file system of the MicroSD card via SPI.

## 2. Libraries
The following external libraries are strictly required for the build process (compilation via PlatformIO or Arduino IDE):

* `TinyGPSPlus`: Efficient parsing of incoming raw NMEA data.
* `OneWire`: Protocol layer for the temperature sensor bus.
* `DallasTemperature`: Higher-level abstraction layer for addressing and reading the DS18B20 ICs.
* `SPI` and `SD`: Core libraries for file access to the MicroSD module.
"""

tests_readme = """# Test Procedures and Verification

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
"""

testrun_readme = """# Test Protocol: In-Vehicle Integration

## Table of Contents
* [1. Test Setup and Specifications](#1-test-setup-and-specifications)
* [2. Test Procedure and Methodology](#2-test-procedure-and-methodology)
* [3. Test Results and Validation](#3-test-results-and-validation)

## 1. Test Setup and Specifications
The integration test of the telemetry unit was performed mounted within the vehicle chassis.
* **Power Supply:** The ESP32 was powered exclusively parasitically via the BEC port (Battery Eliminator Circuit) of the RC receiver at a nominal voltage of 5.0 V.
* **Data Storage:** A 16 GB SDHC card (FAT32, cluster size 32 KB) was used for logging.
* **Environment:** The vehicle was positioned stationary under an open sky to guarantee an unobstructed line-of-sight for the satellite fix of the GPS module.
* **Test Duration:** The test run lasted exactly 180 seconds.

## 2. Test Procedure and Methodology
The test focused on verifying system stability and data integrity under real mechanical integration conditions.
* It was verified whether the inrush current of the ESP32 causes a reset or voltage drop ("Brownout") of the receiver.
* Data throughput on the SPI bus to the SD module was monitored at a 2 Hz interval.
* An immunity test regarding electromagnetic interference (EMI) between the electronic speed controller (ESC) and the GPS module was conducted.

## 3. Test Results and Validation
* **Power Supply:** The test was successful. The receiver's BEC delivered sufficient current (peaks up to 250 mA) for the boot process. Brownout detections by the ESP32 did not occur.
* **Data Recording:** Logging to the MicroSD card proceeded entirely error-free. No dropped frames were recorded.
* **Sensor Data:** Parameters recorded in `log.csv` (temperature values in °C, GPS coordinates) underwent a plausibility check. Temperature values were stable within ambient range (approx. 22 °C), and the GPS fix achieved an acceptable HDOP (Horizontal Dilution of Precision).
"""

with open("cad/readme.md", "w", encoding="utf-8") as f:
    f.write(cad_readme)
with open("schematic/readme.md", "w", encoding="utf-8") as f:
    f.write(schematic_readme)
with open("src/main/readme.md", "w", encoding="utf-8") as f:
    f.write(main_readme)
with open("src/tests/readme.md", "w", encoding="utf-8") as f:
    f.write(tests_readme)
with open("testrun/readme.md", "w", encoding="utf-8") as f:
    f.write(testrun_readme)

print("Markdown files successfully translated.")
