# Test Procedures and Verification

## Table of Contents
* [1. Methodology and Acceptance Criteria](#1-methodology-and-acceptance-criteria)
* [2. General Preparation](#2-general-preparation)
* [3. Phase 1: System Boot](#3-phase-1-system-boot)
* [4. Phase 2A: Temperature Sensors](#4-phase-2a-temperature-sensors)
* [5. Phase 2B: Hall Sensor](#5-phase-2b-hall-sensor)
* [6. Phase 3: microSD Card](#6-phase-3-microsd-card)
* [7. Phase 4: GPS Module](#7-phase-4-gps-module)

## 1. Methodology and Acceptance Criteria
The test sketches in this directory verify each hardware component in isolation. Each component is tested individually before the main firmware is uploaded.
A test is passed if the serial monitor shows the expected output listed for the respective phase.

## 2. General Preparation
1. Connect the ESP32 to the PC with a USB data cable (charge-only cables have no data lines).
2. In the Arduino IDE, create a new sketch and copy the content of the respective test file into it.
3. In menu `Tools` -> `Board`: Select `ESP32 Dev Module`.
4. In menu `Tools` -> `Port`: Select the COM port (Windows) or `/dev/ttyUSB*` (Linux) or `/dev/cu.*` (macOS).
5. Click Upload. If the upload stops at `Connecting...`, hold the `BOOT` button on the ESP32 until the upload starts.
6. Open the serial monitor and set the baud rate to `115200`.

## 3. Phase 1: System Boot
**Sketch:** [`blink.cpp`](blink.cpp)
**Goal:** Verification of the basic ESP32 function, the serial interface and the upload process.
**Expected Output:** `ESP32 is alive and starting the test!`, followed by `LED ON` and `LED OFF` alternating every second. On boards with the onboard LED on `GPIO 2`, the LED blinks synchronously.

## 4. Phase 2A: Temperature Sensors
**Sketch:** [`temp.cpp`](temp.cpp) (1-Wire bus on `GPIO 4`)
**Goal:** Verification of the 1-Wire communication.
**Expected Output:** `Temperature test started.`, followed by `Current temperature: 22.50 C` (example value) approx. every 1.75 s. The sketch shows the sensor with bus index 0.

**Error Values:**
* `-127.00 C`: No sensor responds. Wiring or the pull-up resistor on the adapter board must be checked.
* `85.00 C`: Power-on value of the DS18B20. The conversion was not completed, usually because of an unstable supply.

**Assignment of the probes:** The main firmware logs bus index 0 as motor temperature (`t_m`) and index 1 as ESC temperature (`t_e`). The index is determined by the ROM code of each sensor. With both probes connected, one probe is warmed in the hand: if the displayed value rises, this probe has index 0 and is mounted on the motor. The probe should be marked accordingly.

## 5. Phase 2B: Hall Sensor
**Sketch:** [`hall.cpp`](hall.cpp) (signal on `GPIO 2`)
**Goal:** Verification of the A3144 signal with a GPIO interrupt on the falling edge.
**Expected Output:** `Waiting for magnet...`. A single pass of the neodymium magnet produces `Magnet detected! Counter: 1`. Higher counts for a single pass indicate multiple triggering.

**Notes:**
* The A3144 only switches when the south pole faces its marked side. Without a detection, the magnet must be turned over.
* The main firmware uses the hardware pulse counter (PCNT) with a glitch filter instead of the interrupt.

## 6. Phase 3: microSD Card
**Sketch:** [`micro_sd.cpp`](micro_sd.cpp) (chip select on `GPIO 5`)
**Goal:** Verification of the SPI bus and a write cycle. The module is supplied with 3.3 V.
**Expected Output:** `Initializing SD card...`, `SD card found.`, `Successfully written to test.txt.` The card then contains the file `test.txt` with the line `Hello from the ESP32! The card is working.`

**Error Outputs:**
* `Error: SD card not found or wired incorrectly!`: Wiring, supply or file system must be checked. The card must be formatted with FAT32; cards larger than 32 GB (SDXC) are delivered with exFAT and must be reformatted.
* `Error opening the file.`: The card was detected, but the file could not be created (e.g., write protection or a damaged file system).

## 7. Phase 4: GPS Module
**Sketch:** [`gps.cpp`](gps.cpp) (GPS TX to `GPIO 16`, GPS RX to `GPIO 17`)
**Goal:** Verification of the UART reception of NMEA sentences from the NEO-7M module.
**Expected Output:** `Waiting for GPS raw data...`, followed by NMEA sentences once per second (e.g., `$GPRMC`, `$GPGGA`, `$GPGSV`).

**Acceptance Criterion:** With the external antenna connected and an unobstructed view of the sky, the status field of `$GPRMC` changes from `V` (void) to `A` (valid) and the position fields are filled. After a cold start, this can take several minutes.

**Error Patterns:**
* No output after the start message: TX and RX are not crossed, or the module has no supply.
* Unreadable characters: The baud rate does not match (NEO-7M default: 9600 baud).
