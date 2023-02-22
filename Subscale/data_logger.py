import csv
import time

from data_filter import DataFilter
from sensors import Accelerometer, Altimeter, IMU
from utils import HEADERS


class DataLogger:
    def __init__(self, name: str, accelerometer: Accelerometer, altimeter: Altimeter, imu: IMU, dfilter: DataFilter):
        self.name = name
        self.file = open(name, "w")
        self.samples = 0
        self.accelerometer = accelerometer
        self.altimeter = altimeter
        self.imu = imu
        self.dfilter = dfilter

        self._initialize_csv()

    def _initialize_csv(self):
        csv.writer(self.file).writerow(HEADERS)

    def log_sensors(self):
        acceleration_acce_x, acceleration_acce_y, acceleration_acce_z = self.accelerometer.acceleration_acce
        altitude = self.altimeter.altitude
        acceleration_imu_x, acceleration_imu_y, acceleration_imu_z = self.imu.acceleration_imu
        linacceleration_imu_x, linacceleration_imu_y, linacceleration_imu_z = self.imu.linacceleration_imu
        eulerangle_imu_x, eulerangle_imu_y, eulerangle_imu_z = self.imu.eulerangle_imu
        gravity_imu_x, gravity_imu_y, gravity_imu_z = self.imu.gravity_imu

        self.dfilter.filter_data(altitude, acceleration_acce_z, linacceleration_imu_z, eulerangle_imu_z)
        kalman_acceleration = self.dfilter.kalman_acceleration
        kalman_velocity = self.dfilter.kalman_velocity
        kalman_altitude = self.dfilter.kalman_altitude
        orientation_beta = self.dfilter.orientation_beta

        row = [
            "%.4f" % time.time(),  # sensors.curr_time,
            "%.4f" % acceleration_acce_x,
            "%.4f" % acceleration_acce_y,
            "%.4f" % acceleration_acce_z,
            "%.4f" % altitude,
            "%.4f" % acceleration_imu_x,
            "%.4f" % acceleration_imu_y,
            "%.4f" % acceleration_imu_z,
            "%.4f" % linacceleration_imu_x,
            "%.4f" % linacceleration_imu_y,
            "%.4f" % linacceleration_imu_z,
            "%.4f" % eulerangle_imu_x,
            "%.4f" % eulerangle_imu_y,
            "%.4f" % eulerangle_imu_z,
            "%.4f" % gravity_imu_x,
            "%.4f" % gravity_imu_y,
            "%.4f" % gravity_imu_z,
            "%.4f" % kalman_acceleration,  # data_filter.kalman_acceleration,
            "%.4f" % kalman_velocity,  # data_filter.kalman_velocity,
            "%.4f" % kalman_altitude,  # data_filter.kalman_altitude,
            "%.4f" % orientation_beta  # data_filter.orientation_beta
        ]
        csv.writer(self.file).writerow(row)
        self.samples += 1

