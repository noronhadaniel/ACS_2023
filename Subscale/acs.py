import time

import board

from data_filter import DataFilter
from data_logger import SensorLogger
from sensors import Accelerometer, Altimeter, IMU
from state_manager import StateManager
import utils

brd = board.I2C()
accelerometer = Accelerometer(brd)
altimeter = Altimeter(brd)
imu = IMU(brd)

datafilter = DataFilter()
datalogger = SensorLogger(utils.DATA_PATH + f"/data_{utils.file_number()}.csv", accelerometer, altimeter, imu, datafilter)
statemanager = StateManager(accelerometer, altimeter, imu, datafilter)


while True:
    datalogger.log()
    print("--------------------------------------------------")
    if datalogger.samples > 1:
        print(f"\nSample #{datalogger.samples}; Time: {time.time()}s")
        print(f"State: {StateManager.state}")
        print(f"Sample Rate = {datalogger.samples / 1}Hz\n")
    print("--------------------------------------------------")

