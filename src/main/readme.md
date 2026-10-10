# Firmware Core

## Table of Contents
* [1. Program Logic](#1-program-logic)
* [2. Libraries](#2-libraries)
* [3. Known Limitations](#3-known-limitations)

## 1. Program Logic
`main_offline.cpp` reads all sensors and appends one record every 500 ms (2 Hz) to `/log.csv` on the microSD card. The record format is described in the [main README](../../README.md#61-log-format).

**Setup:**
* UART 2 is started at 9600 baud on `GPIO 16` (RX) and `GPIO 17` (TX) for the GPS module.
* The DS18B20 sensors are switched to non-blocking mode, and the first temperature conversion is started.
* `GPIO 2` is configured as input with internal pull-up. PCNT unit 0 counts falling edges of the Hall sensor signal. A glitch filter of 100 APB clock cycles (1.25 µs) suppresses short interference pulses. The counter wraps at 30000.
* The microSD card is initialized via SPI with chip select on `GPIO 5`.

**Main loop:**
1. All bytes received from the GPS module are passed to the TinyGPS++ parser.
2. Every 800 ms, the results of the previous temperature conversion are read (bus index 0: motor, index 1: ESC) and a new conversion is started. A 12-bit conversion takes up to 750 ms.
3. Every 500 ms, the PCNT counter is read without resetting it. The difference to the previous reading is corrected for a counter wrap. The RPM is calculated from this difference and the measured interval length: `rpm = pulses × 60000 / interval_ms`. The record is formatted as JSON, the log file is opened in append mode, the line is written and the file is closed.

## 2. Libraries
External libraries (Arduino Library Manager):
* `TinyGPSPlus` (Mikal Hart): Parsing of the NMEA sentences.
* `OneWire` (Paul Stoffregen): Protocol layer for the 1-Wire bus.
* `DallasTemperature` (Miles Burton): Addressing and reading of the DS18B20 sensors.

Included in the ESP32 board package:
* `SPI`, `SD`: File access to the microSD card.
* `HardwareSerial`: UART 2 for the GPS module.
* `driver/pcnt.h`: ESP-IDF driver for the hardware pulse counter.

## 3. Known Limitations
The following points are properties of the current firmware version. They are documented here for a future revision.
* The log file has the extension `.csv` but contains JSON Lines. [`scripts/log_to_csv.py`](../../scripts/log_to_csv.py) converts it.
* All sessions are appended to the same file. Sessions can only be separated by the reset of the timestamp `ts`.
* Missing GPS data is logged as `0.0`, which cannot be distinguished from a real value of zero. Satellite count, HDOP and GPS time are not logged.
* The GPS module runs at its default rate of 1 Hz. The NEO-7M supports up to 10 Hz, which requires a configuration command (UBX-CFG-RATE) at startup.
* The assignment of the DS18B20 probes to motor and ESC depends on their ROM codes. Replacing a probe can swap `t_m` and `t_e`.
* If the microSD card is not detected at startup, initialization is not retried.
