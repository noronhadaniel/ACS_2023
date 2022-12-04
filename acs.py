import time

import board

from data_logger import DataLogger
from sensors import Accelerometer, Altimeter, IMU
import utils

brd = board.I2C()
accelerometer = Accelerometer(brd)
altimeter = Altimeter(brd)
imu = IMU(brd)
datalogger = DataLogger(utils.DATA_PATH + f"/data_{utils.file_number()}.csv", accelerometer, altimeter, imu)


while True:
    datalogger.log_sensors()
    print("--------------------------------------------------")
    if datalogger.samples > 1:
        print(f"\nSample #{datalogger.samples}; Time: {time.time()}s")
        print(f"Sample Rate = {datalogger.samples / 1}Hz\n")
    print("--------------------------------------------------")
