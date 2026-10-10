# Test Protocol: In-Vehicle Integration

## Table of Contents
* [1. Test Setup and Specifications](#1-test-setup-and-specifications)
* [2. Test Procedure and Methodology](#2-test-procedure-and-methodology)
* [3. Test Results and Validation](#3-test-results-and-validation)
* [4. Photos](#4-photos)

## 1. Test Setup and Specifications
The integration test of the telemetry unit was performed with the unit connected in the vehicle chassis.
* **Power Supply:** The ESP32 was powered exclusively by the BEC of the ESC via a free port of the RC receiver (6.0 V or 7.4 V, depending on the ESC setting).
* **Data Storage:** A 32 GB microSDHC card (FAT32) was used for logging.
* **Environment:** The vehicle was stationary under an open sky to give the GPS module an unobstructed view of the satellites.
* **Test Duration:** 180 seconds.

## 2. Test Procedure and Methodology
The test verified system stability and data integrity under real mechanical integration conditions.
* It was checked whether the inrush current of the ESP32 causes a reset or a voltage drop (brownout) of the receiver.
* Data throughput on the SPI bus to the microSD module was monitored at a 2 Hz interval.
* An immunity test regarding electromagnetic interference (EMI) between the electronic speed controller (ESC) and the GPS module was conducted.

## 3. Test Results and Validation
* **Power Supply:** The receiver's BEC delivered sufficient current (peaks up to 250 mA) for the boot process. The ESP32 did not detect a brownout.
* **Data Recording:** Logging to the microSD card proceeded without errors. No records were missing.
* **Sensor Data:** The parameters recorded in `log.csv` (temperature values in °C, GPS coordinates) underwent a plausibility check. Temperature values were stable within the ambient range (approx. 22 °C), and the GPS fix achieved an acceptable HDOP (Horizontal Dilution of Precision).

## 4. Photos

<img src="vehicle_test/PXL_20260518_144521252.jpg" height="300" alt="Telemetry unit next to the vehicle" /> <img src="vehicle_test/PXL_20260518_144728325.jpg" height="300" alt="Telemetry unit connected to the receiver" />
