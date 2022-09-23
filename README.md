# ACS 2023
This repository contains all (Python 3) code and libraries required for the 2022-2023 Notre Dame Rocketry Team (NDRT) Apogee Control System (ACS). It also contains sensor/actuator example code and flight data.

## Interfacing with the Microcontroller
1. Connect to `ND-guest`
2. Open a terminal
3. Type `ssh pi@mulberry`
4. Enter password `ACS_2023`
5. Always use `git pull` before pushing changes to avoid merge conflicts

## Batteries

## Sensors

| Sensor Type | Sensor Model |
| ----------- | ------------ |

## Microcontroller
Raspberry Pi 4 Model B (4GB RAM)

## Actuator

## Subscale Workflow

*
  *
  *
*
*

## Fullscale Workflow

*
  *
  *
*
*

## Miscellaneous Notes/Troubleshooting
* Command: `ssh pi@mulberry`
  * Error: `ssh: Could not resolve hostname [hostname]: nodename nor servname provided, or not known`
  * Solution: Run `sudo killall -HUP mDNSResponder` and then try `ssh pi@mulberry` again

