# 3D Printing Files for ESP32 Enclosure

## Table of Contents
* [1. Enclosure Description](#1-enclosure-description)
* [2. Specifications and Tolerances](#2-specifications-and-tolerances)
* [3. Printing Parameters](#3-printing-parameters)

## 1. Enclosure Description
The STL files contain an enclosure for the 30-pin ESP32 terminal breakout board. It consists of two parts:
* [`esp32-30pin-breakoutboard-case.stl`](esp32-30pin-breakoutboard-case.stl): Base tray.
* [`esp32-30pin-breakoutboard-lid.stl`](esp32-30pin-breakoutboard-lid.stl): Lid.

In the test setup, the GPS and microSD modules are attached to the top of the lid (see [test photos](../testrun/readme.md#4-photos)).

## 2. Specifications and Tolerances
* **Dimensions (L × W × H):** Case 73.8 × 67.5 × 22.0 mm, lid 73.8 × 67.5 × 11.0 mm.
* **Tolerances:** The cutouts for the screw terminals have a clearance of 0.2 mm.
* **Mounting:** The board is held by a press fit without screws. The lid snaps onto the case.

## 3. Printing Parameters
Recommended parameters for FDM printing:
* **Material:** PETG or ABS. PLA is not suitable because its glass transition temperature (approx. 60 °C) can be exceeded near the motor.
* **Layer Height:** 0.2 mm.
* **Infill:** 20 %, gyroid pattern.
* **Support Structures:** Not required. The overhangs are designed for printing without supports.
