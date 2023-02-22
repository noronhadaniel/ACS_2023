import os

HOME_PATH = "/home/pi"
ACS_PATH = HOME_PATH + "/ACS_2023"
DATA_PATH = ACS_PATH + "/_data"
LOGS_PATH = ACS_PATH + "/_logs"

HEADERS = [
    "Time",
    "ADXL_Acceleration_X",
    "ADXL_Acceleration_Y",
    "ADXL_Acceleration_Z",
    "Altitude",
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
    "Orientation(Beta)"
]


def file_number() -> int:
    data_path = ACS_PATH + "/_data"
    csvs = [file for file in os.listdir(data_path) if file.endswith("csv")]

    if not csvs:
        return 0

    csvs = [csv[5:].removesuffix(".csv") for csv in csvs]
    nums = map(int, csvs)
    return max(nums) + 1

