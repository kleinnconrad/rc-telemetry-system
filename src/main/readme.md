# Firmware Core

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
