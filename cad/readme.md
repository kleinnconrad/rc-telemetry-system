# 3D Printing Files for ESP32 Enclosure

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
