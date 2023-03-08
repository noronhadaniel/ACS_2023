# ACS 2023
This repository contains all (Python 3) code and libraries required for the 2022-2023 Notre Dame Rocketry Team (NDRT) Apogee Control System (ACS). It also contains sensor/actuator example code and flight data.

## Interfacing with the Microcontroller
SSH:
1. Connect to `ND-guest` (or hotspot)
2. Open a terminal
3. Type `ssh pi@mulberry` (or `ssh pi@mulberry.local` if using hotspot)
4. Enter password `ACS_2023`
5. Always use `git pull` before pushing changes to avoid merge conflicts (`git status` is also useful)

VNC Viewer (Remote Desktop):
1. Connect to the Raspberry Pi via SSH
2. Run `vncserver` and copy the IP address (same as wlan0 IPv4 from running `ifconfig`)
3. Open RealVNC VNC Viewer and enter the copied IP address (with username: pi and password: ACS_2023)
4. When finished, disconnect the VNC Viewer and run `vncserver -kill :1' to kill connection 1 (check ~/.vnc to make sure no .pid process files exist)

## Batteries
* YDL PL 115659 3.7V LiPo (5000mAh Logic Circuit Battery)
* 7.4V 2S 3000mAh LiPo (Servo Motor Battery)

## Sensors

|  Sensor Type  | Sensor Model |
| ------------- | ------------ |
| Accelerometer |    ADXL343   |
|  Altimeter 1  |   MPL3115A2  |
|  Altimeter 2  |     BMP390   |
|      IMU      |     BNO055   |

## Microcontroller
Raspberry Pi 4 Model B (4GB RAM)

## Actuator
DSSERVO DS5180 80kg High-Torque Standard Servo Motor

## Subscale Workflow

* Data Logger Initialization
  * Check for existing data files and find new filename (to prevent overwriting)
  * Create new CSV file with new filename
  * Add Header Row
* Initialize sensors
* Read sensor data
* Add sensor data to new row in CSV file
* Loop indefinitely

## Fullscale Workflow (Control Code Flowchart)
![image](https://user-images.githubusercontent.com/91227299/223595209-889868e9-dea8-4749-9dbb-75108b3a8092.png)

## Miscellaneous Notes/Troubleshooting
* Command: `ssh pi@mulberry`
  * Error: `ssh: Could not resolve hostname [hostname]: nodename nor servname provided, or not known`
  * Solution: Run `sudo killall -HUP mDNSResponder` and then try `ssh pi@mulberry` again
* Command: `ssh pi@mulberry`
  * Error: `ssh: connect to host mulberry port 22: Undefined error: 0`
  * Solution: Make sure you run `ssh pi@mulberry.local` if using a hotspot connection
* `sudo raspi-config`
* `iwgetid -r` to find out what Wi-Fi you are connected to
