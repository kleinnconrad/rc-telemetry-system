# Test Protocol: In-Vehicle Integration

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
