# Carten T410R Telemetry

## Table of Contents
* [1. Project Description and Specifications](#1-project-description-and-specifications)
* [2. Repository Structure](#2-repository-structure)
* [3. Bill of Materials (BOM)](#3-bill-of-materials-bom)
* [4. Schematic and Pin Mapping](#4-schematic-and-pin-mapping)
* [5. Implementation and Setup](#5-implementation-and-setup)
  * [5.1 Firmware Compilation and Upload](#51-firmware-compilation-and-upload)
  * [5.2 Electrical Wiring](#52-electrical-wiring)
  * [5.3 Mechanical Integration](#53-mechanical-integration)
* [6. Operation and Data Analysis](#6-operation-and-data-analysis)
  * [6.1 Log Format](#61-log-format)
  * [6.2 Post-Processing](#62-post-processing)
* [7. Reddit Feedback Synchronization](#7-reddit-feedback-synchronization)
* [8. License](#8-license)

## 1. Project Description and Specifications

<img src="testrun/vehicle_test/PXL_20260518_144521252.jpg" height="300" alt="Telemetry unit next to the vehicle" /> <img src="testrun/vehicle_test/PXL_20260518_144728325.jpg" height="300" alt="Telemetry unit connected to the receiver" />

Local telemetry system for the RC car Carten T410R (vehicle build: [RC100 repository](https://github.com/kleinnconrad/RC100)). An ESP32 records thermal and dynamic parameters during driving and writes them to a microSD card.

**Recorded Metrics:**
* **Temperature:** Motor and ESC temperature via two DS18B20 sensors on a shared 1-Wire bus. Measuring range -55 °C to +125 °C, accuracy ±0.5 °C (-10 °C to +85 °C), 12-bit resolution.
* **RPM:** Driveshaft RPM via a Hall sensor and a neodymium magnet (one pulse per revolution), counted by the ESP32 hardware pulse counter (PCNT).
* **Position and Speed:** Latitude, longitude and speed over ground from a u-blox NEO-7M GPS module (NMEA 0183, 9600 baud). The module runs at its default update rate of 1 Hz; the firmware does not reconfigure it.

**Architecture Variant:**
* Offline logging to a local microSD card. No data is transmitted over wireless networks, which avoids latencies and connection drops. An earlier variant with LTE/MQTT streaming was discontinued.

## 2. Repository Structure

| Path | Content |
| :--- | :--- |
| [`cad/`](cad/readme.md) | 3D-printable enclosure (STL) and print parameters |
| [`schematic/`](schematic/readme.md) | Wiring schematic (SVG) and its generator script |
| [`scripts/`](scripts/) | Log conversion (`log_to_csv.py`) and Reddit synchronization (`fetch_reddit.py`) |
| [`src/main/`](src/main/readme.md) | Logging firmware |
| [`src/tests/`](src/tests/readme.md) | Test sketches for each component |
| [`testrun/`](testrun/readme.md) | In-vehicle test protocol and photos |
| [`reddit/`](reddit/reddit_feedback.md) | Synchronized feedback from the Reddit thread |

## 3. Bill of Materials (BOM)
The as-built configuration consists of the following components:

| Component | Specification / Type | Qty | Function in System |
| :--- | :--- | :---: | :--- |
| Microcontroller | ESP32 DevKit, 30-pin, ESP-WROOM-32 (Freenove board used here) | 1 | Data acquisition and logging |
| Expansion Board | ESP32 terminal breakout board, 30-pin | 1 | Screw-terminal connections without soldering |
| GPS Module | u-blox NEO-7M breakout board with SMA connector | 1 | Position and speed over ground (UART, 9600 baud) |
| GPS Antenna | External GPS antenna with SMA connector | 1 | Satellite reception (the breakout board has no onboard antenna) |
| Storage Module | microSD card module, SPI, 3.3 V version without onboard regulator | 1 | Data storage |
| microSD Card | microSDHC, FAT32 (32 GB used) | 1 | Log medium |
| Temperature Sensor | DS18B20, waterproof probe | 2 | Motor and ESC temperature |
| 1-Wire Adapter | DS18B20 adapter board with screw terminal and 4.7 kΩ pull-up | 1 | Parallel connection of both probes to the bus |
| RPM Sensor | A3144 Hall sensor module | 1 | Detection of the driveshaft magnet |
| Magnet | Neodymium, 3 × 2 mm | 1 | Pulse generator on the driveshaft |
| Splice Connectors | WAGO 221 lever connector, 5-conductor | 2 | Distribution of 3.3 V and GND |
| Power Cable | 3-pin servo cable (JR) | 1 | Supply from the ESC BEC via a free receiver port |
| Enclosure | 3D-printed case and lid, see [`cad/`](cad/readme.md) | 1 | Protection of the ESP32 and breakout board |

**Notes on component selection:**
* **microSD module:** Modules with an onboard AMS1117 regulator and level shifter are designed for a 5 V supply. At 3.3 V the card receives too low a voltage. Use a 3.3 V module (pins labeled `3.3V`) as listed.
* **Hall sensor:** The A3144 is specified for a supply voltage of 4.5 V to 24 V. In this build it runs from 3.3 V, below the specified minimum. For operation within the datasheet limits, a 3.3 V-capable Hall switch with open-drain output (e.g., TI DRV5023 or Allegro A1120) can be used with the same wiring.

## 4. Schematic and Pin Mapping

![Wiring schematic](schematic/Schematic_Graphical.svg)

All components share a common ground (GND). The UART connection between the ESP32 and the GPS module is crossed (TX to RX, RX to TX). The ESP32 and all peripherals are supplied by the 3.3 V regulator of the ESP32 board; the estimated peak current of the overall system is approx. 200 mA to 250 mA.

| Component | Interface | ESP32 Pin | Sensor Pin | Remark |
| :--- | :--- | :--- | :--- | :--- |
| RC Receiver | Power | `VIN` | + (red) | ESC BEC output, 6.0 V or 7.4 V |
| | | `GND` | − (black) | Common ground |
| GPS Module | UART 2 | `GPIO 16` (RX2) | TX | VCC from 3.3 V |
| | | `GPIO 17` (TX2) | RX | |
| microSD Module | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | VCC from 3.3 V |
| DS18B20 (2×) | 1-Wire | `GPIO 4` | DQ | Both probes in parallel; 4.7 kΩ pull-up on the adapter board |
| A3144 Hall Sensor | Digital In | `GPIO 2` | DO | Internal pull-up enabled; counted by the PCNT |

The schematic is generated by a script. Details are in [`schematic/readme.md`](schematic/readme.md).

## 5. Implementation and Setup

### 5.1 Firmware Compilation and Upload
* **Environment:** Arduino IDE with the ESP32 board package (Espressif Systems). Board selection: `ESP32 Dev Module`.
* **Libraries:** Install `TinyGPSPlus` (Mikal Hart), `OneWire` (Paul Stoffregen) and `DallasTemperature` (Miles Burton) via the Library Manager.
* **Sketch:** The Arduino IDE requires an `.ino` file inside a folder of the same name. Create a sketch (e.g., `main_offline/main_offline.ino`) and copy the content of [`src/main/main_offline.cpp`](src/main/main_offline.cpp) into it.
* **Upload:** Upload via USB. If the upload fails with "Wrong boot mode detected", disconnect the Hall sensor from `GPIO 2` during the upload (see [5.2](#52-electrical-wiring)).
* **Diagnostics:** The serial monitor (`115200` baud) shows `SD OK - Offline Logging ready` after a successful start, or `SD Error! Please check card.` if the card is not detected.
* **Component tests:** Before the first upload of the main firmware, each component should be verified with the test sketches in [`src/tests/`](src/tests/readme.md).

### 5.2 Electrical Wiring
* The ESP32 is plugged onto the terminal breakout board. All jumper wires are fastened in the screw terminals to obtain vibration-resistant connections.
* The servo cable connects `VIN` and `GND` with correct polarity to a free port of the RC receiver. The signal wire remains unconnected.
* **Supply voltage:** The BEC of the Hobbywing QuicRun WP 10BL120 G2 ESC outputs 6.0 V or 7.4 V (selectable). The ESP32 board reduces this to 3.3 V with a linear regulator, which converts the voltage difference into heat. At an estimated average load of 120 mA, the dissipation is approx. 0.5 W at 7.4 V and 0.3 W at 6.0 V. The 6.0 V setting is preferable if the steering servo permits it.
* GPS, microSD module, Hall sensor and DS18B20 adapter are connected according to the pin mapping in [section 4](#4-schematic-and-pin-mapping).
* The 3.3 V and GND lines of the peripherals are joined in two WAGO 221 lever connectors. The correct seating of each conductor in the clamps must be verified to prevent loose contacts under vibration.
* **GPIO 2:** This pin is a boot strapping pin and must be low or floating when the ESP32 enters the download mode. A Hall sensor module with an onboard pull-up resistor can prevent the upload. On boards with the onboard LED on `GPIO 2`, the LED follows the sensor output.

### 5.3 Mechanical Integration
* **Central Unit:** The ESP32 enclosure is mounted in the chassis with screwed carrier plates or hook-and-loop tape.
* **GPS:** The external antenna is mounted horizontally with an unobstructed view of the sky, at a distance from the motor, ESC and battery cables.
* **RPM Measurement:** The neodymium magnet is bonded to the driveshaft (e.g., cyanoacrylate or epoxy resin). A counterweight on the opposite side of the shaft prevents imbalance at high rotational speeds. The Hall sensor is mounted rigidly with a maximum gap of 2 mm to the magnet. The A3144 only switches when the south pole faces its marked side; if no pulses are detected, the magnet must be turned over.
* **Temperatures:** The DS18B20 probes are attached to the motor and ESC housings with thermal adhesive.

## 6. Operation and Data Analysis
* **Start:** The system starts when the vehicle is switched on. Logging begins immediately; if the microSD card was not detected at startup, every write attempt fails and is reported on the serial monitor.
* **Logging Cycle:** One record every 500 ms (2 Hz). The log file is opened, appended and closed for each record, so a power loss affects at most the record being written.
* **Sessions:** All runs are appended to the same file. The timestamp restarts at zero after each power-on, which marks the beginning of a new session.
* **Retrieval:** After the run, the microSD card is removed and read on a PC.

### 6.1 Log Format
The firmware writes to `/log.csv`. Despite the file extension, each line is a JSON object (JSON Lines format), for example:

```json
{"ts":152500,"rpm":8040,"t_m":41.3,"t_e":36.8,"lat":52.520008,"lng":13.404954,"spd":27.45}
```

| Field | Unit | Content |
| :--- | :--- | :--- |
| `ts` | ms | Time since power-on (not GPS time) |
| `rpm` | 1/min | Driveshaft RPM, calculated from the pulses of the last interval |
| `t_m` | °C | Motor temperature (DS18B20 with bus index 0) |
| `t_e` | °C | ESC temperature (DS18B20 with bus index 1) |
| `lat`, `lng` | ° | Position; `0.000000` without a valid GPS fix |
| `spd` | km/h | Speed over ground; `0.00` without valid GPS data |

**Value ranges and limits:**
* A temperature of `-127.0` indicates a sensor that did not respond.
* The bus index of a DS18B20 is determined by its ROM code, not by the wiring. The assignment of the probes to motor and ESC must be verified once (see [test procedure](src/tests/readme.md#4-phase-2a-temperature-sensors)).
* The GPS module delivers new positions at 1 Hz, so two consecutive records usually contain the same position.
* With one pulse per revolution and a 500 ms interval, the RPM resolution is 120 1/min.

### 6.2 Post-Processing
The script [`scripts/log_to_csv.py`](scripts/log_to_csv.py) converts the log into a CSV file with one column per field and an additional session number. It requires only the Python standard library:

```
python scripts/log_to_csv.py E:\log.csv
```

The result (`log_converted.csv`) can be opened in spreadsheet programs or analysis tools. Lines that were cut off by a power loss are skipped and counted.

## 7. Reddit Feedback Synchronization
The project was discussed in the [r/esp32 thread](https://www.reddit.com/r/esp32/comments/1s9dydh/). A GitHub Action copies the comments of this thread into the repository.

* **Script (`scripts/fetch_reddit.py`):** Reads the RSS feed of the thread, converts the comments to plain text and writes them to [`reddit/reddit_feedback.md`](reddit/reddit_feedback.md). The file is only rewritten when the comments have changed.
* **Workflow (`.github/workflows/reddit-sync.yml`):** Runs the script and commits a changed file to the branch the workflow was started on. The workflow has no schedule and is started manually.
* **Dependencies:** `requirements.txt` (kept up to date by Dependabot).

Manual start:
1. Open the "Actions" tab of the GitHub repository.
2. Select the "Fetch Reddit Feedback" workflow.
3. Click "Run workflow".

## 8. License
This project is licensed under the [MIT License](LICENSE).
