"""
utils.py contains constants and helpful functions.
"""

import os

HOME_PATH = "/home/pi"
ACS_PATH = HOME_PATH + "/ACS_2023"
DATA_PATH = ACS_PATH + "/_data"
LOGS_PATH = ACS_PATH + "/_logs"

HEADERS = [
    "Time",
    "State",
    "Altitude",
    "ADXL_Acceleration_X",
    "ADXL_Acceleration_Y",
    "ADXL_Acceleration_Z",
    "IMU_Acceleration_X",
    "IMU_Acceleration_Y",
    "IMU_Acceleration_Z",
    "Linear_Acceleration_X",
    "Linear_Acceleration_Y",
    "Linear_Acceleration_Z",
    "Euler_Angle_X",
    "Euler_Angle_Y",
    "Euler_Angle_Z",
    "Gravity_X",
    "Gravity_Y",
    "Gravity_Z",
    "Kalman_Acceleration",
    "Kalman_Velocity",
    "Kalman_Altitude",
    "Orientation(Beta)",
    "Angle"
]

LAUNCH_ACCELERATION = 50  # m/s^2
LAUNCH_ALTITUDE = 50  # m
BURNOUT_ACCELERATION = -6  # m/s^2
APOGEE_VELOCITY = 0  # m/s
APOGEE_ALTITUDE = 1402  # m


def file_number() -> str:
    data_path = ACS_PATH + "/_data"
    csvs = [file for file in os.listdir(data_path) if file.endswith("csv")]

    if not csvs:
        return "00"

    csvs = [csv[5:].removesuffix(".csv") for csv in csvs]
    nums = map(int, csvs)
    return str(max(nums) + 1).zfill(2)

