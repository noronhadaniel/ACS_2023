"""
logger.py contains the implementation of Logger,
which is responsible for writing the time, state, and sensor values
to a CSV for later inspection.
"""

import csv

from sensor_manager import SensorManager
from proportional_controller import Proportional_Controller
from servo import Servo
from utils import HEADERS


class Logger:
    def __init__(self, name: str, sensor_manager: SensorManager, servo: Servo, proportional_controller: Proportional_Controller):
        self.name = name
        self.sensor_manager = sensor_manager
        self.servo = servo
        self.proportional_controller = proportional_controller

        self._initialize_csv()

    def _initialize_csv(self):
        """
        The _initialize_csv function is called internally exactly once to load the csv writer
        and write the titles of each column. Note that there is no deinit function ... the file
        is not gracefully closed. We simply pray that this has no impact.
        """

        self.file = open(self.name, "w")
        self.writer = csv.writer(self.file)
        self.writer.writerow(HEADERS)

    def log(self):
        """
        The log function adds a row to the csv with the current sensor readings. Note that the
        log function simply records values and does not directly read them from the sensor 
        (nor does it recalculate the time).
        """

        row = [
            self.sensor_manager.readings-1,
            "%.4f" % self.sensor_manager.time,
            self.sensor_manager.state.name,
            "%.4f" % self.sensor_manager.altitude,
            "%.4f" % self.sensor_manager.acceleration_acce_x,
            "%.4f" % self.sensor_manager.acceleration_acce_y,
            "%.4f" % self.sensor_manager.acceleration_acce_z,
            "%.4f" % self.sensor_manager.acceleration_imu_x,
            "%.4f" % self.sensor_manager.acceleration_imu_y,
            "%.4f" % self.sensor_manager.acceleration_imu_z,
            "%.4f" % self.sensor_manager.linacceleration_imu_x,
            "%.4f" % self.sensor_manager.linacceleration_imu_y,
            "%.4f" % self.sensor_manager.linacceleration_imu_z,
            "%.4f" % self.sensor_manager.eulerangle_imu_x,
            "%.4f" % self.sensor_manager.eulerangle_imu_y,
            "%.4f" % self.sensor_manager.eulerangle_imu_z,
            "%.4f" % self.sensor_manager.gravity_imu_x,
            "%.4f" % self.sensor_manager.gravity_imu_y,
            "%.4f" % self.sensor_manager.gravity_imu_z,
            "%.4f" % self.sensor_manager.kalman_acceleration,
            "%.4f" % self.sensor_manager.kalman_velocity,
            "%.4f" % self.sensor_manager.kalman_altitude,
            "%.4f" % self.sensor_manager.orientation_beta,
            # "%.4f" % self.sensor_manager.predicted_apogee
            "%.4f" % self.servo.angle,
            "%.4f" % self.proportional_controller.servo_target_angle,
            "%.4f" % self.proportional_controller.apogee_projected,
            "%.4f" % self.proportional_controller.apogee_error
        ]
        csv.writer(self.file).writerow(row)
